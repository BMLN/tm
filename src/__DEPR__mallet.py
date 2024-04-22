#DEPRECATED

import urllib.request
import zipfile
import os
from sys import exit


from gensim.models.wrappers import LdaMallet




def fetch_mallet(src, dest):
    urllib.request.urlretrieve(src, dest + ".zip")
    with zipfile.ZipFile(dest + ".zip", "r") as zip_ref:
        zip_ref.extractall(dest)

def load_mallet(src, corpus, num_topics, id2word):
    return LdaMallet(src, corpus, num_topics, id2word)



    


if __name__ == "__main__":
    vars = ["MALLET_SRC", "MALLET_DEST"]

    for x in vars:
        if os.environ.get(x) is None:
            exit(str("Define all params to run: " + "[" + str(vars) + "]"))

    if os.path.exists(os.environ["MALLET_SRC"]) == False:
        fetch_mallet(os.environ["MALLET_SRC"], os.environ["MALLET_DEST"])
    
    load_mallet(os.environ["MALLET_SRC"])