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


def read_scorepos_from_file(file_path):
    if1 = open(file_path)
    largest_score, largest_score_idx = if1.readline().split(",")
    second_largest_score, second_largest_score_idx = if1.readline().split(",")
    if1.close()

    if largest_score == 'nan' or second_largest_score == 'nan':
        return None

    return ScorePos(float(largest_score), int(largest_score_idx), float(second_largest_score), int(second_largest_score_idx))


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
        scorepos = read_scorepos_from_file(fn)
        if scorepos is not None:
            scorepos_l.append(scorepos)
            #print (scorepos.ratio)
            scorepos.reason = f"lu_dd_top2_output/{d}"
            

    for d in os.listdir("mp_abjoin_output"):
        fn = f"mp_abjoin_output/{d}/{file_no}.txt"
        scorepos = read_scorepos_from_file(fn)
        if scorepos is not None:
            scorepos_l.append(scorepos)
            #print (scorepos.ratio)
            scorepos.reason = f"mp_abjoin_output/{d}"

    for d in os.listdir("mp_selfjoin_output"):
        fn = f"mp_selfjoin_output/{d}/{file_no}.txt"
        scorepos = read_scorepos_from_file(fn)
        if scorepos is not None:
            scorepos_l.append(scorepos)
            scorepos.reason = f"mp_selfjoin_output/{d}"

    for d in os.listdir("gv_hotsax_output"):
        fn = f"gv_hotsax_output/{d}/{file_no}.txt"
        scorepos = read_scorepos_from_file_hotsax(fn)
        if scorepos is not None:
            scorepos_l.append(scorepos)
            scorepos.reason = f"gv_hotsax_output/{d}"

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
        
    print (file_no, max_scorepos.largest_score_idx + train_size, max_scorepos.ratio, max_scorepos.reason)
        

if __name__ == "__main__":
    for fn in os.listdir("samples"):
        file_no = int(fn.split("_")[0])

        train_size = get_train_size_from_filename("samples/"+fn)

        deal_one(file_no, train_size)
