import sys
import io
from textrank import textrank
from parsetext import parseText
#retrieve each of the articles

def summarize(url):
    print("opening URL")
    text = parseText(url)
    print (textrank(text))

if __name__ == "__main__":
    summarize(sys.argv[1])
