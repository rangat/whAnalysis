import os
import json

def get_file_paths(path:str, extension:str)->list:
    fnames = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if not f.endswith(extension):
                continue
            
            fnames.append(os.path.join(root, f))
    return fnames

def collect_json(directory:str, enddir:str):
    collected = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        
        if not filename.endswith(".json"):
            continue
        
        with open(f'{enddir}/{filename}') as json_data:
            data = json.load(json_data)
            collected.extend(data)

    with open(f"{enddir}.json", 'w') as outfile:
        json.dump(collected, outfile, indent=4)
        print("successfully made complete json")
    return True

def isWh(un_tagged)->str:
    from nltk import word_tokenize
    tagged = word_tokenize(un_tagged)
    tagged = [x.lower() for x in tagged]
    whs = set(['who', 'where', 'how'])

    return not whs.isdisjoint(set(tagged))