from bs4 import BeautifulSoup
import re
import urllib

CANDIDATE_MIN_WIDTH = 280
CANDIDATE_MIN_HEIGHT = 295
CANDIDATE_MIN_AREA = 170000
CANDIDATE_MAX_TOP = 1300
NOT_SUITABLE_ELEMENTS = set(["ul", "li", "param", "figure", "a", "body", "embed", "form","html","iframe", "object", "option","script", "style", "img", "svg"]);
TAG_NAMES_TO_IGNORE = set(["picture","figure", "source","link", "dd", "dt", "noscript", "ol", "option", "pre", "script", "style", "td", "ul"])

TEXT_MIN_LENGTH = 20

def isElementVisible(element):
    return True


class CandidateElement:

    def usableTextNodesInCandidate(self, element):
        textNodes = []
        if not element:
            return textNodes
        allTextNodes = element.findAll(text=True)
        for tn in allTextNodes:
            if tn.parent.name not in TAG_NAMES_TO_IGNORE:
                if len(' '.join(tn.split())) >= 1:
                    textNodes.append(tn)
        return textNodes

    def rawScoreForTextNode(self, textNode):
        textLengthPower = 1.25
        if not textNode:
            return 0
        if len(' '.join(textNode.split())) < TEXT_MIN_LENGTH:
            return 0
        ancestor = textNode.parent
        if not isElementVisible(ancestor):
            return 0
        mult = 1
        while (ancestor and ancestor != self):
            mult -= 0.1
            if(mult < 0 ):
                mult = 0;
                break;
            ancestor = ancestor.parent
        return pow(len(' '.join(textNode.split()))*mult, textLengthPower)

    def calculateRawScore(self):
        score = 0
        textNodes = self.textNodes
        for tn in textNodes:
            score += self.rawScoreForTextNode(tn)
        return score

    def __init__(self, e):
        self.element = e
        self.textNodes = self.usableTextNodesInCandidate(self.element)
        self.rawScore = self.calculateRawScore()
        self.depth = 0


def isElementViable(element):
    return True


def highestScoringCandidate(candidates):
    highScore = 0
    highestCandidate = None
    for candidate in candidates:
        score = candidate.rawScore
        if score >= highScore:
            highScore = score
            highestCandidate = candidate
    return highestCandidate

def isSubset(a, b):
    if not a or not b:
        return True
    for i in a:
        if len(' '.join(i.split())) >= 1:
            if i not in b:
                return False
    return True

def findArticle(allElements):
    #first loop through all elements
    allCandidates = []
    for element in allElements:
        if element not in NOT_SUITABLE_ELEMENTS:
            if isElementViable(element):
                candidate = CandidateElement(element)
                allCandidates.append(candidate)
    return highestScoringCandidate(allCandidates)

def findBestElement(bestSection):
        maxL = len(bestSection[0])
        bestChoice = 0
        betterSection = []
        for i,t in enumerate(bestSection):
            if len(t) > 80:
                betterSection.append(t)
            if maxL < len(t):
                maxL = len(t)
                bestChoice = i
        p = bestSection[bestChoice].parent
        while(not isSubset(betterSection, p.findAll(text=True))):
            p = p.parent
        return p


def getBestSection(articleDict):
    maxL = 0
    maxK = 0
    for k,nodes in articleDict.items():
        count = 0
        for n in nodes:
            if len(n) > 80:
                count +=1
        if maxL < count:
            maxL = count
            maxK = k
    return maxK

def parseText(url):
    with urllib.request.urlopen(url) as url:
        r = url.read()
    print("opened URL");
    soup = BeautifulSoup(r, "html.parser")
    article = findArticle(soup.findAll())
    # return article
    dictA = {}
    for t in article.textNodes:
        s = 0
        p = t.parent
        while(p and p != article.element):
            s+=1
            p = p.parent

        if s not in dictA:
            dictA[s] = [t]
        else:
            dictA[s].append(t)
    bestSect = getBestSection(dictA)
    bestParentElement = findBestElement(dictA[bestSect])
    allBestText = bestParentElement.findAll(text=True)
    story = ""
    for t in allBestText:
        if len(''.join(t.split())) > 0 and t.parent.name not in TAG_NAMES_TO_IGNORE:
            story += ' '.join(t.split()) + ' '
    print(story)
    print("\n-----------------------------------------------\n")
    return story
