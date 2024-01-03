try:
    from pytube import YouTube
    from pytube.cli import _unique_name, safe_filename
    from convert import merge_video
    from time import sleep
    from litfun import show_download_message
    from vars import *
    from http.client import RemoteDisconnected
    import os
except ImportError:
    from install_requirements import main
    main()


class Video:
    def __init__(self, url: str) -> None:
        self.video = YouTube(url)
        self.__title = None
        self.__streams = None
        self.__selected_stream = None
        self.__resolution = None
        self.__path = None
        self.__ext = None
        self.__itag = None
        self.type = 'video'

    @property
    def title(self):
        if self.__title:
            return self.__title
        self.__title = self.video.title
        return self.__title

    def nothing(self):
        self.video

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def streams(self):
        if self.__streams:
            return self.__streams
        for _ in range(4):
            try:
                self.__streams = self.video.streams.filter(
                    type='video',
                    subtype='mp4'
                )
                if not self.__streams:
                    self.__streams = self.video.streams.filter(
                        type='video'
                    )
                return self.__streams
            except RemoteDisconnected:
                print("Trying to connect...")
                sleep(1)
        else:
            print("Cannot connect to server. Exiting.")
            exit()

    @property
    def resolution(self):
        if self.__resolution:
            return self.__resolution
        self.__resolution = self.selected_stream.resolution
        return self.__resolution

    @property
    def path(self):
        if self.__path:
            return self.__path
        APP_NAME = "Youtube Downloader MAA"
        if os.name == 'nt':
            userprofile = os.getenv("userprofile")
            path = str(os.path.join(
                userprofile, 'Downloads',
                APP_NAME, self.type.capitalize()))
        else:
            userprofile = os.getenv("USER") if os.getenv(
                'SUDO_USER') is None else os.getenv('SUDO_USER')
            path = str(os.path.join(
                "/", "home", userprofile, "Downloads",
                APP_NAME, self.type.capitalize()))
            os.makedirs(path, exist_ok=True)
        self.__path = path
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @path.deleter
    def path(self):
        delattr(self, '__path')

    @property
    def extension(self):
        if self.__ext:
            return self.__ext
        self.__ext = self.selected_stream.subtype
        return self.__ext

    @property
    def itag(self):
        if self.__itag:
            return self.__itag
        self.select_detail()
        return self.__itag

    @itag.setter
    def itag(self, itag):
        if not self.__itag:
            self.__itag = itag

    @property
    def selected_stream(self):
        if self.__selected_stream:
            return self.__selected_stream
        self.__selected_stream = self.streams.get_by_itag(self.itag)
        return self.__selected_stream

    # Method for user to get video's details
    def get_details(self, adaptive: bool = None):
        details = []
        for stream in self.streams.filter(adaptive=adaptive):
            if not stream.is_progressive:
                audfilesize = self.video.streams.filter(
                    only_audio=True).order_by("abr").last().filesize
            else:
                audfilesize = 0
            details.append([stream.resolution,
                            "{:,.2f}".format(
                                (stream.filesize + audfilesize) / (1024**2)),
                            stream.subtype,
                            stream.is_progressive,
                            stream.itag
                            ])
        return details

    def select_detail(self, adaptive: bool = None):
        details = self.get_details(adaptive=adaptive)
        print("\nSelect a resolution to download:")
        for i in range(len(details)):
            print(f"{cyan}[{i + 1}]{yellow:2}",
                  f"Resolution: {details[i][0]:20}",
                  f"Approx_Size: {details[i][1]} MB{'':20}",
                  f"Format: {details[i][2]:15}",
                  f"{green}No Combine" if details[i][3] else '',
                  rset)
            sleep(0.08)
        print(f"{cyan}[{len(details) + 1}]{blue}",
              "Download All resolutions", rset, sep='\t')
        while True:
            try:
                select = int(input("\nEnter the number of resolution: "))
                if 0 < select <= len(details) + 1:
                    if select == len(details) + 1:
                        self.download_all_resolutions()
                        return None
                    # Set video resolution
                    self.__resolution = details[select - 1][0]
                    # Set video extesion
                    self.__ext = details[select - 1][2]
                    # Set video itag
                    self.__itag = details[select - 1][-1]
                    # return None to break the while loop
                    # and quit from function
                    return None
                else:
                    print(red, "You entered a number out of range!", sep='')
                    print("Please enter a number between 1 and",
                          len(details) + 1, rset)
            except ValueError:
                print(red, "You have to enter only numbers!", rset, sep='')

    def download(self):
        """Download video"""
        # Filter the title
        self.title = safe_filename(self.title)
        # Set output path
        final_path = os.path.join(
            self.path,
            f'{self.title}_{self.resolution}.{self.extension}'
        )
        # Download progressive stream
        if self.selected_stream.is_progressive:
            # Set vdieo name with extension
            video_unique_name = f"{self.title}_{self.resolution}.{self.extension}"
            # Check if video exist
            if os.path.exists(final_path):
                if os.path.getsize(final_path) == 0:
                    os.remove(final_path)
                else:
                    return None
            # Download video
            self.streams.get_by_itag(self.itag).download(
                output_path=self.path, filename=video_unique_name, max_retries=3)
        else:
            # Check if video exists
            if os.path.exists(final_path):
                return None
            # Stream only audio
            audio_stream = (
                self.video.streams
                .get_audio_only(None)
                )
            # Set video name with extension
            video_unique_name = _unique_name(
                self.title,
                self.selected_stream.subtype,
                'video',
                self.path
            )
            # Format audio name
            audio_unique_name = _unique_name(
                self.title,
                audio_stream.subtype,
                'audio',
                self.path
            )
            # Download Only Video
            self.selected_stream.download(
                output_path=self.path,
                filename=video_unique_name,
                max_retries=3
            )
            # Download Only Audio
            audio_stream.download(
                output_path=self.path,
                filename=audio_unique_name,
                max_retries=3
            )
            ##############  MERGE SECSION   ##############
            # Set video path
            video_path = os.path.join(self.path, video_unique_name)
            # Set audio path
            audio_path = os.path.join(self.path, audio_unique_name)
            # Merge Video with Audio into one Video file
            merge_video(
                video_path,
                audio_path,
                final_path,
                self.selected_stream.fps
            )

    def download_all_resolutions(self, subtype: str | None = None):
        """
        Download all available resolutions with a specific format
        :param str subtype:
            To specify a format. For example: "mp4", "webm"
            Default: download all available types
        """
        for _ in range(4):
            try:
                streams = self.streams.filter(adaptive=True, subtype=subtype)
                break
            except RemoteDisconnected:
                print("Trying to connect...")
        else:
            print("Cannot connect to server. Exiting.")
            exit()
        if streams is None:
            print(
                yellow,
                'Could not find the media type "%s" ' %
                'Downloading default media type...',
                subtype,
                rset,
                sep='',
                end=''
            )
            streams = self.streams.filter(adaptive=True, subtype="mp4")
        for stream in streams:
            self.__itag = stream.itag
            self.__title = stream.title
            self.__resolution = stream.resolution
            self.__selected_stream = stream
            if not self.path.endswith(safe_filename(self.title)):
                self.path = os.path.join(self.path, safe_filename(self.title))
            show_download_message(
                media_type=stream.type,
                text=f'with resolution: {yellow}{self.resolution}{rset}'
            )
            self.download()

    @staticmethod
    def __check_title(title: str):
        # Only allowed chars !@&+=(){}[]-_
        specialChar = "#$%^;'.,/\\:*?\"<>|~"
        for char in specialChar:
            title = title.replace(char, "")
        return title
