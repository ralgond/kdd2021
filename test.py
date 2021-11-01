import numpy as np
import pandas as pd

import rolling 

def moving_avg(s, win_size):
    ret = [float('-inf') for _ in range(0, win_size)]
    ret2 = np.convolve(s, np.ones(2*win_size)/(2*win_size), mode='valid').tolist()
    ret.extend(ret2)
    return ret

def test01():
    ret = moving_avg([1, 2, 3, 4, 5, 6], 3)
    print(ret)

def test02():
    l = [float('nan'), 1, 2, 3, 4, 5, 6]
    print(list(rolling.Max(l, 3)))

def test03():
    a = float('nan')
    print (a + 1)
    print (max([a, 1]))

    l = [float('nan'), 1, 2, 3, 4, 5, 6]
    print (np.argmax(l))

def test04():
    ret = moving_avg([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)
    print (ret)

def test05():
    l = [1, 2, 3, 4, 5, 7]
    #l = [float('nan'), 1, 2, 3, 4, 5, 6]
    print(list(rolling.Std(l, 3)))

def test06():
    #l = [1, 2, 3, 4, 5, 7]
    l = [float('nan'), 1, 2, 3, 4, 5, 6]
    s = pd.Series(l)
    print(s.rolling(3).std())


import numpy as np

def test09():
    l = [float("nan"), 1, 3,6,4]
    print(np.nanargmax(l))


def moving_avg(s, win_size):
    ret = [float('nan') for _ in range(0, win_size)]
    ret2 = np.convolve(s, np.ones(2*win_size)/(2*win_size), mode='valid').tolist()
    ret.extend(ret2)
    return ret

def test10():
    l = [float("nan"), 1, 2, 3, 4, float("nan"), 5, 6, 7, 8]
    print(moving_avg(l, 2))


import numpy as np
import pandas as pd

import pyscamp as mp
def test11():
    # fn = 'samples/001_UCR_Anomaly_35000.txt'

    fn = 'samples/239_UCR_Anomaly_190037.txt'

    number = int(fn.split("/")[1].split("_")[0])
    split = int(fn.split('_')[-1].split('.')[0])

    X = np.loadtxt(fn)
    print (X.dtype)

    profile, index = mp.abjoin(X[split:], X[:split], 25)

    print (type(profile))
    print (profile)

def test12():
    a = np.array([1,2,3, float("nan")])
    b = np.array([1,2,3,4])
    print (a*b)

if __name__ == "__main__":
    test12()