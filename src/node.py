from parsel import Selector
import pandas as pd
from argparse import ArgumentParser





searchtags_de = [ ["Aufgabe", "Anforderung", ], [], []]






def uls(node_text):
    output = []
    #__inp = node_text.replace("<br>", "")
    selector = Selector(text=node_text)
    
    return selector.xpath("//ul").getall()


#TODO: invert for speedup
def max__indices(list, match_list):
    matches = [ i for i, x in enumerate(list) if any((_x in x) for _x in match_list) ] #[ (i, x) for i, x in enumerate(list) if x in match_list ]
    if len(matches) == 0:
        return -1
    else:
        return max(matches)
        #return max(matches, key=lambda x: x[0])


def occ(list, elem):
    out = len(list)
    for i, x in enumerate(list):
        if x == elem:
            return i
    return out



def group_ranges(node_text, search_list=None):
    selector = Selector(text=node_text)
    print(selector.xpath(".//h4/text()").getall()) #listings
    # for x in selector.xpath(".//ul"):
    #     print(x.xpath(".//preceding::*//child::*/text()").getall())
    #     break

def taskestest(node_text, n=5, search_list=[["Aufgabe"], ["Profil"], []]):
    input = search_list
    output = { i: [] for i in range(len(input))}
    out_i = 0

    selector = Selector(text=node_text).xpath(".//ul")
    

    for listings in selector:
        list_elems = [ x for x in listings.xpath(".//text()").getall() if len(x) > 5 ]#potential data
        preceeding_text = listings.xpath(".//preceding::*//text()").getall()
        end = occ(preceeding_text, list_elems[0])
        preceeding_text = preceeding_text[:end]


        print("-------------------")
        print(list_elems)
        print(preceeding_text)


        matches = { i: max__indices(preceeding_text, x) for i, x in enumerate(input) }
        print(matches)
        match = max(matches.items(), key=lambda x : x[1])
        if match[1] != -1:
            #if (len(preceeding_text) - 1 - match[1]) < n: #and out_i <= match[0] + 1:
            if True:
                print("adds", match[0])
                output[match[0]].extend(list_elems)
                input[match[0]].append(list_elems[-1])
                out_i = match[0]
            else:
                if len(output[out_i]) == 0:
                    print("hmm")
        

    print(output)


def tasks(node_text, n=5):
    __s = Selector(text=node_text)
    __s = __s.xpath(".//ul")
    #print(__s)

    for x in __s:
        print("-------------------")
        print(x.xpath(".//text()").getall())
        print(x.xpath(".//preceding::*//text()").getall())
        #__s = __s.xpath(".//ul//preceding::*")
        #print(__s.getall())
    #return __s.xpath("//ul//preceding::*").get()






def stepstone(text_node):
    selector = Selector(text=text_node)

    tasks = selector.xpath(".//div[@data-at='section-text-description-content']//ul")
    tasks = [ [_x for _x in x.xpath(".//text()").getall() if len(_x) > 5] for x in tasks ]
    tasks = [ item for list_list in tasks for item in list_list ]

    quals = selector.xpath(".//div[@data-at='section-text-profile']//ul")
    quals = [ [_x for _x in x.xpath(".//text()").getall() if len(_x) > 5] for x in quals ]
    quals = [ item for list_list in quals for item in list_list ]


    return tasks, quals



#not rly robust
def indeed(text_node):
    tasks = []
    quals = []

    selector = Selector(text=text_node)

    potentials_headlines = selector.xpath(".//b//text()").getall()
    potentials_headlines = [ x for x in potentials_headlines if len(x) > 5 ] 

    #print(potentials_headlines)
    selector = selector.xpath(".//ul")

    for listing in selector:
        list_elems = [ x for x in listing.xpath(".//text()").getall() if len(x) > 5 ]#potential data
        #print(list_elems)
        preceeding_text = " ".join(listing.xpath(".//preceding::*//text()").getall())
        matches = { i: preceeding_text.rfind(x) for i, x in enumerate(potentials_headlines) }
        #print(matches)
        match = max(matches.items(), key=lambda x : x[1])
        if match[1] != -1:
            if match[0] == 0:
                tasks.extend(list_elems)
            elif match[0] == 1:
                quals.extend(list_elems)

    return tasks, quals



if __name__ == "__main__":
    # inp =   r"C:\Users\Lorand\Documents\Arbeit\april - 2024\tm\input\stepstone_job.html"
    # with open(inp, "r") as file:
    #     texts = file.read()
    #     __sel = Selector(text=str(texts)).xpath("//div[@data-atx-component='JobAdContent']").get()
    #data = pd.DataFrame({"job_node": [__sel]})


    arg_parser = ArgumentParser()

    arg_parser.add_argument("--data", type=str)
    arg_parser.add_argument("--column", type=str)
    arg_parser.add_argument("--use_indeed", action="store_true", default=False)
    arg_parser.add_argument("--use_stepstone", action="store_true", default=True)
    arg_parser.add_argument("--out", default="./output/noded.csv")

    args = vars(arg_parser.parse_args())
    

    data = pd.read_csv(args["data"])

    if args["use_indeed"]:
        print("using indeed processing...")
        processings = data[args["column"]].apply(indeed)

    else:
        print("using stepstone processing...")
        processings = data[args["column"]].apply(stepstone)
    
    data["Tasks"] = processings.apply(lambda x: x[0])
    data["Qualifications"] = processings.apply(lambda x: x[1])
    data.to_csv(args["out"])

