try:
    from video import Video
    from audio import Audio
    from playlist import Playlist
    from time import sleep
    from gui import *
    from os import system
    from vars import *
    from literal_functions import *
    from http.client import IncompleteRead
    from urllib.error import URLError
    import pytube.exceptions as exceptions
except ImportError:
    from install_requirements import main
    main()


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
    show_title(title=object.title, type=object.type)
    sleep(0.5)
    if ask_select_dir(message='Would you like to select a folder to download in?'):
        object.path = select_dir()
    print(blue, f'Getting {object.type.capitalize()} information...', rset)
    object.download()
    system(clear)
    print(green,
          f"The {object.type.capitalize()} has been downloaded successfully.",
          rset, sep='\n')
    return object.path


def download_playlist(object: Playlist):
    show_title(title=object.title, type='playlist')
    sleep(1)
    if ask_select_dir(message='Would you like to select a folder to download in?'):
        object.path = select_dir()
    object.download()
    return object.object_path


def main():
    try:
        system(clear)
        url = check_url(input("\nEnter a YouTube Link -> "))
        system(clear)
        object = (Playlist(url) if is_playlist(url)
                  else Video(url) if ask_video_audio(  # True If Video, Else Audio
            "Would you like to download as Video or Audio?") else Audio(url))
        path = download_playlist(object) if isinstance(
            object, Playlist) else download(object)
        opendir(path)
        exit_message()
    except KeyboardInterrupt:
        print(red, "\n\tOperation cancelled by user", rset)
        sleep(1)
    except IncompleteRead:
        print(red, "Internet connection has interrupted.",
              "Please check your internet connection and try again.", rset, sep='\n')
        sleep(3)
    except URLError:
        print(red, 'No internet connection', rset)
        sleep(2)
    except exceptions.RegexMatchError or exceptions.AgeRestrictedError as e:
        print(red, 'Something wrong happened:\n', e, rset, sep='')


main()
