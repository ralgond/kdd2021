import pyscamp as mp # Uses GPU if available and CUDA was available during the build
import numpy as np
import os
import sys
import math

import matplotlib.pyplot as plt

from base import *

def mp_detect_selfjoin_multiwin(ts, win_size_l):
    l = []
    p_l = []
    for w in win_size_l:
        p, pi, profile = mp_detect_selfjoin(ts, w)
        l.append((p/math.sqrt(w), pi, w))
        p_l.append(profile)

    l.sort(key=lambda x: x[0], reverse=True)
    return l[0], p_l

def mp_detect_abjoin_multiwin(ts, query, win_size_l):
    l = []
    p_l = []
    for w in win_size_l:
        p, pi, profile = mp_detect_abjoin(ts, query, w)
        l.append((p/math.sqrt(w), pi, w))
        p_l.append(profile)

    l.sort(key=lambda x: x[0], reverse=True)
    return l[0], p_l

if __name__ == '__main__':
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "samples"))
    result_file_name_prefix = sys.argv[0].split(".")[0]
    start_file_no = int(sys.argv[1])

    #of = open(result_file_name_prefix+".csv", "a+")
    #of.write("No.,location\n")
    #of2 = open(result_file_name_prefix+"_winsize.csv", "a+")
    #of2.write("No.,winsize\n")
    for sample_file in os.listdir(sample_dir):
        file_no = int(sample_file.split("_")[0])
        if file_no < start_file_no:
            continue

        train_size = get_train_size_from_filename(sample_file)

        all_data = []
        for line in open(os.path.join(sample_dir, sample_file)):
            all_data.append(float(line.strip()))


        train = all_data[:train_size].copy()
        test = all_data[train_size:].copy()


        mp_value = 0.0
        window_size = 0
        outlier_pos = 0
        if file_no in [239,240,241]:
            outlier_pos, window_size = 0 + train_size, 0 #give up large samples
        else:
            fft_win_size = cal_window_size(train)
            all_wins2 = [fft_win_size]
            all_wins2.extend([25, 50, 100, 150, 200, 300, 400, 500, 600, 700, 800])

            plt.cla()
            #plt.figure(figsize=(100,100))
            plt.subplot(len(all_wins2)+2, 1, 1)
            plt.title("{} - fft_win_size={}".format(file_no, fft_win_size))
            plt.plot([i for i in range(len(train))], train, color="green")
            plt.plot([i + train_size for i in range(len(test))], test, color="blue")

            
            #draw luminol
            if len(all_data) < 100 * 1000:
                lu_anomaly_score_l = luminol_detect(test)
                plt.subplot(len(all_wins2)+2, 1, 2)
                plt.ylabel("lu")
                plt.plot([i for i in range(len(train))], [0 for i in range(len(train))])
                plt.plot([i + train_size for i in range(len(lu_anomaly_score_l))], lu_anomaly_score_l)
                if len(lu_anomaly_score_l) < len(test):
                        plt.plot([i + train_size + len(lu_anomaly_score_l) for i in range(len(test)- len(lu_anomaly_score_l))], 
                                [0 for i in range(len(test)- len(lu_anomaly_score_l))])
                lu_anomaly_score_max_index = np.argmax(lu_anomaly_score_l) + train_size
                plt.axvline(lu_anomaly_score_max_index, color="black")

            #draw matrix profile
            res, p_l = mp_detect_abjoin_multiwin(test, train, all_wins2)
            for idx, profile in enumerate(p_l):
                plt.subplot(len(all_wins2)+2, 1, 3+idx)
                plt.ylabel("{}".format(all_wins2[idx]))
                plt.plot([i for i in range(len(train))], [0 for i in range(len(train))])
                plt.plot([i + train_size for i in range(len(profile))], profile)
                if len(profile) < len(test):
                    plt.plot([i + train_size + len(profile) for i in range(len(test)- len(profile))], [0 for i in range(len(test)- len(profile))])

                max_index = np.argmax(profile) + train_size
                plt.axvline(max_index, color="black")
            plt.show()

            res_p, res_pi, res_w = res
            #res_p, res_pi, res_w = detect2_1(test, train, [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
            outlier_pos = res_pi + train_size
            window_size = res_w
            mp_value = res_p

            

        print(file_no, mp_value, outlier_pos, window_size)
        sys.stdout.flush()
        
        #of.write(""+str(file_no)+","+str(outlier_pos)+"\n")
        #of.flush()
        #of2.write(""+str(file_no)+","+str(window_size)+"\n")
        #of2.flush()

        
    #of.close()
    #of2.close()