import pyscamp as mp # Uses GPU if available and CUDA was available during the build
import numpy as np
import os
import sys
import math

import matplotlib.pyplot as plt

from base import *

class Tsctl:
    def __init__(self, file_no, mp_win_size, hardcore, method_name):
        self.file_no = int(file_no)
        self.mp_win_size = int(mp_win_size)
        self.hardcore = hardcore
        self.method_name = method_name
        if (self.method_name == ''):
            self.method_name = "matrixprofile"

        if (self.method_name not in ["matrixprofile", "lu"]):
            raise ValueError(f"unsupported method: {self.method_name}")

def read_tsctl_array_all(dir_path):
    ret = [None]
    for file_name in os.listdir(dir_path):
        fn = os.path.join(dir_path, file_name)
        print(fn)
        for line in open(fn):
            arr = line.strip().split(",")
            if len(arr) == 4:
                file_no, mp_win_size, hardcore, method_name = arr[0], arr[1], arr[2], arr[3]
                ret.append(Tsctl(file_no, mp_win_size, hardcore, method_name))
            elif len(arr) == 3:
                file_no, mp_win_size, hardcore, method_name = arr[0], arr[1], arr[2], ""
                ret.append(Tsctl(file_no, mp_win_size, hardcore, method_name))

    for i in range(1, 251):
        assert(ret[i] is not None)
    return ret

def read_tsctl_array_one(file_path):
    fn = file_path.split(os.path.sep)[-1]
    _, _, start_fileno_and_end_fileno = fn.split(".")[0].split("_")
    start_fileno, end_fileno = start_fileno_and_end_fileno.split('-')
    start_fileno = int(start_fileno)
    end_fileno = int(end_fileno)
    ret = [None for i in range(0, 251)]
    for line in open(file_path):
        arr = line.strip().split(",")
        if len(arr) == 4:
            file_no, mp_win_size, hardcore, method_name = arr[0], arr[1], arr[2], arr[3]
            ret[int(file_no)]= Tsctl(file_no, mp_win_size, hardcore, method_name)
        elif len(arr) == 3:
            file_no, mp_win_size, hardcore, method_name = arr[0], arr[1], arr[2], ""
            ret[int(file_no)] = Tsctl(file_no, mp_win_size, hardcore, method_name)
        else:
            raise ValueError(f"unsupported tsctl length: {len(arr)}")
    
    for i in range(1, 251):
        if i >= start_fileno and i <= end_fileno:
            assert(ret[i] is not None)
        else:
            assert(ret[i] is None)
    
    return ret

if __name__ == '__main__':
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "samples"))
    result_file_name_prefix = sys.argv[0].split(".")[0]
    start_file_no = int(sys.argv[1])
    tsctl_path = "tsctl"
    all_or_one = sys.argv[2]
    
    tsctl_array = []
    if (all_or_one == 'all'):
        tsctl_array = read_tsctl_array_all(tsctl_path)
    elif all_or_one == 'one':
        one_argv = sys.argv[3]
        assert (one_argv.startswith("tsctl"+os.path.sep))
        tsctl_array = read_tsctl_array_one(one_argv)
        result_file_name_prefix = result_file_name_prefix + "_" + one_argv.split(os.path.sep)[-1].split('.')[0]
    else:
        raise ValueError(f"unsupported all_or_one: {all_or_one}")


    output_file_path = os.path.join("output", result_file_name_prefix+".csv")
    of = open(output_file_path, "a+")
    of.write("No.,location\n")

    for sample_file in os.listdir(sample_dir):
        file_no = int(sample_file.split("_")[0])
        if file_no < start_file_no:
            continue

        if tsctl_array[file_no] is None:
            print(f"{file_no},0")
            of.write(f"{file_no},0\n")
            of.flush()
        else:
            train_size = get_train_size_from_filename(sample_file)

            train, test = read_train_test(os.path.join(sample_dir, sample_file), train_size)

            outlier_pos = 0
            if file_no in [239,240,241]:
                outlier_pos = 0 #give up large samples
            else:
                tsctl = tsctl_array[file_no]
                if tsctl.method_name == 'matrixprofile':
                    win_size = tsctl.mp_win_size
                    p, outlier_pos, p_l = mp_detect_abjoin(test, train, win_size)
                    if (win_size > 100):
                        outlier_pos += int(win_size/2)
                elif tsctl.method_name == 'lu':
                    anomaly_score_l = luminol_detect(test)
                    outlier_pos = np.argmax(anomaly_score_l)

            outlier_pos += train_size

            print(f"{file_no},{outlier_pos}")
            of.write(f"{file_no},{outlier_pos}\n")
            of.flush()

    of.close()