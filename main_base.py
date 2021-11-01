import os
import sys
import math
from base import *

class ScorePos:
    def __init__(self, largest_score, largest_score_idx, second_largest_score, second_largest_score_idx):
        self.largest_score = largest_score
        self.largest_score_idx = largest_score_idx
        self.second_largest_score = second_largest_score
        self.second_largest_score_idx = second_largest_score_idx
        self.ratio = largest_score / second_largest_score
        self.reason = ""


def _score_list_2_scorepos(profile, win_size, train_size, add_train_size):
    ret = topk(profile, 2, win_size)

    if len(ret) < 2:
        return None

    largest_score_idx = ret[0]
    largest_score = profile[largest_score_idx]
    second_largest_score_idx = ret[1]
    second_largest_score = profile[second_largest_score_idx]

    if second_largest_score == 0.0:
        return None
        
    if math.isnan(largest_score) or math.isnan(second_largest_score):
        return None

    if add_train_size:
        return ScorePos(float(largest_score), int(largest_score_idx) + train_size, 
            float(second_largest_score), int(second_largest_score_idx) + train_size)
    else:
        return ScorePos(float(largest_score), int(largest_score_idx), 
            float(second_largest_score), int(second_largest_score_idx))


def score_list_2_scorepos(profile, win_size, train_size, add_train_size):
    try:
        scorepos = _score_list_2_scorepos(profile, win_size, train_size, add_train_size)
        if scorepos is None:
            return None
        if scorepos.largest_score in [float("nan"), float("inf"), float("-inf")]:
            return None
        else:
            return scorepos
    except Exception as e:
        print (e)
        return None


def add_scorepos(scorepos_l, scorepos, reason, train_size):
    if scorepos is None:
        return

    if scorepos.largest_score_idx < train_size:
        return
    
    scorepos_l.append(scorepos)
    scorepos.reason = reason


def moving_avg(s, win_size):
    ret = [float('nan') for _ in range(0, win_size)]
    #ret2 = np.convolve(s, np.ones(2*win_size)/(2*win_size), mode='valid').tolist()
    ret2 = np.convolve(s, np.ones(win_size)/(win_size), mode='valid').tolist()
    ret.extend(ret2)
    return ret

def read_score(file_path):
    score_l = []
    for line in open(file_path):
        score = float(line.strip())
        score_l.append(score)
    return score_l

