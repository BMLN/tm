import pandas as pd


#from langdetect import detect as detect_language
from lingua import Language, LanguageDetectorBuilder
languages = [ Language.ENGLISH, Language.GERMAN ]


from spacy_download import load_spacy
#from spacy import load
#no lemmatizer incl?
#from spacy.lang.de import German
#from spacy.lang.en import English
from spacy.pipeline import Sentencizer




ACCEPTED_POS = ["PROPN", "NOUN", "ADJ" , "VERB" ]#, "ADV", "ADP"]


#text_string -> ||| normalize -> lemmatize -> tokenize ||| -> processed_text (prepared tokens)


#necessities
def load_langdetector():
    return LanguageDetectorBuilder.from_languages(*languages).build() 


def load_langpipeline(language="de"):
    if language == "de":
        return load_spacy("de_core_news_sm")
    if language == "en":
        return load_spacy("en_core_web_sm")
    


#text processing

def normalize(text_string):
    keep = [".", ",", "!", "?", " "]
    #replace = {"&": "und", "-": " "}
    replace = {"-": " "}

    out = ""
    for char in text_string:
        _c = str(char)
        if _c in replace.keys():
            out += replace[_c]
        if _c.isalnum() or _c in keep:
            out += _c
    #cleanString = re.sub('\W+|r"s"',' ', text )
    out = out.replace("  ", " ")

    return out


def language(text_string, detector):
    return detector.detect_language_of(text_string)



# def tokenize(text_string, language="de"):
#     __l_p = german if language == "de" else english

#     return [ token.text for token in __l_p(text_string) ]

# def tokenize_and_filterstopwords(text_string, language="de"):
#     __l_p = german if language == "de" else english

#     return [ token.text for token in __l_p(text_string) if token.is_stop == False ]


# #TODO: is bullshit
# def filterstopwords(tokens, language="de"):
#     __l_p = german if language == "de" else english

#     return [ token.text for token in __l_p(tokens) if token.is_stop == False ]



#only necessary

def preprocess(text_string, nlp_pipeline):
    return [ token.lemma_ for token in nlp_pipeline(text_string) if token.is_stop == False and token.is_alpha == True and token.pos_ in ACCEPTED_POS ]





if __name__ == "__main__":
    inp = "./input/stepstone_info.csv"
    data = pd.read_csv(inp)
    data["textdata"] = data["raw_text"]

    detector = load_langdetector()
    de_pipeline = load_langpipeline("de")


    data["language"] = data["textdata"].apply(language, args=(detector,))

    data["textdata"] = data["textdata"].apply(normalize)

    data_de = data[ data["language"] == Language.GERMAN ]
    data_de["textdata"] = data_de["textdata"].apply(preprocess, args=(de_pipeline,))

    
    print(data_de["textdata"][0])