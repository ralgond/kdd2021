import os
import sys

from base import *
from base_mp import *
from base_win_size_l import *

def deal_one(file_no, train, test, output_path):
    train_profile, train_index = mp2_selfjoin(train, ws)

    profile, index = mp2_abjoin(test, train, ws)

    of = open(output_path, "w+")
    for (d, train_idx) in zip(profile, index):
        z = train_profile[train_idx]
        try:
            of.write(f"{d/z}\n")
        except Exception as e:
            of.write("0\n")
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

        train_diff = diff(train)
        test_diff = diff(test)

        print (file_no)

        if file_no in [239,240,241]:
            continue

        path1 = f"interdata\{file_no}"
        os.system("md " + path1)

        for ws in win_size_l:
            path2 = f"{path1}\{ws}"
            os.system("md " + path2)

            deal_one(file_no, train_diff, test_diff, f"{path2}\\diff_mp_abjoin_normalized.txt")