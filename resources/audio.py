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
            os.system(clear)
            print(
                f'The {self.type.capitalize()} has been downloaded successfully'
            )
        except KeyboardInterrupt or IncompleteRead:
            try:
                # Delete downloaded files
                os.remove(audio_path)
                os.remove(temp_file_path)
            except Exception as e:
                print(e)

    # def merge(self, audio_path, output_path):
    #     """Convert audio to the desire format and save to output path"""
    #     convert_audio(audio_path, output_path,
    #                   bitrate=self.audio_stream.abr.rstrip('bps'))
