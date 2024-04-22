#import tm_lda
from argparse import ArgumentParser
from pandas import read_csv, read_json
from sys import exit

from src import tm_lda


def read(path):
    match(path.split(".")[-1]):
        case "csv":
            return read_csv(path)
        case "json":
            return read_json(path)
        case _:
            return None



if __name__ == "__main__":

    #args
    arg_parser = ArgumentParser()

    arg_parser.add_argument("--data_file", type=str, dest="input", default="")
    arg_parser.add_argument("--data_column", type=str, dest="column", default="")

    arg_parser.add_argument("--n_topics", type=int, dest="n", default=20)


    args = vars(arg_parser.parse_args())

    print(args)
    


    #check conf
    if type(data := read(args["input"])) == type(None):
        exit("no valid data provided")

    if ((column := args["column"]) in data) == False:
        exit("no valid data column provided")



    #run 
    #out2 = tm_lda.lda_apply(data, incl_topics=False)
    #print(out2)



    