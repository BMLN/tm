import pandas as pd

from gensim.models import LdaModel, CoherenceModel
from gensim.corpora import Dictionary

import data
from argparse import ArgumentParser





#all of LDA working on !tokens!


#lda preprocess

#TODO: filter
def lda_dict(data, filter=None):
    """
        data: df.Series of list of tokens 

        returns a gensim Dictionary containing the token types
    """
    return  Dictionary(data)


def lda_bow(data, dictionary):
    """
        data: pd.Series of tokens

        returns bag of words representation for each element in the pd.Series
    """
    return data.apply(lambda x: dictionary.doc2bow(x))


#model

def lda(bow, dict, n_topics):
    """
        trains and returns LdaModel
    """
    return LdaModel(
        bow,
        num_topics=n_topics,
        id2word=dict,
        #alpha=,
        #eta=
    )


def lda_from(path):
    return LdaModel.load(path)




#may include roundi9nsg
def lda_topic_distributions(model ,data):
    __dict = lda_dict(data)
    __bow = lda_bow(data, __dict)
    topics = model.get_document_topics(__bow, minimum_probability=0.0)
    topic_ids = [ x[0] for x in topics ] if len(topics) > 0 else []
    #print(topics)
    #print(topic_ids)
    #import numpy as np
    #print(np.shape(topics))

    topics = pd.DataFrame(topics).apply(lambda x : x.apply(lambda y: y[1]))
    #print(topics.T)
    return topics


def lda_topics(model, data, n_top=10):
    __dict = lda_dict(data)
    __data = lda_bow(data, __dict)
    topics = model.get_document_topics(__data)
    topic_names = model.show_topics(num_topics= len(model.get_topics()), formatted=False)
    topic_names = [ [ xx[0] for xx in x[1] ] for x in topic_names ]
    #top_topics = mopel.top_to
    topics = pd.Series(topics)
    topics = topics.apply(lambda x : max(x, key=lambda item: item[1])[0])
    topics = topics.apply(lambda x : topic_names[x])

    return topics


def lda_coherence(model, data, dict):
    return CoherenceModel(model, texts=data, dictionary=dict, coherence="c_v" )


def lda_range(data, start, end, step):
    output = []

    __dict = lda_dict(data)
    __bow = lda_bow(data, __dict)

    for x in range(start, end, step):
        print("...", x)
        __model = lda(__bow, __dict, x)
        __coherence = lda_coherence(__model, data, __dict).get_coherence()

        #print(__coherence.get_coherence()) if new best
        if len(output) > 0 and __coherence > max([_x[1] for _x in output]):
            print("n_topic=" + str(x), " improved the score to", __coherence )  
        output.append((__model, __coherence, x))
  

    return output



if __name__ == "__main__":
    

    #args
    arg_parser = ArgumentParser()

    arg_parser.add_argument("--data", type=str)
    arg_parser.add_argument("--column", type=str)
    arg_parser.add_argument("--benchmarks", type=str, default=None)
    arg_parser.add_argument("--model", type=str, default=None)

    arg_parser.add_argument("--ntopics_from", type=int, default=10)
    arg_parser.add_argument("--ntopics_to", type=int, default=315)
    arg_parser.add_argument("--ntopics_stepsize", type=int, default=5)


    args = vars(arg_parser.parse_args())

    import ast
    data = pd.read_csv(args["data"])[args["column"]].apply(ast.literal_eval)
    start, stop, step = args["ntopics_from"], args["ntopics_to"], args["ntopics_stepsize"]


    print("applying lda...")

    print(data)
    outs = lda_range(data, start, stop, step)
    #model_de = max(outs_de, key=lambda x : x[1])[0]
    if args["benchmarks"] != None:
        benchmarks = {
            "n" : [ x[2] for x in outs ],
            "coherence" : [ x[1] for x in outs ]
        }
        pd.DataFrame(benchmarks).to_csv(args["benchmarks"])

    print("done!")

    if args["model"] != None:
        max(outs, key=lambda x : x[1])[0].save(args["model"])
    