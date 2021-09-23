import os
import sys
import math

import pandas as pd

from base import *
from base_win_size_l import *
from base_math import sliding_window_std

if __name__ == "__main__":
    from_file_no = int(sys.argv[1])

    for fn in os.listdir("samples"):
        file_no = int(fn.split("_")[0])
        if file_no < from_file_no:
            continue

        fp = os.path.join("samples", fn)
        train_size = get_train_size_from_filename(fp)

        train, test = read_train_test(fp, train_size)

        all_data = train.copy()
        all_data.extend(test)

        print (file_no, len(all_data))

        path1 = f"interdata\{file_no}"
        os.system("md " + path1)

        for ws in win_size_l:
            path2 = f"{path1}\{ws}"
            os.system("md " + path2)

            diff_l = diff(test)

            output_path = f"{path2}\\diff_std.txt"

            diff_l = diff_l[1:] # cut the first one nan value

            std_l = sliding_window_std(diff_l, ws)

            of = open(output_path, "w+")
            for v in std_l:
                of.write(f"{v}\n")
            of.close()