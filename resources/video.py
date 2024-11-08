# try:
import os
import sys
from paths import Paths
from http.client import RemoteDisconnected
from time import sleep

from pytube import YouTube
from pytube.cli import safe_filename

from convert import merge_video
from literal_functions import show_download_message
from vars import *


# except ImportError:
#     from install_requirements import main
#     main()


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
        self.type: str = 'video'
        self.preferred_extension: str = 'mp4'

    @property
    def streams(self):
        if self._streams is None:
            for _ in range(4):
                try:
                    self._streams = super().streams.filter(
                        only_video=True,
                        adaptive=True, subtype='webm')
                    if self._streams is None:
                        self._streams = super().streams.filter(
                            only_video=True,
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
            self._audio_stream = (
                super().streams.filter(only_audio=True)
                .order_by("abr")
                .last()
            )
        return self._audio_stream

    @property
    def resolution(self):
        if self._resolution is None:
            self._resolution = self.selected_stream.resolution
        return self._resolution

    @property
    def path(self) -> str:
        if self._path is None:
            app_name: str = "Youtube Downloader MAA"
            downloads_folder_path: str = Paths.get_referenced_folder(
                'Downloads') if sys.platform == 'win32' else os.path.join(
                os.getenv("HOME"), 'Downloads')
            self._path: str = os.path.normpath(os.path.join(
                downloads_folder_path, app_name,
                self.type.capitalize()))
            os.makedirs(self._path, exist_ok=True)
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def file_path(self):
        """Get the final path to download in with safe file name"""
        return os.path.join(
            self.path,
            f'{safe_filename(self.title)} ({self.resolution}).{self.preferred_extension}')

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

    def select_detail(self):
        details = [{'reso': stream.resolution,
                    'fps': stream.fps,
                    'size': "{:,.2f}".format(
                        (stream.filesize_mb + self.audio_stream.filesize_mb)
                    ),
                    'subtype': stream.subtype,
                    'itag': stream.itag} for stream in self.streams]

        print("\nSelect a resolution to download:")
        sleep(1)
        for i, detail in enumerate(details, 1):
            print(f"{cyan}[{i}]{yellow}",
                  f"Resolution: {detail['reso']:10}",
                  f"FPS: {detail['fps']}\t",
                  f"Approx_Size: {detail['size']} MB{'':10}",
                  reset, sep='\t')
        while True:
            try:
                select = int(input("\nEnter the number of resolution: "))
                if 0 < select <= len(details):
                    # Set video resolution
                    self._resolution = details[select - 1]['reso']
                    # Set video extension
                    self._subtype = details[select - 1]['subtype']
                    # Set video itag
                    self._itag = details[select - 1]['itag']
                    # return None to break the while loop
                    # and quit from function
                    return None
                else:
                    print(red, "You entered a number out of range!", sep='')
                    print("Please enter a number between 1 and",
                          len(details), reset)
            except ValueError:
                print(red, "You have to enter only numbers!", reset, sep='')

    def download(self):
        """Download video"""
        video_path = self.file_path

        # Check if video exists
        if os.path.exists(video_path):
            return None

        show_download_message(self.type)
        try:
            # Download Only Video
            temp_file_path = self.selected_stream.download(
                output_path=self.path,
                filename_prefix='video_',
                max_retries=3
            )
            # Download Only Audio
            audio_path = self.audio_stream.download(
                output_path=self.path,
                filename_prefix='audio_',
                max_retries=3
            )
            merge_video(
                temp_file_path,
                audio_path,
                video_path,
                self.selected_stream.fps
            )
            os.system(clear)
        except:
            try:
                # Delete downloaded files
                os.remove(temp_file_path)
                os.remove(audio_path)
                os.remove(video_path)
            except:
                pass

    def download_all_resolutions(self, subtype: str | None = "webm"):
        """
        Download all available resolutions with a specific format
        :param str subtype:
            To specify a format. For example: "mp4", "webm"
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
            #     print(
            #         yellow,
            #         f'Could not find the media subtype "{self.subtype}" ',
            #         'Downloading default media subtype...',
            #         subtype,
            #         reset,
            #         sep='',
            #         end=''
            #     )
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
                text=f'with resolution: {yellow}{self.resolution}{reset}'
            )
            self.download()
