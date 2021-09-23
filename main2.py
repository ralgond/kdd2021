import os
from base import *

class ScorePos:
    def __init__(self, largest_score, largest_score_idx, second_largest_score, second_largest_score_idx):
        self.largest_score = largest_score
        self.largest_score_idx = largest_score_idx
        self.second_largest_score = second_largest_score
        self.second_largest_score_idx = second_largest_score_idx
        self.ratio = largest_score / second_largest_score
        self.reason = ""


def read_scorepos_from_file(file_path, train_size, add_train_size = True):
    if1 = open(file_path)
    largest_score, largest_score_idx = if1.readline().split(",")
    second_largest_score, second_largest_score_idx = if1.readline().split(",")
    if1.close()

    if largest_score == 'nan' or second_largest_score == 'nan':
        return None

    if add_train_size:
        return ScorePos(float(largest_score), int(largest_score_idx) + train_size, 
            float(second_largest_score), int(second_largest_score_idx) + train_size)
    else:
        return ScorePos(float(largest_score), int(largest_score_idx), 
            float(second_largest_score), int(second_largest_score_idx))


def read_scorepos_from_file_hotsax(file_path):
    def read_scorepos_from_file_hotsax_one_line(line):
        s = line.split(",")[1].strip().split()
        return float(s[-1]), int(s[1])

    top2_line = []
    if1 = open(file_path)
    for line in if1:
        if line.startswith("discord #"):
            top2_line.append(line)
    if1.close()

    largest_score, largest_score_idx = read_scorepos_from_file_hotsax_one_line(top2_line[0])
    second_largest_score, second_largest_score_idx = read_scorepos_from_file_hotsax_one_line(top2_line[1])

    return ScorePos(float(largest_score), int(largest_score_idx), float(second_largest_score), int(second_largest_score_idx))


def read_scorepos_from_file_rra(file_path):
    def read_scorepos_from_file_rra_one_line(line):
        s = line.split(", info string")[0].split(", at ")[-1].strip().split()
        return float(s[-1]), int(s[0])

    top2_line = []
    if1 = open(file_path)
    for line in if1:
        if line.startswith("discord #"):
            top2_line.append(line)
    if1.close()

    largest_score, largest_score_idx = read_scorepos_from_file_rra_one_line(top2_line[0])
    second_largest_score, second_largest_score_idx = read_scorepos_from_file_rra_one_line(top2_line[1])

    return ScorePos(float(largest_score), int(largest_score_idx), float(second_largest_score), int(second_largest_score_idx))


def deal_one(file_no, train_size):
    scorepos_l = []

    for d in os.listdir("lu_dd_top2_output"):
        fn = f"lu_dd_top2_output/{d}/{file_no}.txt"
        scorepos = read_scorepos_from_file(fn, train_size, add_train_size=True)
        if scorepos is not None:
            scorepos_l.append(scorepos)
            scorepos.reason = f"lu_dd_top2_output/{d}"
            

    path1 = f"interdata/{file_no}"

    for d in os.listdir(path1):
        fn = f"{path1}/{d}/mp_abjoin.txt"
        scorepos = read_scorepos_from_file(fn, train_size, add_train_size=True)
        if scorepos is not None:
            scorepos_l.append(scorepos)
            scorepos.reason = fn

    for d in os.listdir(path1):
        fn = f"{path1}/{d}/mp_selfjoin.txt"
        scorepos = read_scorepos_from_file(fn, train_size, add_train_size=True)
        if scorepos is not None:
            scorepos_l.append(scorepos)
            scorepos.reason = fn

    # for d in os.listdir(path1):
    #     fn = f"{path1}/{d}/mp_selfjoin_all.txt"
    #     scorepos = read_scorepos_from_file(fn, train_size, add_train_size=False)
    #     if scorepos is not None and scorepos.largest_score_idx >= train_size:
    #         scorepos_l.append(scorepos)
    #         scorepos.reason = fn


    # for d in os.listdir("nmp_selfjoin_all_output"):
    #     fn = f"nmp_selfjoin_all_output/{d}/{file_no}.txt"
    #     scorepos = read_scorepos_from_file(fn, train_size, add_train_size=False)
    #     if scorepos is not None and scorepos.largest_score_idx >= train_size:
    #         scorepos_l.append(scorepos)
    #         scorepos.reason = f"norm_mp_selfjoin_all_output/{d}"

    # for d in os.listdir("gv_hotsax_output"):
    #     fn = f"gv_hotsax_output/{d}/{file_no}.txt"
    #     scorepos = read_scorepos_from_file_hotsax(fn)
    #     if scorepos is not None:
    #         scorepos_l.append(scorepos)
    #         scorepos.reason = f"gv_hotsax_output/{d}"

    # for d in os.listdir("gv_rra_output"):
    #     fn = f"gv_rra_output/{d}/{file_no}.txt"
    #     scorepos = read_scorepos_from_file_rra(fn)
    #     if scorepos is not None:
    #         scorepos_l.append(scorepos)
    #         scorepos.reason = f"gv_rra_output/{d}"


    max_scorepos = scorepos_l[0]
    for sp in scorepos_l[1:]:
        if sp.ratio > max_scorepos.ratio:
            max_scorepos = sp
        
    print (file_no, max_scorepos.largest_score_idx, max_scorepos.ratio, max_scorepos.reason)

    return max_scorepos
        

if __name__ == "__main__":
    of = open("output/main2.csv", "w+")
    of.write("No.,location\n")

    for fn in os.listdir("samples"):
        file_no = int(fn.split("_")[0])

        train_size = get_train_size_from_filename("samples/"+fn)

        if file_no in [239,240,241]:
            of.write(f"{file_no},0\n")
        else:
            max_scorepos = deal_one(file_no, train_size)
            of.write(f"{file_no},{max_scorepos.largest_score_idx}\n")

    of.close()
