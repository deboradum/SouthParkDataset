import json

OUTPUT_FOLDER_NAME = "parsed_context_full"
MAX_CONTEXT = 1000

def append_context(context, new_item, max_context):
    if len(context) >= max_context:
        del context[0]
    context.append(new_item)

    return context

def context_to_string(context):
    string = ""
    for l in context:
        string += l

    return string

dataAll = []
for season in range(1,27):
    dataSeason = []
    for episode in range(1, 19):
        data = []
        try:
            with open(f"scripts/S{season:02}/S{season:02}E{episode:02}.txt", "r") as f:
                currItem = {
                    "input": "", 
                    "output": "",
                    "context": "",
                }
                context = []
                for line in f:
                    if line.isupper():
                        data.append(currItem.copy())
                        dataSeason.append(currItem.copy())
                        dataAll.append(currItem.copy())
                        currItem["input"] = currItem["output"]
                        currItem["context"] = context_to_string(append_context(
                                                                    context, 
                                                                    currItem["output"], 
                                                                    max_context=MAX_CONTEXT))
                        currItem["output"] = line
                    else:
                        currItem["output"] += line

            with open(f"{OUTPUT_FOLDER_NAME}/S{season:02}/S{season:02}E{episode:02}.json", "w+") as f:
                f.write(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Error converting season {season} - Episode {episode}", e)

        with open(f"{OUTPUT_FOLDER_NAME}/S{season:02}/S{season:02}.json", "w+") as f:
                f.write(json.dumps(dataSeason, indent=2))

with open(f"{OUTPUT_FOLDER_NAME}/all.json", "w+") as f:
        f.write(json.dumps(dataAll, indent=2))
