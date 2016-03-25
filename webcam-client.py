#!/bin/python2

import Tkinter
from PIL import ImageTk

IMGPATH = '/tmp/webcam.jpg'

root = Tkinter.Tk()
root.title('Webcam')
im = ImageTk.PhotoImage(file=IMGPATH)

startframe = Tkinter.Frame(root)
canvas = Tkinter.Canvas(startframe,width=1280,height=720)
startframe.pack()
canvas.pack()

canvas.img = im
canvasImg = canvas.create_image((0,0), image=im, anchor='nw')

def callback(e):
	img2 = ImageTk.PhotoImage(file=IMGPATH)
	canvas.itemconfig(canvasImg, image = img2)
	canvas.img = img2
	print "wew"


root.bind("<Return>", callback)
root.mainloop()
