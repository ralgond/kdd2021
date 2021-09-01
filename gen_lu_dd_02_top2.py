import sys
import os
import numpy as np
from base import *

if __name__ == "__main__":
    output_path_1 = "lu_dd_top2_output/0.2"
    os.system(f"mkdir -p {output_path_1}")
    for if1 in os.listdir("lu_dd_output/0.2"):
        file_no = int(if1.split(".")[0])

        if2 = "lu_dd_output/0.2"+"/"+if1

        scores = []
        for line in open(if2):
            scores.append(float(line.strip()))
        
        win_size = cal_window_size(scores)
        if win_size > 800:
            win_size = 800

        output_path = output_path_1 + "/" + if1

        print (file_no, len(scores), win_size, output_path)

        max_idx_l = topk(scores, 2, win_size)

        of = open(output_path, "w+")
        for max_idx in max_idx_l:
            of.write(f"{scores[max_idx]},{max_idx}\n")
        of.close()

        

