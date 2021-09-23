from base_win_size_l import *

def has_nan_profile(fn):
    for line in open(fn):
        profile,index = line.strip().split(",")
        if profile == 'nan':
            return True
    return False

for file_no in range(1,251):
    for ws in win_size_l:
        path = f"interdata\{file_no}\{ws}\\mp_abjoin.txt"

        if has_nan_profile(path):
            print("Yes, path:",path)