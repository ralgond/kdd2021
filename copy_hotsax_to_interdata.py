import os

if __name__ == "__main__":
    win_size_l = [25, 50, 75, 100, 125, 150, 175, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800]

    for file_no in range(1, 251):
        for win_size in win_size_l:
            if_path = f"gv_hotsax_output/{win_size}/{file_no}.txt"
            out_path = f"interdata/{file_no}/{win_size}/hotsax.txt"

            infile = open(if_path)
            outfile = open(out_path, "w+")
            for line in infile:
                outfile.write(line)
            infile.close()
            outfile.close()