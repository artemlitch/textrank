from __future__ import division
import networkx as nx
import numpy as np
import io
import operator
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

from bs4 import BeautifulSoup
import urllib

def parseText(url):
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)
    pargs = soup.find_all("p")
    story = ""
    for p in pargs:
        story = p.get_text() + '\n'
    return story





