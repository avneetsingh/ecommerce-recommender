from PIL import Image, ImageTk
from cStringIO import StringIO
from urllib import urlopen
from Tkinter import *
from PIL import Image
import Tkinter as tk


def main(par):
    
    root = Tk()
    #url = "http://www.wired.com/wp-content/uploads/2015/03/10182025tonedfull-660x441.jpg"
    url="http://img6a.flixcart.com/image/sofa-sectional/w/a/c/6000020310001-semi-aniline-leather-hometown-brown-brown-400x400-imae94v2g7gdcdsk.jpeg"
    url=par
    u = urlopen(url)
    raw_data = u.read()
    u.close()
    image_file = Image.open(StringIO(raw_data))
    photo_image = ImageTk.PhotoImage(image_file)
    label = tk.Label(image=photo_image)
    label.pack()
    root.mainloop()
