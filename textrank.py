from __future__ import division
import networkx as nx
import operator
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

def textrank(document):
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc','H','W','h.w','No','p'])
    sentence_tokenizer = PunktSentenceTokenizer(punkt_param)
    sentences = sentence_tokenizer.tokenize(document)
    print("creating sentence tokens")
    bow_matrix = CountVectorizer(stop_words='english').fit_transform(sentences)
    normalized = TfidfTransformer().fit_transform(bow_matrix)

    print("creating similarity graph")
    similarity_graph = normalized * normalized.T

    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
    print("performing pagerank")
    scores = nx.pagerank(nx_graph)

    scores = {k:v*1000 for k,v in scores.iteritems()}
    dropoff = 1/len(scores) * 1000
    good_sentences = {k:v for k,v in scores.iteritems() if v-dropoff > 2}
    filtered_scores = sorted(map(lambda(x): x[0], sorted(good_sentences.items(), key=operator.itemgetter(1), reverse=True)))[1:]

    print "Summarized! {} sentences reduced to {}, reduced to {}%".format(len(sentences), len(filtered_scores), (len(filtered_scores)/len(sentences))*100)
    summary = sentences[0] + '\n'
    for k,v in enumerate(filtered_scores):
        summary += sentences[v] + '\n'
    return summary

