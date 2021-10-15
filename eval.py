import sys


# def read_loess_pos():
#     d = {}
#     for idx, line in enumerate(open("output\\main3_loess.csv")):
#         if idx == 0:
#             continue
#         file_no, pos = line.strip().split(",")
#         pos = int(pos)

#         d[file_no] = pos
#     return d

if __name__ == "__main__":
    # loess_d = read_loess_pos()

    d = {}
    for line in open("labels.txt"):
        file_no, low, high = line.strip().split()
        d[file_no] = (int(low)-100, int(high)+100)

    cnt = 0
    total = 0

    for idx, line in enumerate(open(sys.argv[1])):
        if idx == 0:
            continue
        file_no, pos = line.strip().split(",")
        pos = int(pos)

        # if loess_d[file_no] != 0:
        #     pos = loess_d[file_no]

        label = d[file_no]

        if pos <= label[1] and pos >= label[0]:
            cnt += 1

        total += 1

    print (cnt / 250)



