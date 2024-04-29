from argparse import ArgumentParser

import data as dt
import lda
import nlp

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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
        ax.bar([""], vals[x], width=2, bottom=vals[0:x].sum(), label= label )

    ax.legend(title="topic ids", loc="center left", bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True),# n_col = 
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    plt.show()





def word_cloud(model, bow):

    for t in range(1):
        #topics = model.get_document_topics(bow)
        plt.figure()
        # plt.imshow(WordCloud().fit_words(dict(model.show_topic(t, 200))))
        #plt.imshow(WordCloud().fit_words(topics))

        plt.axis("off")
        plt.title(str(t))
        plt.show()



#TODO:mask
def worder_clours(data, mask=None):
    __data = data.apply(lambda x : " ".join(x) if x != None else " ")
    c = WordCloud(background_color="white").generate(" ".join(__data))
    plt.figure()
    plt.axis("off")
    plt.imshow(c)
    plt.show()


if __name__ == "__main__":
    
    #args
    arg_parser = ArgumentParser()


    arg_parser.add_argument("--data", type=str, default=None) 
    arg_parser.add_argument("--model", type=str, default=None) 
    

    args = vars(arg_parser.parse_args())


    #todo err checking
    data = dt.read(args["data"])["Tasks_processed"]#["Qualifications_processed"]
    de_pipeline = nlp.load_langpipeline("de")
    #data = data.apply(nlp.preprocess, args=(de_pipeline,))
    from ast import literal_eval
    data = data.apply(literal_eval)

    # print(data)
    # model = lda.lda_from(args["model"])
    
    #wordcloud
    if False:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator("de", "en")
        data = data.apply(lambda x : [ translator.translate(_x) for _x in x ] )
        data = data.apply(lambda x : [ str(_x) for _x in x if _x != None ]) #lmao had x instead of _x
        worder_clours(data)
    
    
    if True:
        model = lda.lda_from(args["model"])
        #print(model.show_topics(num_topics=100))#

        # __dict = lda.lda_dict(data)
        # __bow = lda.lda_bow(data, __dict)
        # outs = model.get_document_topics(__bow, minimum_probability=0.0) ### <---- this was the problem
        # print(np.shape(outs))
        # print(pd.DataFrame(outs).apply(lambda x : x.apply(lambda y: y[1])))
        distr = lda.lda_topic_distributions(model, data)
        
        topics_bar(distr, min_relevance=0.0)
        topic_ids = [ x for x in range(len(distr.columns)) ]
        #terms 
        terms = [ [ _x[0] for _x in  model.show_topic(x) ] for x in topic_ids ]
        terms = pd.DataFrame({"topic_id": topic_ids, "terms": terms })
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator("de", "en")
        terms["terms"] = terms["terms"].apply(lambda x : [ translator.translate(_x) for _x in x ] )
        terms["terms"] = terms["terms"].apply(lambda x : [ str(_x) for _x in x if _x != None ]) #lmao had x instead of _x
        terms.to_csv("./topic_terms_tasks.csv")


    exit()
    print(data)
    f = data.explode().value_counts()
    f = f[ f > 5]
    print(f)

    fig, ax = plt.subplots()
    vals = f.values
    labels = f.index.to_list()

    for x, label in enumerate(labels):
        ax.bar([""], vals[x], label= label, bottom=vals[0:x].sum(), width=0.2 )

    ax.legend(title="topic ids", loc="center left", bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True),# n_col = 

    plt.show()