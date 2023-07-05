from video import Video
from audio import Audio
from playlist import Playlist
from time import sleep
from gui import *
from os import system
from vars import *
from litfun import *
from http.client import IncompleteRead


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


def download(object: Video):
    system(clear)
    show_title(object.title)
    sleep(0.5)
    object.select_detail()
    if ask_select_dir(message='Would you like to select a folder to download in?'):
        object.path = select_dir()
    system(clear)
    show_download_message()
    object.download()
    system(clear)
    print(green, end='')
    spelling("The Video is downloaded successfully.")
    print(rset)
    opendir(object.path)
    exit_message()


def download_playlist(object: Playlist):
    system(clear)
    show_title(object.title, object.type)
    sleep(1)
    object.download()
    opendir(object.path)
    exit_message()


system(clear)
url = input("\nEnter a YouTube Link -> ")
url = check_url(url)
system(clear)
try:
    for _ in range(4):
        try:
            if is_playlist(url):
                obj = Playlist(url)
                break
            else:
                if ask_video_audio(
                    "Would you like to download as Video or Audio?"
                ):
                    obj = Video(url)
                else:
                    obj = Audio(url)
                break
        except:
            print("Trying to reconnect...")
            sleep(1)
    else:
        print(red, "Cannot connect to the server.", sep='')
        print("Please check you interner connection and try again.", rset)
        exit()

    if is_playlist:
        download_playlist(obj)
    else:
        download(obj)

except KeyboardInterrupt:
    print(red, "Operation cancelled by user", rset)
    exit()
except IncompleteRead:
    spelling(red, "Internet connection has inturrupted.")
    spelling("Please check your internet connection and try again.", rset)
    exit()
