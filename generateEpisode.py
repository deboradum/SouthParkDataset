import re

from mlx_lm import generate, load

from createDataset import generate_system_prompt, generate_speaker_prompt


# dialog = [{"speaker": <speaker>, "text": <text>}, ...]
def dialog_to_prompt(dialog):
    prompt = ""
    for monolog in dialog:
        if monolog["speaker"] == "sysyem":
            prompt += generate_system_prompt(monolog["text"])
        else:
            prompt += generate_speaker_prompt(monolog["speaker"], monolog["text"])

    return prompt


def response_to_monolog(text):
    print("----------")
    print("parsing:", text)
    pattern = re.compile(
        r"<|start_header_id|>(.*?)<|end_header_id|>\n(.*?)(<|eot_id|>\n)?",
        re.DOTALL,
    )
    match = pattern.search(text)
    if match:
        speaker = match.group(1)
        text = match.group(2)

        print("speaker:", speaker, "text:", text)

        return {"speaker": speaker, "text": text}

    return None


class EpisodeGenerator:
    def __init__(self, model, adapter_path):
        self.model, self.tokenizer = load(model, adapter_path=adapter_path)
        self.script = []

    def generate_next_dialog(self, dialog, max_tokens=1000, temp=0):
        return generate(
            self.model,
            self.tokenizer,
            dialog_to_prompt(self.script[-4:]),
            max_tokens,
            verbose=True,
            temp=temp,
        )

    # initial_dialog = [{"speaker": <speaker>, "text": <text>}, ...]
    # initial_dialog should be less than 3 monologs, else the title will be
    # ignored.
    def generate_start_episode(
        self, episode_title, initial_dialog=[], episode_length=100
    ):
        self.script = []
        self.script.append({"speaker": "system", "text": episode_title})

        # Sets up initial dialog
        for monolog in initial_dialog:
            self.script.append(monolog)
        for _ in range(episode_length):

            response = self.generate_next_dialog(self.script[-4:])
            monolog = response_to_monolog(response)
            if monolog:
                self.script.append(monolog)


if __name__ == "__main__":
    generator = EpisodeGenerator("meta-llama/Meta-Llama-3-8B-Instruct", "adapters")
    title = "Michael Jackson loves little boys"
    initial_dialog = [
        {"speaker": "CARTMAN", "text": "Holy shit guys! I just got a text message from Michael jackson. He wants to see me!"},
        {"speaker": "STAN", "text": "He probably just wants to rape you cartman, don't do it"},
    ]
    generator.generate_start_episode(title, initial_dialog)
