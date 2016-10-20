A python script (and future application) that takes a URL to a news article, and outputs a summary

#HTML Parser
The first stage of this script is the HTML Parser
The HTML is parsed using BeatufiulSoup 4
To get the article (this is still not 100% accurate), we go through a few steps:
This also comes with a html parser to attempt to extract the article out of a news site.
It uses several layers of ranking:
 1. take entire article, and remove all elements that are not suitable for holding text (script, link, etc etc)
 2. out of the elements that are left, find the "highest scoring" element
  2.1. Per element, find all children elements that contain text 
  2.2. calculate a raw score of each text element by measuring length, and depth to parent (the deeper it is the worse it scores)
  2.3. Raw score is the sum of all text element scores
 note: Ideally, we could "see" how a text element gets rendered, and score based on size of the element, the theory is that the larger the element is, the more likely it would be the article (combined with the text length). But we can't do this in just python, so.. we have to do more work
 The next steps take the most likely candidate element returned by step 2, and prune text (like advertisements and links not related to the article). This step is still a WIP, and only the first iteration. It makes an assumption that there exists an element that will be the lowest parent of the most textNodes that are most likely to be part of the article. So, if there are 5 <p> elements that all are quite long and similiar in size to each other, their first common parent is most likely to be the article. This is the assumption.
 
 3. Create a dict of all textNodes from the element returned from part 2
   This dict will take every textNode, and return its depth to the parent element
 4. Return the level at which the most "good"(longer than 80 chars, which is what I assumed the length would be for advertisements and other links) text is found (The assumption here is that an article will be written with most paragraphs and other elements residing on the same depth in the HTML)
 5. Given this best level and section of elements, work up the element tree and find the best parent that contains all of these divs
  5.1 essentially loop up until you get an element that contains text outside of the BestSection of text (so we have gone too far)
 6. This best Parent is now hopefully the article element
 
 What can go wrong?
 I made a few assumptions on how an article is written on the web.
 The first assumption is that the article is written in paragraphs that are on the same height in the tree
 eg: 
 <article id='our_article'>
 <p>Blah Blah Blah...</p>
 <p>Blah Blah Blah...</p>
 <p>Blah Blah Blah...</p>
 <p>Blah Blah Blah...</p>
</article>
Here we can see that the paragraphs are all on the same level. However, if there is a bunch of advertisement elements that are all on the same height, they will be included.
Second assumption I made is that "bad text" caps off at 80 chars. This is a cutoff that I can modify but, its just guessing, so if there is a link to an article or some advertisement with more than 80 chars, this algorithm will consider it "good text"

A way to solve this issue is to look at the way Apple does their "Reader" feature in iOS and OSX Safari. They look directly at the size of elements when deciding if the elements should be pruned; A luxury I unfortunately do not have in just a python script.

#Textrank
This is the fun part :)
After getting all the text, we can now try to summarize it as best as we can. There is a great paper called [Textrank](http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf), which uses Google's Pagerank on text to decide which ones are most important. I won't go over pagerank implementation, but it takes a sparce matrix (where each Vij = 1 or 0 if there is a link from i to j), and outputs which pages are most important, based on how many links the page has pointing to it. 

Textrank is similar, and I will explain it here:
1. Split up every sentence. I used the NLTK tokenizer for this so that I wouldn't have to write any rules like "ignore Mr. as a sentence ender". And because the NLTK tokenizer already uses lots of grammar rules to handle this in a much better way than just splitting based on '.' symbols.
2. Now, using the array of sentences, we create a NxN sparse markov matrix where each Vij represents a similarity (based on how many of the same words were used) between i and j
3. Apply pagerank on this NxN matrix and get a array of sentences sorted in priority
4. Set a threshold (top 40% for example) and return a summary

Dependencies
============
Networkx - http://networkx.github.io/download.html
NLTK 3.0 - http://nltk.org/install.html
Numpy - http://sourceforge.net/projects/numpy/files/


