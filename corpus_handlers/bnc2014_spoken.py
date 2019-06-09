import os
import sys
import json
from bs4 import BeautifulSoup

from multiprocessing import Pool

import nltk
from nltk import word_tokenize
from nltk import pos_tag

import handler_helpers as hh

bnc_spoken_dir = 'corpora/bnc2014spoken-xml/spoken/untagged'
bnc_extension = ".xml"

def extract_wh_sentences_from_file(file:str)->list:
    with open(file, 'r') as f:
        xml_content = f.read()
    soup = BeautifulSoup(xml_content, 'lxml')
    all_sents = list(map(lambda x: x.text, soup.find_all('u')))
    return list(filter(lambda x: hh.isWh(x), all_sents))

def put_sent_in_file(fname:str):
    sents = extract_wh_sentences_from_file(fname)
    jlist = list(map(lambda s: {'sentence':s, 'corpus':'bnc', 'medium':'spoken'}, sents))    
    file = fname.split('/')[-1].split('.')[0]
    new_fname = f'bnc_spoken/{file}.json'
    with open(new_fname, 'w') as j:
        json.dump(jlist, j)

def pool_handler(fnames:list):
    p = Pool(10)
    p.map(put_sent_in_file, fnames)

if __name__ == "__main__":
    fnames = hh.get_file_paths(bnc_spoken_dir, bnc_extension)
    pool_handler(fnames)
    hh.collect_json('./bnc_spoken', 'bnc_spoken')