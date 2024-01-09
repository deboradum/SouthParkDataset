import argparse
import json
from pathlib import Path
from typing import List

import mlx.core as mx
import mlx.nn as nn
import numpy as np
from mlx.utils import tree_unflatten
from models import LoRALinear, Model, ModelArgs
from sentencepiece import SentencePieceProcessor


def build_parser():
    parser = argparse.ArgumentParser(description="LoRA or QLoRA finetuning.")
    parser.add_argument(
        "--model",
        default="mlx_model",
        help="A path to the model files containing the tokenizer, weights, config.",
    )
    parser.add_argument(
        "--adapter-file",
        type=str,
        default="adapters.npz",
        help="Save/load path for the trained adapter weights.",
    )
    parser.add_argument(
        "--max-tokens", "-n", type=int, default=500, help="Maximum amount of tokens to generate"
    )
    parser.add_argument(
        "--write-every", type=int, default=1, help="After how many tokens to detokenize"
    )
    parser.add_argument(
        "--temp", type=float, default=0.8, help="The sampling temperature"
    )
    parser.add_argument(
        "--eos-token", type=str, default="<|ENDOFTEXT|>", help="EOS token on which to stop generating"
    )
    parser.add_argument(
        "--prompt",
        "-p",
        type=str,
        help="The prompt for generation",
        default=None,
    )

    parser.add_argument("--seed", type=int, default=0, help="The PRNG seed")
    return parser


class Tokenizer:
    def __init__(self, model_path: str):
        assert Path(model_path).exists(), model_path
        self._model = SentencePieceProcessor(model_file=model_path)
        self._sep = "▁"
        assert self._model.vocab_size() == self._model.get_piece_size()

    def encode(self, s: str, eos: bool = False) -> List[int]:
        toks = [self._model.bos_id(), *self._model.encode(s)]
        if eos:
            toks.append(self.eos_id)
        return toks

    @property
    def eos_id(self) -> int:
        return self._model.eos_id()

    def decode(self, t: List[int]) -> str:
        out = self._model.decode(t)
        if t and self._model.id_to_piece(t[0])[0] == self._sep:
            return " " + out
        return out

    @property
    def vocab_size(self) -> int:
        return self._model.vocab_size()


class Dataset:
    """
    Light-weight wrapper to hold lines from a jsonl file
    """

    def __init__(self, path: Path, key: str = "text"):
        if not path.exists():
            self._data = None
        else:
            with open(path, "r") as fid:
                self._data = [json.loads(l) for l in fid]
        self._key = key

    def __getitem__(self, idx: int):
        return self._data[idx][self._key]

    def __len__(self):
        return len(self._data)


def load(args):
    names = ("train", "valid", "test")
    train, valid, test = (Dataset(Path(args.data) / f"{n}.jsonl") for n in names)
    if args.train and len(train) == 0:
        raise ValueError(
            "Training set not found or empty. Must provide training set for fine-tuning."
        )
    if args.train and len(valid) == 0:
        raise ValueError(
            "Validation set not found or empty. Must provide validation set for fine-tuning."
        )
    if args.test and len(test) == 0:
        raise ValueError(
            "Test set not found or empty. Must provide test set for evaluation."
        )
    return train, valid, test


def loss(model, inputs, targets, lengths):
    # Run model on inputs
    logits, _ = model(inputs)
    logits = logits.astype(mx.float32)

    # Mask padding tokens
    length_mask = mx.arange(inputs.shape[1])[None, :] < lengths[:, None]

    # Calculate the loss
    ce = nn.losses.cross_entropy(logits, targets) * length_mask
    ntoks = length_mask.sum()
    ce = ce.sum() / ntoks
    return ce, ntoks

def generate(model, prompt, tokenizer, args):
    print(args.prompt, end="", flush=True)
    prompt = mx.array(tokenizer.encode(args.prompt))

    # print("token:", tokenizer.encode("<|EOT|>"))

    def generate_step():
        temp = args.temp

        def sample(logits):
            if temp == 0:
                return mx.argmax(logits, axis=-1)
            else:
                return mx.random.categorical(logits * (1 / temp))

        logits, cache = model(prompt[None])
        y = sample(logits[:, -1, :])
        yield y

        while True:
            logits, cache = model(y[:, None], cache)
            y = sample(logits.squeeze(1))
            yield y

    tokens = []
    for token, _ in zip(generate_step(), range(args.max_tokens)):
        tokens.append(token)

        if (len(tokens) % 10) == 0:
            mx.eval(tokens)
            s = tokenizer.decode([t.item() for t in tokens])
            print(s, end="", flush=True)
            tokens = []

    mx.eval(tokens)
    s = tokenizer.decode([t.item() for t in tokens])
    print(s, flush=True)


def load_model(folder: str):
    model_path = Path(folder)
    tokenizer = Tokenizer(str(model_path / "tokenizer.model"))
    with open(model_path / "config.json", "r") as f:
        config = json.loads(f.read())
        quantization = config.pop("quantization", None)
        model_args = ModelArgs(**config)
    model = Model(model_args)
    if quantization is not None:
        quantization["linear_class_predicate"] = lambda m: isinstance(
            m, nn.Linear
        ) and (m.weight.shape[0] != model_args.vocab_size)
        nn.QuantizedLinear.quantize_module(model, **quantization)

    weights = mx.load(str(model_path / "weights.npz"))
    weights = tree_unflatten(list(weights.items()))
    model.update(weights)
    return model, tokenizer

def generate_episode():
    pass

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    np.random.seed(args.seed)

    print("Loading model")
    model, tokenizer = load_model(args.model)

    # Load the LoRA adapter weights which we assume should exist by this point
    if not Path(args.adapter_file).is_file():
        raise ValueError(
            f"Adapter file {args.adapter_file} missing. "
            "Use --train to learn and save the adapters.npz."
        )
    model.load_weights(args.adapter_file, strict=False)

    if args.prompt is None:
        print("Generating")
        exit()

    generate(model, args.prompt, tokenizer, args)
