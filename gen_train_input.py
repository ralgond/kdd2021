import os
from base import *

if __name__ == "__main__":
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "samples"))

    for sample_file in os.listdir(sample_dir):
        file_no = int(sample_file.split("_")[0])

        train_size = get_train_size_from_filename(sample_file)

        all_data = []
        for line in open(os.path.join(sample_dir, sample_file)):
            all_data.append(float(line.strip()))
        train = all_data[:train_size].copy()
        test = all_data[train_size:].copy()

        of = open(os.path.join("only_train_input", f"{file_no}.txt"), "w+")
        for i in train:
            of.write(f"{i}\n")