import platform
import os


def clear_terminal():
    os.system('cls' if platform.system().lower() == 'windows' else 'reset')