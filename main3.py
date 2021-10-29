import os
import sys
import math
from base import *
from base_mp import *

from main_base import *

def deal_one(file_no, train_size):
    # lu does not work

    scorepos = None

    scorepos_l = []

    path1 = f"interdata/{file_no}"

    #=======================================================================================
    # ORIG
    #=======================================================================================
    for d in os.listdir(path1):
        fn = f"{path1}/{d}/mp_abjoin.txt"
        win_size = int(d)
        profile, index = read_matrix_profile_from_file(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)

    for d in os.listdir(path1):
        fn = f"{path1}/{d}/mp_selfjoin.txt"
        win_size = int(d)
        profile, index = read_matrix_profile_from_file(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)


    for d in os.listdir(path1):
        fn = f"{path1}/{d}/orig_p2p.txt"
        win_size = int(d)
        profile = read_score(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)

        # orig_p2p.txt-inv does not work

    # orig_mp_selfjoin_p2p.txt does not work

    # orig_mp_abjoin_p2p.txt does not work

    # mp_abjoin_normalized.txt does not work

    # mp_selfjoin_normalized.txt does not work

    # mp_allselfjoin_normalized.txt does not work

    # without moving_avg the mp_abjoin_normalized.txt does not work


    #=======================================================================================
    # DIFF
    #=======================================================================================
    for d in os.listdir(path1):
        fn = f"{path1}/{d}/diff_p2p.txt"
        win_size = int(d)
        profile = read_score(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)

        # diff_p2p.txt-inv deos not work

    for d in os.listdir(path1):
        fn = f"{path1}/{d}/diff_std.txt"
        win_size = int(d)
        profile = read_score(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)

        profile_inv = []
        for v in profile:
            if v == 0.0:
                profile_inv.append(float('-inf'))
            else:
                profile_inv.append(1.0/v)

        profile_inv = moving_avg(profile_inv, win_size)
        scorepos = score_list_2_scorepos(profile_inv, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn+"-inv")

    for d in os.listdir(path1):
        fn = f"{path1}/{d}/diff_mp_selfjoin.txt"
        win_size = int(d)
        profile, index = read_matrix_profile_from_file(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)

    for d in os.listdir(path1):
        fn = f"{path1}/{d}/diff_mp_abjoin.txt"
        win_size = int(d)
        profile, index = read_matrix_profile_from_file(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)

    for d in os.listdir(path1):
        fn = f"{path1}/{d}/diff_mp_abjoin_normalized.txt"
        if not os.path.exists(fn):
            continue
        win_size = int(d)
        profile = read_score(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)

    # diff_small does not work
    # diff_mp_selfjoin_normalized.txt does not work
    # diff_mp_allselfjoin_normalized.txt does not work

    #=======================================================================================
    # ACC
    #=======================================================================================
    for d in os.listdir(path1):
        fn = f"{path1}/{d}/acc_p2p.txt"
        win_size = int(d)
        profile = read_score(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)

        profile_inv = []
        for v in profile:
            if v == 0.0:
                profile_inv.append(float('-inf'))
            else:
                profile_inv.append(1.0/v)
        profile_inv = moving_avg(profile_inv, win_size)
        scorepos = score_list_2_scorepos(profile_inv, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn+"-inv")

    for d in os.listdir(path1):
        fn = f"{path1}/{d}/acc_std.txt"
        win_size = int(d)
        profile = read_score(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)

        profile_inv = []
        for v in profile:
            if v == 0.0:
                profile_inv.append(float('-inf'))
            else:
                profile_inv.append(1.0/v)
        profile_inv = moving_avg(profile_inv, win_size)
        scorepos = score_list_2_scorepos(profile_inv, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn+"-inv")

    for d in os.listdir(path1):
        fn = f"{path1}/{d}/acc_mp_selfjoin.txt"
        win_size = int(d)
        profile, index = read_matrix_profile_from_file(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)

    for d in os.listdir(path1):
        fn = f"{path1}/{d}/acc_mp_abjoin.txt"
        win_size = int(d)
        profile, index = read_matrix_profile_from_file(fn)
        profile = moving_avg(profile, win_size)
        scorepos = score_list_2_scorepos(profile, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn)

    # acc_mp_selfjoin_normalized.txt does not work
    # acc_mp_abjoin_normalized.txt does not work


    # mad does not work.
    # fcm does not work.

    if len(scorepos_l) == 0:
        print (file_no, 0, "scorepos_l is empty")
        return None

    max_scorepos = scorepos_l[0]
    for sp in scorepos_l[1:]:
        if sp.ratio > max_scorepos.ratio:
            max_scorepos = sp
    
    print (file_no, max_scorepos.largest_score_idx, max_scorepos.ratio, max_scorepos.reason)

    return max_scorepos
        

if __name__ == "__main__":
    of = open("output/main3.csv", "w+")
    of.write("No.,location\n")

    from_file_no = int(sys.argv[1]) 
    
    for fn in os.listdir("samples"):
        file_no = int(fn.split("_")[0])
        if file_no < from_file_no:
            continue

        train_size = get_train_size_from_filename("samples/"+fn)

        # if file_no in [239,240,241]:
        #     of.write(f"{file_no},0\n")
        # else:
        max_scorepos = deal_one(file_no, train_size)
        if max_scorepos is None:
            of.write(f"{file_no},0\n")
        else:
            of.write(f"{file_no},{max_scorepos.largest_score_idx}\n")

    of.close()
