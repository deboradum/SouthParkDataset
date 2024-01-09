import json

MAX_CONTEXT = 1000


def convertNoContext(contexts, outputFolder):
    for context in contexts:
        for season in range(1,27):
            for episode in range(1, 19):
                try:
                    with open(f"parsed_context_{context}/S{season:02}/S{season:02}E{episode:02}.json", "r") as f:
                        data = json.load(f)
                    for e in data:
                        inputText = e['input']
                        outputText = e['output']
                        string = f"<|INPUT|>\n{inputText}\n<|OUTPUT|>\n{outputText}\n<|ENDOFTEXT|>"
                        elementJson = {"text": string}
                        # Episode convert
                        with open(f"{outputFolder}/S{season:02}/S{season:02}E{episode:02}.jsonl", "a+") as f:
                            f.write(json.dumps(elementJson, indent=None))
                            f.write("\n")
                        # Whole season convert
                        with open(f"{outputFolder}/S{season:02}/S{season:02}.jsonl", "a+") as f:
                            f.write(json.dumps(elementJson, indent=None))
                            f.write("\n")
                        # For everything
                        with open(f"{outputFolder}/all.jsonl", "a+") as f:
                            f.write(json.dumps(elementJson, indent=None))
                            f.write("\n")
                except Exception as e:
                    print(f"Error converting season {season} - Episode {episode}", e)

def convertContext(contexts):
    for context in contexts:
        for season in range(1,27):
            for episode in range(1, 19):
                try:
                    with open(f"parsed_context_{context}/S{season:02}/S{season:02}E{episode:02}.json", "r") as f:
                        data = json.load(f)
                    for e in data:
                        inputText = e['input']
                        outputText = e['output']
                        contextText = e["context"]
                        string = f"<|INPUT|>\n{inputText}\n<|OUTPUT|>\n{outputText}\n<|CONTEXT|>\n{contextText}<|ENDOFTEXT|>"
                        elementJson = {"text": string}
                        # Episode convert
                        with open(f"parsed_context_{context}_rewrite/S{season:02}/S{season:02}E{episode:02}.jsonl", "a+") as f:
                            f.write(json.dumps(elementJson, indent=None))
                            f.write("\n")
                        # Whole season convert
                        with open(f"parsed_context_{context}_rewrite/S{season:02}/S{season:02}.jsonl", "a+") as f:
                            f.write(json.dumps(elementJson, indent=None))
                            f.write("\n")
                        # For everything
                        with open(f"parsed_context_{context}_rewrite/all.jsonl", "a+") as f:
                            f.write(json.dumps(elementJson, indent=None))
                            f.write("\n")
                except Exception as e:
                    print(f"Error converting season {season} - Episode {episode}", e)

convertNoContext(["5"], "parsed_context_0_rewrite")
convertContext(["5", "10", "20", "30", "full"])