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
            self.video.streams
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
        title = safe_filename(self.title)
        audio_unique_name = _unique_name(
            title,
            self.selected_stream.subtype,
            'audio',
            self.path
        )
        # Set output path
        final_path = os.path.join(
            self.path,
            f'{title}.mp3'
        )
        # Check if audio exists
        if os.path.exists(final_path):
            return None
        # Set audio path
        audio_path = os.path.join(
            self.path,
            audio_unique_name
        )
        self.selected_stream.download(
            output_path=self.path,
            filename=audio_unique_name,
            max_retries=3
        )
        convert_audio(
            audio_path,
            final_path
        )
