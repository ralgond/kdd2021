import os
import sys

from base import *
from base_mp import *
from base_win_size_l import *

import rolling
   
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

        if file_no in [239,240,241]:
            continue

        path1 = f"interdata\{file_no}"
        os.system("md " + path1)

        for ws in win_size_l:
            path2 = f"{path1}\{ws}"
            os.system("md " + path2)

            #profile, index = mp2_selfjoin(test, ws)
            profile, index = read_matrix_profile_from_file(f"{path2}\\mp_selfjoin.txt")

            max_list = list(rolling.Max(profile, ws))
            min_list = list(rolling.Min(profile, ws))
            output_path = f"{path2}\orig_mp_selfjoin_p2p.txt"
            of = open(output_path, "w+")
            for idx, max_score in enumerate(max_list):
                of.write(f"{max_score-min_list[idx]}\n")
            of.close()




        

