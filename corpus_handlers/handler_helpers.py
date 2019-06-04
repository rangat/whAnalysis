def get_file_paths(path:str, extension:str)->list:
    import os
    
    fnames = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if not f.endswith(extension):
                continue
            
            fnames.append(os.path.join(root, f))
    return fnames