import os
import platform


def clear_terminal():
    print('clear')
    os.system('cls') if platform.system().lower() == 'windows' else os.system('reset')
