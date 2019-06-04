import os

import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag

import bs4 as BeautifulSoup

bnc_dir = 'corpora/2554/2554/download/Texts/'

def get_file_paths(path:str, extension:str)->list:
    fnames = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if not f.endswith(extension):
                continue
            
            fnames.append(os.path.join(root, f))
    return fnames

fnames = get_file_paths(bnc_dir, '.xml')
print(len(fnames))