import os
import sys

def get_save_path(filename):
    if getattr(sys, 'frozen', False):
        # Running from .exe — save next to the .exe
        return os.path.join(os.path.dirname(sys.executable), filename)
    else:
        # Running from script — save in current working dir
        return os.path.join(os.getcwd(), filename)

max_score_file = get_save_path('BallBounce_HIGH_SCORE.txt')


def load_max_score():
    if os.path.exists(max_score_file):
        with open(max_score_file, 'r') as file:
            try:
                return int(file.read())
            except:
                return 0
    else:
        return 0

def save_max_score(score):
    with open(max_score_file, 'w') as file:
        file.write(str(score))




def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)