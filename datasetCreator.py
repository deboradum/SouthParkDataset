import os
import json
for season in range(1,27):
    for episode in range(1, 27):
        data = []
        try:
            with open(f"scripts/S{season:02}/S{season:02}E{episode:02}.txt", "r") as f:
                currItem = {
                    "input": "", 
                    "output": ""
                }
                for line in f:
                    if line.isupper():
                        data.append(currItem.copy())
                        currItem["input"] = currItem["output"]
                        currItem["output"] = ""
                    else:
                        currItem["output"] += line

            with open(f"parsed/S{season:02}/S{season:02}E{episode:02}.json", "w+") as f:
                f.write(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Error converting season {season} - Episode {episode}")