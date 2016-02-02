import nltk
import re
import time
exampleArray=["PROS1.Display is outstanding i.e Full HD awesome and everything is perfect.2.Processor is just oustanding...Octa Core is truly defined here..Any heavy game will run smooth without any interruption..3.Sound Quality is just excellent with the Dolby Atmos feature4.Camera(13+5)overall very good..5.Battery Life is also good...1 or 2 day is enough for normal use and 1 day approx for gaming purpose..Cons:no heating issues,no lag as such,but the only thing as a disadvantage is external memory expandable upto 32 gb only...thats the only drawback...Otherwise oustanding phone.... "]


def processLanguage():
    try:
        for item in exampleArray:
            tokenized =nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            #print tagged
            chunkGram =r"""Chunk:{<NN|VB|JJ|RB|NNP\w*>*<NN|VB|JJ|RB|NNP|VBZ|VBD\w*>*<VBD|TO|RP|RB|VBN|NN|NNS|NNP|JJ\w*>*<VBD|VBN|NN|NNS|NNP|VBG|VB\w*>*<VBD|VBN|NN|NNS|NNP|RB\w*>*<VBD|VBN|NN|NNS|NNP|RB|JJ|VBZ\w?>}"""
            chunkParser =nltk.RegexpParser(chunkGram)
            chunked =chunkParser.parse(tagged)
            namedEnt = nltk.ne_chunk(tagged, binary=True)
            entities=re.findall(r'Chunk\s(.*)/',str(chunked))
            entities=re.sub(r'/[^\s]+','',str(entities))
            print entities
            words=entities.split(',')
            for items in words:
                count = len(re.findall(r'\w+', items))
                if count <=1:
                    pass
                else:
                    print items
                
            #chunked.draw()
            #namedEnt.draw()
            
    except Exception , e:
        print str(e)

processLanguage()
