import json
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
    pattern = re.compile(r'<\|start_header_id\|>(.*?)<\|end_header_id\|>\n(.*?)(?:<\|eot_id\|>\n)?$', re.DOTALL)
    match = pattern.search(text)
    if match:
        speaker = match.group(1)
        text = match.group(2)

        return {"speaker": speaker, "text": text}

    return None

def filter_non_standard_characters(text):
    pattern = re.compile(r'[^\w\s.,:;!?\'"@#%&*()\-+=/\\[\]{}<>|`~^]', re.UNICODE)
    cleaned_string = pattern.sub('', text)

    return cleaned_string


class EpisodeGenerator:
    def __init__(self, model, adapter_path, script_filepath):
        self.model, self.tokenizer = load(model, adapter_path=adapter_path)
        self.script = []
        self.filepath = script_filepath

    def generate_next_dialog(self, dialog, max_tokens=100, temp=0.3):
        return generate(
            self.model,
            self.tokenizer,
            dialog_to_prompt(dialog),
            max_tokens,
            verbose=True,
            temp=temp,
            # repetition_penalty=1.5,
            # repetition_context_size=200,
        )

    # initial_dialog = [{"speaker": <speaker>, "text": <text>}, ...]
    # initial_dialog should be less than 3 monologs, else the title will be
    # ignored.
    def generate_start_episode(
        self, episode_title, initial_dialog=[], episode_length=100
    ):
        self.script = []
        system_prompt = {"speaker": "system", "text": episode_title}
        self.script.append(system_prompt)
        self.write_monolog_to_file(system_prompt)

        # Sets up initial dialog
        for monolog in initial_dialog:
            self.script.append(monolog)
            self.write_monolog_to_file(monolog)

        for _ in range(episode_length):
            response = self.generate_next_dialog(self.script[-4:])
            filtered_response = filter_non_standard_characters(response)
            monolog = response_to_monolog(filtered_response)
            if monolog:
                self.script.append(monolog)
                self.write_monolog_to_file(monolog)
            else:
                print("Error: Could not convert the following response to a monolog object:")
                print("---------")
                print(filtered_response)


    def write_monolog_to_file(self, monolog):
        with open(self.filepath, "a+") as f:
            json.dump(monolog, f)
            f.write("\n")


    def write_script_to_file(self, filepath):
        with open(filepath, "w") as f:
            json.dump(self.script, f)


if __name__ == "__main__":
    generator = EpisodeGenerator("meta-llama/Meta-Llama-3-8B-Instruct", "adapters", "michaelJackson.jsonl")
    title = "Michael Jackson loves little boys"
    initial_dialog = [
        {"speaker": "CARTMAN", "text": "Holy shit guys! I just got a text message from Michael jackson. He wants to see me!"},
        {"speaker": "STAN", "text": "He probably just wants to rape you cartman, don't do it"},
    ]
    generator.generate_start_episode(title, initial_dialog=initial_dialog, episode_length=69)
    generator.write_to_file("testScript.json")
