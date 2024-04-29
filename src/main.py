#import tm_lda
from argparse import ArgumentParser
from sys import exit
import os

import pandas as pd
import lda
import nlp
import data

def read(path):
    match(path.split(".")[-1]):
        case "csv":
            return pd.read_csv(path, encoding = "ISO-8859-1")
        case "json":
            return pd.read_json(path)
        case _:
            return None



if __name__ == "__main__":

    #args
    arg_parser = ArgumentParser()

   # arg_parser.add_argument("--data_files", action="append", dest="input", default="")
    arg_parser.add_argument("--data", type=str, nargs="*", action="append", dest="inputs")
    #arg_parser.add_argument("--datacolumn", type=str, nargs=2, action="append", dest="inputs")

    arg_parser.add_argument("--n_topics", type=int, dest="n", default=20)


    arg_parser.add_argument("--de", action="store_true", default=False)
    arg_parser.add_argument("--de_out", type=str, default="./output/output_de.csv")
    arg_parser.add_argument("--en", action="store_true", default=False)
    arg_parser.add_argument("--en_out", type=str, default="./output/output_en.csv")

    arg_parser.add_argument("--model", action="store_true", default=False)
    arg_parser.add_argument("--model_out_en", type=str, default="./output/model_en") #change to only these with nargs 0 for default or 1 with set
    arg_parser.add_argument("--model_out_de", type=str, default="./output/model_de")

    

    args = vars(arg_parser.parse_args())

    



    #run it, or not?
    if args["de"] == False and args["en"] == False:
        exit()

    if args["de"]:
        if os.path.exists(args["de_out"]):
            exit(str("file already exists: " + args["de_out"]))
    
    if args["en"]:
        if os.path.exists(args["en_out"]):
            exit(str("file already exists: " + args["en_out"]))
    

    #get data(frame)
    print("loading data...")

    data = data.data(args["inputs"])

    # data = []

    # for x in args["inputs"]:
        
    #     if os.path.exists(x[0]) and type(_d := read(x[0])) != type(None):
    #         if len(x) == 2:
    #             _d = _d[[x[1]]]
    #         _d = _d.stack().reset_index()[0]
    #         data.append(_d)

    #     else:
    #         exit( str("couldn't read file '", x, "'") )

    # data = pd.DataFrame({"text": pd.concat(data)})
    
    print("...done!")
    

    #data
    #textdata preprocessing
    print("preparing textdata...")

    detector = nlp.load_langdetector()
    de_pipeline = nlp.load_langpipeline("de")
    en_pipeline = nlp.load_langpipeline("en")


    data["language"] = data["textdata"].apply(nlp.language, args=(detector,))

    data["textdata"] = data["textdata"].apply(nlp.normalize)
    if args["de"]:
        data_de = data[ data["language"] == nlp.Language.GERMAN ]
        data_de["textdata"] = data_de["textdata"].apply(nlp.preprocess, args=(de_pipeline,))
    if args["en"]:
        data_en = data[ data["language"] == nlp.Language.ENGLISH ]
        data_en["textdata"] = data_en["textdata"].apply(nlp.preprocess, args=(en_pipeline,))
    #data["text"] = data["text"].apply(lambda x : [ nlp.normalize(token) for token in x] ) 

    print("...done!")


    #training
    exit()
    print("applying lda...")

    if args["de"]:
        print("..for de..")
        outs_de = lda.lda_range(data_de["textdata"], 5, 20, 5)
        model_de = max(outs_de, key=lambda x : x[1])[0]
    if args["en"]:
        print("..for en..")
        outs_en = lda.lda_range(data_en["textdata"], 5, 20, 5)
        model_en = max(outs_en, key=lambda x : x[1])[0]

    print("done!")

    
    #save csv + model if param

    if args["de"]:
        data_de["topics"] = lda.lda_topics(model= model_de,data=data_de["textdata"]) 
        data_de.drop(["textdata", "language"], axis=1).to_csv(args["de_out"])

    if args["en"]:
        data_en["topics"] = lda.lda_topics(model= model_en,data=data_en["textdata"])
        data_en.drop(["textdata", "language"], axis=1).to_csv(args["en_out"])


    if args["model"]:
        if args["de"]:
            model_de.save(args["model_out_de"])
        if args["en"]:
            model_en.save(args["model_out_en"])

