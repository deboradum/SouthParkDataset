import json
import random
import re
import os


SYSTEM = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>"
USER = "<|start_header_id|>user<|end_header_id|>"
ASSISTENT = "<|start_header_id|>assistant<|end_header_id|>"

CONVO_CONTEXT = 10


def generate_system_prompt(prompt):
    return f"{SYSTEM}\n\n{prompt}<|eot_id|>\n"


def get_speaker_header(speaker):
    return f"<|start_header_id|>{speaker}<|end_header_id|>"


def generate_speaker_prompt(speaker, prompt):
    return f"{get_speaker_header(speaker)}\n\n{prompt}<|eot_id|>\n"


def append_to_history(history, new, max_length=CONVO_CONTEXT):
    if len(history) < max_length:
        history.append(new)
    else:
        history = history[1:]
        history.append(new)

    return history

def has_alphabetical_characters(input_string):
    return bool(re.search(r'[a-zA-Z]', input_string))

def parse_episode_convo_window(season, episode):
    first = True
    history = []
    speaker = None
    speakerText = ""
    with open(f"scripts/{season}/{episode}", "r") as f:
        for line in f:
            if line.startswith("[") and line.endswith("]\n"):
                continue
            if not has_alphabetical_characters(line):
                continue

            if first:
                history = append_to_history(
                    history, generate_system_prompt(line.replace("\n", "").strip())
                )
                first = False
                continue

            # Finds speaker
            if line.isupper():
                if speakerText:
                    history = append_to_history(history, generate_speaker_prompt(speaker, speakerText))
                    with open(f"parsed/{season}/{episode.replace('.txt','')}.jsonl", "a+") as output_f:
                        output_f.write(json.dumps({"text": "".join(history)}) + "\n")

                speaker = line.replace("\n", "").strip()
                speakerText = ""
            else:
                speakerText += line

def parse_episode_full(season, episode):
    first = True
    history = []
    speaker = None
    speakerText = ""
    with open(f"scripts/{season}/{episode}", "r") as f:
        for line in f:
            if line.startswith("[") and line.endswith("]\n"):
                continue
            if not has_alphabetical_characters(line):
                continue

            if first:
                history.append(generate_system_prompt(line.replace("\n", "").strip()))
                first = False
                continue

            # Finds speaker
            if line.isupper():
                if speakerText:
                    history.append(generate_speaker_prompt(speaker, speakerText))

                speaker = line.replace("\n", "").strip()
                speakerText = ""
            else:
                speakerText += line

    num = random.random()
    if num < 0.75:
        with open("train.jsonl", "a+") as output_f:
            output_f.write(json.dumps({"text": "".join(history)}) + "\n")
    else:
        with open("test.jsonl", "a+") as output_f:
            output_f.write(json.dumps({"text": "".join(history)}) + "\n")

if __name__ == "__main__":
    for season in os.listdir("scripts/"):
        if season.startswith("."):
            continue
        for episode in os.listdir(f"scripts/{season}"):
            if episode.startswith("."):
                continue
            parse_episode_full(season, episode)
            # exit()
