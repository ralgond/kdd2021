import os
import sys

if __name__ == "__main__":
    for fn in os.listdir("samples"):
        file_no = int(fn.split("_")[0])
        fp = os.path.join("samples", fn)
        os.system(f"java -cp grammarviz2_src/target/grammarviz2-0.0.1-SNAPSHOT-jar-with-dependencies.jar net.seninp.grammarviz.GrammarVizAnomaly -alg RRASAMPLED  -b 10,100,10,4,5,10,4,5,2 -i {fp} > gv_raasampled_output/{file_no}.txt")