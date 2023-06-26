from pytube import YouTube, Playlist
from time import sleep
import os
import moviepy.editor as mpe
import easygui


class YD:

    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    rset = '\033[39m'

    titles = set()
    APP_NAME = "Youtube Downloader MAA"

    if os.name == "nt":
        clear = "cls"
        pip = "pip"
        user = os.getenv('userprofile')
        PATH = os.path.join(user, "Downloads", APP_NAME)
        EXPLORER = "explorer"
    else:
        clear = "clear"
        pip = "pip3"
        user = os.getenv("USER") if os.getenv(
            'SUDO_USER') is None else os.getenv('SUDO_USER')
        PATH = os.path.join("/home/", user, "Downloads", APP_NAME)
        EXPLORER = "nautilus"

    @staticmethod
    def check_url(link: str):
        validUrl = ("https://www.youtube.com/", "youtube.com/",
                    "www.youtube.com/", "https://youtu.be/", "youtu.be/", "https://youtube.com/")
        while True:
            for url in validUrl:
                if link.startswith(url):
                    return link
            else:
                print(f'{YD.red}That is not a YouTube link!{YD.rset}')
                link = input(
                    f'{YD.yellow}Please enter a valid YouTube link: {YD.rset}')

    @staticmethod
    def display_download_process(type: str):
        spell = f'\nDownloading the {type.capitalize()}.....'
        YD.spelling(spell)

        spell = 'It may take a long time. Please wait until you be alerted.'
        YD.spelling(spell)

    @staticmethod
    def combine_audio(vidname: str, audname: str, outname: str, fps=30):
        my_clip = mpe.VideoFileClip(vidname)
        audio_background = mpe.AudioFileClip(audname)
        final_clip = my_clip.set_audio(audio_background)
        final_clip.write_videofile(outname, fps=fps)

        os.remove(vidname)
        os.remove(audname)

    @staticmethod
    def convert_audio(audname: str, outname: str):
        my_audio = mpe.AudioFileClip(audname)
        my_audio.write_audiofile(outname)

        os.remove(audname)

    @staticmethod
    def spelling(spell):
        for i in spell:
            print(i, end="")
            sleep(0.04)
        print()

    def __init__(self, link: str):
        self.link = YD.check_url(str(link))
        self.__itag = None
        self.__type = "video"
        self.__video_extention = None
        self.__audio_extention = None
        self.filename = None
        if "playlist?" in self.link:
            self.__yt = Playlist(self.link)
            self.__playlist_title = self.__yt.title
            self.__ob_type = "Playlist"
            self.__plvideo = self.__yt.videos
            self.__title = None
            self.__streams = None
            YD.prepare_playlist(self)
            self.path = os.path.join(
                YD.PATH, "Playlists", self.__playlist_title)
        else:
            self.__yt = YouTube(self.link)
            self.__ob_type = "YouTube"
            self.__title = self.__yt.title
            self.__streams = self.__yt.streams
            self.path = YD.PATH
            YD.set_object_title(self)

    def prepare_playlist(self):
        for video in self.__plvideo:
            self.__title = video.title
            YD.set_object_title(self)
            self.__streams = video.streams
            self.__itag = self.__streams.get_by_itag(self.__streams[0].itag)
            break

    def set_object_title(self):
        spell = "Getting information..."
        YD.spelling(spell)

        title = self.__title
        specialChar = "!@#$%^&*+=\";:'.,<>/?`~{}[]\\|"

        for char in specialChar:
            title = title.replace(char, "")

        # Return the condition to "Youtube" if something wrong with titling.
        # if self.__ob_type == "Playlist":
            # global LOG_FILE
            # try:
            #     LOG_FILE = open(os.path.join(
            #         os.path.dirname(__file__), ".log.txt"))
            #     read = LOG_FILE.read()
            #     LOG_FILE.close()
            # except FileNotFoundError:
            #     read = ''

            # if title in YD.titles:
            #     for i in range(2, 11):
            #         if f"{title} ({i})" in YD.titles:
            #             continue
            #         else:
            #             title += f" ({i})"
            #             break

        self.__title = title

    def set_file_extention(self):
        mimetype = self.__streams.get_by_itag(self.__itag).mime_type.split("/")
        self.__type = mimetype[0]

        if mimetype[0].startswith("video"):
            self.__video_extention = mimetype[1]

            if not self.__streams.get_by_itag(self.__itag).is_progressive:
                audtype = self.__streams.get_audio_only().mime_type.split("/")
                self.__audio_extention = audtype[1]

        elif mimetype[0].startswith("audio"):
            self.__audio_extention = mimetype[1]

        if not self.path.endswith(f"{self.__type.capitalize()}s"):
            self.path = os.path.join(self.path, f"{self.__type.capitalize()}s")
            os.makedirs(self.path, exist_ok=True)

    def get_title(self):
        """Return the title of the object"""
        os.system(YD.clear)
        if self.__ob_type == "YouTube":
            spell = f"The title of the {self.__type} is: "
            YD.spelling(spell)
            print(self.__title + "\n")
        else:
            spell = f"The name of the {self.__ob_type} is: "
            YD.spelling(spell)
            print(self.__playlist_title + "\n")

    def select_folder(self):
        """Open a graphical window to select a folder."""
        ask = easygui.ynbox(
            "Would you like to select a folder to download in?")
        if ask:
            path = easygui.diropenbox(default=self.path)
            if path != None:
                self.path = path

    def __set_filename(self):
        if self.__itag == None:
            YD.streams_menu(self)

        if self.__type == "video":
            resolution = self.__streams.get_by_itag(self.__itag).resolution
            self.filename = f'{self.__title}_{resolution}'
        else:
            self.filename = self.__title

    def streamAudio(self):
        filename = f"{self.filename}.{self.__audio_extention}"

        self.__streams.get_by_itag(self.__itag).download(
            self.path, filename=filename, max_retries=3)

        YD.convert_audio(os.path.join(self.path, filename),
                         os.path.join(self.path, f"{self.__title}.mp3")
                         )

    def streamVideo(self):
        if self.__streams.get_by_itag(self.__itag).is_progressive:
            resolution = self.__streams.get_by_itag(self.__itag).resolution
            vidName = f"{self.__title}_{resolution}.{self.__video_extention}"
        else:
            vidName = f"{self.__title}.{self.__video_extention}"

        audName = f"{self.__title}_audio.{self.__audio_extention}"

        self.__streams.get_by_itag(self.__itag).download(
            self.path, filename=vidName, max_retries=3)

        if not self.__streams.get_by_itag(self.__itag).is_progressive:
            self.__streams.get_audio_only().download(
                self.path, filename=audName, max_retries=3)

            YD.combine_audio(os.path.join(self.path, vidName),
                             os.path.join(self.path, audName),
                             os.path.join(
                                 self.path, f"{self.filename}.mp4"),
                             self.__streams.get_by_itag(self.__itag).fps
                             )

    def downloadPlaylist(self):
        """Start downloading the playlist's videos."""

        for video in self.__plvideo:
            # self.__ob_type = "YouTube"  # Return this code if there is something wrong with titling.

            self.__title = video.title
            YD.set_object_title(self)

            if self.__title in YD.titles:
                for i in range(2, 11):
                    if f"{self.__title} ({i})" in YD.titles:
                        continue
                    else:
                        self.__title += f" ({i})"
                        break

            YD.__set_filename(self)

            spell = f'{YD.yellow}Preparing the {self.__type.capitalize()}: {YD.green}"{self.__title}"{YD.rset}'
            YD.spelling(spell)

            self.__streams = video.streams

            YD.downloadVideo(self)
            YD.titles.add(self.__title)

        spell = f'All {self.__type}s downloaded successfully.'.title(
        )
        YD.spelling(spell)
        print()
        sleep(1)

    def downloadVideo(self):
        """Start downloading the video."""
        YD.set_file_extention(self)
        YD.display_download_process(self.__type)

        # Stream only Audio.
        if self.__type.startswith("audio"):
            if not os.path.exists(os.path.join(self.path, f"{self.filename}.mp3")):
                YD.streamAudio(self)

        # Stream Video with Audio.
        else:
            if self.__streams.get_by_itag(self.__itag).is_progressive:
                if not os.path.exists(os.path.join(self.path, f"{self.filename}.{self.__video_extention}")):
                    YD.streamVideo(self)
            else:
                if not os.path.exists(os.path.join(self.path, f"{self.filename}.mp4")):
                    YD.streamVideo(self)

        # LOG_FILE = open(os.path.join(
        #     os.path.dirname(__file__), ".log.txt"), "a")
        # LOG_FILE.write(self.__title + "\n")
        # LOG_FILE.close()

        spell = f'{YD.green}The {self.__type} is downloaded successfully.{YD.rset}'
        YD.spelling(spell)
        sleep(1)
        os.system(YD.clear)

    def download(self):
        try:
            if self.__ob_type == "YouTube":
                YD.set_object_title(self)
                YD.__set_filename(self)
                self.downloadVideo()
            else:
                self.downloadPlaylist()
        except KeyboardInterrupt:
            print(f"\n\n{YD.red}Exited by user.{YD.rset}")
            exit()

    def openFileDir(self):
        """Open the file path in a graphical window"""
        os.system(f'{YD.EXPLORER} "{self.path}"')

    def openFile(self):
        """Open the file with the default media player"""
        if self.__ob_type == "Playlist":
            YD.openFileDir(self)
        else:
            OPEN_FILE = "xdg-open " if os.name != "nt" else ""

            if self.__type == "video":
                path = os.path.join(self.path, f"{self.filename}.mp4")
            else:
                path = os.path.join(self.path, f"{self.__title}.mp3")

            os.system(
                f'{OPEN_FILE}"{path}"')

    def streams_menu(self):
        # Displaying the resolutions' menu.
        if self.__ob_type == "Playlist":
            for video in self.__plvideo:
                self.__streams = video.streams
                break

        spell = "Here are the available resolutions:"
        YD.spelling(spell)

        for num, stream in enumerate(self.__streams, 1):
            print(f'[{num}]',
                  stream.resolution,
                  stream.type,
                  ", Size: {:,.0f} MB".format(stream.filesize),
                  stream.is_progressive
                  )

        while True:
            try:
                choice = int(input('Choose the number of resolution: '))
                while choice > len(self.__streams) or choice < 1:
                    choice = int(input(
                        f'{YD.red}\nYou entered a wrong choice.{YD.rset}'))
                else:
                    self.__itag = self.__streams[choice - 1].itag
                    break
            except ValueError:
                print(f'{YD.red}That is not a number!{YD.rset}')

        YD.set_file_extention(self)
        os.system(YD.clear)

    @property
    def exit_msg(self):
        """Dispalying a message for exiting the program."""

        spell = f'{YD.yellow}\nThanks for using our YouTube Downloader.{YD.rset}'
        YD.spelling(spell)
        print(YD.cyan)
        spell = '\tMADE BY MAA\t'.center(50, "#")
        YD.spelling(spell)
        print(YD.rset)
        sleep(0.8)

        spell = f'{YD.red}Exiting from downloader...{YD.rset}'
        YD.spelling(spell)
        sleep(0.8)

    def wel_msg(self, title="Welcome", message="Welcome to our YouTube Downloader!"):
        """Display a greating message in a graphical window"""
        easygui.msgbox(message, title)
