import subprocess
from http.client import IncompleteRead
from os import system
from urllib.error import URLError
from literal_functions import *

try:
    from video import Video
    from audio import Audio
    from playlist import Playlist
    from gui import *
    import pytube.exceptions as exceptions
except ImportError:
    from install_requirements import main

    main()


def is_playlist(url):
    return "playlist?" in url


def check_url(link: str) -> str:
    valid_url = ("https://www.youtube.com/", "youtube.com/",
                 "www.youtube.com/", "https://youtu.be/", "youtu.be/", "https://youtube.com/")
    while True:
        for url in valid_url:
            if link.startswith(url):
                return link
        else:
            print(f'{red}Not a YouTube url!{reset}')
            link = input(
                f'{yellow}Please enter a valid YouTube url: {reset}')


def download(obj: Video | Audio):
    show_title(title=obj.title, subtype=obj.type)
    sleep(0.5)
    if ask_select_dir(message='Would you like to select a folder to download in?'):
        obj.path = select_dir()
    print(blue, f'Getting {obj.type.capitalize()} information...', reset)
    obj.download()
    system(clear)
    print(green,
          f"The {obj.type.capitalize()} has been downloaded successfully.",
          reset, sep='\n')
    return obj.path


def download_playlist(obj: Playlist):
    show_title(title=obj.title, subtype='playlist')
    sleep(1)
    if ask_select_dir(message='Would you like to select a folder to download in?'):
        obj.path = select_dir()
    obj.download()
    return obj.object_path


def main():
    try:
        system(clear)
        url = check_url(input("\nEnter a YouTube Link -> "))
        system(clear)
        obj = (Playlist(url) if is_playlist(url)
               else Video(url) if ask_video_audio(  # True If Video, Else Audio
            "Would you like to download as Video or Audio?") else Audio(url))
        path = download_playlist(obj) if isinstance(
            obj, Playlist) else download(obj)
        opendir(path)
        exit_message()
    except KeyboardInterrupt:
        print(red, "\n\tOperation cancelled by user", reset)
    except IncompleteRead:
        print(red, "Internet connection has interrupted.",
              "Please check your internet connection and try again.", reset, sep='\n')
    except URLError:
        print(red, 'No internet connection', reset)
    except exceptions.RegexMatchError or exceptions.AgeRestrictedError as e:
        print(red, 'Something wrong happened:\n', e, reset, sep='')
        sleep(2)
        print("Trying to update libraries...", '\n')
        command = ['python.exe -m pip install --upgrade pip'.split(), 'python -m pip install pytube'.split()]
        for i in command:
            subprocess.run(i)
        print(yellow, 'Please rerun the app and try again.', reset)
        sleep(7)


main()
