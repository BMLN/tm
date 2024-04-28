from argparse import ArgumentParser
import pandas as pd




def read(path):
    match(path.split(".")[-1]):
        case "csv":
            return pd.read_csv(path)#, encoding = "ISO-8859-1")
        case "json":
            return pd.read_json(path)
        case _:
            return None
        

def data(input):
    data = []

    for x in input:
        
        if type(__csv := read(x[0])) == None:
            print("a file couldn't be read! -", x[0])
            
        else:
            #text == all columns
            if len(x) == 0:
                columns = __csv.columns    
            else:
                columns = x[1:]
            #text == the passed columns
            __csv["textdata"] = __csv[columns].agg(" ".join, axis=1)
            data.append(__csv)

    return pd.concat(data).reset_index()




# different csvs -> 
#TODO
if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--data", type=str, nargs="*", action="append", dest="inputs")
    arg_parser.add_argument("--output", type=str, default="./output/combined.csv")
    
    args = vars(arg_parser.parse_args())

    print(args)
    output = data(args["inputs"])
    output.to_csv(args["output"])