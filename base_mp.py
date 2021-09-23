import pyscamp as mp
import numpy as np

def mp2_selfjoin(ts, win_size):
    profile, index = mp.selfjoin(ts, win_size)
    return profile, index

def mp2_abjoin(ts, query, win_size):
    profile, index = mp.abjoin(ts, query, win_size)
    return profile, index

import stumpy
def mp_selfjoin(ts, win_size):
    ts = [v*1.0 for v in ts]
    res = stumpy.stump(ts, win_size)
    return res[:,0], res[:,1]

def mp_abjoin(ts, query, win_size):
    ts = [v*1.0 for v in ts]
    query = [v*1.0 for v in query]
    res = stumpy.stump(T_B = query, T_A = ts, m = win_size, ignore_trivial = False)
    return res[:,0], res[:,1]

def read_matrix_profile_from_file(file_path):
    profile = []
    index = []
    if1 = open(file_path)
    for line in if1:
        p, i = line.strip().split(',')
        profile.append(float(p))
        index.append(int(i))
    if1.close()

    return profile, index
