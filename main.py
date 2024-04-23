#import tm_lda
from argparse import ArgumentParser
from sys import exit
import os

import pandas as pd
import src.lda as lda
import src.nlp as nlp

def read(path):
    match(path.split(".")[-1]):
        case "csv":
            return pd.read_csv(path) #encoding = "ISO-8859-1"
        case "json":
            return pd.read_json(path)
        case _:
            return None



if __name__ == "__main__":

    #args
    arg_parser = ArgumentParser()

   # arg_parser.add_argument("--data_files", action="append", dest="input", default="")
    arg_parser.add_argument("--de", action="store_true", default=False)
    arg_parser.add_argument("--de_out", type=str, default="./output/topics_de.csv")
    arg_parser.add_argument("--en", action="store_true", default=False)
    arg_parser.add_argument("--en_out", type=str, default="./output/topics_en.csv")

    arg_parser.add_argument("--data", type=str, nargs=1, action="append", dest="inputs")
    arg_parser.add_argument("--datacolumn", type=str, nargs=2, action="append", dest="inputs")

    arg_parser.add_argument("--n_topics", type=int, dest="n", default=20)
    

    args = vars(arg_parser.parse_args())
    print(args)
    
    



    #run it, or not?
    if args["de"] == False and args["en"] == False:
        exit()

    if args["de"]:
        if os.exists(args["de_out"]):
            exit(str("file already exists:", args["de_out"]))
    
    if args["en"]:
        if os.exists(args["en_out"]):
            exit(str("file already exists:", args["en_out"]))
    

    #get data(frame)
    print("loading data...")

    data = []

    for x in args["inputs"]:
        
        if os.path.exists(x[0]) and type(_d := read(x[0])) != type(None):
            if len(x) == 2:
                _d = _d[[x[1]]]
            _d = _d.stack().reset_index()[0]
            data.append(_d)

        else:
            exit( str("couldn't read file '", x, "'") )

    data = pd.DataFrame({"text": pd.concat(data)}).iloc[:2]

    print("...done!")
    
    


    #textdata preprocessing
    print("preparing textdata...")

    detector = nlp.load_langdetector()
    de_pipeline = nlp.load_langpipeline("de")
    en_pipeline = nlp.load_langpipeline("en")


    data["Language"] = data["text"].apply(nlp.language, args=(detector,))

    data["text"] = data["text"].apply(nlp.normalize)
    if args["de"]:
        data_de = data[ data["Language"] == nlp.Language.GERMAN ]
        data_de["text"] = data_de["text"].apply(nlp.preprocess, args=(de_pipeline,))
    if args["en"]:
        data_en = data[ data["Language"] == nlp.Language.ENGLISH ]
        data_en["text"] = data_en["text"].apply(nlp.preprocess, args=(en_pipeline,))
    #data["text"] = data["text"].apply(lambda x : [ nlp.normalize(token) for token in x] ) 

    print("...done!")




    #lda
    print("applying lda...")
    if args["de"]:
        print("..for de..")
        outs_de = lda.lda_range(data_de["text"], 10, 100, 5)
    if args["en"]:
        print("..for en..")
        outs_en = lda.lda_range(data_en["text"], 10, 100, 5)


    
    print("done!")

    