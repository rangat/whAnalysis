import json

def get_modded_json(fname):
    jlist = []
    ret = []
    with open(fname, 'r') as j:
        jlist = json.load(j)
    
    for obj in jlist:
        ret.append({'sentence': obj['sentence'], 'corpus': 'reuters', 'medium': 'print'})
    return ret

if __name__ == "__main__":
    j = get_modded_json('corpora/reuters_data_ALL.json')

    with open('reuters.json', 'w') as b:
        json.dump(j, b)