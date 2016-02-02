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
from cStringIO import StringIO
try:
    # Python2
    import Tkinter as tk
    from urllib2 import urlopen
except ImportError:
    # Python3
    import tkinter as tk
    from urllib.request import urlopen

        
        
class ExampleApp(tk.Tk):
    def __init__(self,par):
        tk.Tk.__init__(self)
        SimpleTable(self,par).pack(side="top", fill="both", expand=True)
        
        
        #t.set(0,0,"Hello, world")
#url=""
class SimpleTable(tk.Frame):
    
    def __init__(self, root,par ):
        # use black background so it "peeks through" to 
        # form grid lines
        url=par
        tk.Frame.__init__(self, root, background="black")
        #url="C:\Users\Space\Desktop\python projects\homrtown.htm"
        #url="http://www.flipkart.com/hometown-belmont-lhs-fabric-6-seater-sectional/p/itme9a8vy4vaewpv?pid=SOFE9A8VBYHCHWAC&al=PkGIJW3ywg1BOE%2BjqMQyMsldugMWZuE7eGHgUTGjVrorjjG6mWQYexJNoqguxi7zAlasJtENodI%3D&ref=L%3A-2969820631779752190&srno=b_1"
        r=requests.get(url)
        soup=BeautifulSoup(r.content)
        #url=par
        #print par+str("avneet")
        #soup=BeautifulSoup(open(url))
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((200,200), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        #self._widgets = []
        r=10
        #display_image(root)
        g_data=soup.find_all("div",{"class":"product-details"})
        #print g_data
        for titles in g_data:
            key = titles.find_all("h1",{"class":"title"})
            #print key
            for t in key:
                tk.Label(self.frame,text=t.getText(),borderwidth=0, relief="solid",font=("Helvetica", 18)).grid(row=r,column=4,sticky="nsew",padx=1, pady=1)
                r=r+1
            for i in range(4):
                tk.Label(self.frame,text=" ",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=4,sticky="nsew",padx=1, pady=1)
                r=r+1
            price = soup.find_all("span",{"class":"selling-price"})
            for p in price:
                tk.Label(self.frame,text=str("Selling Price : ")+ p.getText(),borderwidth=0, relief="solid",font=("Helvetica", 18)).grid(row=r,column=4,sticky="nsew",padx=1, pady=1)
                r=r+1
            for i in range(4):
                tk.Label(self.frame,text=" ",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=4,sticky="nsew",padx=1, pady=1)
                r=r+1
            key = titles.find_all("li",{"class":"key-specification"})
            print key
            for t in key:
                tk.Label(self.frame,text=t.getText(),borderwidth=0, relief="solid",font=("Helvetica", 16)).grid(row=r,column=4,sticky="nsew",padx=1, pady=1)
                r=r+1        
            for i in range(4):
                tk.Label(self.frame,text=" ",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=4,sticky="nsew",padx=1, pady=1)
                r=r+1   
        g_data=soup.find_all("div",{"class":"gu12"})
        keytitle=""
        for i in range(10):
                tk.Label(self.frame,text=" ",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=4,sticky="nsew",padx=1, pady=1)
                r=r+1  
        test=""

        for titles in g_data:
                key = titles.find_all("div",{"class":"keyFeatures"})
                #Label(self,text=str(titles)).grid(row=r,column=0,sticky=W)
                #print key
                for t in key:
                    tt=t.find_all("h3",{"sectionTitle"})
                    for ttt in tt:
                        keytitle+=ttt.getText()
                        #print keytitle
                        tk.Label(self.frame,text=keytitle,borderwidth=0, relief="solid",font=("Helvetica", 16)).grid(row=r,column=4,sticky="nsew",padx=1, pady=1)
                        r=r+1
                    
                td=titles.find_all("ul",{"class":"keyFeaturesList"})
                for tr in td:
                    tr1=tr.find_all("li");
                    for t in tr1:
                        tk.Label(self.frame,text=t.getText(),borderwidth=0, relief="solid",font=("Helvetica", 14)).grid(row=r,column=4,sticky="nsew",padx=1, pady=1)
                        r=r+1
                        test+=t.getText()
                        
        g_data=soup.find_all("div",{"class":"productSpecs"})
        r=r+4
        for titles in g_data:
            tables =titles.find_all("table",{"class":"specTable"})
            for table in tables:
                    #print table
                    tr1=table.find_all("td",{"class":"specsKey"})
                    tr2=table.find_all("td",{"class":"specsValue"})
                    for i in range(len(tr1)):
                        specsKey=tr1[i].getText()
                        specsValue=tr2[i].getText()
                        current_row = []
                        label = tk.Label(self.frame, text=specsKey, borderwidth=0, relief="solid",font=("Helvetica", 10))
                        label.grid(row=r, column=3, sticky="nsew",padx=1, pady=1)
                        #r=r+1
                        current_row.append(label)
                        label = tk.Label(self.frame, text=specsValue , borderwidth=0, relief="solid",font=("Helvetica", 10))
                        
                        label.grid(row=r, column=4, sticky="nsew", padx=1, pady=1)
                        r=r+1
                        current_row.append(label)
                    #self._widgets.append(current_row)
        #display_image(root)
        #for column in range(2):
            #self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
        
def main(par):
    app = ExampleApp(par)
    app.title("Product Specification")
    '''
    url="http://img6a.flixcart.com/image/sofa-sectional/w/a/c/6000020310001-semi-aniline-leather-hometown-brown-brown-400x400-imae94v2g7gdcdsk.jpeg"
    u = urlopen(url)
    raw_data = u.read()
    u.close()
    app.image_file = Image.open(StringIO(raw_data))
    photo_image = ImageTk.PhotoImage(app.image_file)
    app.label = tk.Label(image=photo_image)
    #r=r+2
    app.label.pack()'''
    app.mainloop()
    
