import pandas as pd


from langdetect import detect as detect_language

from spacy.lang.de import German
from spacy.lang.en import English
from spacy.pipeline import Sentencizer




#text_string -> ||| normalize -> lemmatize -> tokenize ||| -> processed_text (prepared tokens)
english = English()
german = German()


def normalize(text):
    keep = [".", ",", "!", "?", " "]
    replace = {"&": "und", "-": " "}

    out = ""
    for char in text:
        _c = str(char)
        if _c in replace.keys():
            out += replace[_c]
        if _c.isalnum() or _c in keep:
            out += _c
    #cleanString = re.sub('\W+|r"s"',' ', text )
    out = out.replace("  ", " ")

    return out



def tokenize(text_string, language="de"):
    __l_p = german if language == "de" else english

    return [ token.text for token in __l_p(text_string) ]

def tokenize_and_filterstopwords(text_string, language="de"):
    __l_p = german if language == "de" else english

    return [ token.text for token in __l_p(text_string) if token.is_stop == False ]


#TODO: is bullshit
def filterstopwords(tokens, language="de"):
    __l_p = german if language == "de" else english

    return [ token.text for token in __l_p(tokens) if token.is_stop == False ]



#only necessary

def preprocess(text_string, language="de"):
    __l_p = german if language == "de" else english

    return [ token.lemma for token in __l_p(text_string) if token.is_stop == False ]

