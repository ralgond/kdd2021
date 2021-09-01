import pyscamp as mp

def mp_detect_selfjoin(ts, win_size):
    profile, index = mp.selfjoin(ts, win_size)
    max_index = np.argmax(profile)
    return profile[max_index], max_index, profile

def mp_detect_abjoin(ts, query, win_size):
    profile, index = mp.abjoin(ts, query, win_size)
    max_index = np.argmax(profile)
    return profile[max_index], max_index, profile