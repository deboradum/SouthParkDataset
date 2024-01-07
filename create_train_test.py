import random

TRAIN_FILE = "train.jsonl"
TEST_FILE = "test.jsonl"
VAL_FILE = "valid.jsonl"

# Shuffles lines.
def shuffle_file(input_file, output_folder):
    with open(input_file,'r') as source:
        data = [ (random.random(), line) for line in source ]
        data.sort()

    with open(f"{output_folder}/{TRAIN_FILE}",'w') as target:
        for _, line in data:
            target.write( line )

def split_test(num, output_folder):
    with open(f"{output_folder}/{TRAIN_FILE}", 'r') as f:
        lines = f.readlines()

    random_lines = random.sample(lines, num)

    with open(f"{output_folder}/{TEST_FILE}", 'a') as test_file:
        for line in random_lines:
            test_file.write(line)

    with open(f"{output_folder}/{TRAIN_FILE}", 'w') as train_file:
        for line in lines:
            if line not in random_lines:
                train_file.write(line)

def split_val(num, output_folder):
    with open(f"{output_folder}/{TRAIN_FILE}", 'r') as f:
        lines = f.readlines()

    random_lines = random.sample(lines, num)

    with open(f"{output_folder}/{VAL_FILE}", 'a') as val_file:
        for line in random_lines:
            val_file.write(line)

    with open(f"{output_folder}/{TRAIN_FILE}", 'w') as train_file:
        for line in lines:
            if line not in random_lines:
                train_file.write(line)

# Splits train.jsonl into a test and train dataset.
def prepare(input_file, output_folder, test_num, val_num):
    shuffle_file(input_file, output_folder)
    split_test(test_num, output_folder)
    split_val(val_num, output_folder)

prepare("parsed_context_0_rewrite/all.jsonl", "parsed_context_0_rewrite", 20000, 10000)
prepare("parsed_context_5_rewrite/all.jsonl", "parsed_context_5_rewrite", 20000, 10000)
prepare("parsed_context_10_rewrite/all.jsonl", "parsed_context_10_rewrite", 20000, 10000)
prepare("parsed_context_20_rewrite/all.jsonl", "parsed_context_20_rewrite", 20000, 10000)
prepare("parsed_context_30_rewrite/all.jsonl", "parsed_context_30_rewrite", 20000, 10000)
prepare("parsed_context_full_rewrite/all.jsonl", "parsed_context_full_rewrite", 20000, 10000)
