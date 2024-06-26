import imageio_ffmpeg as ffmpeg
import subprocess
import os
from vars import clear


ffmpeg_path = ffmpeg.get_ffmpeg_exe()


def merge_video(video_path: str, audio_path: str, output_path: str, fps=30):
    command = [ffmpeg_path, '-i', video_path, '-i', audio_path, '-c:v',
               'copy', '-r', str(fps), '-c:a', 'aac', '-strict', 'experimental', output_path]
    subprocess.run(command, check=True)
    os.remove(video_path)
    os.remove(audio_path)
    os.system(clear)


def convert_audio(input_file: str, output_file: str, bitrate: str = '192k'):
    command = [ffmpeg_path, '-i', input_file, '-b:a', bitrate, output_file]
    subprocess.run(command, check=True)
    os.remove(input_file)
    os.system(clear)
