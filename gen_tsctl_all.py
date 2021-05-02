import os

def merge_tsctl(path):
    ret = [None]
    for file_name in os.listdir(path):
        fn = os.path.join(path, file_name)
        for line in open(fn):
            arr = line.strip().split(",")
            if len(arr) == 3:
                arr.append("")
            print(",".join(arr))

if __name__ == '__main__':
    tsctl_path = "tsctl"

    merge_tsctl(tsctl_path)
                