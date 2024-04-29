import pandas as pd
import data
from argparse import ArgumentParser

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

#TODO: check why mwd needs extra filter
def preprocess(text_string, nlp_pipeline):
    return [ token.lemma_ for token in nlp_pipeline(text_string) if token.is_stop == False and token.is_alpha == True and token.pos_ in ACCEPTED_POS and token.lemma_ != "mwd"]





if __name__ == "__main__":


    #args
    arg_parser = ArgumentParser()

    arg_parser.add_argument("--data", type=str, nargs="*", action="append", dest="inputs")

    arg_parser.add_argument("--de", action="store_true", default=False)
    arg_parser.add_argument("--de_out", type=str, default="./output/output_de.csv")
    arg_parser.add_argument("--en", action="store_true", default=False)
    arg_parser.add_argument("--en_out", type=str, default="./output/output_en.csv")

    
    args = vars(arg_parser.parse_args())

    


    
    print("loading data...")

    data = data.data(args["inputs"])
    
    print("...done!")
    

    #data
    #textdata preprocessing
    print("preparing textdata...")

    detector = load_langdetector()
    de_pipeline = load_langpipeline("de")
    en_pipeline = load_langpipeline("en")


    data["language"] = data["textdata"].apply(language, args=(detector,))

    data["textdata"] = data["textdata"].apply(normalize)
    
    if args["de"]:
        data_de = data[ data["language"] == Language.GERMAN ]
        data_de["textdata"] = data_de["textdata"].apply(preprocess, args=(de_pipeline,))

    if args["en"]:
        data_en = data[ data["language"] == Language.ENGLISH ]
        data_en["textdata"] = data_en["textdata"].apply(preprocess, args=(en_pipeline,))
    #data["text"] = data["text"].apply(lambda x : [ nlp.normalize(token) for token in x] ) 

    print("...done!")


    print("saving...")
    if args["de"]:
        data_de.to_csv(args["de_out"])

    if args["en"]:
        data_en.to_csv(args["en_out"])