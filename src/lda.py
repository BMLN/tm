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
        output.append((__model, __coherence))
  

    return output



if __name__ == "__main__":
    inpt = "./input/abcnews-date-text.csv"
    data = pd.read_csv(inpt)[:20]
    tokenized = data["headline_text"].apply(lambda x : x.split(" "))

    __dict = lda_dict(tokenized)
    __bow = lda_bow(tokenized, __dict)
    
    outs = lda_range(tokenized, 10, 15, 5)
    s = outs[0][0]
    #tops = s.show_topics(num_topics= len(s.get_topics()) ,formatted=False)
    #tops = [ [ xx[0] for xx in x[1] ] for x in tops ]
    #print(tops)
    #ts = outs[0][0].get_document_topics(__bow)

    out = lda_topics(s, tokenized)
    print(out)

    #for x in ts:
    #    print(x)
    #t= pd.DataFrame(ts)
    #print(outs[0][0].top_topics(__bow))