#All high scores will be saved as name........score. Total string length will be 20,
#with name being at most 10 long and dots filling the gap between name and score.

def score_from_string(score_string):
    #Our strings will, by design, be formatted to end with \n. So remember this!
    i = len(score_string)
    while score_string[i-1] != ".":
        i = i-1
    try:
        return int(score_string[i:len(score_string)])
    except:
        pass

def score_to_string(score, name):
    if len(name) > 10:
        pass
    else:
        score_string = str(score)
        while len(score_string)<20 - len(name):
            score_string = "." + score_string
        return name + score_string

def save_score_to_file(score, name):
    f = open("C:/Users/Eddie Revell/Documents/Learning Python/Games/Pacman/game/high_scores.txt", "r+")
    if f.read() == "":
        f.write(score_to_string(score, name))
    else:
        f.close() #we've read the file so need to reopen it.
        f = open("C:/Users/Eddie Revell/Documents/Learning Python/Games/Pacman/game/high_scores.txt", "r+")
        file_content = ""
        line_counter = 0
        score_added = False
        for line in f:
            if line == "\n":
                file_content = file_content + "\n"
            elif line_counter<=8:
                if score_from_string(line) < score and not(score_added):
                    file_content = file_content + score_to_string(score, name) + "\n" + line
                    score_added = True
                    line_counter +=2
                else:
                    file_content = file_content + line
                    line_counter += 1
            elif line_counter == 9:
                if score_from_string(line) < score and not(score_added):
                    file_content = file_content + score_to_string(score, name) + "\n"
                    score_added = True
                    line_counter +=1
                else:
                    file_content = file_content + line
                    line_counter += 1
        if line_counter<10 and not(score_added):
            file_content = file_content + "\n" + score_to_string(score, name)
        f.close()
        open("C:/Users/Eddie Revell/Documents/Learning Python/Games/Pacman/game/high_scores.txt", "w").close()
        f = open("C:/Users/Eddie Revell/Documents/Learning Python/Games/Pacman/game/high_scores.txt", "r+")
        f.write(file_content)
    f.close()

def get_low_and_high_scores():
    scores = []
    f = open("C:/Users/Eddie Revell/Documents/Learning Python/Games/Pacman/game/high_scores.txt", "r")
    for line in f:
        scores.append(score_from_string(line))
    f.close()
    if len(scores) == 0:
        return 0, 0
    else:
        min , max = scores[0], scores[0]
        for score in scores:
            if score<min:
                min = score
            if score>max:
                max = score
        if len(scores)== 10:
            return min, max
        else:
            return 0, max
