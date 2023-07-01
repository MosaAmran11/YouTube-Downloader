from pytube import YouTube
from convert import merge_video
import os


red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'
magenta = '\033[35m'
cyan = '\033[36m'
rset = '\033[39m'


class Video:
    def __init__(self, url: str) -> None:
        self.video = YouTube(url)
        self.__title = None
        self.__streams = None
        self.__resolution = None
        self.__path = None
        self.__ext = None
        self.__itag = None

    @property
    def title(self):
        if self.__title:
            return self.__title
        self.__title = self.video.title
        return self.__title

    @property
    def streams(self):
        if self.__streams:
            return self.__streams
        self.__streams = self.video.streams.filter(type='video', adaptive=True)
        return self.__streams

    def get_all_resolutions(self):
        res_list = []
        for stream in self.streams:
            res_list.append(stream.resolution)
        return res_list

    @property
    def resolution(self):
        if self.__resolution:
            return self.__resolution
        self.__resolution = self.streams.get_by_itag(self.itag).resolution
        return self.__resolution

    @property
    def path(self):
        if self.__path:
            return self.__path
        APP_NAME = "Youtube Downloader MAA"
        if os.name == 'nt':
            userprofile = os.getenv("userprofile")
            path = str(os.path.join(
                userprofile, 'Downloads', APP_NAME, "Video"))
        else:
            userprofile = os.getenv("USER") if os.getenv(
                'SUDO_USER') is None else os.getenv('SUDO_USER')
            path = str(os.path.join(
                "/", "home", userprofile, "Downloads", APP_NAME, "Video"))
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
        self.__ext = self.__streams.get_by_itag(
            self.itag).mime_type.split("/")[1]
        return self.__ext

    @property
    def itag(self):
        if self.__itag:
            return self.__itag
        self.__itag = self.select_detail()
        return self.__itag

    # Method for user to get video's details
    def get_details(self):
        details = []
        for stream in self.streams:
            details.append([stream.resolution,
                            "Size: {:,.0f} MB".format(stream.filesize),
                            stream.mime_type.split('/')[1],
                            stream.itag
                            ])
        return details

    def select_detail(self):
        details = self.get_details()
        print("\nSelect a resolution to download:")
        for i in range(len(details)):
            print(f"{cyan}[{i + 1}]{yellow}", details[i], rset, sep='')
        while True:
            try:
                select = int(input("\n\nEnter the number of resolution: "))
                if 0 < select <= len(details):
                    # Set video resolution
                    self.__resolution = details[select - 1][0]
                    # Set video extesion
                    self.__ext = details[select - 1][-2]
                    # Set video itag
                    self.__itag = details[select - 1][-1]
                    # break the while loop
                    break
                else:
                    print(red, "You entered a number out of range!",
                          "\nPlease enter a number between 1 and",
                          len(details), rset, sep='')
            except ValueError:
                print(red, "You have to enter only numbers!", rset, sep='')

    def download(self):
        """Download video"""
        try:
            if self.streams.get_by_itag(self.itag).is_progressive:
                # Set vdieo name with extension
                vidname = Video.__check_title(
                    self.title) + f"_{self.resolution}.{self.extension}"
                # Download video
                self.streams.get_by_itag(self.itag).download(
                    output_path=self.path, filename=vidname, max_retries=3)
            else:
                # Filter the title
                title = Video.__check_title(self.title)
                # Set video name with extension
                vidname = title + f".{self.extension}"
                # Stream only audio types
                audstream = self.video.streams.get_audio_only()
                # Extract the extesion of audio
                audext = audstream.mime_type.split("/")[1]
                # Format the name of audio
                audname = Video.__check_title(self.title) + f"_audio.{audext}"
                # Download Only Video
                self.streams.get_by_itag(self.itag).download(
                    output_path=self.path, filename=vidname, max_retries=3)
                # Download Only Audio
                audstream.download(
                    output_path=self.path, filename=audname, max_retries=3)
                ##############  MERGE SECSION   ##############
                # Set video path
                vidpath = os.path.join(self.path, vidname)
                # Set audio path
                audpath = os.path.join(self.path, audname)
                # Set output path
                outpath = os.path.join(
                    self.path, f'{title}_{self.resolution}.{self.extension}')
                fps = self.streams.get_by_itag(self.itag).fps
                # Merge Video with Audio into one Video file
                merge_video(vidpath, audpath, outpath, fps)
        except KeyboardInterrupt:
            print(red, "Exited by user.", rset, sep='')
            exit()

    @staticmethod
    def __check_title(title: str):
        # Only allowed chars !@&+=(){}[]-_
        specialChar = "#$%^;'.,/\\:*?\"<>|"
        for char in specialChar:
            title = title.replace(char, "")
        return title
