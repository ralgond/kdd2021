
import sys
from base import *
import numpy as np

def autocorr(x):
    n = x.size
    norm = (x - np.mean(x))
    result = np.correlate(norm, norm, mode='same')
    acorr = result[n//2 + 1:] / (x.var() * np.arange(n-1, n//2, -1))
    lag = np.abs(acorr).argmax() + 1
    r = acorr[lag-1]        
    if np.abs(r) > 0.5:
      print('Appears to be autocorrelated with r = {}, lag = {}'. format(r, lag))
    else: 
      print('Appears to be not autocorrelated')
    return r, lag

if __name__ == "__main__":
    train_size = get_train_size_from_filename(sys.argv[1])

    train, test = read_train_test(sys.argv[1], train_size)

    win_size = cal_window_size(train)

    print(f"fft, {win_size}")

    autocorr(np.array(train))