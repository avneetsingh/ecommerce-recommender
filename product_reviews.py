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
from cStringIO import StringIO
import plotly.graph_objs as go
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
import plotly

plotly.tools.set_credentials_file(username='SPACE007', api_key='o61g0qzbgl')

py.sign_in('SPACE007', 'o61g0qzbgl')
f=open('negative-words.txt','r')
neg = f.read().split('\n')[:-1]
f.close()
f=open('positive-words.txt','r')
pos=f.read().split('\n')[:-1]
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

        #r=requests.get(url,proxies=proxies)
        #r=requests.get(url)
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
        #features={'camera':[[],[],[]],'picture':[[],[],[]],'display':[[],[],[]],'processor':[[],[],[]],'battery':[[],[],[]],'control':[[],[],[]],'touch':[[],[],[]],'memory':[[],[],[]],'nfc':[[],[],[]],'design':[[],[],[]],'price':[[],[],[]],'experience':[[],[],[]]}
        for j in exampleArray:
            #print (ids[kk])
            tokens=nltk.word_tokenize(j)
            if(flag==1):
                userId=userId+1
            flag=1-flag
            #print userId
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
                    features[c][0].append(kk)
                    if(certified[userId]==1):
                        rate =rate+ 0.9
                    else:
                        rate=rate+ 0.7
                    kk=kk+1
                elif feat_o[c]==-1:
                    features[c][1].append(kk)
                    if(certified[userId]==1):
                        rate =rate+0.5
                    else:
                        rate=rate-+0.3
                    kk=kk+1
                else:
                    features[c][2].append(kk)
                    if(certified[userId]==1):
                        rate =rate + 0.8
                    else:
                        rate=rate + 0.6
                    kk=kk+1
		#kk=kk+1
            print str(rate)+" hello"
            if(rate>0):
                active=active+1
            averagerating = averagerating + 4.0*rate
        #print active
        averagerating=averagerating/active
        print "Average Rating of "+ title+ " = " +str(averagerating)
        for each in display:
            print (each)
        print "\n"
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
        plot_url = py.plot(fig)
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
        print url2
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
