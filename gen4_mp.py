import os
import sys
import pandas as pd

from main_base import *
from base_win_size_l import *

def write_to_file(data, file_path):
    of = open(file_path, "w+")
    for v in data:
        of.write(f"{v}\n")
    of.close()

denom_threshold = 0.1
upper_threshold = 0.75
lower_threshold = 0.25
const_threshold = 0.05
min_coef = 0.5

def gen_interdata(file_no, train_size, X):
    os.system(f"md interdata\{file_no}")

    train = X[:train_size]
    test = X[train_size:]

    for ws in win_size_l:
        path2 = f"interdata\{file_no}\{ws}"
        os.system(f"md {path2}")

        seq = pd.DataFrame(X, columns=['orig'])

        rolling_max = seq['orig'].rolling(ws).max()
        rolling_min = seq['orig'].rolling(ws).min()
        seq['orig_p2p'] = (rolling_max - rolling_min).shift(-ws)

        # coef for penalizing subsequences with little change
        name = 'orig_p2p'
        mean = seq[name].mean()
        upper = mean * upper_threshold
        lower = mean * lower_threshold
        const = mean * const_threshold
        seq['coef'] = (seq[name] - lower) / (upper - lower)
        seq['coef'].clip(upper=1.0, lower=0.0, inplace=True)
        print (seq['coef'])
        cond = (seq[name] <= const).rolling(2 * ws).max().shift(-ws) == 1
        seq.loc[cond, 'coef'] = 0.0
        print(seq['coef'].mean())
        if seq['coef'].mean() < min_coef:
            seq['coef'] = 0.0

        print (seq['coef'])

        # Generate matirx profile abjoin
        mpv, mpi = mp2_abjoin(test, train, ws)
        print(f"abjoin.len={len(mpv)}")
        begin = train_size
        end = begin + len(mpv) - 1
        mpv *= seq.loc[begin:end, 'coef']
        write_to_file(mpv, f"{path2}\\orig_mp_abjoin_withpen.txt")

        # Generate matirx profile selfjoin
        mpv, mpi = mp2_selfjoin(test, ws)
        print(f"selfjoin.len={len(mpv)}")
        begin = train_size
        end = begin + len(mpv) - 1
        mpv *= seq.loc[begin:end, 'coef']
        write_to_file(mpv, f"{path2}\\orig_mp_selfjoin_withpen.txt")

        os._exit(0)

        
if __name__ == "__main__":
    from_file_no = int(sys.argv[1]) 
    
    for fn in os.listdir("samples"):
        file_no = int(fn.split("_")[0])
        if file_no < from_file_no:
            continue

        print(file_no)

        train_size = get_train_size_from_filename("samples/"+fn)

        X = np.loadtxt("samples/"+fn)

        gen_interdata(file_no, train_size, X)