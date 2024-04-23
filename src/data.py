import pandas as pd





def data(inp, data_column):
    for x in inp:
        __csv = read
        





# different csvs -> 
if __name__ == "__main__":
    inp = "./input/d/get-in-it_info.csv"
    inp = "./input/d/Stepstone_jobs.csv"

    d = pd.read_csv(inp, encoding = "ISO-8859-1")
    print(d.columns)
    d = d.iloc[:1][["Qualifikationen", "Aufgaben"]]
    print(d)