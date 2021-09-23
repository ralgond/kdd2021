import os
import sys
import math

import rolling

from base import *
from base_win_size_l import *
from base_mp import *

def mp(profile, index, output_path):
    of = open(output_path, "w+")
    for idx, mp_score in enumerate(profile):
        of.write(f"{mp_score},{index[idx]}\n")

    of.close()

if __name__ == "__main__":
    from_file_no = int(sys.argv[1])

    for fn in os.listdir("samples"):
        file_no = int(fn.split("_")[0])
        if file_no < from_file_no:
            continue

        fp = os.path.join("samples", fn)
        train_size = get_train_size_from_filename(fp)

        train, test = read_train_test(fp, train_size)

        print(file_no)

        test_diff = diff(test)

        path1 = f"interdata\{file_no}"
        os.system("md " + path1)

        for ws in win_size_l:
            path2 = f"{path1}\{ws}"
            os.system("md " + path2)

            profile, index = mp2_selfjoin(test_diff, ws)
            mp(profile, index, f"{path2}\\diff_mp_selfjoin.txt")