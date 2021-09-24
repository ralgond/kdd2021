import os
import sys

from base import *
from base_mp import *
from base_win_size_l import *


def nmp(profile, output_path):
    of = open(output_path, "w+")
    for idx, mp_score in enumerate(profile):
        of.write(f"{mp_score}\n")

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

        print (file_no)

        path1 = f"interdata\{file_no}"
        os.system("md " + path1)

        for ws in win_size_l:
            path2 = f"{path1}\{ws}"
            os.system("md " + path2)

            test_profile, test_index = mp2_abjoin(test, train, ws)

            train_profile, train_index = mp2_selfjoin(train, ws)

            d_z = []
            for idx, d in enumerate(test_profile):
                d_idx = test_index[idx]
                z = train_profile[d_idx]
                d_z.append(d/z)
        
            nmp(d_z, f"{path2}\\nmp.txt")
