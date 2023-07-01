import moviepy.editor as mpe
import os


def merge_video(vidname: str, audname: str, outname: str, fps=30):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)
    os.remove(vidname)
    os.remove(audname)


def convert_audio(audname: str, outname: str):
    my_audio = mpe.AudioFileClip(audname)
    my_audio.write_audiofile(outname)
    os.remove(audname)
