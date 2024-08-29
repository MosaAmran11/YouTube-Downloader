from os import name

red: str = '\033[31m'
green: str = '\033[32m'
yellow: str = '\033[33m'
blue: str = '\033[34m'
magenta: str = '\033[35m'
cyan: str = '\033[36m'
reset: str = '\033[39m'
clear: str = 'cls' if name == 'nt' else 'clear'
