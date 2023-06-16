# importing integrated modules
import cv2
import glob
import os
import re
import textwrap
from datetime import timedelta
import numpy as np
import soundfile as sf
from PIL import ImageFile, Image
from natsort import natsorted

from video_gen import *

ImageFile.LOAD_TRUNCATED_IMAGES = True


def text_impose(image_path, text):
    try:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    except:
        try:
            img_pil = Image.open(image_path)
            img_pil.load()
            # Convert PIL image to OpenCV format
            img = np.array(img_pil)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except:
            raise ValueError("Image empty")

    font = cv2.FONT_HERSHEY_TRIPLEX
    font_size = 0.5
    font_thickness = 1
    text = ' '.join(text)
    wrapped_text = textwrap.wrap(text, width=40)
    for i, line in enumerate(wrapped_text):
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]

        gap = textsize[1] + 10

        y = int((img.shape[0] + textsize[1] + 250) / 2) + i * gap
        x = int((img.shape[1] - textsize[0]) / 2)

        I = cv2.rectangle(img, (x - 15, y - 15), (x + textsize[0], y + textsize[1] - 5), (0, 0, 0), -1)

        I = cv2.putText(I, line, (x, y), font,
                        font_size,
                        (255, 255, 255),
                        font_thickness,
                        lineType=cv2.LINE_AA)
    return I


def main_new(path, vdo_path):
    try:
        img_path = f"{path}/images/"
        ado_path = f"{path}/audios/wavs/"
        dirFiles = os.listdir(ado_path)
        dirFiles.sort(key=lambda f: int(re.sub('\D', '', f)))

        inputtxt = f'{path}/text_*.txt'
        sub_paths = glob.glob(inputtxt)

        print(img_path)
        print(ado_path)
        print(sub_paths)

        if not sub_paths:  # No text files found
            print(f"No text files found in {path}")
            return
        sub_path = sub_paths[0]
        with open(sub_path) as f:
            subtxt = f.read()

        par = re.split('\n{1,}', subtxt)
        npar = len(par)

        tdstart = timedelta(hours=0, seconds=0)
        total_video_time = 0

        image_clips = image_clip_generator(img_path, ado_path, par, npar, dirFiles)

        gen_video(image_clips, fps=total_video_time, filename=vdo_path)

    except Exception as e:
        print(f"An error occurred: {e}")


def image_clip_generator(img_path, ado_path, par, npar, dirFiles):
    for i in range(npar - 1):
        image_impsd = []
        with sf.SoundFile(ado_path + dirFiles[i]) as f:
            dur = len(f) / f.samplerate

        img_index = dirFiles[i].split('.')[0]
        img_list = glob.glob(img_path + f'{img_index}.*')
        img_list = natsorted(img_list)
        tok_text = par[i].split(' ')
        for lp in range(len(tok_text)):
            text = tok_text[:lp + 1]
            image_impsd.append(text_impose(img_list[0], text))

        yield add_static_image_to_audio(image_impsd, ado_path + dirFiles[i], len(image_impsd) / dur)


def main(path, vdo_path):
    # image files
    # try:
    img_path = f"{path}/images/"

    # video files handling
    ado_path = f"{path}/audios/wavs/"
    dirFiles = os.listdir(ado_path)
    dirFiles.sort(key=lambda f: int(re.sub('\D', '', f)))

    # intializing .txt file locared in the same folder as this python script
    inputtxt = f'{path}/text_*.txt'
    sub_path = glob.glob(inputtxt)[0]
    subtxt = open(sub_path).read()

    # splitting paragraphs into list items with regex
    par = re.split('\n{1,}', subtxt)

    # pulling number of paragraphs in a text doc
    npar = len(par)
    # print('lines ',npar, sub_path)

    # initializing starting subtitle and subtitile duration
    tdstart = timedelta(hours=0, seconds=0)

    total_video_time = 0

    # creating a list of timedeltas with audio time sync
    tdlist = [tdstart]
    image_clips = []

    for i in range(npar - 1):
        image_impsd = []

        with sf.SoundFile(ado_path + dirFiles[i]) as f:
            dur = len(f) / f.samplerate

        img_index = dirFiles[i].split('.')[0]

        img_list = glob.glob(img_path + f'{img_index}.*')
        img_list = natsorted(img_list)
        if len(img_list) == 0:
            print("NO IMAGES")
            return
        # print('IMG:',img_list)
        tok_text = par[i].split(' ')
        for lp in range(len(tok_text)):
            text = tok_text[:lp + 1]
            try:
                image_impsd.append(text_impose(img_list[0], text))
            except Exception as e:
                print(e)
                return

        image_clips.append(add_static_image_to_audio(image_impsd, ado_path + dirFiles[i], len(image_impsd) / dur))
        total_video_time += dur

    gen_video(image_clips, fps=total_video_time, filename=vdo_path)
