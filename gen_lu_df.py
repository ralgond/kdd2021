import sys
import os
import numpy as np
from base import *

if __name__ == "__main__":
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "samples"))
    result_file_name_prefix = sys.argv[0].split(".")[0]

    for sample_file in os.listdir(sample_dir):
        file_no = int(sample_file.split("_")[0])

        output_file_path = os.path.join("lu_df_output", str(file_no)+".txt")

        train_size = get_train_size_from_filename(sample_file)

        all_data = []
        for line in open(os.path.join(sample_dir, sample_file)):
            all_data.append(float(line.strip()))
        train = all_data[:train_size].copy()
        test = all_data[train_size:].copy()

        lu_score_l = luminol_detect_df(test)

        of = open(output_file_path, "w+")
        for score in lu_score_l:
            of.write(f"{score}\n")
        of.close()