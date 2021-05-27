import os
import pyscamp as mp
import numpy as np
from scipy.fftpack import fft,ifft

from luminol.anomaly_detector import AnomalyDetector

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

def mp_detect_selfjoin(ts, win_size):
    profile, index = mp.selfjoin(ts, win_size)
    max_index = np.argmax(profile)
    return profile[max_index], max_index, profile

def mp_detect_abjoin(ts, query, win_size):
    profile, index = mp.abjoin(ts, query, win_size)
    max_index = np.argmax(profile)
    return profile[max_index], max_index, profile

def luminol_detect_dd(ts, smoothing_factor=None):
    ts2 = {}
    for idx,value in enumerate(ts):
        ts2[idx] = value
    ap = {}
    if smoothing_factor is not None:
        ap['smoothing_factor'] = smoothing_factor
    my_detector = AnomalyDetector(ts2, algorithm_name="derivative_detector", algorithm_params=ap)
    anomaly_score_l = [value for timestamp, value in my_detector.get_all_scores().iteritems()]
    return anomaly_score_l


def read_train_test(file_path, train_size):
    train = []
    test = []
    for idx, line in enumerate(open(file_path)):
        if idx < train_size:
            train.append(float(line.strip()))
        else:
            test.append(float(line.strip()))
    return train, test

def zl(length):
    return [0 for i in range(length)]


def read_lu_dd_02(file_no):
    file_path = os.path.join("lu_dd_output"+os.path.sep+"0.2", str(file_no)+".txt")
    lu_score_l = []
    for line in open(file_path):
        lu_score_l.append(float(line.strip()))
    return lu_score_l


def read_rra(win_size, file_no):
    file_path = os.path.join("gv_rra_output"+os.path.sep+f'{win_size}', str(file_no)+".txt")
    if not os.path.exists(file_path):
        return None
    l = []
    for line in open(file_path):
        if line.startswith("discord "):
            pos = line.strip().split("position")[1].split()[0].strip().split(',')[0]
            l.append(int(pos))
    return l

def read_hotsax_test(win_size, file_no):
    file_path = os.path.join("gv_hotsax_output"+os.path.sep+f'{win_size}', str(file_no)+".txt")
    if not os.path.exists(file_path):
        return None
    l = []
    for line in open(file_path):
        if line.startswith("discord "):
            pos = line.strip().split("position")[1].split()[0].strip().split(',')[0]
            l.append(int(pos))
    return l

def read_hotsax_all(win_size, file_no, train_size):
    file_path = os.path.join("gv_hotsax_all_output"+os.path.sep+f'{win_size}', str(file_no)+".txt")
    if not os.path.exists(file_path):
        return None
    l = []
    for line in open(file_path):
        if line.startswith("discord "):
            pos = line.strip().split("position")[1].split()[0].strip().split(',')[0]
            if int(pos) >= train_size:
                l.append(int(pos) - train_size)
    return l


def to50fold(n):
    return (int(n) // 50 + 1) * 50


def to25fold(n):
    return (int(n) // 25 + 1) * 25

if __name__ == "__main__":
    print (read_hotsax(8))
