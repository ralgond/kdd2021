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

def deal_one2(file_no, train, test, output_path):
    mpv = {}
    mpi = {}

    train_profile, train_index = mp2_selfjoin(train, ws)

    mpv['train'] = np.array(train_profile)
    mpi['train'] = np.array(train_index)

    profile, index = mp2_abjoin(test, train, ws)

    mpv['join'] = np.array(profile)
    mpi['join'] = np.array(index)

    numer = mpv['join']
    denom = mpv['train'][mpi['join']]


    with np.errstate(all='ignore'):
        d_z_l = numer / denom

        of = open(output_path, "w+")
        for d_z in d_z_l:
                of.write(f"{d_z}\n")
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

        if file_no in [239,240,241]:
            continue

        path1 = f"interdata\{file_no}"
        os.system("md " + path1)

        for ws in win_size_l:
            path2 = f"{path1}\{ws}"
            os.system("md " + path2)

            deal_one2(file_no, train, test, f"{path2}\\mp_abjoin_normalized.txt")