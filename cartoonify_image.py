#importing libraries
import cv2
import imutils
import easygui
import imageio
import sys
import matplotlib.pyplot as plt
import os
import numpy
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

#Upload image from system
def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)

#Define cartoonify function
def cartoonify(ImagePath):
    originalImage = cv2.imread(ImagePath)
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)

#Check if the image is chosen
    if originalImage is None:
        print("Cannot find any image. Choose appropriate file!!")
        sys.exit()
#Image resizing
    Resized1 = cv2.resize(originalImage, (960,540))
    grayScaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    Resized2 = cv2.resize(grayScaleImage, (960,540))

#Applying median blur to smoothen the image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    Resized3 = cv2.resize(smoothGrayScale, (960,540))

#Retrieving edges for cartoon effect
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    Resized4 = cv2.resize(getEdge, (960,540))

#Applying bilateral filter to remove noise and keep the edges sharp as required
    colorImage = cv2.bilateralFilter(originalImage, 9, 300, 300)
    Resized5 = cv2.resize(colorImage, (960,540))

#Masking edged image with our "CARTOONIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    Resized6 = cv2.resize(cartoonImage, (960,540))

#Plotting the whole transition
    images = [Resized1, Resized2, Resized3, Resized4, Resized5, Resized6]
    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    plt.show()

#GUI for cartoonify app
top = tk.Tk()
top.geometry('500x500')
top.title('Cartoonify Your Image!!')
top.configure(background='#eadbc8')
label=Label(top,background='#eadbc8', font=('ariel',20,'bold'))

#Adding button
upload = Button(top,text="Cartoonify Image",command=upload,padx=50,pady=10)
upload.configure(background='blue', foreground='white', font=('ariel',10,'bold'))
upload.pack(side=TOP,pady=200)

#Saving Image
def save(Resized6, ImagePath):
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(Resized6, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + newName + " at "+path
    tk.messagebox.showinfo(title=None, message=I)

#Creating the save button
save1=Button(top,text="Save cartoon image",command=lambda: save(Resized6,ImagePath),padx=30,pady=5)
save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
save1.pack(side=TOP,pady=50)

top.mainloop()


