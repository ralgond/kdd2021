import os
import sys
import math

import pandas as pd
import numpy as np

from base import *
from base_win_size_l import *

from base_math import *

# if __name__ == "__main__":
#     sliding_window_mad([1, 1, 2, 2, 4, 6, 9], 7)

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

            output_path = f"{path2}\\orig_mad.txt"

            mad_l = sliding_window_mad(test, ws)

            of = open(output_path, "w+")
            for v in mad_l:
                of.write(f"{v}\n")
            of.close()