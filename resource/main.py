from video import Video
from time import sleep
from gui import GUI
from os import name, system


red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'
magenta = '\033[35m'
cyan = '\033[36m'
rset = '\033[39m'
clear = 'cls' if name == 'nt' else 'clear'


def spelling(spell):
    for i in spell:
        print(i, end="")
        sleep(0.04)


def is_playlist(url):
    return "playlist?" in url


def check_url(url: str):
    validUrl = ("https://www.youtube.com/", "youtube.com/",
                "www.youtube.com/", "https://youtu.be/", "youtu.be/", "https://youtube.com/")
    while True:
        for url in validUrl:
            if url.startswith(url):
                return url
        else:
            print(f'{red}That is not a YouTube url!{rset}')
            url = input(
                f'{yellow}Please enter a valid YouTube url: {rset}')


def show_title(title):
    spell = "The title of video is:"
    spelling(spell)
    print(green)
    spelling(title)
    print(rset)


def exit_message():
    spell = f'{yellow}\nThanks for using our YouTube Downloader.{rset}'
    spelling(spell)
    print(cyan)
    spell = '\tMADE BY MAA\t'.center(50, "#")
    spelling(spell)
    print(rset)
    sleep(0.8)
    spell = f'{red}Exiting from downloader...{rset}'
    spelling(spell)
    sleep(0.8)


def display_download_process():
    spell = f'\nDownloading the Video.....'
    spelling(spell)
    print()
    spell = 'It may take a long time. Please wait until you be alerted.'
    spelling(spell)


url = input("\nEnter a YouTube Link -> ")
for num in range(4):
    try:
        vd = Video(url)
        break
    except:
        pass
system(clear)
ui = GUI(vd.path)
show_title(vd.title)
sleep(1)
spell = "Loading video information..."
print(cyan, end='')
spelling(spell)
print(rset)
vd.select_detail()
if ui.ask_select_dir(message='Would you like to select a folder to download in?'):
    vd.path = ui.select_dir()
system(clear)
display_download_process()
vd.download()
system(clear)
ui.opendir()
exit_message()
