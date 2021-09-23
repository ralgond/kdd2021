import os
import sys

from base import *
from base_mp import *
from base_win_size_l import *

def mp_top2(max_profile, max_index, profile, index, output_path):
    top2_idx = topk(profile, 2, ws)

    of = open(output_path, "w+")
    for idx in top2_idx:
        of.write(f"{profile[idx]},{idx}\n")

    of.close()

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

        all_data = train.copy()
        all_data.extend(test)

        period = cal_window_size(train)

        print (file_no, len(all_data), period)

        path1 = f"interdata\{file_no}"
        os.system("md " + path1)

        for ws in win_size_l:
            path2 = f"{path1}\{ws}"
            os.system("md " + path2)

            #print (len(test), len(train), ws)
            profile, index = mp2_abjoin(test, train, ws)
            mp(profile, index, f"{path2}\\mp_abjoin.txt")

            profile, index = mp2_selfjoin(test, ws)
            mp(profile, index, f"{path2}\\mp_selfjoin.txt")
            




        

