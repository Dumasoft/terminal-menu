import os
import platform


def clear_terminal():
    os.system('cls') if platform.system().lower() == 'windows' else os.system('reset')
