try:
    from pytube import Playlist as plt
    from vars import *
    from video import Video
    from audio import Audio
    from gui import ask_video_audio
    from time import sleep
    import os
    from concurrent.futures import ProcessPoolExecutor
except ImportError:
    from install_requirements import main
    main()


class Playlist(plt):
    def __init__(self, url) -> None:
        super().__init__(url)
        self._object_type = ask_video_audio(
            'Would you like to download the Playlist as Video or Audio?')
        self._object = None
        self._path = None
        self._itag = None
        self._resolution = None
        self._subtype = None
        self._video_urls = None

    @property
    def video_urls(self):
        if self._video_urls is None:
            self._video_urls = self.url_generator()
        return self._video_urls

    @property
    def path(self):
        if self._path is None:
            APP_NAME = "Youtube Downloader MAA"
            userprofile = os.getenv(
                "userprofile") if os.name == 'nt' else f'/home/{os.getenv("USER")}'
            self._path = str(os.path.join(
                userprofile, 'Downloads',
                APP_NAME, type(self).__name__.capitalize(), self.title))
            os.makedirs(self._path, exist_ok=True)
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def object(self):
        if self._object is None:
            self._object = self.create_object()
        return self._object

    @object.deleter
    def object(self):
        self._object = None

    @property
    def object_path(self):
        if not self.path.endswith(os.path.join(self.title, self.object.type.capitalize())):
            self.path = os.path.join(
                self.path, self.title, self.object.type.capitalize())
        return self.path

    @property
    def itag(self):
        if self._itag is None:
            self._itag = self.object.itag
        return self._itag

    @itag.setter
    def itag(self, itag):
        if not self._itag:
            self._itag = itag

    @property
    def resolution(self):
        if self._resolution is None:
            self._resolution = self.object.resolution
        return self._resolution

    @property
    def subtype(self):
        if self._subtype is None:
            self._subtype = self.object.selected_stream.subtype
        return self._subtype

    def create_object(self):
        return (Video(next(self.video_urls))
                if self._object_type is True  # True means Video, False means Audio
                else Audio(next(self.video_urls))
                )

    def initial_properties(self):
        self.object.path = self.object_path
        self.itag
        self.resolution
        self.subtype

    def _check_available_itag(self):
        if self.object.selected_stream is not None:
            return None

        sorted_streams = self.object.streams.asc()
        available_itags = [
            stream.itag for stream in sorted_streams]

        for itag in available_itags:
            if itag < self.itag:
                self.object.itag = itag
                return None

        available_resolutions = [
            stream.resolution for stream in sorted_streams]

        for resolution in available_resolutions:
            if int(resolution.rstrip('p')) <= int(self.resolution.rstrip('p')):
                self.object.itag = self.object.streams.filter(
                    resolution=resolution).last().itag
                return None
        else:
            print(yellow, f'This {self.object.type.capitalize()} does not match the selected resolution\n',
                  'Please select from the following available resolutions:', rset)
            self.object.select_detail()

    def download(self):
        for _ in range(self.length):
            print('\n')
            self.object  # Create the object if None
            # print(cyan,
            #       f"Getting {self.object.type.capitalize()} information...",
            #       rset)
            os.system(clear)
            print(cyan,
                  self.object.type.capitalize(),
                  f"title: {self.object.title}",
                  rset)
            print(
                blue, f'\nGetting {self.object.type.capitalize()} information...', rset)
            self.initial_properties()
            self.object.itag = self.itag
            self._check_available_itag()
            self.object.download()
            print(
                f'The {self.object.type.capitalize()} has been downloaded successfully'
            )
            if _ < self.length - 1:  # If the object is the last, don't delete it
                del self.object  # Delete the current object to download the next one
            sleep(1)
        os.system(clear)
        print(green,
              f"All {self.object.type.capitalize()}s are downloaded successfully.",
              rset)
