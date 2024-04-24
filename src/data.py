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
if __name__ == "__main__":
    inp1 = "./input/d/get-in-it_info.csv"
    inp2 = "./input/d/Stepstone_jobs.csv"

    d1 = pd.read_csv(inp1, encoding = "ISO-8859-1")
    d2 = pd.read_csv(inp2, encoding = "ISO-8859-1")
    print(d1.columns, d2.columns)
    
    #d = d.iloc[:1][["Qualifikationen", "Aufgaben"]]
    #print(d)

    print(pd.concat([d1, d2]).columns)