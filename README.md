# EDEN: Enhanced Database Expansion in eLearning: A System for Automated Generation of Academic Videos

This is a guide on how to install and use the project on your local machine. 

# Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

This system has been tested on :
```
Ubuntu: 22.04.2 LTS
CPU: Intel i9-12900K
GPU: Nvidia RTX 3060
```
All other requirements are present in Installation and Setup section

### Prerequisites

You need to have Conda installed on your system. If you don't have Conda installed, please follow the [official documentation](https://docs.anaconda.com/anaconda/install/linux/).

### Installation and Setup

To set up the project on your local machine, follow these steps:

1. Clone the repository

```
git clone https://github.com/edensubrrs/EDEN-Demo.git
```

2. Install Rust-Compiler for Tagerec

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Restart the terminal

3. Navigate to the project directory

```
cd EDEN-Demo
```

4. Create Conda environments using the provided `.yml` files:

```
cd envs/
conda env create -f Eden_pre_env.yml
pip install transformers==2.8.0
conda env create -f Eden_env_1.yml
conda env create -f Eden_env_2.yml
```

5. Download the required weights for the models and other pertinent folders from the following URLs:

```
## TagRec Weights
https://drive.google.com/drive/folders/15ODGLe7Lhg9ZmQa-Gt53J9KQ6eZTXz_o?usp=sharing

## Text Generation Weights
https://drive.google.com/file/d/1kKinIFYJOtWKGeQiWQX3-oibIXzRzelu/view?usp=sharing

## Image Generation Weights
https://drive.google.com/file/d/1e1isTRiOsxYGlEPtMxoHR0dM49Pc2ILR/view?usp=sharing
```

6. Download the Videos Database from the following path and unzip it in **EDEN-Demo** (root folder):

```
https://drive.google.com/file/d/1whNe31ngerFTD_sbcofhzPY7K1H4b4fh/view?usp=sharing
```
7. Unzip the _text_gen.zip_ and _image_gen.zip_ inside the **EDEN-Demo/model** folder.

8. Copy the tagrec weights _model_weights.zip_ to 

```
EDEN-Demo/models/TagRec_Plus_Plus_TKDE-main/taxonomy_predictor_api_and_ui/app/api/modle/
```

### How to Run

Here is how to use the application:

1. Activate the `eden_pre_env` environment and run the `api.py` file in a separate terminal:

```
conda activate eden_pre_env
cd "models/TagRec_Plus_Plus_TKDE-main/taxonomy_predictor_api_and_ui"
uvicorn app.main:app --port 8081
```

Leave this terminal running and proceed to the next steps in a new terminal.

2. Activate the `eden_env_1` environment and run the `main.py` file in the root directory **EDEN-Demo**:

```
conda activate eden_env_1
python main.py
```

Enter the Topic for which the user wants to generate the video.

If the video/s for that topic is already present in the database it will print the path of all those videos. (As shown in the image below)

![alt text](https://github.com/edensubrrs/EDEN-Demo/blob/main/readme_files/Screenshot%20from%202023-06-16%2017-13-32.png)

3. After the execution of the `main.py` file, deactivate the current environment, activate the `eden_env_2` environment:

```
conda deactivate
conda activate eden_env_2
cd "PriorGrad-acoustic/"
./run.sh
```

4. Finally, deactivate the current environment, reactivate the 'eden_env_1' environment and run the following commands:

```
conda deactivate
conda activate eden_env_1
cd ..
cd "Video Generate"
python video_pipe.py
```

Generated Video is saved in: 'EDEN-Demo/videos_db'
Generated Text, Images and Audio is saved in: 'EDEN-Demo/Raw_Data'

**The details of the video have been successfully stored in the database, contributing to its expansion!**

# Database Explained

The database organisation which caches the video paths, title, embeddings and other important information is explained subsequently.

We release the json dump of this database (**database.json**).


```
{
  "Concept": {
    "id": 1,
    "embedding": [0.5, 0.4, -0.3, 0.2],
    "taxonomy": ["root>>level1>>level2>>level3"],
    "prompt": ["This is a test sentence explaining the concept."],
    "video_details": [
      {
        "data_path": "/TestPath/Concept/text_output_0",
        "video_path": "test_videos_db/Concept_text_output_0.mp4",
        "transcript": ["This is a test transcript of the video content.\n"]
      },
      {
        "data_path": "/TestPath/Concept/text_output_1",
        "video_path": "test_videos_db/Concept_text_output_1.mp4",
        "transcript": ["This is another test transcript of the video content.\n"]
      }
    ]
  }
}

```
In this structure:

1. "Concept" can be replaced with any topic you are describing.
2. "id" can be any unique integer that represents the concept.
3. "embedding" is a list of floating-point numbers.
4. "taxonomy" is a list of strings describing the hierarchy of the topic.
5. "prompt" is a list of strings, each a sentence or paragraph describing the topic.
6. "video_details" is a list of objects, where each object represents a specific video and its details. Each object has:
7. "data_path": a string representing the file path of raw data.
8. "video_path": a string representing the file path of the video.
9. "transcript": a list of strings, each a sentence or paragraph from the video transcript.


### Dataset

The released dataset folder can be found here:

```
https://drive.google.com/drive/folders/1dxeFfsZRUldMrCrU7lmb0pAgMEWkag3K?usp=sharing
```
# Citations

This project utilizes work from the following repositories:

1. **TagRec++: Hierarchical Label Aware Attention Network for Question Categorization**

   Repository: [https://github.com/ADS-AI/TagRec_Plus_Plus_TKDE](https://github.com/ADS-AI/TagRec_Plus_Plus_TKDE)

   Citation:

   ```
   @article{viswanathan2022tagrec++,
     title={TagRec++: Hierarchical Label Aware Attention Network for Question Categorization},
     author={Viswanathan, Venktesh and Mohania, Mukesh and Goyal, Vikram},
     journal={arXiv preprint arXiv:2208.05152},
     year={2022}
   }
   ```

2. **High-Resolution Image Synthesis with Latent Diffusion Models**

   Repository: [https://github.com/CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion)

   Citation:

   ```
   @misc{rombach2021highresolution,
         title={High-Resolution Image Synthesis with Latent Diffusion Models}, 
         author={Robin Rombach and Andreas Blattmann and Dominik Lorenz and Patrick Esser and Björn Ommer},
         year={2021},
         eprint={2112.10752},
         archivePrefix={arXiv},
         primaryClass={cs.CV}
   }
   ```

3. **PriorGrad: Improving Conditional Denoising Diffusion Models with Data-Dependent Adaptive Prior**

   Repository: [https://github.com/microsoft/NeuralSpeech/tree/master/PriorGrad-acoustic](https://github.com/microsoft/NeuralSpeech/tree/master/PriorGrad-acoustic)

   Citation:

   ```
   @inproceedings{
     lee2022priorgrad,
     title={PriorGrad: Improving Conditional Denoising Diffusion Models with Data-Dependent Adaptive Prior},
     author={Lee, Sang-gil and Kim, Heeseung and Shin, Chaehun and Tan, Xu and Liu, Chang and Meng, Qi and Qin, Tao and Chen, Wei and Yoon, Sungroh and Liu, Tie-Yan},
     booktitle={International Conference on Learning Representations},
     year={2022},
   }
   ```

4. **Language Models are Unsupervised Multitask Learners GPT-2**

   Repository: [https://huggingface.co/gpt2](https://huggingface.co/gpt2)

   Citation:

   ```
   @article{radford2019language,
     title={Language Models are Unsupervised Multitask Learners},
     author={Radford, Alec and Wu, Jeff and Child, Rewon and Luan, David and Amodei, Dario and Sutskever, Ilya},
     year={2019}
   }
   ```
   
5. **EduBERT: Pretrained Deep Language Models for Learning Analytics**

   Repository: [https://huggingface.co/bclavie/edubert](https://huggingface.co/bclavie/edubert)

   Citation:

   ```
   @misc{clavié2019edubert,
         title={EduBERT: Pretrained Deep Language Models for Learning Analytics}, 
         author={Benjamin Clavié and Kobi Gal},
         year={2019},
         eprint={1912.00690},
         archivePrefix={arXiv},
         primaryClass={cs.CY}
   }
   ```

6. **MoviePy**

   Repository: [https://github.com/Zulko/moviepy](https://github.com/Zulko/moviepy)

It's essential to acknowledge and respect the work of others when we benefit from it. Thank you to the authors of these repositories for their significant contributions.
