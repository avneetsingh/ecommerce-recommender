from Tkinter import*
import requests
import sys
from bs4 import BeautifulSoup
import Tkinter as tk
import urllib
from PIL import ImageTk, Image
import os
import json
import io
import base64
import turtle
import image_file
import create_table
import product_reviews
import time
from multiprocessing import pool
from glob import glob
from cStringIO import StringIO
try:
    # Python2
    import Tkinter as tk
    from urllib2 import urlopen
except ImportError:
    # Python3
    import tkinter as tk
    from urllib.request import urlopen

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def features1(par):
        create_table.main(par)

def reviewsfeatures1(par):
        product_reviews.main(par)
def viewImage(par):
    #image_file.main(par)
    url=par
    u = urlopen(url)
    raw_data = u.read()
    u.close()
    image_file = Image.open(StringIO(raw_data))
    photo_image = ImageTk.PhotoImage(image_file)
    label = tk.Label(image=photo_image)
    label.pack()
    root.mainloop()

class Application(Frame):

    def __init__(self,master):
        Frame.__init__(self,master)
        tk.Frame.__init__(self, master)
        self.canvas = tk.Canvas(master, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.cur=0
        self.image = PhotoImage()
        self.images = glob("*.gif")
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.create_widgets()

    def create_widgets(self):
        
        self.instruction = Label(self,text="Search Product").grid(row=0,column=0,columnspan=1)
        self.text = Entry(self)
        self.text.grid(row=0,column=1)
        
        self.submit_button = Button(self,text="Search", command=self.update_text).grid(row=0,column=3)

        Label(self,text="Choose Sites").grid(row=3,column=0,sticky=W)

        #instructions
        #Label(self,text="Select all that apply:").grid(row=4,column=0,sticky=W)

        #Flipkart check button
        self.flipkart = BooleanVar()
        Checkbutton(self,text = "Flipkart",variable = self.flipkart,command = self.update_text).grid(row = 2,column =2)

        
        #Amazon check button
        self.amazon = BooleanVar()
        #Checkbutton(self,text = "Amazon",variable = self.amazon,command = self.update_text).grid(row = 2,column = 3)
        
        #Snapdeal check button
        self.snapdeal = BooleanVar()
        #Checkbutton(self,text = "Snapdeal",variable=self.snapdeal,command=self.update_text).grid(row = 2,column =4)

        self.result = Text(self,width = 40,height = 5,wrap = WORD)
        #self.result.grid(row = 8,column = 0,columnspan = 3)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def show_next(self):
        self.cur = (self.cur + 1) % 150
        self.image.configure(file=self.images[self.cur])
 
    def update_text(self):
        likes=""
        if self.flipkart.get():
            rr=7
            for i in range(150):
                tk.Label(self.frame,text="",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=rr,column=4,sticky="nsew",padx=1, pady=5)
                tk.Label(self.frame,text="",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=rr,column=6,sticky="nsew",padx=1, pady=5)
                tk.Label(self.frame,text="",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=rr,column=8,sticky="nsew",padx=1, pady=5)
                rr=rr+1
                tk.Label(self.frame,text="",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=rr,column=4,sticky="nsew",padx=1, pady=5)
                tk.Label(self.frame,text="",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=rr,column=6,sticky="nsew",padx=1, pady=5)
            url ="http://www.flipkart.com/search?q="
            url2=url+self.text.get()+"&as=off&as-show=on&otracker=end";
            #print(url2)
            r= requests.get(url2);
            soup =BeautifulSoup(r.content);
            links =soup.find_all("a");
            r=7
            for i in range(10):
                tk.Label(self.frame,text=" ",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=4,sticky="nsew",padx=1, pady=5)
                r=r+1
            
            #for link in links:
            #   print "<a href='%s'>%s</a>"%(link.get("href"),link.text)
            #for i in range(b_id):
            #   del lst[i]
            lst=[]
            b_id=0
            b_id2=0
            g_data =soup.find_all("div",{"class":"gu3"})
            self.button3=[]
            self.button4=[]
            self.button5=[]
            self.button6=[]
            b_id3=0
            b_id4=0
            for col in g_data:
                for sets in col.find_all("div",{"class":"pu-title"}):
                    #print sets.get_text('|',strip=True)
                    tk.Label(self.frame,text=sets.get_text(' ',strip=True),borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=4,sticky="nsew",padx=1, pady=5)
                    #r=r+1
                for sets in col.find_all("div",{"class":"pu-price"}):
                    #print sets.get_text('|',strip=True)
                    tk.Label(self.frame,text=sets.get_text(' ',strip=True),borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=6,sticky="nsew",padx=1, pady=5)
                    #r=r+1
                for sets in col.find_all("div",{"class":"pu-rating"}):
                    #print sets.get_text('|',strip=True)
                    tk.Label(self.frame,text=sets.get_text(' ',strip=True),borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=8,sticky="nsew",padx=1, pady=5)
                    
                for sets in col.find_all("div",{"class":"pu-visual-section"}):
                    #print sets
                    p_img=sets.find_all("img")
                    #print p_img
                    for pimg in p_img:
                        var=pimg.get("data-src")
                        #url="http://img6a.flixcart.com/image/sofa-sectional/w/a/c/6000020310001-semi-aniline-leather-hometown-brown-brown-400x400-imae94v2g7gdcdsk.jpeg"
                        #print var
                        url=var
                        #url="http://img6a.flixcart.com/image/sofa-sectional/w/a/c/6000020310001-semi-aniline-leather-hometown-brown-brown-400x400-imae94v2g7gdcdsk.jpeg"
                        u = urlopen(url)
                        raw_data = u.read()
                        u.close()
                        image_file = Image.open(StringIO(raw_data))
                        self.photo_image = ImageTk.PhotoImage(image_file)
                        #tk.Label(self.frame,text=" ",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=9,sticky="nsew",padx=1, pady=5)
                        #tk.Label(self.frame,text=" ",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=10,sticky="nsew",padx=1, pady=5)
                        self.button4.append(tk.Button(self.frame,text="Zoom Image",image=self.photo_image))
                        #self.button4[b_id2].grid(row=r,column=14,sticky="nsew")
                        #self.button4.size(height=250, width=150)
                        r=r+1
                        #self.button4[b_id2].grid(row=r,column=14,sticky="nsew")
                        #self.grid()
                        self.button6.append(Button(self.frame,text="view Image", command=lambda var=var:viewImage(var)))
                        self.button6[b_id4].grid(row=r,column=20,sticky="nsew")
                        b_id4=b_id4+1
                        #self.show_next()
                        #self.button4[b_id2].pack()
                        #self.image = Tkinter.PhotoImage(file=filename)
                        b_id2=b_id2+1
                        #b.pack(side="right")
                        
                        #label = tk.Label(image=photo_image)
                        #label.grid(row=r,column=9)
                        #r=r+2
                        #label.pack()
                    r=r+1
                for sets in col.find_all("a",{"class":"pu-image"}):
                    #print sets.get_text('|',strip=True)
                    val="http://www.flipkart.com"+sets.get("href")
                    tk.Label(self.frame,text=" ",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=4,sticky="nsew",padx=1, pady=5)
                    r=r+1
                    #print val
                    lst.append(val)
                    #tk.Label(self.frame,text="http://www.flipkart.com"+sets.get("href"),borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=4,sticky="nsew",padx=1, pady=5)
                    self.button3.append(Button(self.frame,text="Check this Product", command=lambda val=val:features1(val)))                    
                    self.button3[b_id].grid(row=r,column=4,sticky="nsew")
                    b_id=b_id+1
                    #self.button1["command"]=self.features
                    #tk.button1.grid(row=r,column=4,sticky="nsew")
                    #r=r+1
                    self.button5.append(Button(self.frame,text="Check out reviews", command=lambda val=val:product_reviews.main(val)))
                    self.button5[b_id3].grid(row=r,column=6,sticky="nsew")
                    b_id3=b_id3+1
                    

                    #print "<a href= http://www.flipkart.com%s>%s</a>"%(sets.get("href"),sets.text)
                    r=r+1
                for i in range(3):
                    tk.Label(self.frame,text=" ",borderwidth=0, relief="solid",font=("Helvetica", 10)).grid(row=r,column=4,sticky="nsew",padx=1, pady=5)
                    r=r+1
                #r=r+100
        if self.amazon.get():
           likes += "You like amazon"
        if self.snapdeal.get():
           likes +="You like Snapdeal"
        self.result.delete(0.0,END)
        self.result.insert(0.0,likes)


root=Tk()
root.title("Products")
Application(root).pack(side="top", fill="both", expand=True)
root.mainloop()

           
        
