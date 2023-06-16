import os
import json
import glob
from transformers import AutoTokenizer, AutoModel
from scipy.spatial.distance import cosine
import text_gen as generate
import image_gen as img_generate
from configparser import ConfigParser

configur = ConfigParser()
configur.read('config.ini')
configur.set('paths', 'prefix', os.getcwd())
db_path = configur['paths']['db_path']
dir_path = configur['paths']['video_save_path']

with open('config.ini', 'w') as config:
        configur.write(config)


# Set the directory path and pattern
pattern = '*text_output_*.mp4'

file_list = os.listdir(dir_path)

file_name_to_path = {}

# # Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bclavie/edubert")
model = AutoModel.from_pretrained("bclavie/edubert")


# Function to embed a text string
def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state[0, -1, :].detach().numpy()


def get_data(path, yes):
    trans_path = glob.glob(path + '/*.txt')

    trans = open(trans_path[0], 'r')
    trans = trans.readlines()

    if yes:
        par_dir = os.path.dirname(path)

        prompt = open(f'{par_dir}/prompt.txt', 'r')
        prompt = prompt.readlines()

        taxo = open(f'{par_dir}/taxonomy.txt', 'r')

        taxo = taxo.readlines()

        return trans, prompt, taxo

    return trans


topic = input('Please Enter the topic: ')
topic_embedding = embed_text(topic)



db_dump = json.load(open(db_path, "r"))

# Create a dictionary to hold file names and their similarity scores
similarity_scores = {}

# Iterate over the file name embeddings
for file_name in db_dump:
    # Compute the cosine similarity between the topic and file name embeddings
    similarity = 1 - cosine(topic_embedding, db_dump[file_name]['embedding'])

    # Store the similarity score in the dictionary
    similarity_scores[file_name] = similarity
# Find the file name with the highest similarity score
best_match = max(similarity_scores, key=similarity_scores.get)

# Print the closest match if its similarity score is greater than 0.95, else print "Video not found!"
if similarity_scores[best_match] > 0.98:
    print(f'The closest match to the topic "{topic}" is the file "{best_match}"')

    vdo_lst = [i['video_path'] for i in db_dump[best_match]['video_details']]

    print(f"Path to videos {vdo_lst}")
else:
    print("Video not found!")
    print("Generating New Content.....")

    generate.gen_text_main([topic])

    print("Generating Images.....")

    img_generate.img_gen()
