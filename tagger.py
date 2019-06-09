import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag

import json
import sys
import os
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

    obj['questType'] = ""
    obj['heuristic'] = ""

    # Tag Question Type: 
    if not h.x_in_set("V", tagged, is_pos=True):
        obj['questType'] = "Fragment"
        obj['heuristic'] = 'frag'
    
    # Strict Embedded Heuristic
    elif h.emb_seq(start_wh, rel_clause_heur):
        obj['questType'] = "Embedded Question"
        obj['heuristic'] = 'strict_emb'
    
    # Strict Relative Clause Heuristic
    elif h.rel_clause_seq(start_wh, rel_clause_heur):
        obj['questType'] = "Relative Clause"
        obj['heuristic'] = 'strict_rel'

    # Loose Relative Clause Heuristic
    elif h.x_in_set(rel_clause_heur, start_wh, is_pos=True):
        obj['questType'] = "Relative Clause"
        obj['heuristic'] = 'rel_clause'

    # Strict Root Question Heuristic
    elif h.is_sub_aux_inv(lowered_pos, obj['wh'], aux, rel_clause_heur):
        obj['questType'] = "Root Question"
        obj['heuristic'] = 'sub_aux_inv'

    # Loose Root Question Heuristic
    elif "?" in lowered_pos[-1][0]:
        obj['questType'] = "Root Question"
        obj['heuristic'] = '?'
    
    # Loose Embedded Question Heuristic
    elif h.x_in_set("V", start_wh, is_pos=True):
        obj['questType'] = "Embedded Question"
        obj['heuristic'] = 'v_before_wh'
    
    else:
        obj['questType'] = "Ambiguous"
        obj['heuristic'] = 'amb'
    
    
    # Second pass:
    if obj['heuristic'] == 'rel_clause':
        if h.x_in_set("V", start_wh, is_pos=True) and not h.is_sub_aux_inv(lowered_pos, obj['wh'], aux, rel_clause_heur):
            obj['questType'] = "Embedded Question"
            obj['heuristic'] = 'second_pass'

    v_before_wh = h.get_v_before_wh(tagged, obj['wh'])
    v_1_after, v_2_after, v_3_after = h.get_three_v_after_wh(tagged, obj['wh'])
    wh_v1 = h.get_set_wh_v1(tagged, obj['wh'])

    obj['v_before'] = v_before_wh
    obj['v1_after'] = v_1_after
    obj['v2_after'] = v_2_after
    obj['v3_after'] = v_3_after
    obj['wh_v1'] = wh_v1

    obj['mat_verb'] = h.modded_lemma(v_before_wh)
    obj['emb_verb'] = h.modded_lemma(v_1_after)
    modals = ['can', 'could', 'may', 'might', 'shall', 'should', 'will', 'would', 'must']
    
    # Tag Clause Type:
    if v_1_after.lower() in modals:
            obj['clauseType'] = "Modal"
    elif h.x_in_set('to', wh_v1, is_pos=False) and obj['questType'] != "Root Question":
        obj['clauseType'] = "Non-Finite"
    else:
        obj['clauseType'] = "Finite"

    return obj

def tagList(json:list):
    ret = []
    for obj in json:
        ret.append(tagObj(obj))
    return json

def pool_tag(jlist):
    p = Pool()
    return p.map(tagObj, jlist)

def multi_run():
    jList = []
    with open('unread/corpus.json', 'r') as j:
        jList = json.load(j)
    
    tagged = pool_tag(jList)
    # Remove None objects in list
    tagged = [x for x in tagged if x is not None]
    with open('edited/edited_corpus.json', 'w') as j:
        json.dump(tagged, j, indent=4)

if __name__ == '__main__':
    filepath = sys.argv[1]
    filename = os.path.basename(filepath)
    jList = []
    with open(filepath, 'r') as j:
        jList = json.load(j)
    
    tagged = pool_tag(jList)
    # Remove None objects in list
    tagged = [x for x in tagged if x is not None]

    end_filename = f'tagged_{filename}'
    with open(end_filename, 'w') as j:
        json.dump(tagged, j, indent=4)
    
    print(f"Successfully tagged {filename} and created {end_filename}")