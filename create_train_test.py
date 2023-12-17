import json
import random

TRAIN_FILE = "train.jsonl"
TEST_FILE = "test.jsonl"

# Converts the file to the proper format needed for finetuning lora.
def convert(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    with open(TRAIN_FILE, 'w') as output_file:
        for item in data:
            formatted_item = json.dumps(item, separators=(',', ':'))
            output_file.write(formatted_item + '\n')

# Shuffles lines.
def shuffle_file():
    with open(TRAIN_FILE,'r') as source:
        data = [ (random.random(), line) for line in source ]
        data.sort()

    with open(file,'w') as target:
        for _, line in data:
            target.write( line )

# Splits train.jsonl into a test and train dataset.
def split(num):
    with open(TRAIN_FILE, 'r') as f:
        lines = f.readlines()

    random_lines = random.sample(lines, num)

    with open(TEST_FILE, 'a') as test_file:
        for line in random_lines:
            test_file.write(line)

    with open(TRAIN_FILE, 'w') as train_file:
        for line in lines:
            if line not in random_lines:
                train_file.write(line)


# convert("parsed_context_5/all.json")
# shuffle_file(TRAIN_FILE)
# split(20000)