import os
import json
from bs4 import BeautifulSoup

from multiprocessing import Pool

import nltk
from nltk import word_tokenize
from nltk import pos_tag

# from corpus_handlers import handler_helpers as hh

bnc_dir = '/Users/rangat/Documents/lingResearch/whAnalysis/corpora/2554/2554/download/Texts'
bnc_extension = ".xml"

def isWh(un_tagged)->str:
    tagged = word_tokenize(un_tagged)
    tagged = [x.lower() for x in tagged]
    whs = set(['who', 'where', 'how'])

    return not whs.isdisjoint(set(tagged))

def extract_wh_sentences_from_file(file:str)->list:
    with open(file, 'r') as f:
        xml_content = f.read()
    soup = BeautifulSoup(xml_content, 'lxml')
    all_sents = list(map(lambda x: x.text, soup.find_all('s')))
    return list(filter(lambda x: isWh(x), all_sents))

def append_sentences_to_file(files:list, fname:str):
    wh_json = []
    for file in files:
        sents = extract_wh_sentences_from_file(file)
        wh_json.extend(list(map(lambda s: {'sentence':s, 'corpus':'bnc', 'medium':'print'}, sents)))
    
    with open(fname, 'w') as f:
        json.dump(wh_json, f)

def put_sent_in_file(fname:str):
    sents = extract_wh_sentences_from_file(fname)
    jlist = list(map(lambda s: {'sentence':s, 'corpus':'bnc', 'medium':'print'}, sents))
    '/Users/rangat/Documents/lingResearch/whAnalysis/corpora/2554/2554/download/Texts/A/A0/A00.xml'
    file = fname.split('/')[-1].split('.')[0]
    new_fname = f'bnc/{file}.json'
    with open(new_fname, 'w') as j:
        json.dump(jlist, j)

def get_file_paths(path:str, extension:str)->list:
    fnames = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if not f.endswith(extension):
                continue
            
            fnames.append(os.path.join(root, f))
    return fnames

def collect_json():
    collected = []
    for file in os.listdir('./bnc'):
        filename = os.fsdecode(file)
        
        if not filename.endswith(".json"):
            continue
        
        with open(f'bnc/{filename}') as json_data:
            data = json.load(json_data)
            collected.extend(data)

    with open("bnc.json", 'w') as outfile:
        json.dump(collected, outfile, indent=4)
        print("successfully made complete json")

def pool_handler(fnames:list):
    p = Pool(10)
    p.map(put_sent_in_file, fnames)

if __name__ == "__main__":
    fnames = get_file_paths(bnc_dir, bnc_extension)
    #append_sentences_to_file(fnames, 'bnc.json')
    pool_handler(fnames)
    collect_json()
