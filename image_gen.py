import torch
from tqdm import tqdm
import os, glob
import shutil
from diffusers import StableDiffusionPipeline
from configparser import ConfigParser



def clear_folder(folder_name):
    files = os.listdir(folder_name)
    for file in files:
        shutil.rmtree(folder_name + file)
    return


def img_gen():

    configur = ConfigParser()
    configur.read('config.ini')
    gen_path = configur['paths']['generated_content']

    model_path = "models/image_gen"
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
    pipe.unet.load_attn_procs(model_path)
    pipe.to("cuda")

    folder = glob.glob(gen_path + '*')
    print('PATH:', folder)
    for i in tqdm(folder):
        gen = glob.glob(i + '/text_*')

        for path in gen:
            print(path)
            if not os.path.exists(path + "/images"):
                text_file = path + '/' + path.split('/')[-1] + ".txt"
                try:
                    # os.mkdir(path)
                    os.mkdir(path + "/images")
                    os.mkdir(path + "/audios")
                except:
                    pass
                f = open(text_file, "r")
                lines = f.readlines()
                f.close()
                count = 1
                for line in lines:
                    # print(line)
                    image = pipe(line, num_inference_steps=30, guidance_scale=7.5).images[0]
                    image.save(path + "/images/" + str(count) + ".png")
                    count = count + 1
            else:
                print("skipping" + str(path))
