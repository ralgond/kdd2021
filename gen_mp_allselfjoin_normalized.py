import os
import sys

from base import *
from base_mp import *
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

            all_data_profile, all_data_index = mp2_selfjoin(all_data, ws)

            output_path = f"{path2}\\mp_allselfjoin_normalized.txt"
            of = open(output_path, "w+")
            for (d, idx) in zip(all_data_profile, all_data_index):
                z = all_data_profile[idx]
                try:
                    of.write(f"{d/z}\n")
                except Exception as e:
                    of.write("0\n")
            of.close()