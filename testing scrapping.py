import requests
from Tkinter import *
from bs4 import BeautifulSoup

root=Tk()
root.title("Simple GUI")
root.geometry("200x100")
#root.mainloop()
testVar = raw_input("Ask user for something.")
url ="http://www.flipkart.com/search?q="
url2=url+testVar+"&as=off&as-show=on&otracker=end";
r= requests.get(url2);
soup =BeautifulSoup(r.content);
links =soup.find_all("a");
#for link in links:
 #   print "<a href='%s'>%s</a>"%(link.get("href"),link.text)
g_data =soup.find_all("div",{"class":"gu3"})
for col in g_data:
    for sets in col.find_all("div",{"class":"pu-title"}):
        print sets.get_text('|',strip=True)
    for sets in col.find_all("div",{"class":"pu-price"}):
        print sets.get_text('|',strip=True)
    for sets in col.find_all("div",{"class":"pu-rating"}):
        print sets.get_text('|',strip=True)
    for sets in col.find_all("a",{"class":"pu-image"}):
        #print sets.get_text('|',strip=True)
        print "<a href='%s'>%s</a>"%(sets.get("href"),sets.text)
