try:
    from video import Video
    from pytube.cli import _unique_name, safe_filename
    from convert import convert_audio
    from time import sleep
    from litfun import show_download_message
    from vars import *
    from http.client import IncompleteRead
    import os
except ImportError:
    from install_requirements import main
    main()


class Audio(Video):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.type = 'audio'

    @property
    def subtype(self):
        if self._subtype is None:
            self._subtype = self.audio_stream.subtype
        return self._subtype

    def download(self):
        '''Download the Audio'''
        self.title = safe_filename(self.title)
        # Audio name to be saved
        audio_name = f'{self.title} ({self.audio_stream.abr}).mp3'
        # Set output filename with path
        audio_path = os.path.join(self.path, audio_name)
        # Audio file with temp name to download
        temp_file_name = _unique_name(
            self.title,
            self.subtype,
            'audio',
            self.path
        )
        # Set temp audio file path
        temp_file_path = os.path.join(self.path, temp_file_name)

        # Check if audio exists
        if os.path.exists(audio_path):
            return None
        show_download_message(self.type)
        try:
            self.audio_stream.download(
                output_path=self.path,
                filename=temp_file_name,
                max_retries=3
            )
            convert_audio(temp_file_path, audio_path,
                          # The convert function accepts 'k' only; not 'kbps'
                          bitrate=self.audio_stream.abr.replace('bps', '')
                          )
        except KeyboardInterrupt or IncompleteRead:
            try:
                # Delete downloaded files
                os.remove(audio_path)
                os.remove(temp_file_path)
            except:
                pass
