from __future__ import division
import networkx as nx
import numpy as np
import io
import operator
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

def textrank(document):
    sentence_tokenizer = PunktSentenceTokenizer()
    sentences = sentence_tokenizer.tokenize(document)

    bow_matrix = CountVectorizer(stop_words='english').fit_transform(sentences)
    normalized = TfidfTransformer().fit_transform(bow_matrix)

    similarity_graph = normalized * normalized.T

    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
    scores = nx.pagerank(nx_graph)
    scores = {k:v*1000 for k,v in scores.iteritems()}
    import pdb; pdb.set_trace();
    dropoff = max(scores.values()) - (max(scores.values()) - min(scores.values()))*0.3
    above_average = {k:v for k,v in scores.iteritems() if v >= dropoff}
    filtered_scores = sorted(map(lambda(x): x[0], sorted(above_average.items(), key=operator.itemgetter(1), reverse=True)))

    print "Summarized! {} sentences reduced to {}, a {}% reduction".format(len(sentences), len(filtered_scores), (len(filtered_scores)/len(sentences))*100)
    summary = sentences[0] + '\n'
    for k,v in enumerate(filtered_scores):
        summary += sentences[v] + '\n'
    return summary
#retrieve each of the articles
articleFile = io.open('articles/2.txt', 'r')
text = articleFile.read()
print (textrank(text))
