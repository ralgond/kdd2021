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

def luminol_detect(ts):
    ts2 = {}
    for idx,value in enumerate(ts):
        ts2[idx] = value
    my_detector = AnomalyDetector(ts2, algorithm_name="derivative_detector")
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