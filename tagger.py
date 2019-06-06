import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag

import json

import helper as h

from multiprocessing import Pool


aux = ['did', 'do', 'does', 'am', 'is', 'are', 'was', 'were', 'have', 'has', 'had', "'d", "'s", "'re", 'can', 'could', 'shall', 'should', 'may', 'might', 'must', 'will', 'would']
rel_clause_heur = ['NN', 'NNS', 'NNP', 'NNPS', 'DT', 'JJ', 'PDT', 'POS', 'PRP', 'PRP$', 'CD']

def tagObj(obj):
    sent = obj["sentence"]
    
    obj['clauseType'] = None
    obj['phrase'] = ''
    obj['wh'] = None

    tagged = pos_tag(word_tokenize(sent))
    lowered_pos = [(x[0].lower(), x[1]) for x in tagged]
    obj['wh'] = h.getWh(tagged)
    
    if not obj['wh']:
        return None

    start_wh = h.start_to_wh(lowered_pos, obj['wh'])

    # Tag Question Type: 
    if not h.x_in_set("V", tagged, is_pos=True):
        obj['questType'] = "Fragment"
    
    # Exclusive Relative Clause Heuristic
    elif h.rel_clause_seq(start_wh, rel_clause_heur):
        obj['questType'] = "Relative Clause"
    
    # Exclusive Root Question Heuristic
    elif h.is_sub_aux_inv(lowered_pos, obj['wh'], aux, rel_clause_heur):
        obj['questType'] = "Root Question"

    # Inclusive Root Question Heuristic
    elif "?" in lowered_pos[-1][0]:
        obj['questType'] = "Root Question"
    
    # Inclusive Embeded Question Heuristic
    elif h.x_in_set("V", start_wh, is_pos=True):
        obj['questType'] = "Embeded Question"
    
    # Inclusive Relative Clause Heuristic
    elif h.x_in_set(rel_clause_heur, start_wh, is_pos=True):
        obj['questType'] = "Relative Clause"
    
    else:
        obj['questType'] = "Ambiguous"

    # Tag Clause Type:
    obj['clauseType'] = "null"

    return obj

def tagList(json:list):
    ret = []
    for obj in json:
        ret.append(tagObj(obj))
    return json

def pool_tag(jlist):
    p = Pool()
    return p.map(tagObj, jlist)

if __name__ == '__main__':
    jList = []
    with open('unread/corpus.json', 'r') as j:
        jList = json.load(j)
    
    tagged = pool_tag(jList)
    with open('edited/edited_corpus_2.json', 'w') as j:
        json.dump(tagged, j, indent=4)