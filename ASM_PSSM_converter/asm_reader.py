def get_final_scores(file_path):
    scores = []
    asm_file = open(file_path, "r")
    while asm_file:
        if "finalData {" in asm_file.readline() and "scores {" in asm_file.readline():
            score_line = asm_file.readline()
            while "}" not in score_line:
                score = score_line.strip().strip(',')
                scores.append(score)
                score_line = asm_file.readline()
            break
    asm_file.close()
    return scores

