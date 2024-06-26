try:
    from pytube import Playlist as plt
    from vars import *
    from video import Video
    from audio import Audio
    from gui import ask_video_audio
    from time import sleep
    import threading
    import os
except ImportError:
    from install_requirements import main
    main()


class Playlist(plt):
    def __init__(self, url) -> None:
        super().__init__(url)
        self._object = None
        self._object_type = None
        self._path = None
        self._itag = None
        self._resolution = None
        self._subtype = None
        self._video_urls = None

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
        return self._object

    @object.setter
    def object(self, value):
        self._object = value

    @object.deleter
    def object(self):
        self._object = None

    @property
    def object_type(self):
        if self._object_type is None:
            self._object_type = ask_video_audio(
                'Would you like to download the Playlist as Video or Audio?')
        return self._object_type

    @property
    def object_path(self):
        return os.path.join(
            self.path, self.title, self.object.type.capitalize())

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

    # @property
    # def subtype(self):
    #     if self._subtype is None:
    #         self._subtype = self.object.selected_stream.subtype
    #     return self._subtype

    def create_object(self, url):
        return (Video(url)
                if self.object_type  # True means Video, False means Audio
                else Audio(url)
                )

    def get_available_itag(self, object: Video | Audio):
        if isinstance(object, Audio):
            return None
        if object.streams.get_by_itag(self.itag) is not None:
            return self.itag

        sorted_streams = object.streams.asc()
        available_itags = [
            stream.itag for stream in sorted_streams]

        for itag in available_itags:
            if itag < self.itag:
                return itag

        available_resolutions = [
            stream.resolution for stream in sorted_streams]

        for resolution in available_resolutions:
            if int(resolution.rstrip('p')) <= int(self.resolution.rstrip('p')):
                return object.streams.filter(
                    resolution=resolution).first().itag

    def select_detail(self, object: Video | Audio):
        details = [(stream.resolution,
                    stream.subtype,
                    stream.itag) for stream in object.streams]
        print("\nSelect a resolution to download:")
        sleep(1)

        for i in range(len(details)):
            print(f"{cyan}[{i + 1}]{yellow}",
                  f"Resolution: {details[i][0]:10}",
                  f"Format: {details[i][1]}",
                  rset, sep='\t')
        while True:
            try:
                select = int(input("\nEnter the number of resolution: "))
                if 0 < select <= len(details) + 1:
                    # Set video resolution
                    self._resolution = details[select - 1][0]
                    # Set video extension
                    self._subtype = details[select - 1][1]
                    # Set video itag
                    self._itag = details[select - 1][-1]
                    # return None to break the while loop
                    # and quit from function
                    return None
                else:
                    print(red, "You entered a number out of range!", sep='')
                    print(f"Please enter a number between 1 and {len(details)}",
                          rset)
            except ValueError:
                print(
                    red, "You have to enter only the number that represents the resolution!", rset, sep='')

    def process_object(self, url, output_dir):
        object = self.create_object(url)
        object.itag = self.get_available_itag(object)
        object.path = output_dir
        print(cyan,
              f"{object.type.capitalize()} title: {object.title}",
              f'{blue}Getting information...',
              rset, sep='\n')
        object.download()
        print(f'{yellow}Done: {object.title}', rset)

    def download(self):
        self._object = self.create_object(self.video_urls[0])
        if isinstance(self.object, Video):
            self.select_detail(self.object)
        threads = []
        for i in range(0, self.length, 2):
            batch = self.video_urls[i:i+2]
            # Start a thread for each download in the batch
            threads = [threading.Thread(
                target=self.process_object, args=(url, self.object_path)) for url in batch]

            # Start all threads in the batch
            for thread in threads:
                thread.start()

            # Wait for all threads in the batch to complete
            for thread in threads:
                thread.join()

        os.system(clear)
        print(green,
              f"All {self.object.type.capitalize()}s are downloaded successfully.",
              rset)
