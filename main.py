import os
import sys


if __name__ == '__main__':
    os.system(
        f'{sys.executable} {os.path.normpath(os.path.join(os.path.dirname(__file__), "resources", "main.py"))}')
