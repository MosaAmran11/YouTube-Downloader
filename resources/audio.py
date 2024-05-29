try:
    from video import Video
    from pytube.cli import _unique_name, safe_filename
    from convert import convert_audio
    from time import sleep
    from litfun import show_download_message
    from vars import *
    from http.client import RemoteDisconnected
    import os
except ImportError:
    from install_requirements import main
    main()


class Audio(Video):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.__selected_stream = None
        self.__itag = None
        self.type = 'audio'

    @property
    def selected_stream(self):
        if self.__selected_stream:
            return self.__selected_stream
        self.__selected_stream = (
            super().streams
            .get_audio_only(None)
        )
        return self.__selected_stream

    @property
    def itag(self):
        if self.__itag:
            return self.__itag
        self.__itag = self.selected_stream.itag
        return self.__itag

    @itag.setter
    def itag(self, itag):
        if not self.__itag:
            self.__itag = itag

    def download(self):
        self.title = safe_filename(self.title)
        audio_name = f'{self.title}({self.selected_stream.abr})'
        # Set output filename with path
        file_path = os.path.join(self.path, f"{audio_name}.mp3")
        # Check if audio exists
        if os.path.exists(file_path):
            return None
        show_download_message(self.type)
        self.selected_stream.download(
            output_path=self.path,
            filename=f'{audio_name}.{self.selected_stream.subtype}',
            max_retries=3
        )
        convert_audio(
            os.path.join(
                self.path, f'{audio_name}.{self.selected_stream.subtype}'),
            file_path,
            # The convert function accepts 'k' only; not 'kbps'
            bitrate=self.selected_stream.abr.replace('bps', '')
        )
