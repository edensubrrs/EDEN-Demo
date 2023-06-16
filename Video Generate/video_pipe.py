from tqdm import tqdm
import main_process as M
import shutil, glob, os, json
from configparser import ConfigParser
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from transformers import AutoTokenizer, AutoModel


configur = ConfigParser()
configur.read('../config.ini')
gen_path = configur['paths']['generated_content']
data_vdo_path = configur['paths']['video_save_path']
db_path = configur['paths']['db_path']
raw_data = configur['paths']['raw_data']

print('DB:', db_path)

db_dump = json.load(open(db_path, "r"))
count = list(db_dump.values())[-1]['id'] + 1

data = glob.glob(f"{gen_path}*")

tokenizer = AutoTokenizer.from_pretrained("bclavie/edubert")
model = AutoModel.from_pretrained("bclavie/edubert")


# Function to embed a text string
def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state[0, -1, :].detach().numpy()


def get_data(par_dir, path, yes):
    trans_path = glob.glob(path + '/*.txt')

    trans = open(trans_path[0], 'r')
    trans = trans.readlines()

    if yes:
        prompt = open(f'{par_dir}/prompt.txt', 'r')
        prompt = prompt.readlines()

        taxo = open(f'{par_dir}/taxonomy.txt', 'r')

        taxo = taxo.readlines()

        return trans, prompt, taxo

    return trans


for j in tqdm(data):
    key_topic = j.split('/')[-1].replace('_', ' ')
    folder_path = glob.glob(j + "/text*")
    for i in folder_path:
        # print('folder path',i)
        folder = i.rsplit('/', 2)[-2:]
        dp = '/'.join(folder)
        sp = '_'.join(folder)

        vdo_path = data_vdo_path + sp
        print(vdo_path)
        M.main(i, vdo_path)
        print('save path', raw_data.split('/')[-2]+'/'+dp)
        if key_topic not in db_dump:
            db_dump[key_topic] = {}
            db_dump[key_topic]["id"] = count
            db_dump[key_topic]["embedding"] = embed_text(key_topic).tolist()

            trans, prmpt, taxo = get_data(j, i, True)

            db_dump[key_topic]['taxonomy'] = taxo
            db_dump[key_topic]['prompt'] = prmpt
            db_dump[key_topic]["video_details"] = [{'data_path': raw_data.split('/')[-2]+'/'+dp,
                                                    'video_path': data_vdo_path.split('/')[-2]+'/' + sp + '.mp4',
                                                    'transcript': trans}]
            count += 1
        trans = get_data(j, i, False)

        db_dump[key_topic]["video_details"].append({'data_path': raw_data.split('/')[-2]+'/'+dp,
                                                    'video_path': data_vdo_path.split('/')[-2]+'/' + sp + '.mp4',
                                                    'transcript': trans})
    dest = shutil.copytree(j, raw_data + key_topic)
    # shutil.rmtree(j)

f = open(db_path, "r+")
s = json.dumps(db_dump)
f.write(s)
f.close()
