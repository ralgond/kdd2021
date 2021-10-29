import numpy as np
import pandas as pd

import pyscamp as mp

if __name__ == '__main__':
    # fn = 'samples/001_UCR_Anomaly_35000.txt'

    fn = 'samples/239_UCR_Anomaly_190037.txt'

    number = int(fn.split("/")[1].split("_")[0])
    split = int(fn.split('_')[-1].split('.')[0])

    X = np.loadtxt(fn)
    print (X.dtype)

    profile, index = mp.abjoin(X[split:], X[:split], 25)

    print (type(profile))
    print (profile)
