from Tkinter import*
import requests
from bs4 import BeautifulSoup
import Tkinter as tk
import urllib
from PIL import ImageTk, Image
import os
import json
import io
import base64
import turtle
import nltk
import re
import time
import pdb
import sys
import math
from textblob import TextBlob
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from cStringIO import StringIO
import plotly.graph_objs as go
from nltk.corpus import wordnet as wn
from itertools import product
try:
    # Python2
    import Tkinter as tk
    from urllib2 import urlopen
except ImportError:
    # Python3
    import tkinter as tk
    from urllib.request import urlopen
import plotly.plotly as py
from plotly.graph_objs import *
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
#print __version__ # requires version >= 1.9.0
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly


plotly.tools.set_credentials_file(username='SPACE007', api_key='o61g0qzbgl')

py.sign_in('SPACE007', 'o61g0qzbgl')
f=open('negative-words.txt','r')
neg = f.read().split('\n')[:-1]
f.close()
f=open('positive-words.txt','r')
pos=f.read().split('\n')[:-1]
# USe graph theorotic approach##############################################        
class Graph:
	def __init__(self):
		self.Vertices = []
		self.Edges = []

	def getRankedVertices(self):
		res = defaultdict(float)
		for e in self.Edges:
			res[e.Vertex1] += e.Weight
		return sorted(res.items(), key=lambda x: x[1], reverse=True)

class Vertex:
	def __init__(self):
		self.Sentence = None

class Edge:
	def __init__(self):
		self.Vertex1 = None
		self.Vertex2 = None
		self.Weight = 0

class WordType:
	Content=0
	Function=1
	ContentPunctuation=2
	FunctionPunctuation=3

class Word:
	def __init__(self):
		self.Text=''
		self.Type=''

class Sentence:
	def __init__(self):
		self.Words = []

	def getFullSentence(self):
		text = ''
		for w in self.Words:
			text += w.Text
		return text.strip()

	def getReducedSentence(self):
		sentenceText = ''
		sentenceEnd = self.Words[len(self.Words)-1]
		contentWords = filter(lambda w: w.Type == WordType.Content, self.Words)
		i = 0
		while i < len(contentWords):
			w = contentWords[i]
			# upper case the first character of the sentence
			if i == 0:
				li = list(w.Text)
				li[0] = li[0].upper()
				w.Text = ''.join(li)
			sentenceText += w.Text
			if i < len(contentWords)-1:
				sentenceText += ' '
			elif sentenceEnd.Text != w.Text:
				sentenceText += sentenceEnd.Text
			i = i+1
		return sentenceText
			

class Paragraph:
	def __init__(self):
		self.Sentences = []
from nltk.corpus import wordnet as wn
from itertools import product

def compare(word1, word2):
    ss1 = wn.synsets(word1)
    ss2 = wn.synsets(word2)
    #return ss1.shortest_path_distance(ss2)
    x=0.0
    f=0
    i=0
    for each in product(ss1,ss2):
        f=1
        break
    if(f):
        for (s1,s2) in product(ss1,ss2):
            x=max(x,s1.path_similarity(s2))
            i=i+1
            if(i>=1):
                break
        #x= max(s1.path_similarity(s2) for (s1, s2) in product(ss1, ss2))
    return x
class Reduction:
	functionPunctuation = ' ,-'
	contentPunctuation = '.?!\n'
	punctuationCharacters = functionPunctuation+contentPunctuation
	sentenceEndCharacters = '.?!'
	
	def isContentPunctuation(self, text):
		for c in self.contentPunctuation:
			if text.lower() == c.lower():
				return True
		return False

	def isFunctionPunctuation(self, text):
		for c in self.functionPunctuation:
			if text.lower() == c.lower():
				return True
		return False

	def isFunction(self, text, stopWords):
		for w in stopWords:
			if text.lower() == w.lower():
				return True
		return False

	def tag(self, sampleWords, stopWords):
		taggedWords = []
		for w in sampleWords:
			tw = Word()
			tw.Text = w
			if self.isContentPunctuation(w):
				tw.Type = WordType.ContentPunctuation
			elif self.isFunctionPunctuation(w):
				tw.Type = WordType.FunctionPunctuation
			elif self.isFunction(w, stopWords):
				tw.Type = WordType.Function
			else:
				tw.Type = WordType.Content
			taggedWords.append(tw)
		return taggedWords

	def tokenize(self, text):
		return filter(lambda w: w != '', re.split('([{0}])'.format(self.punctuationCharacters), text))	

	def getWords(self, sentenceText, stopWords):
		return self.tag(self.tokenize(sentenceText), stopWords) 

	def getSentences(self, line, stopWords):
		sentences = []
		sentenceTexts = filter(lambda w: w.strip() != '', re.split('[{0}]'.format(self.sentenceEndCharacters), line))	
		sentenceEnds = re.findall('[{0}]'.format(self.sentenceEndCharacters), line)
		sentenceEnds.reverse()
		for t in sentenceTexts:
			if len(sentenceEnds) > 0:
				t += sentenceEnds.pop()
			sentence = Sentence()
			sentence.Words = self.getWords(t, stopWords)
			sentences.append(sentence)
		return sentences

	def getParagraphs(self, lines, stopWords):
		paragraphs = []
		for line in lines:
			paragraph = Paragraph()
			paragraph.Sentences = self.getSentences(line, stopWords)
			paragraphs.append(paragraph)
		return paragraphs

	def findWeight(self, sentence1, sentence2):
		length1 = len(filter(lambda w: w.Type == WordType.Content, sentence1.Words))
		length2 = len(filter(lambda w: w.Type == WordType.Content, sentence2.Words))
		if length1 < 4 or length2 < 4:
			return 0
		weight = 0.0
		for w1 in filter(lambda w: w.Type == WordType.Content, sentence1.Words):
			for w2 in filter(lambda w: w.Type == WordType.Content, sentence2.Words):
			    #weight = weight + (float)(compare(str(w1.Text.lower()),str(w2.Text.lower())))
                            #first=wn.synsets(str(w1.Text.lower()))[0]
                            #second=wn.synsets(str(w2.Text.lower()))[0]
                            try:
                                weight= weight + compare(str(w1.Text.lower()),str(w2.Text.lower()))
                            except Exception:
                                if w1.Text.lower() == w2.Text.lower():
					weight = weight + 1
				
                print weight
		normalised1 = 0
		if length1 > 0:
			normalised1 = math.log(length1)
		normalised2 = 0
		if length2 > 0:
			normalised2 = math.log(length2)
		norm = normalised1 + normalised2
		if norm == 0:
			return 0
		return weight / float(norm)

	def buildGraph(self, sentences):
		g = Graph()
		for s in sentences:
			v = Vertex()
			v.Sentence = s
			g.Vertices.append(v)
		for i in g.Vertices:
			for j in g.Vertices:
				if i != j:
					w = self.findWeight(i.Sentence, j.Sentence)
					e = Edge()
					e.Vertex1 = i
					e.Vertex2 = j
					e.Weight = w
					g.Edges.append(e)
		return g

	def sentenceRank(self, paragraphs):
		sentences = []
		for p in paragraphs:
			for s in p.Sentences:
				sentences.append(s)
		g = self.buildGraph(sentences)
		return g.getRankedVertices()

	def reduce(self, text, reductionRatio):
		stopWordsFile = 'stopWords.txt'
		stopWords= open(stopWordsFile).read().splitlines()

		lines = '\n'.join(text)
		lines = lines.splitlines()
		contentLines = filter(lambda w: w.strip() != '', lines)

		paragraphs = self.getParagraphs(contentLines, stopWords)

		rankedSentences = self.sentenceRank(paragraphs)

		orderedSentences = []
		for p in paragraphs:
			for s in p.Sentences:
				orderedSentences.append(s)

		reducedSentences = []
		i = 0
		while i < math.trunc(len(rankedSentences) * reductionRatio):
			s = rankedSentences[i][0].Sentence
			position = orderedSentences.index(s)
			reducedSentences.append((s, position))
			i = i + 1
		reducedSentences = sorted(reducedSentences, key=lambda x: x[1])
		
		reducedText = []
		for s,r in reducedSentences:
			reducedText.append(s.getFullSentence())
		return reducedText	
ow=[]
but=0
def but_rule(feat,ow,sent):
	split_sent=sent.split('but')
	but_clause=nltk.word_tokenize(split_sent[1])
	orient=0
	if feat in but_clause:
		for opinion in ow:
			if opinion in but_clause:
				orient=orient+word_orient(opinion,feat,split_sent[1])
		if orient!=0:
			return orient
		else:
			for opinion in ow:
				if opinion in nltk.word_tokenize(split_sent[0]):
					orient=orient+word_orient(opinion,feat,split_sent[0])
			if orient!=0:
				return -1*orient
			else:
				return 0
			

def check_neg(opinion):
	if opinion=='no' or opinion=='not' or opinion=='never':
		return True
	else:
		return False		

def dist(opinion,feat,sent):
	op=sent.index(opinion)
	try:
		fe=sent.index(feat)
		d=fe-op
		if d>0:
			return d
		elif d<0:
			return -1*d
		else:
			return 0.000001
	except:
		return 9999999
		

def neg_rule(op,feat,sent):
	tokens=nltk.word_tokenize(sent)
	try:
		now=tokens[tokens.index(op)+1]
		orient=word_orient(now,feat,sent)
		try :
			ow.pop(ow.index(now))
			if orient==0 or orient==1:
				return -1
			else:
				return -1*orient
		
		except:
		
			if orient==0 or orient==1:
				return -1
			else:
				return -1*orient
	except:
		return -1
	
	

def word_orient(opinion,feat,sent):
	orient=0
	tokens=nltk.word_tokenize(sent)
	if check_neg(opinion):
		orient=neg_rule(opinion,feat,sent)
	else:
		if opinion in neg:
			orient=-1.0
		elif opinion in pos:
			orient=1.0
		else:
			orient=0.0
	d=dist(opinion,feat,tokens)
	final_op=(orient/d)
	return final_op

def processLanguage(exampleArray, ids,url,reviewTitle,certified):
    try:
        #print exampleArray
        display=[]
        rest=exampleArray
        '''for items in rest:
            #rest = rest.replace('\n', ' ').replace('\r', '')
            #print exampleArray
            item =items
            #print item
            tokenized =nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            item = item.replace('\n', ' ').replace('\r', '')
            chunkGram =r"""Chunk:{<NN|VB|JJ|RB|NNP\w*>*<NN|VB|JJ|RB|NNP|VBZ|VBD\w*>*<VBD|TO|RP|RB|VBN|NN|NNS|NNP|JJ\w*>*<VBD|VBN|NN|NNS|NNP|VBG|VB\w*>*<VBD|VBN|NN|NNS|NNP|RB\w*>*<VBD|VBN|NN|NNS|NNP|RB|JJ|VBZ\w?>}"""
            chunkParser =nltk.RegexpParser(chunkGram)
            chunked =chunkParser.parse(tagged)
            namedEnt = nltk.ne_chunk(tagged, binary=True)
            entities=re.findall(r'Chunk\s(.*)/',str(chunked))
            entities=re.sub(r'/[^\s]+','',str(entities))
            #print entities
            words=entities.split(',')
            for items2 in words:
                count = len(re.findall(r'\w+', items2))
                if count <=2:
                    pass
                else:
                    display.append(items2)
                    
                #chunked.draw()
                #namedEnt.draw()'''
        reduction = Reduction()
        #text = open('product.txt').read()
        text = exampleArray
        reduction_ratio =0.04
        #reduced_text=[]
        reduced_text = reduction.reduce(text, reduction_ratio)
        #r=requests.get(url,proxies=proxies)
        r=requests.get(url)
        feature=[]
        averagerating=0;
        #soup=BeautifulSoup(r.content, 'html.parser')
        features={}
        features['performance']=[[],[],[]]
        feature.append("performance")
        features['price']=[[],[],[]]
        feature.append("price")
        features['reliability']=[[],[],[]]
        feature.append("reliability")
        features['service']=[[],[],[]]
        feature.append("service")
        features['delivery']=[[],[],[]]
        feature.append("delivery")
        #print url
        #r= requests.get(url,proxies=proxies);
        r=requests.get(url)
        #specsKey=""
        soup=BeautifulSoup(r.content, 'html.parser')
        g_data=soup.find_all("div",{"class":"productSpecs"})
        for titles in g_data:
            tables =titles.find_all("table",{"class":"specTable"})
            for table in tables:
                tr1=table.find_all("td",{"class":"specsKey"})
                for i in range(len(tr1)):
                        specsKey=tr1[i].getText().lower()
                        feature.append(specsKey)
                        features[specsKey]=[[],[],[]]
                        
        title=""
        for i in reviewTitle:
            for j in feature:
                res= i.find(j)
                if(res!=-1):
                    display.append(i)
                    break
        g_data=soup.find_all("div",{"class":"product-details"})
        for titles in g_data:
            key = titles.find_all("h1",{"class":"title"})
            for t in key:
                title=t.getText();
        kk=0
        userId=-1
        flag=1
        active=0;
        for each in display:
            print (each)
        print "\n"
        for each in reduced_text:
            print each
            print "\n"
        #features={'camera':[[],[],[]],'picture':[[],[],[]],'display':[[],[],[]],'processor':[[],[],[]],'battery':[[],[],[]],'control':[[],[],[]],'touch':[[],[],[]],'memory':[[],[],[]],'nfc':[[],[],[]],'design':[[],[],[]],'price':[[],[],[]],'experience':[[],[],[]]}
        for j in exampleArray:
            #print (ids[kk])
            tokens=nltk.word_tokenize(j)
            if(flag==1):
                userId=userId+1
            flag=1-flag
            if(flag):
                print userId
            t = nltk.pos_tag(tokens)
            temp={}
            feat_o={}
            ow=[]
            but=0
            for k in t:
                if features.has_key(k[0]):
                    temp[k[0]]=0
                    feat_o[k[0]]=''
                if(k[0]=='but'):
                    but=1
                if k[1]=='JJ' or k[1]=='JJR' or k[1]=='JJS' or k[1]=='NN' or k[1]=='NNS' or k[1]=='RB' or k[1]=='RBR' or k[1]=='VB' or k[1]=='VBG':
                    ow.append(k[0])
            for feat in temp:
                if but==1:
                    temp[feat]=but_rule(feat,ow,j)
                else:
                    for opinion in ow:
                        temp[feat]=temp[feat]+word_orient(opinion,feat,j)
                if temp[feat]>0:
                    feat_o[feat]=1
                elif  temp[feat]<0:
                    feat_o[feat]=-1
                else:
                    feat_o[feat]=0
            rate=0
            temp = 0
            for c in feat_o:
                temp=temp+1
                if feat_o[c]==1:
                    if userId not in features[c][0]:
                        features[c][0].append(userId)
                        if(certified[userId]==1):
                            rate =rate+ 0.9
                        else:
                            rate=rate+ 0.7
                        kk=kk+1
                elif feat_o[c]==-1:
                    if userId not in features[c][1]:
                        features[c][1].append(userId)
                        if(certified[userId]==1):
                            rate =rate+0.5
                        else:
                            rate=rate-+0.3
                        kk=kk+1
                else:
                    if userId not in features[c][2]:
                        features[c][2].append(userId)
                        if(certified[userId]==1):
                            rate =rate + 0.8
                        else:
                            rate=rate + 0.6
                        kk=kk+1
		#kk=kk+1
            if(flag):
                print str(rate)+" hello"
            if(rate>0):
                active=active+1
            averagerating = averagerating + 4.1*rate
        #print active
        averagerating=averagerating/active
        print "Average Rating of "+ title+ " = " +str(averagerating)
        
        labelpos=[]
        labelneg=[]
        valuepos=[]
        valueneg=[]
        for each in features:
            if(int(len(features[each][0]))> 0):
                print str(len(features[each][0]))+ " people were happy and satisfied about "+each+" of "+title+"."
                labelpos.append(each)
                valuepos.append(len(features[each][0]))
            if(len(features[each][1]) > 0):
                print str(len(features[each][1]))+ " people were not happy about "+each+" of "+title+"."
                labelneg.append(each)
                valueneg.append(len(features[each][1]))
            if(len(features[each][2]) > 0 ):
                print str(len(features[each][2]))+ " people did average rating about "+each+" of "+title+"."
                if each in labelpos:
                    findex=labelpos.index(each)
                    valuepos[findex]=valuepos[findex]+ len(features[each][2])
                else:
                    labelpos.append(each)
                    valuepos.append(len(features[each][2]))
                #print "\n"
        trace1 = Pie(
            domain=dict(
            x=[0, 0.52]
            ),
            hole=0.4,
            hoverinfo='label+percent+name',
            labels=labelpos,
            labelssrc='SPACE007:3:bd9c85',
            name='Positive Feedback Percentage of'+ title,
            values=valuepos,
            valuessrc='SPACE007:3:319bc1'
        )
        trace2 = Pie(
            domain=dict(
            x=[0.48, 1]
            ),
            hole=0.4,
            hoverinfo='label+percent+name',
            labels=labelneg,
            labelssrc='SPACE007:3:bd9c85',
            name='Negative Feedback Percentage of'+ title,
            #text='Mobile',
            textposition='inside',
            values=valueneg,
            valuessrc='SPACE007:3:230ab3'
        )
        data = Data([trace1, trace2])
        layout = Layout(
            annotations=Annotations([
                Annotation(
                    x=0.2,
                    y=0.5,
                    font=Font(
                        size=20
                    ),
                    showarrow=False,
                    text='Positive'
                ),
                Annotation(
                    x=0.8,
                    y=0.5,
                    font=Font(
                        size=20
                    ),
                    showarrow=False,
                    text='Negative'
                )
            ]),
            title='Review Analysis of '+title+ " from Flipkart"
        )
        fig = Figure(data=data, layout=layout)
        plot(fig)
    except Exception , e:
        print str(e)
        
class ExampleApp(tk.Tk):
    def __init__(self,par):
        tk.Tk.__init__(self)
        SimpleTable(self,par).pack(side="top", fill="both", expand=True)
        
class SimpleTable(tk.Frame):
    
    def __init__(self, root,par ):
        # use black background so it "peeks through" to 
        # form grid lines
        url=par
        tk.Frame.__init__(self, root, background="white")
        #url="C:\Users\Space\Desktop\python projects\homrtown.htm"
        #url="http://www.flipkart.com/hometown-belmont-lhs-fabric-6-seater-sectional/p/itme9a8vy4vaewpv?pid=SOFE9A8VBYHCHWAC&al=PkGIJW3ywg1BOE%2BjqMQyMsldugMWZuE7eGHgUTGjVrorjjG6mWQYexJNoqguxi7zAlasJtENodI%3D&ref=L%3A-2969820631779752190&srno=b_1"
        #r=requests.get(url,proxies=proxies)
        r=requests.get(url)
        soup=BeautifulSoup(r.content, 'html.parser')
        container=[]
        reviewTitle=[]
        certified=[]
        ids=[]
        temp_url=url
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((200,200), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        #r= requests.get(url,proxies=proxies);
        r= requests.get(url);
        soup =BeautifulSoup(r.content, 'html.parser')
        g_data= soup.find_all("div",{"class":"recentReviews"})
        for links in g_data:
            aa=links.find_all("a")
            for link in aa:
                url=link.get("href")
        url= url[:-17]
        url2 = "http://www.flipkart.com"+ url+str("&rating=1,2,3,4,5&reviewers=all&type=top&sort=most_recent&start=")
        r=2
        #print url2
        number=0;
        for i in range(2):
            url3= url2+str((i)*10)
            #rr= requests.get(url3,proxies=proxies);
            rr= requests.get(url3);
            soup =BeautifulSoup(rr.content, 'html.parser')
            g_data= soup.find_all("div",{"class":"review-list"})
            #print url3
            for col in g_data:
                for sets in col.find_all("div",{"class":"fk-review"}):
                    #print sets
                    for ratings in sets.find_all("div",{"class":"fk-stars"}):
                        v=ratings.get("title")
                        tk.Label(self.frame,text=str(v),borderwidth=0, relief="solid",font=("Helvetica", 12)).grid(row=r,column=0,sticky="nsew",padx=1, pady=5)
                    for user in sets.find_all("a",{"class":"load-user-widget"}):
                        #print user.get_text()
                        ids.append(user.get_text())
                        tk.Label(self.frame,text=user.get_text(),borderwidth=0, relief="solid",font=("Helvetica", 14)).grid(row=r,column=1,sticky="nsew",padx=1, pady=5)
                        r=r+1
                    for user in sets.find_all("span",{"class":"review-username"}):
                        #print user.get_text()
                        ids.append(user.get_text())
                        tk.Label(self.frame,text=user.get_text(),borderwidth=0, relief="solid",font=("Helvetica", 14)).grid(row=r,column=1,sticky="nsew",padx=1, pady=5)
                        r=r+1
                    badge=sets.find_all("div",{"class":"badge-certified-buyer"})
                    if not badge:
                        certified.append(0)
                    else:
                        certified.append(1)
                    number=number+1
                    #print badge
                    for date in sets.find_all("div",{"class":"date"}):
                        #print date.get_text()
                        tk.Label(self.frame,text=date.get_text(),borderwidth=0, relief="solid",font=("Helvetica", 16)).grid(row=r,column=1,sticky="nsew",padx=1, pady=5)
                        r=r+1
                    for review in sets.find_all("div",{"class":"lastUnit"}):
                        for titles in review.find_all("div",{"class":"fk-font-normal"}):  
                            tk.Label(self.frame,text=titles.get_text(),borderwidth=0, relief="solid",font=("Helvetica", 12)).grid(row=r,column=1,sticky="nsew",padx=1, pady=5)
                            container.append((titles.get_text()))
                            reviewTitle.append((titles.get_text()))
                            r=r+1
                        #print review
                        for comments in review.find_all("span",{"class":"review-text"}):
                            #print comments.get_text()
                            container.append((comments.get_text()))
                            tk.Label(self.frame,text=comments.get_text(),borderwidth=0, relief="solid",font=("Helvetica", 8)).grid(row=r,column=0,sticky="nsew",padx=1, pady=5,columnspan=10)
                            r=r+2
                    r=r+1
        #print number
        processLanguage(container,ids,temp_url,reviewTitle,certified)
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

def main(par):
    app = ExampleApp(par)
    app.title("Product Reviews")
    app.mainloop()
