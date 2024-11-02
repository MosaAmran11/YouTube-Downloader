# try:
import os
from http.client import IncompleteRead

import lyricsgenius
import pytube
import pysrt
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
        self.__genius_api_token: str = "JaewfJIWcfwemCcVjLHTCqOQaNOwo_8nog-4uqnKUVaRqcbDISY7oEDHAlEc_Y6g"
        self.author = super().author
        self.type: str = 'audio'
        self.preferred_extension: str = 'mp3'


    @property
    def file_path(self):
        """Get the final path to download in with safe file name"""
        return os.path.join(
            self.path,
            f'{safe_filename(self.title)} ({self.audio_stream.abr}).{self.preferred_extension}')

    @property
    def subtype(self):
        if self._subtype is None:
            self._subtype = self.audio_stream.subtype
        return self._subtype

    def __fetch_lyrics(self, song_title, artist_name, api_token) -> str | pytube.Caption | None:
        try:
            genius = lyricsgenius.Genius(api_token)
            song = genius.search_song(song_title, artist_name)
            return super().captions.get_by_language_code(
                lang_code='en').generate_srt_captions() if not song else song.lyrics
        except:
            return None

    @staticmethod
    def __convert_srt_to_lrc(srt_file_path, lrc_file_path, delete_old_file=False):
        # Load subtitles from the SRT file
        subs = pysrt.open(srt_file_path)

        # Open the LRC file for writing
        with open(lrc_file_path, 'w', encoding='utf-8') as lrc_file:
            for sub in subs:
                # Format the start time for LRC
                start_time = sub.start.to_time().strftime('%H:%M:%S.%f')[:-3]  # Keep only milliseconds
                lrc_file.write(f'[{start_time}] {sub.text.strip()}\n')

        # Delete the old SRT file
        if delete_old_file:
            os.remove(srt_file_path)

    def download(self):
        """Download the Audio"""
        audio_path = self.file_path
        lyrics_path = self.file_path.replace(f'.{self.preferred_extension}', '.lrc')

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
            lyrics = self.__fetch_lyrics(self.title, self.author, self.__genius_api_token)
            # Save the song's lyrics (if found) at the same audio path
            if lyrics:
                if lyrics is pytube.Caption:
                    path = lyrics.download(
                        title=self.file_path.removesuffix(f'.{self.preferred_extension}'),
                        srt=True)
                    Audio.__convert_srt_to_lrc(path, lyrics_path)
                else:
                    with open(lyrics_path, "w", encoding="utf-8") as f:
                        f.write(lyrics)
        except KeyboardInterrupt or IncompleteRead:
            try:
                # Delete downloaded files
                os.remove(temp_file_path)
                os.remove(audio_path)
            except:
                pass
