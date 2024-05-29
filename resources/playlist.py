try:
    from pytube import Playlist as plt
    from vars import *
    from litfun import show_download_message, spelling
    from video import Video
    from audio import Audio
    from gui import ask_video_audio
    from time import sleep
    import os
except ImportError:
    from install_requirements import main
    main()


class Playlist:
    def __init__(self, url) -> None:
        self.playlist = plt(url)
        self.__title = self.playlist.title
        self.__video_titles = tuple()
        self.__type = 'playlist'
        self.__subtype = None
        self.subject = None
        self.__video_urls = None
        self.__path = None
        self.__itag = None
        self.__available_itag = list()

    @property
    def title(self):
        if self.__title:
            return self.__title
        self.__title = self.playlist.title
        return self.__title

    @property
    def video_urls(self):
        if self.__video_urls:
            return self.__video_urls
        self.__video_urls = self.playlist.video_urls
        return self.__video_urls

    @property
    def path(self):
        if self.__path:
            return self.__path
        APP_NAME = "Youtube Downloader MAA"
        if os.name == 'nt':
            userprofile = os.getenv("userprofile")
            path = str(os.path.join(
                userprofile, 'Downloads', APP_NAME, "Playlist", self.title))
        else:
            userprofile = os.getenv("USER") if os.getenv(
                'SUDO_USER') is None else os.getenv('SUDO_USER')
            path = str(os.path.join(
                "/", "home", userprofile, "Downloads", APP_NAME, "Playlist", self.title))
            os.makedirs(path, exist_ok=True)
        self.__path = path
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @property
    def type(self):
        if self.__type:
            return self.__type
        if ask_video_audio(
            "Would you like to download the playlist as Videos or Audios?"
        ):
            self.__type = 'video'
        else:
            self.__type = 'audio'
        if not self.path.endswith(self.__type.capitalize()):
            self.path = os.path.join(self.path, self.__type.capitalize())
        return self.__type

    @property
    def subtype(self):
        if self.__subtype:
            return self.__subtype
        self.set_url()
        return self.__subtype

    @property
    def itag(self):
        if self.__itag:
            return self.__itag
        self.__itag = self.subject.itag
        return self.__itag

    @itag.setter
    def itag(self, itag):
        if not self.__itag:
            self.__itag = itag

    def __get_available_itag(self):
        self.subject.select_detail()
        self.__available_itag.append(
            self.subject.selected_stream.itag
        )

    def __check_available_itag(self):
        self.subject.itag = self.itag
        while self.subject.selected_stream.itag is None:
            for itag in self.__available_itag:
                self.subject.itag = itag
                if self.subject.selected_stream.itag is not None:
                    return None
            else:
                self.__get_available_itag()

    def __check_duplicate_title(self):
        title = self.subject.title
        if title in self.__video_titles:
            expand = 1
            while True:
                expand += 1
                new_title = f'{title} ({expand})'
                if new_title in self.__video_titles:
                    continue
                else:
                    self.subject.title = new_title
                    break
        self.__video_titles += (self.subject.title,)

    def set_url(self, url):
        if self.type == 'video':
            self.subject = Video(url)
        else:
            self.subject = Audio(url)
        self.__check_available_itag()
        self.__subtype = self.subject.selected_stream.subtype
        self.subject.path = self.path

    def download(self):
        if self.type == 'playlist':
            self.__type = None
            self.__type = self.type
        for url in self.video_urls:
            os.system(clear)
            spelling(
                cyan, f"Loading {self.type.capitalize()} information...", rset)
            self.set_url(url)
            self.__check_duplicate_title()
            os.system(clear)
            show_download_message(
                self.subject.selected_stream.type, f": {self.subject.title}")
            print(
                yellow,
                'Approxmate Size: {:,.2f} MB'.format(
                (self.subject.selected_stream.filesize + 
                (self.subject.video.streams.get_audio_only(None)
                .filesize if self.subject.selected_stream.is_adaptive else 0))
                / (1024**2)),
                rset
                )
            self.subject.download()
            spelling(
                f'The {self.type.capitalize()} is downloaded successfully'
            )
            sleep(1)
        os.system(clear)
        print(green, end='')
        spelling(f"All {self.type.capitalize()}s are downloaded successfully.")
        print(rset)
