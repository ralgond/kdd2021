import numpy as np
import pandas as pd
import stumpy

# Select stump function
stump = stumpy.stump

def compute_score(X, number, split, w):
    # original time series (orig)
    seq = pd.DataFrame(X, columns=['orig'])

    # matrix profile value (mpv) and index (mpi)
    mpv = {}
    mpi = {}
    for mode in ['train', 'join', 'all']:
        if mode == 'train':
            mp = stump(X[:split], w)
        elif mode == 'join':
            mp = stump(X[split:], w, X[:split], ignore_trivial=False)
        elif mode == 'all':
            mp = stump(X, w)
        mpv[mode] = mp[:, 0].astype(float)
        mpi[mode] = mp[:, 1].astype(int)
    
    # matrix profile (mp) and normalized profile (np) for novelty detection (AB-join)
    numer = mpv['join']
    denom = mpv['train'][mpi['join']]
    begin = split
    end = begin + len(numer) - 1
    seq.loc[begin:end, 'orig_mp_novelty'] = numer
    with np.errstate(all='ignore'):
        seq.loc[begin:end, 'orig_np_novelty'] = numer / denom
    print (seq.loc[begin:end, 'orig_np_novelty'])

if __name__ == '__main__':
    fn = 'samples/001_UCR_Anomaly_35000.txt'

    number = int(fn.split("/")[1].split("_")[0])
    split = int(fn.split('_')[-1].split('.')[0])

    X = np.loadtxt(fn)

    compute_score(X, number, split, 25)