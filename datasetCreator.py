import os
import json

data = []
prevText = ""
newText = ""

with open("scripts/S01/S01E01.txt") as f:
    currItem = {
        "input": "", 
        "output": ""
    }
    nextItem = {
        "input": "", 
        "output": ""
    }
    for line in f:
        if line.isupper():
            data.append(currItem)
            currItem["output"] += line
            nextItem["input"] += line
        else:
            currItem["output"] += line
            nextItem["input"] += line
