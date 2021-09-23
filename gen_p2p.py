import os
import sys
import math

import rolling

from base import *
from base_win_size_l import *

if __name__ == "__main__":
    from_file_no = int(sys.argv[1])

    for fn in os.listdir("samples"):
        file_no = int(fn.split("_")[0])
        if file_no < from_file_no:
            continue

        fp = os.path.join("samples", fn)
        train_size = get_train_size_from_filename(fp)

        train, test = read_train_test(fp, train_size)

        print (file_no)

        path1 = f"interdata\{file_no}"
        os.system("md " + path1)

        for ws in win_size_l:
            path2 = f"{path1}\{ws}"
            os.system("md " + path2)

            max_list = list(rolling.Max(test, ws))
            min_list = list(rolling.Min(test, ws))
            output_path = f"{path2}\orig_p2p.txt"
            of = open(output_path, "w+")
            for idx, max_score in enumerate(max_list):
                of.write(f"{max_score-min_list[idx]}\n")
            of.close()

            diff_l = diff(test)
            max_list = list(rolling.Max(diff_l, ws))
            min_list = list(rolling.Min(diff_l, ws))
            output_path = f"{path2}\diff_p2p.txt"
            of = open(output_path, "w+")
            for idx, max_score in enumerate(max_list):
                of.write(f"{max_score-min_list[idx]}\n")
            of.close()

            acc_l = diff(diff_l)
            max_list = list(rolling.Max(acc_l, ws))
            min_list = list(rolling.Min(acc_l, ws))
            output_path = f"{path2}\acc_p2p.txt"
            of = open(output_path, "w+")
            for idx, max_score in enumerate(max_list):
                of.write(f"{max_score-min_list[idx]}\n")
            of.close()

