import os

import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag

import bs4 as BeautifulSoup

from corpus_handlers import handler_helpers as hh

bnc_dir = 'corpora/2554/2554/download/Texts/'

if __name__ == "__main__":
    fnames = hh.get_file_paths(bnc_dir, '.xml')