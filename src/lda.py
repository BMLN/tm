import pandas as pd

from gensim.models import LdaModel, CoherenceModel
from gensim.corpora import Dictionary






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


def lda_coherence(model, data, dict):
    return CoherenceModel(model, texts=data, dictionary=dict, coherence="c_v" )


def lda_range(data, start, end, step):
    output = []

    __dict = lda_dict(data)
    __bow = lda_bow(data, __dict)

    for x in range(start, end, step):
        __model = lda(__bow, __dict, x)
        __coherence = lda_coherence(__model, data, __dict).get_coherence()

        #print(__coherence.get_coherence()) if new best
        if len(output) > 0 and __coherence > max([_x[1] for _x in output]):
            print("new n_topic=" + str(x), "model improved the score to", __coherence )  
        output.append((__model, __coherence))
  

    return output



if __name__ == "__main__":
    inpt = "./input/abcnews-date-text.csv"
    data = pd.read_csv(inpt)[:2000]
    tokenized = data["headline_text"].apply(lambda x : x.split(" "))

    
    
    outs = lda_range(tokenized, 10, 300, 5)
    print(outs)