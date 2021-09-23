def read_hotsax(file_path, train_size, add_train_size = True):
    lines = []
    for line in open(file_path):
        if line.startswith("discord #"):
            lines.append(line)
        if len(lines) == 2:
            break
    
    pos, score = lines[0].split(', info string: ')[0].split(', at ')[1].split(' distance to closest neighbor: ')
    largest_score_idx = int(pos)
    largest_score = float(score)
    #print(largest_score_idx, largest_score, file_path)

    pos, score = lines[1].split(', info string: ')[0].split(', at ')[1].split(' distance to closest neighbor: ')
    second_largest_score_idx = int(pos)
    second_largest_score = float(score)
    #print(second_largest_score_idx, second_largest_score, file_path)

    if math.isnan(largest_score) or math.isnan(second_largest_score):
        return None

    if add_train_size:
        return ScorePos(float(largest_score), int(largest_score_idx) + train_size, 
            float(second_largest_score), int(second_largest_score_idx) + train_size)
    else:
        return ScorePos(float(largest_score), int(largest_score_idx), 
            float(second_largest_score), int(second_largest_score_idx))