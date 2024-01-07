import json

MAX_CONTEXT = 1000

def convertNoContext(contexts, outputFolder):
    convertEpisodesNoContext(contexts, outputFolder)
    # convertSeasonsNoContext(contexts, outputFolder)

def convertEpisodesNoContext(contexts, outputFolder):
    for context in contexts:
        for season in range(1,27):
            for episode in range(1, 19):
                try:
                    with open(f"parsed_context_{context}/S{season:02}/S{season:02}E{episode:02}.json", "r") as f:
                        data = json.load(f)
                    for e in data:
                        inputText = e['input']
                        outputText = e['output']
                        string = f"<|INPUT|>\n\n{inputText}\n\n<|OUTPUT|>\n\n{outputText}\n\n<|=====|>"
                        elementJson = {"text": string}
                        with open(f"{outputFolder}/S{season:02}/S{season:02}E{episode:02}.jsonl", "a+") as f:
                            f.write(json.dumps(elementJson, indent=2))
                            f.write("\n")
                        with open(f"{outputFolder}/S{season:02}/S{season:02}.jsonl", "a+") as f:
                            f.write(json.dumps(elementJson, indent=2))
                            f.write("\n")
                except Exception as e:
                    print(f"Error converting season {season} - Episode {episode}", e)

def convertSeasonsNoContext(contexts, outputFolder):
    for context in contexts:
        for season in range(1,27):
            try:
                with open(f"parsed_context_{context}/S{season:02}/S{season:02}.json", "r") as f:
                    data = json.load(f)
                for e in data:
                    inputText = e['input']
                    outputText = e['output']
                    string = f"<|INPUT|>\n\n{inputText}\n\n<|OUTPUT|>\n\n{outputText}\n\n<|=====|>"
                    elementJson = {"text": string}
                    with open(f"{outputFolder}/S{season:02}/S{season:02}.jsonl", "a+") as f:
                        f.write(json.dumps(elementJson, indent=2))
                        f.write("\n")
            except Exception as e:
                print(f"Error converting season {season}", e)

def convertContext(contexts):
    convertEpisodesContext(contexts)
    convertSeasonsContext(contexts)

def convertEpisodesContext(contexts):
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
                        string = f"<|INPUT|>\n\n{inputText}\n\n<|OUTPUT|>\n\n{outputText}\n\n<|CONTEXT|>\n\n{contextText}<|=====|>"
                        elementJson = {"text": string}
                        # Episode convert
                        with open(f"parsed_context_{context}_rewrite/S{season:02}/S{season:02}E{episode:02}.jsonl", "a+") as f:
                            f.write(json.dumps(elementJson, indent=2))
                            f.write("\n")
                        # Whole season convert
                        with open(f"parsed_context_{context}_rewrite/S{season:02}/S{season:02}.jsonl", "a+") as f:
                            f.write(json.dumps(elementJson, indent=2))
                            f.write("\n")
                except Exception as e:
                    print(f"Error converting season {season} - Episode {episode}", e)

def convertSeasonsContext(contexts):
    for context in contexts:
        for season in range(1,27):
            try:
                with open(f"parsed_context_{context}/S{season:02}/S{season:02}.json", "r") as f:
                    data = json.load(f)
                for e in data:
                    inputText = e['input']
                    outputText = e['output']
                    contextText = e["context"]
                    string = f"<|INPUT|>\n\n{inputText}\n\n<|OUTPUT|>\n\n{outputText}\n\n<|CONTEXT|>\n\n{contextText}<|=====|>"
                    elementJson = {"text": string}
                    with open(f"parsed_context_{context}_rewrite/S{season:02}/S{season:02}.jsonl", "a+") as f:
                        f.write(json.dumps(elementJson, indent=2))
                        f.write("\n")
            except Exception as e:
                print(f"Error converting season {season}", e)

convertNoContext(["5"], "parsed_context_0_rewrite")
convertEpisodesContext(["5", "10", "20", "30", "full"])