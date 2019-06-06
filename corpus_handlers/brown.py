import os
import sys
import json
from bs4 import BeautifulSoup

from multiprocessing import Pool

import nltk
from nltk import word_tokenize
from nltk import pos_tag
from nltk.tokenize.treebank import TreebankWordDetokenizer as Detok
detokenizer = Detok()

import collections

import handler_helpers as hh

brown_dir = 'corpora/brown_tei'
brown_extension = '.xml'

def extract_wh_sentences_from_file(file:str)->list:
    with open(file, 'r') as f:
        xml_content = f.read()
    soup = BeautifulSoup(xml_content, 'lxml')
    all_sents = list(map(lambda x: x.text, soup.find_all('s')))
    return list(filter(lambda x: hh.isWh(x), all_sents))

def put_sent_in_file(fname:str):
    sents = extract_wh_sentences_from_file(fname)
    jlist = list(map(lambda s: {'sentence':s, 'corpus':'brown', 'medium':'print'}, sents))    
    file = fname.split('/')[-1].split('.')[0]
    new_fname = f'brown/{file}.json'
    with open(new_fname, 'w') as j:
        json.dump(jlist, j)

def pool_handler(fnames:list):
    p = Pool(10)
    p.map(put_sent_in_file, fnames)

def get_modded_json(fname):
    jlist = []
    ret = []
    with open(fname, 'r') as j:
        jlist = json.load(j)
    
    for obj in jlist:
        sent = obj['sentence']
        sent = detokenizer.detokenize(word_tokenize(sent))
        ret.append({'sentence': sent, 'corpus': 'brown', 'medium': 'print'})
    return ret

def remove_dups(fname:str) -> list:
    compare = {}
    ret = []
    with open(fname, 'r') as j:
        jlist = json.load(j)
    print(len(jlist))
    for x in range(len(jlist)):
        sent = jlist[x]['sentence']
        if not sent in compare:
            compare[sent] = True
            ret.append(jlist[x])
        else:
            print(sent)
    print(len(ret))
    return ret

def remove_subsequent_dup(data) -> list:
    ret = []
    if type(data) == list:
        jlist = data
    else:
        with open(data, 'r') as j:
            jlist = json.load(j)
    print(len(jlist))

    last_obj = None
    for obj in jlist:
        if not obj == last_obj:
            ret.append(obj)
        last_obj = obj
    print(len(ret))
    return ret

if __name__ == "__main__":
    j = remove_subsequent_dup('unread_split/brown.json')

    with open('good_brown.json', 'w') as b:
        json.dump(j, b)

    # fnames = hh.get_file_paths(brown_dir, brown_extension)
    # pool_handler(fnames)
    # hh.collect_json('./brown', 'brown')