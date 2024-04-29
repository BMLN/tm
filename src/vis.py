from argparse import ArgumentParser

import data as dt
import lda
import nlp

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from wordcloud import WordCloud



def topics_bar(topic_document_distributions, min_relevance):
    relevance = topic_document_distributions.mean(axis=0)
    __drop = relevance < min_relevance
    print(relevance)
    relevance = relevance[__drop == False]
    print(relevance)
    #adjust % / or include as misc

    fig, ax = plt.subplots()
    vals = relevance.values
    labels = relevance.index.to_list()

    for x, label in enumerate(labels):
        ax.bar([""], vals[x], bottom=vals[0:x].sum(), label= label )

    ax.legend(title="topic ids", loc="center left", bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True),# n_col = 

    #plt.show()





def word_cloud(model):

    for t in range(2):
        plt.figure()
        plt.imshow(WordCloud().fit_words(dict(model.show_topic(t, 200))))
        plt.axis("off")
        plt.title(str(t))
        plt.show()



if __name__ == "__main__":
    
    #args
    arg_parser = ArgumentParser()


    arg_parser.add_argument("--data", type=str, default=None) 
    arg_parser.add_argument("--model", type=str, default=None) 
    

    args = vars(arg_parser.parse_args())



    #
    #todo err checking
    data = dt.read(args["data"])["raw_text"]
    de_pipeline = nlp.load_langpipeline("de")
    data = data.apply(nlp.preprocess, args=(de_pipeline,))
    model = lda.lda(args["model"])
    


    # print(data)
    # print("---")

    # __dict = lda.lda_dict(data)
    # __data = lda.lda_bow(data, __dict)
    # topics = model.get_document_topics(__data)
    
    # outs = lda.lda_topic_distributions(data=data, model=model)

    # print(outs)
    # topics_bar(outs, 0.1)



    # t = model.get_topics()
    # print(np.shape(t))

    # #print( [x for x in t[0] if x > 0.001] )

    ms = model.show_topics()
    print(model.show_topic(0))
    # print(ms)
    # print(dict(ms))
    print(model.show_topics(formatted=True))
    # word_cloud(model)
