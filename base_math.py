import numpy as np
import rolling

def sliding_window_std(s, window_size):
    from numpy.lib.stride_tricks import sliding_window_view

    swv = sliding_window_view(np.array(s), window_shape=window_size)

    return np.std(swv, axis=1)

def sliding_window_skewness(s, window_size):
    return list(rolling.Skew(s, window_size))

def sliding_window_mad(s, window_size):
    from numpy.lib.stride_tricks import sliding_window_view

    swv = sliding_window_view(np.array(s), window_shape=window_size)

    ret = []
    for l in swv:
        x_hat = np.median(l)
        mad = np.median(np.abs(np.array(l) - x_hat))
        #print(l, x_hat, mad)
        ret.append(mad)
    return ret

