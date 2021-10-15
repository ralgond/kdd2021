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

        if file_no in [239,240,241]:
            continue

        test_acc = diff(diff(test))

        path1 = f"interdata\{file_no}"
        os.system("md " + path1)

        for ws in win_size_l:
            path2 = f"{path1}\{ws}"
            os.system("md " + path2)

            test_profile, test_index = mp2_selfjoin(test_acc, ws)
            
            output_path = f"{path2}\\acc_mp_selfjoin_normalized.txt"
            of = open(output_path, "w+")
            for (d, idx) in zip(test_profile, test_index):
                z = test_profile[idx]
                try:
                    of.write(f"{d/z}\n")
                except Exception as e:
                    of.write("0\n")
            of.close()