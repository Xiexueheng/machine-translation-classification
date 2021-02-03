from collections import defaultdict
import string
import numpy as np
import torch

TRAIN_FILE = "./train.txt"
TEST_FILE = "./test.txt"
N_TOKENS = 5000

# index 0: source, index 1: reference, index 2: candidate, index 3: score, index 4: label


def split(file):
    with open(file, "r") as f:
        text = f.read()
        split_text = text.split("\n\n")
        split_text = list(
            map(
                lambda x: [
                    x.split("\n")[2].translate(
                        str.maketrans("", "", string.punctuation)
                    ),
                    x.split("\n")[4],
                ],
                split_text,
            )
        )
        return split_text


def translate_to_integer(data):
    word_to_idx = defaultdict(int)
    idx = 0
    result = []

    for sample in data:
        in_text = sample[0]
        label = sample[1]
        in_text_ints = []

        for word in in_text.split():
            if word not in word_to_idx and idx <= N_TOKENS:
                # this way unknowns all automatically get assigned to '0'
                idx += 1
                word_to_idx[word] = idx

            if (
                word_to_idx[word] != 0
            ):  # temporary measure while I figure out what to do with unknowns
                in_text_ints.append(word_to_idx[word])

        result.append([in_text_ints, label])

    return result


def pad(input, total_length):
    for sample_idx in range(len(input)):
        text_in = input[sample_idx][0]
        while len(text_in) < total_length:
            text_in.append(0)

        input[sample_idx][0] = torch.tensor(text_in)

    return input


def split_data_labels(data):
    data = np.array(data)
    return data[:, 0], data[:, 1]


def give_numeric_labels(labels):
    for i in range(len(labels)):
        if labels[i] == "H":
            labels[i] = torch.tensor([0])
        else:
            labels[i] = torch.tensor([1])


def output_train_ints(seq_length):
    data = split(TRAIN_FILE)
    # padded_ints = pad(translate_to_integer(data), seq_length)
    # no need to pad anymore
    padded_ints = translate_to_integer(data)
    sample, labels = split_data_labels(padded_ints)
    give_numeric_labels(labels)
    return sample, labels


# data = split(TRAIN_FILE)
# final = split_data_labels(pad(translate_to_integer(data), 50))
# give_numeric_labels(final[1])
# print(final[1])
