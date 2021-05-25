
import os
import sys
from base import *

class Slot:
    def __init__(self, span, cnt):
        self.span = span
        self.cnt = cnt

    def add(self, size):
        if size <= self.span:
            self.cnt += 1
            return True
        else:
            return False

if __name__ == "__main__":
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "samples"))

    span_list = [25, 50, 75, 100, 200, 300, 400, 500]
    slot_list = [Slot(span, 0) for span in span_list]

    for sample_file in os.listdir(sample_dir):

        file_no = int(sample_file.split("_")[0])

        train_size = get_train_size_from_filename(sample_file)

        all_data = []
        for line in open(os.path.join(sample_dir, sample_file)):
            all_data.append(float(line.strip()))
        train = all_data[:train_size].copy()
        test = all_data[train_size:].copy()

        fft_win = cal_window_size(train)
        if fft_win <= 150 and fft_win > 100: 
            print(file_no, fft_win)

        for slot in slot_list:
            if slot.add(fft_win):
                continue
        
    # print (slot_list[0].span, slot_list[0].cnt)
    # for idx, slot in enumerate(slot_list[1:], start=1):
    #     print (slot.span, slot.cnt - slot_list[idx-1].cnt)

