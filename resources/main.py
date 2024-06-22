from video import Video
from audio import Audio
from playlist import Playlist
from time import sleep
from gui import *
from os import system
from vars import *
from litfun import *
from http.client import IncompleteRead
import pytube.exceptions as exceptions


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
            print(f'{red}Not a YouTube url!{rset}')
            link = input(
                f'{yellow}Please enter a valid YouTube url: {rset}')


def download(object: Video | Audio):
    obj_type = type(object).__name__
    system(clear)
    show_title(title=object.title, type=obj_type)
    sleep(0.5)
    # if video:
    #     print(cyan, f"Getting {obj_type.capitalize()} information...", rset)
    # object.select_detail()
    if ask_select_dir(message='Would you like to select a folder to download in?'):
        object.path = select_dir()
    # system(clear)
    print(blue, f'Getting {obj_type.capitalize()} information...', rset)
    object.download()
    system(clear)
    print(green,
          f"The {obj_type.capitalize()} has been downloaded successfully.",
          rset, sep='\n')
    opendir(object.path)
    exit_message()


def download_playlist(object: Playlist):
    system(clear)
    show_title(title=object.title, type=type(object).__name__.capitalize())
    sleep(1)
    if ask_select_dir(message='Would you like to select a folder to download in?'):
        object.path = select_dir()
    object.download()
    opendir(object.path)
    exit_message()


def main():
    try:
        system(clear)
        url = input("\nEnter a YouTube Link -> ")
        url = check_url(url)
        system(clear)
        for _ in range(4):
            try:
                if is_playlist(url):
                    obj = Playlist(url)
                    break
                else:
                    video = ask_video_audio(
                        "Would you like to download as Video or Audio?")
                    if video:
                        obj = Video(url)
                    else:
                        obj = Audio(url)
                    break
            except:
                print("Trying to reconnect...")
                sleep(1)
        else:
            print(red, "Cannot connect to the server.", sep='')
            print("Please check you internet connection and try again.", rset)
            exit()

        if isinstance(obj, Playlist):
            download_playlist(obj)
        else:
            download(obj)
        sleep(1)
        exit()

    except KeyboardInterrupt:
        try:
            os.system(clear)
            os.remove(os.path.join(
                obj.path, f"{obj.title} ({obj.resolution}).{obj.subtype}"))
        except:
            pass
        print(red, "\n\tOperation cancelled by user", rset)
        sleep(1)
        exit()
    except IncompleteRead:
        print(red, "Internet connection has interrupted.")
        print("Please check your internet connection and try again.", rset)
        sleep(3)
        exit()
    except exceptions.RegexMatchError as e:
        print(red, e, rset)
    except exceptions.AgeRestrictedError as e:
        print(red, e, rset)


video = None
main()
