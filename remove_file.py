from numpy import frombuffer


from base_win_size_l import *
import os

for i in range(0,251):
    path1 = f"interdata\\{i}"

    print(path1)
    for w in win_size_l:
        path2 = path1+f"\\{w}"

        # os.system(f"del {path2}\\acc_mad.txt")
        # os.system(f"del {path2}\\acc_skew.txt")

        # os.system(f"del {path2}\\diff_mad.txt")
        # os.system(f"del {path2}\\entropy_orig.txt")

        # os.system(f"del {path2}\\hotsax.txt")
        # os.system(f"del {path2}\\orig_mad.txt")
        # os.system(f"del {path2}\\orig_median.txt")

        
        # os.system(f"del {path2}\\nmp_abjoin.txt")
        # os.system(f"del {path2}\\nmp.txt")
        # os.system(f"del {path2}\\nmp_selfjoin.txt")
        # os.system(f"del {path2}\\fcm.txt")
        # os.system(f"del {path2}\\nozmp_abjoin_normalized.txt")

        # os.system(f"del {path2}\\mp_abjoin_normalized.txt")
        # os.system(f"del {path2}\\mp_selfjoin_normalized.txt")
        # os.system(f"del {path2}\\mp_selfjoin_normalized_scramp.txt")

        # os.system(f"ren {path2}\\p2p_orig.txt orig_p2p.txt")
        # os.system(f"ren {path2}\\p2p_diff.txt diff_p2p.txt")
        # os.system(f"ren {path2}\\p2p_acc.txt acc_p2p.txt")

        os.system(f"del {path2}\\diff_small.txt")
        os.system(f"del {path2}\\mp_all_selfjoin.txt")
        