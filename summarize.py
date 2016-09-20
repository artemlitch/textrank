import networkx as nx
import operator
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

from bs4 import BeautifulSoup
import urllib

def parseText(url):
    r = urllib.urlopen(url).read()
    print("opened URL");
    soup = BeautifulSoup(r)
    pargs = soup.find_all("p")
    story = ""
    print("parsing story")
    for p in pargs:
        story = story+ p.get_text() + '\n'
    print("finished parsing")
    return story


def textrank(document):
    sentence_tokenizer = PunktSentenceTokenizer()
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
    dropoff = max(scores.values()) - (max(scores.values()) - min(scores.values()))*0.3
    above_average = {k:v for k,v in scores.iteritems() if v >= dropoff}
    filtered_scores = sorted(map(lambda(x): x[0], sorted(above_average.items(), key=operator.itemgetter(1), reverse=True)))[1:]

    print "Summarized! {} sentences reduced to {}, a {}% reduction".format(len(sentences), len(filtered_scores), (100-(len(filtered_scores)/len(sentences))*100))
    summary = sentences[0] + '\n'
    for k,v in enumerate(filtered_scores):
        summary += sentences[v] + '\n'
    return summary

#retrieve each of the articles
print("opening URL")
text = parseText('http://yournewswire.com/germany-bans-fracking-forever/')
print (textrank(text))

