if __name__ == "__main__":

    for sample_file in os.listdir("samples_tmp"):
        of = open("samples" + os.path.sep + sample_file, "w+")
        for line in open("samples_tmp" + os.path.sep + sample_file):
            line = line.strip()
            if len(line) == 0:
                continue
            term_l = line.split()
            for term in term_l:
                term = term.strip()
                if len(term) == 0:
                    continue
                else:
                    of.write(f"{term}\n")

        of.close()