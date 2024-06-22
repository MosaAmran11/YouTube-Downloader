try:
    from http.client import IncompleteRead
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


class Video(YouTube):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        self._streams = None
        self._audio_stream = None
        self._selected_stream = None
        self._resolution = None
        self._path = None
        self._subtype = None
        self._itag = None
        self.type = 'video'

    @property
    def streams(self):
        if self._streams is None:
            for _ in range(4):
                try:
                    self._streams = super().streams.filter(
                        type=self.type,
                        adaptive=True)
                    break
                except RemoteDisconnected:
                    print("Trying to connect...")
                    sleep(1)
            else:
                print("Cannot connect to server. Exiting.")
                exit()
        return self._streams

    @property
    def selected_stream(self):
        if self._selected_stream is None:
            self._selected_stream = self.streams.get_by_itag(self.itag)
        return self._selected_stream

    @property
    def audio_stream(self):
        if self._audio_stream is None:
            self._audio_stream = super().streams.get_audio_only(None)
        return self._audio_stream

    @property
    def resolution(self):
        if self._resolution is None:
            self._resolution = self.selected_stream.resolution
        return self._resolution

    @property
    def path(self):
        if self._path is None:
            APP_NAME = "Youtube Downloader MAA"
            userprofile = os.getenv(
                "userprofile") if os.name == 'nt' else f'/home/{os.getenv("USER")}'
            self._path = str(os.path.join(
                userprofile, 'Downloads',
                APP_NAME, self.type.capitalize()))
            os.makedirs(self._path, exist_ok=True)
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    # @path.deleter
    # def path(self):
    #     delattr(self, '_path')

    @property
    def subtype(self):
        if self._subtype is None:
            self._subtype = self.selected_stream.subtype
        return self._subtype

    @property
    def itag(self):
        if self._itag is None:
            self.select_detail()
        return self._itag

    @itag.setter
    def itag(self, value):
        self._itag = value

    # Method for user to get video's details
    def get_details(self):
        audio_file_size = super().streams.filter(
            only_audio=True).order_by("abr").last().filesize_mb
        return [(stream.resolution,
                 "{:,.2f}".format(
                     (stream.filesize_mb + audio_file_size)
                 ),
                 stream.subtype,
                 stream.is_progressive,
                 stream.itag) for stream in self.streams]

    def select_detail(self, adaptive: bool = None):
        details = self.get_details()
        print("\nSelect a resolution to download:")
        for i in range(len(details)):
            print(f"{cyan}[{i + 1}]{yellow}",
                  f"Resolution: {details[i][0]:10}",
                  f"Approx_Size: {details[i][1]} MB{'':10}",
                  f"Format: {details[i][2]:15}",
                  #   f"{green}No Combine" if details[i][3] else '',
                  rset, sep='\t')
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
                    self._resolution = details[select - 1][0]
                    # Set video extension
                    self._subtype = details[select - 1][2]
                    # Set video itag
                    self._itag = details[select - 1][-1]
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
        self.title = safe_filename(self.title)
        # Video name to be saved
        video_name = f'{self.title} ({self.resolution}).{self.subtype}'
        # Set target path with filename
        video_path = os.path.join(
            self.path,
            video_name
        )
        # Video file with temp name to download
        temp_file_name = _unique_name(
            self.title,
            self.subtype,
            'video',
            self.path
        )
        # Set temp video file path
        temp_file_path = os.path.join(self.path, temp_file_name)

        # Check if video exists
        if os.path.exists(video_path):
            return None

        # Set audio name
        audio_name = _unique_name(
            self.title,
            self.audio_stream.subtype,
            'audio',
            self.path
        )
        # Set audio path
        audio_path = os.path.join(self.path, audio_name)

        show_download_message(self.type)
        try:
            # Download Only Video
            self.selected_stream.download(
                output_path=self.path,
                filename=temp_file_name,
                max_retries=3
            )
            # Download Only Audio
            self.audio_stream.download(
                output_path=self.path,
                filename=audio_name,
                max_retries=3
            )
            ##############  MERGE SECTION   ##############
            # Merge Video with Audio into one Video file
            merge_video(
                temp_file_path,
                audio_path,
                video_path,
                self.selected_stream.fps
            )
        except KeyboardInterrupt or IncompleteRead:
            try:
                # Delete downloaded files
                os.remove(video_path)
                os.remove(audio_path)
                os.remove(video_path)
            except:
                pass

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
                f'Could not find the media type "{self.type}" ',
                'Downloading default media type...',
                subtype,
                rset,
                sep='',
                end=''
            )
            streams = self.streams.filter(adaptive=True, subtype="mp4")
        for stream in streams:
            self._itag = stream.itag
            self.title = stream.title
            self._resolution = stream.resolution
            self._selected_stream = stream
            if not self.path.endswith(safe_filename(self.title)):
                self.path = os.path.join(self.path, safe_filename(self.title))
            show_download_message(
                media_type=stream.type,
                text=f'with resolution: {yellow}{self.resolution}{rset}'
            )
            self.download()
