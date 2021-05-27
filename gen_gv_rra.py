import os
import sys

if __name__ == "__main__":
    win_size = int(sys.argv[1])
    for fn in os.listdir("only_test_input"):
        file_no = int(fn.split(".")[0])
        fp = os.path.join("only_test_input", fn)
        os.system(f"java -cp grammarviz2_src/target/grammarviz2-0.0.1-SNAPSHOT-jar-with-dependencies.jar net.seninp.grammarviz.GrammarVizAnomaly -alg RRA  -w {win_size} -p 4 -a 4 -i {fp} > gv_rra_output/{win_size}/{file_no}.txt")