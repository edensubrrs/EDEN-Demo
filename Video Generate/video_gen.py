from moviepy.editor import *


def add_static_image_to_audio(image_path, audio_path, duration):
    audio_clip = AudioFileClip(audio_path)

    clip = ImageSequenceClip(image_path, fps=duration)
    clip = clip.set_audio(audio_clip)

    return clip


def gen_video(image_clips, fps, filename):
    concat_clip = concatenate_videoclips(image_clips)

    concat_clip.write_videofile(f"{filename}.mp4")
