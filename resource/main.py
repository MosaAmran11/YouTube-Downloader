from video import Video
from time import sleep
from gui import GUI
from os import system
from vars import *
from litfun import *
from requests.exceptions import HTTPError


def is_playlist(url):
    return "playlist?" in url


def check_url(link: str) -> str:
    validUrl = ("https://www.youtube.com/", "youtube.com/",
                "www.youtube.com/", "https://youtu.be/", "youtu.be/", "https://youtube.com/")
    while True:
        for url in validUrl:
            if link.startswith(url):
                return link
        else:
            print(f'{red}That is not a YouTube url!{rset}')
            link = input(
                f'{yellow}Please enter a valid YouTube url: {rset}')


def download_video():
    vd.select_detail()
    if ui.ask_select_dir(message='Would you like to select a folder to download in?'):
        vd.path = ui.select_dir()
    system(clear)
    show_download_message()
    vd.download()
    system(clear)
    print(green, end='')
    spelling("The Video is downloaded successfully.")
    print(rset)
    ui.opendir()
    exit_message()


def download_all_resolutions(
        media_type: str | None = 'mp4'
) -> None:
    if ui.ask_select_dir(message='Would you like to select a folder to download in?'):
        vd.path = ui.select_dir()
    vd.download_all_resolutions(subtype=media_type)
    system(clear)
    print(green, end='')
    spelling("All Videos are downloaded successfully.")
    print(rset)
    ui.opendir(vd.path)
    exit_message()


try:
    system(clear)
    while True:
        try:
            vd = Video(check_url(input("\nEnter a YouTube Link -> ")))
            break
        except:
            pass
    system(clear)
    show_title(vd.title)
    ui = GUI(vd.path)
    sleep(0.5)
    print(cyan, end='')
    spelling("Loading video information...")
    print(rset)
    download_all_resolutions()
except KeyboardInterrupt:
    print(red, "Exited by user.", rset)
    exit()
