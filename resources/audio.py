# try:
import os
from http.client import IncompleteRead

import lyricsgenius
from pytube.cli import safe_filename

from convert import convert_audio
from literal_functions import show_download_message
from video import Video


# except ImportError:
#     from install_requirements import main
#     main()


class Audio(Video):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.__genius_api_token = "JaewfJIWcfwemCcVjLHTCqOQaNOwo_8nog-4uqnKUVaRqcbDISY7oEDHAlEc_Y6g"
        self.author = super().author
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

    @staticmethod
    def __fetch_lyrics(song_title, artist_name, api_token):
        genius = lyricsgenius.Genius(api_token)
        song = genius.search_song(song_title, artist_name)
        return song.lyrics

    def download(self):
        """Download the Audio"""
        audio_path = self.file_path
        lyrics_path = self.file_path.replace('.mp3', '.lrc')

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
            convert_audio(temp_file_path, audio_path,
                          # The convert function accepts 'k' only; not 'kbps'
                          bitrate=self.audio_stream.abr.rstrip('bps')
                          )
            lyrics = Audio.__fetch_lyrics(self.title, self.author, self.__genius_api_token)
            # Save the song's lyrics (if found) at the same audio path
            if lyrics:
                with open(lyrics_path, "w", encoding="utf-8") as f:
                    f.write(lyrics)
        except KeyboardInterrupt or IncompleteRead:
            try:
                # Delete downloaded files
                os.remove(temp_file_path)
                os.remove(audio_path)
            except:
                pass
