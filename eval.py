import sys

if __name__ == "__main__":
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

        label = d[file_no]

        if pos <= label[1] and pos >= label[0]:
            cnt += 1

        total += 1

    print (cnt / total)



