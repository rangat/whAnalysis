modals = ['can', 'could', 'may', 'might', 'shall', 'should', 'will', 'would', 'must']

def getWh(tagged)->str:
    for tag in tagged:
        if 'who' in tag[0].lower():
            return 'who'
        elif 'where'in tag[0].lower():
            return 'where'
        elif 'how' in tag[0].lower():
            return 'how'
    return None

def start_to_wh(tagged, wh):
    ret = []

    for t in tagged:
        ret.append(t)
        if t[0].lower() == wh.lower():
            break
    return ret

def x_in_set(x, pos_set:list, is_pos=True):
    for pair in pos_set:
        word = pair[0].lower()
        pos = pair[1].lower()

        if type(x) == list:
            for item in x:
                if is_pos and pos[0] == item[0].lower():
                    return True
                elif not is_pos and word == item.lower():
                    return True
        else:
            if is_pos and pos[0]== x[0].lower():
                return True
            elif not is_pos and word == x.lower():
                return True
    return False

def is_sub_aux_inv(tagged:list, wh:str, aux:list, y:list) -> bool:
    rel_clause_heur = ['NN', 'NNS', 'NNP', 'NNPS', 'DT', 'JJ', 'PDT', 'POS', 'PRP', 'PRP$', 'CD']

    hit_wh = False
    hit_aux = False
    hit_y = False

    for word, pos in tagged:
        if word in wh:
            hit_wh = True
        elif hit_wh and pos in rel_clause_heur and not hit_aux:
            return False
        elif hit_wh and word in aux:
            hit_aux = True
        elif hit_wh and hit_aux and 'V' in pos:
            return False
        elif hit_wh and hit_aux and pos in y:
            hit_y = True
    
    if hit_wh and hit_aux and hit_y:
        return True
    return False

def rel_clause_seq(start_wh:list, rel_clause) -> bool:
    hit_v = False
    hit_rel = False

    for word, pos in start_wh:
        if 'V' in pos:
            hit_v = True
        elif hit_v and pos in rel_clause:
            hit_rel = True
    
    if hit_v and hit_rel:
        return True

    return False

def emb_seq(start_wh:list, rel_clause) -> bool:
    hit_rel = False
    hit_v = False
    hit_rel_after_v = False

    for word, pos in start_wh:
        if pos in rel_clause: # Has hit the relative clause
            hit_rel = True
        elif hit_rel and 'V' in pos:
            hit_v = True
        if hit_rel and hit_v and pos in rel_clause:
            hit_rel_after_v = True
        
    if hit_v and hit_rel and not hit_rel_after_v:
        
        return True

    return False

def collect_json(directory:str, endfname:str):
    import os
    import json

    collected = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        
        if not filename.endswith(".json"):
            continue
        
        with open(f'{directory}/{filename}') as json_data:
            data = json.load(json_data)
            collected.extend(data)

    with open(f"{endfname}.json", 'w') as outfile:
        json.dump(collected, outfile, indent=4)
        print("successfully made complete json")
    return True

def get_v_before_wh(tagged:list, wh:str) -> str:
    hit_wh = False
    t = tagged[::-1]
    for word,pos in t:
        if word.lower() == wh.lower():
            hit_wh = True
        elif ('V' in pos[0] or "MD" in pos) and hit_wh:
            return word
    return ""
        
def get_three_v_after_wh(tagged:list, wh:str) -> str:
    hit_wh = False
    hit_v1 = False
    hit_v2 = False
    verb1 = ""
    verb2 = ""
    verb3 = ""
    for word, pos in tagged:
        if word.lower() == wh.lower():
            hit_wh = True
        elif ('V' in pos[0] or "MD" in pos) and hit_wh:
            hit_wh = False
            hit_v1 = True
            verb1 = word
        elif ('V' in pos[0] or "MD" in pos) and hit_v1:
            hit_v1 = False
            hit_v2 = True
            verb2 = word
        elif ('V' in pos[0] or "MD" in pos) and hit_v2: 
            hit_v2 = False
            verb3 = word
    
    return verb1, verb2, verb3

def get_set_wh_v1(tagged_sent:list, wh:str):
    get = False
    ret_list = []

    for word, pos in tagged_sent:
        if wh.lower() == word.lower():
            get = True
        
        if get:
            tup = (word, pos)
            ret_list.append(tup)
        
        if ("V" in pos[0] or "MD" in pos) and get:
            break

    return ret_list

def modded_lemma(verb:str):
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer() 

    if not verb:
        return None
    if verb.endswith((".", "?", "-", "!")):
        verb = verb[:-1]
        
    if verb in ["'re", "'m"]:
        return "be"
    else:
        return lemmatizer.lemmatize(verb, "v")

if __name__ == '__main__':
    # import nltk
    # from nltk import word_tokenize
    # from nltk import pos_tag
    # sent = 'how can I get'
    # lowered_pos = [(x[0].lower(), x[1]) for x in pos_tag(word_tokenize(sent))]
    collect_json('unread_split', 'corpus')
