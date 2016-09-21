from bs4 import BeautifulSoup
import re
import urllib

def parseText(url):
    r = urllib.urlopen(url).read()
    print("opened URL");
    soup = BeautifulSoup(r, "html.parser")
    all_text = soup.findAll(text=True)
    story = ""
    def relevant(element):
        if len(element.split()) < 5:
            return False
        if element.parent.name in ['a','td','span','meta','link','script','h1','h2','h3','h4','li','style', 'body', 'head','footer','tr','[document]','center','b', 'option','em','th']:
            return False
        if re.search('<script|</script', element):
            return False
        return True

    text = filter(relevant, all_text)
    print("parsing story")
    for t in text:
        story = story+ t + '\n'
    print("finished parsing")
    return story
