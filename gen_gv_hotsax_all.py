import os
import sys

if __name__ == "__main__":
    win_size = int(sys.argv[1])
    for fn in os.listdir("samples"):
        file_no = int(fn.split("_")[0])
        fp = os.path.join("samples", fn)
        os.system(f"java -cp grammarviz2_src/target/grammarviz2-0.0.1-SNAPSHOT-jar-with-dependencies.jar net.seninp.grammarviz.GrammarVizAnomaly -alg HOTSAX  -n 10 -w {win_size} -p 4 -a 4 -i {fp} > gv_raasampled_output/{win_size}/{file_no}.txt")