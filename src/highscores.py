import os

HIGHSCORES_FILE = "highscores.txt"
MAX_HIGHSCORES = 5

def read_highscores():
    if not os.path.exists(HIGHSCORES_FILE):
        return []
    
    with open(HIGHSCORES_FILE, "r") as f:
        lines = f.readlines()
        highscores = [int(line.strip()) for line in lines]
        return highscores

def write_highscores(highscores):
    with open(HIGHSCORES_FILE, "w") as f:
        for score in highscores:
            f.write(f"{score}\n")

def add_highscore(score):
    highscores = read_highscores()

    if score not in highscores:
        highscores.append(score)
        highscores.sort(reverse=True)
        highscores = highscores[:MAX_HIGHSCORES]
        write_highscores(highscores)

    return highscores
