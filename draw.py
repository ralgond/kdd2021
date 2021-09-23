import sys

import matplotlib.pyplot as plt

from base import * 

if __name__ == "__main__":

    ab_index_d1 = {}
    for idx, line in enumerate(open("output/main.csv")):
        if idx == 0: continue
        file_no, ab_index = line.strip().split(',')
        ab_index_d1[int(file_no)] = int(ab_index)

    ab_index_d2 = {}
    for idx, line in enumerate(open("output/main2.csv")):
        if idx == 0: continue
        file_no, ab_index = line.strip().split(',')
        ab_index_d2[int(file_no)] = int(ab_index)

    
    from_file_no = int(sys.argv[1])

    for fn in os.listdir("samples"):

        file_no = int(fn.split("_")[0])
        if file_no < from_file_no:
            continue

        train_size = get_train_size_from_filename("samples/"+fn)

        train, test = read_train_test("samples/"+fn, train_size)

        all_data = train.copy()
        all_data.extend(test)

        print (file_no, len(all_data), cal_window_size(all_data))

        ab_index_1 = ab_index_d1[file_no]
        ab_index_2 = ab_index_d2[file_no]

        #plt.cla()
        plt.figure(figsize=(10,1))
        plt.title(f"{file_no}")
        plt.plot([i for i in range(len(all_data))], all_data, color="gray")
        plt.axvline(ab_index_1, color="red")
        plt.axvline(ab_index_2, color="blue")
        plt.show()

