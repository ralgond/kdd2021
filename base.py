import os
import sys
import math

import numpy as np
from scipy.fftpack import fft,ifft

def diff(ts):
    ret = []
    ret.append(float("nan"))
    for idx, v in enumerate(ts):
        if idx == 0: 
            continue
        v = float(v)
        if math.isnan(v):
            ret.append(v)
            continue
        delta = v - ts[idx-1]
        ret.append(delta)
    return ret

def cal_window_size(timeseries):
    yf = abs(fft(timeseries))  # 取绝对值
    yfnormlize = yf / len(timeseries)  # 归一化处理
    yfhalf = yfnormlize[range(int(len(timeseries) / 2))]  # 由于对称性，只取一半区间
    yfhalf = yfhalf * 2   # y 归一化

    xf = np.arange(len(timeseries))  # 频率
    xhalf = xf[range(int(len(timeseries) / 2))]  # 取一半区间

    max_value_idx = -1
    max_value = 0
    for idx, value in enumerate(yfhalf):
        if idx == 0:
            continue
        if (value > max_value):
            max_value = value
            max_value_idx = idx

    window_size = len(timeseries) / max_value_idx
    return int(window_size)

def get_train_size_from_filename(filename):
    return int(filename.split('_')[-1].split('.')[0])


def topk(s, k, win_size):
    ret = []
    s = np.array(s).copy()

    for _ in range(k):
        max_value_idx = np.nanargmax(s)
        if s[max_value_idx] == -np.inf:
            break

        ret.append(max_value_idx)

        left = max(0, int(max_value_idx-win_size))
        right = min(len(s), int(max_value_idx+win_size))
        s[left:right] = -np.inf
    
    return ret

def zl(length):
    return [0 for i in range(length)]

import pyscamp as mp
import numpy as np

def mp2_selfjoin(ts, win_size):
    profile, index = mp.selfjoin(ts, win_size)
    return profile, index

def mp2_abjoin(ts, query, win_size):
    profile, index = mp.abjoin(ts, query, win_size)
    return profile, index

import stumpy
def mp_selfjoin(ts, win_size, normalize=True):
    ts = [v*1.0 for v in ts]
    res = stumpy.stump(ts, win_size, normalize=normalize)
    return res[:,0], res[:,1]

def mp_abjoin(ts, query, win_size, normalize=True):
    ts = [v*1.0 for v in ts]
    query = [v*1.0 for v in query]
    res = stumpy.stump(T_B = query, T_A = ts, m = win_size, ignore_trivial = False, normalize=normalize)
    return res[:,0], res[:,1]

