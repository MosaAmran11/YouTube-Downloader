try:
    from video import Video
    from pytube.cli import _unique_name, safe_filename
    from convert import convert_audio
    from time import sleep
    from literal_functions import show_download_message
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
    def file_path(self):
        """Get the final path to download in with safe file name"""
        audio_name = f'{safe_filename(self.title)} ({self.audio_stream.abr}).mp3'
        return os.path.join(self.path, audio_name)

    @property
    def subtype(self):
        if self._subtype is None:
            self._subtype = self.audio_stream.subtype
        return self._subtype

    def download(self):
        '''Download the Audio'''
        audio_path = self.file_path

        # Check if audio exists
        if os.path.exists(audio_path):
            return None
        show_download_message(self.type)
        try:
            temp_file_path = self.audio_stream.download(
                output_path=self.path,
                filename_prefix='audio_',
                max_retries=3
            )
            # return (temp_file_path, audio_path)
            convert_audio(temp_file_path, audio_path,
                          # The convert function accepts 'k' only; not 'kbps'
                          bitrate=self.audio_stream.abr.rstrip('bps')
                          )
        except KeyboardInterrupt or IncompleteRead:
            try:
                # Delete downloaded files
                os.remove(temp_file_path)
                os.remove(audio_path)
            except:
                pass
