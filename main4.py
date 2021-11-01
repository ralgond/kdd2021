import os
import sys
import math
from base import *

from main_base import *


def deal_one_1(path1, file_name, scorepos_l, train_size, add_train_size = True):
    for d in os.listdir(path1):
        fn = f"{path1}/{d}/{file_name}"
        win_size = int(d)
        scores = read_score(fn)
        scores = moving_avg(scores, win_size)
        scorepos = score_list_2_scorepos(scores, win_size, train_size, add_train_size = True)
        add_scorepos(scorepos_l, scorepos, fn, train_size)

def deal_one(file_no, train_size):
    # lu does not work

    scorepos_l = []
    path1 = f"interdata/{file_no}"

    #=======================================================================================
    # ORIG
    #=======================================================================================
    # deal_one_1(path1, "orig_mp_abjoin.txt", scorepos_l, train_size)
    # deal_one_1(path1, "orig_mp_selfjoin.txt", scorepos_l, train_size)
    deal_one_1(path1, "orig_mp_abjoin_withpen.txt", scorepos_l, train_size)
    deal_one_1(path1, "orig_mp_selfjoin_withpen.txt", scorepos_l, train_size)

    #deal_one_1(path1, "orig_np_abjoin.txt", scorepos_l, train_size)
    #deal_one_1(path1, "orig_np_selfjoin.txt", scorepos_l, train_size)


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

    # diff_small does not work
    # diff_mp_selfjoin_normalized.txt does not work
    # diff_mp_allselfjoin_normalized.txt does not work

    #=======================================================================================
    # ACC
    #=======================================================================================

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
    of = open("output/main4.csv", "w+")
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
