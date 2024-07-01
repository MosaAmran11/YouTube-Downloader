import os
import sys

try:
    os.system(
        f'{sys.executable} {os.path.join(os.path.dirname(__file__), "resources", "main.py")}')
except:
    pass
