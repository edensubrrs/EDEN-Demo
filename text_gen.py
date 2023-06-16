import re
import json
import requests
import wikipedia
import nltk.data
import os, shutil
from tqdm import tqdm
from configparser import ConfigParser
from transformers import GPT2Tokenizer, TrainingArguments, Trainer, GPT2LMHeadModel

def load_model(model_path):
    model = GPT2LMHeadModel.from_pretrained(model_path)
    return model


model_path = "models/text_gen/checkpoint-200000"

model = load_model(model_path)
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = model.cuda()


def load_tokenizer(tokenizer_path):
    # tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    return tokenizer


def generate_text(sequence, max_length, times):
    # model_path = "results/checkpoint-200000"
    model = load_model(model_path)
    tokenizer = load_tokenizer(model_path)
    ids = tokenizer.encode(f'{sequence}', return_tensors='pt')
    output = []
    for time in tqdm(range(times)):
        final_outputs = model.generate(
            ids,
            do_sample=True,
            max_length=max_length,
            pad_token_id=model.config.eos_token_id,
            top_k=50,
            top_p=0.95,
        )
        output.append(tokenizer.decode(final_outputs[0], skip_special_tokens=True))
    return (output)


def generate_text(model, tokenizer, sequence, max_length, times):
    ids = tokenizer.encode(f'{sequence}', return_tensors='pt').cuda()
    output = []
    for time in tqdm(range(times)):
        final_outputs = model.generate(
            ids,
            do_sample=True,
            max_length=max_length,
            pad_token_id=model.config.eos_token_id,
            top_k=50,
            top_p=0.95,
        )
        s = str(tokenizer.decode(final_outputs[0], skip_special_tokens=True))
        s = s.replace(sequence, "")
        output.append(s)
    return (output)


def get_taxo(content):
    # URL = "http://maps.googleapis.com/maps/api/geocode/json"

    data = {
        "content": content
    }

    data = json.dumps(data)

    r = requests.post(url="http://127.0.0.1:8081/gettaxonomy", data=data)

    # extracting data in json format
    # print(r.json())
    data = r.json()[0]['taxonomy']
    return (data)


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def get_lines(content):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return (tokenizer.tokenize(content))


def clear_folder(folder_name):
    files = os.listdir(folder_name)
    for file in files:
        os.remove(folder_name + file)
    return


def generate_using_topic(topic, model, tokenizer, max_length, times):
    li = wikipedia.search(topic)
    found = False
    print(li)
    for i in li:
        try:
            page = wikipedia.page(i)
            print("found for: " + i)
            found = True
        except:
            print(i)
            print("not found")
        if found:
            break
    content = page.content
    content = content.replace("\n", "")
    content = content.strip()
    content = re.sub(' +', ' ', content)
    lines = get_lines(content)[:2]
    prompt = lines[0] + " "
    for i in lines[1:]:
        prompt = prompt + i
    if len(prompt) > 500:
        raise Exception("too much content")
    print("supplying content")
    print(prompt)
    return (prompt, generate_text(model, tokenizer, prompt, max_length, times))


def gen_text_main(lines):
    configur = ConfigParser()
    configur.read('config.ini')
    configur.set('paths', 'prefix', os.getcwd())
    gen_path = configur['paths']['generated_content']

    try:
        shutil.rmtree(gen_path)
    except:
        pass

    print('Save path: ', gen_path)

    with open('config.ini', 'w') as config:
        configur.write(config)

    # f = open('in_process.txt', 'w')
    # s = re.sub(r"\W+|_", " ", lines[0])
    # s = s.replace(" ", "_")
    # print(s)
    # f.write(f"{s}")
    # f.close()

    for s in tqdm(lines):
        s = s.replace("\n", "")
        print("supplying prompt")
        print(s)

        # prompt,generated = "hello testing",["hello testing","hello testing"]
        found = False
        try:
            prompt, generated = generate_using_topic(s, model, tokenizer, 300, 20)
            found = True
        except Exception as e:
            print(e)
            pass
        if found:
            # s = re.sub('[^a-zA-Z0-9 \n\.]', '', s)

            print("got generatted")
            print(generated)

            taxo_prompt = get_taxo(prompt)
            print("Input Taxo:", taxo_prompt)
            # taxo_prompt = "hello testing"
            j = 0
            # print(taxo_prompt)
            s = re.sub(r"\W+|_", " ", s)
            folder = s.replace(" ", "_")

            folder = gen_path + folder
            if not os.path.exists(folder):
                os.makedirs(folder)
            else:
                raise "Unable to create folder"

            f = open(folder + "/taxonomy.txt", "w")
            f.write(taxo_prompt)
            f.close()

            f = open(folder + "/prompt.txt", "w")
            f.write(prompt)
            f.close()

            print("len")
            print(len(generated))
            c = 0
            for i in generated:
                if len(i) > 1:
                    print(len(i))
                    print(isEnglish(i))

                    # print(get_taxo(i))

                    taxo_i = get_taxo(i)
                    # taxo_i = "hello testing"
                    print(taxo_i)
                    print("====")

                    if isEnglish(i) and ((taxo_prompt != 'None' and taxo_i == taxo_prompt) or (taxo_prompt == 'None')):
                        if c == 2:
                            break
                        k = prompt + i
                        lines = get_lines(k)
                        print(lines)
                        try:
                            path = folder + "/" + "text_output_" + str(j)
                            os.mkdir(path)
                        except:
                            pass

                        f = open(path + "/text_output_" + str(j) + ".txt", "w")

                        for line in lines:
                            f.write(line + "\n")
                        f.close()
                        j = j + 1
                        c = c + 1

# gen_text_main(["Sustainable Energy"])
