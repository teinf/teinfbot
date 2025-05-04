import random
import os

data_dir = os.path.join("src", "random_nickname", "data")


nouns_file_path = os.path.join(data_dir, "nouns.txt")
verbs_file_path = os.path.join(data_dir, "verbs.txt")


def read_file(path):
    values = []
    with open(path, "r") as f:
        for line in f.readlines():
            values.append(line.strip())
    return values


verbs = read_file(verbs_file_path)
nouns = read_file(nouns_file_path)


def get_random_name():
    return random.choice(verbs) + " " + random.choice(nouns)


if __name__ == "__main__":
    print(get_random_name())
