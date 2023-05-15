# Finding maximum score
import os


def find_max():
    max = 0
    path = os.getcwd()
    file = open("{}//score.txt".format(path), "r")
    for line in file:
        line = int(line)
        if line > max:
            max = line
    return str(max)

