import sys
import io
from textrank import textrank
from parsetext import parseText
#retrieve each of the articles

def summarize(url):
    print("opening URL")
    f = open(url, "r")
    # text = parseText(f.read())
    print(textrank(f.read()))

if __name__ == "__main__":
    summarize(sys.argv[1])
