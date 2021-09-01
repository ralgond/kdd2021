import os
import sys

from base import *
from base_mp import *

if __name__ == "__main__":
    win_size = int(sys.argv[1])
    os.system(f"md mp_abjoin_output\{win_size}")
    for fn in os.listdir("samples"):
        file_no = int(fn.split("_")[0])
        fp = os.path.join("samples", fn)
        train_size = get_train_size_from_filename(fp)

        train, test = read_train_test(fp, train_size)

        print (file_no, len(train), len(test))

        max_profile, max_index, profile = mp_detect_abjoin(test, train, win_size)

        top2_idx = topk(profile, 2, win_size)

        output_path = os.path.join(f"mp_abjoin_output/{win_size}", f"{file_no}.txt")

        of = open(output_path, "w+")
        for idx in top2_idx:
            of.write(f"{profile[idx]},{idx}\n")

        of.close()
            
        