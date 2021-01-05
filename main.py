from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image

from tools import *

root = Tk()
root.title("AIVO")
root.geometry("800x600")
# root.resizable(width=False, height=False)

currentImage, newImage = "", ""


def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()


def openImage():
    global label
    global currentImage
    global openedImage

    newImage = filedialog.askopenfilename(initialdir="~/Pictures", title="Open image",
                                           filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png")))
    root.title("{} - AIVO".format(newImage.split("/")[-1]))
    currentImage = newImage
    openedImage = currentImage
    img = ImageTk.PhotoImage(Image.open(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def rotateImage(direction):
    global label
    global currentImage
    global openedImage

    angle = 90

    if direction == "RIGHT":
        angle *= -1

    newImage = rotate(cv2.imread(openedImage), angle)
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def grayImage():
    global label
    global currentImage
    global openedImage

    newImage = rgbToGray(cv2.imread(openedImage))
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def binarizeImage():
    global label
    global currentImage
    global openedImage

    newImage = binarize(cv2.imread(openedImage), 128)
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def inverseImage():
    global label
    global currentImage
    global openedImage

    newImage = inverse(cv2.imread(openedImage))
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def adjustConImage():
    global label
    global currentImage
    global openedImage

    newImage = equalizeHist(cv2.imread(openedImage))
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def adjustLumImage():
    global label
    global currentImage
    global openedImage

    newImage = stretchHist(cv2.imread(openedImage), 64, 192)
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def blurImage():
    global label
    global currentImage
    global openedImage

    newImage = blur(cv2.imread(openedImage))
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def edgeImage():
    global label
    global currentImage
    global openedImage

    newImage = edge(cv2.imread(openedImage))
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def openingMorphTransImage():
    global label
    global currentImage
    global openedImage

    newImage = opening(cv2.imread(openedImage))
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def closingMorphTransImage():
    global label
    global currentImage
    global openedImage

    newImage = closing(cv2.imread(openedImage))
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def othMorphTransImage():
    global label
    global currentImage
    global openedImage

    newImage = openingTopHat(cv2.imread(openedImage))
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def cthMorphTransImage():
    global label
    global currentImage
    global openedImage

    newImage = closingTopHat(cv2.imread(openedImage))
    currentImage = newImage
    img = ImageTk.PhotoImage(Image.fromarray(newImage))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()




def showHist():
    global openedImage

    hist = computeHist(cv2.imread(openedImage))
    plt.plot(hist)
    plt.xlabel('Gray level')
    plt.ylabel('Count')
    plt.title("Histogram of the image in gray level")
    plt.show()


def saveImage():
    global currentImage

    if currentImage:
        # imageName = currentImage.split("/")[-1]
        imageName = currentImage
        cv2.imwrite(imageName, currentImage)
    else:
        saveAsImage()


def saveAsImage():
    global currentImage

    imageName = filedialog.asksaveasfilename(defaultextension=".png", initialdir="~/Pictures/", title="Save an image", filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png")))

    if imageName:
        # imageName = imageName.split("/")[-1]
        cv2.imwrite(imageName, currentImage)
        root.title("{} - AIVO".format(imageName.split("/")[-1]))


def closeImage():
    global label
    label.pack_forget()
    label = Label(text="Select an image...", anchor=CENTER)
    label.pack()


menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openImage)
filemenu.add_command(label="Save", command=saveImage)
filemenu.add_command(label="Save as", command=saveAsImage)
filemenu.add_command(label="Close", command=closeImage)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)
editmenu.add_command(label="Redo", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)

imagemenu = Menu(menubar, tearoff=0)
imagemenu.add_command(label="Flip Horizontally", command=donothing)
imagemenu.add_command(label="Flip Vertically", command=donothing)
imagemenu.add_command(label="Rotate Right", command=lambda: rotateImage("RIGHT"))
imagemenu.add_command(label="Rotate Left", command=lambda: rotateImage("LEFT"))
imagemenu.add_command(label="Adjust contraste", command=adjustConImage)
imagemenu.add_command(label="Adjust luminosity", command=adjustLumImage)
imagemenu.add_command(label="Gray color", command=grayImage)
imagemenu.add_command(label="BW color", command=binarizeImage)
imagemenu.add_command(label="Negative color", command=inverseImage)
imagemenu.add_command(label="Blur image", command=blurImage)
imagemenu.add_command(label="Edge detect", command=edgeImage)
imagemenu.add_command(label="Morph Trans Opening", command=openingMorphTransImage)
imagemenu.add_command(label="Morph Trans Closing", command=closingMorphTransImage)
imagemenu.add_command(label="Morph Trans OTH", command=othMorphTransImage)
imagemenu.add_command(label="Morph Trans CTH", command=cthMorphTransImage)
imagemenu.add_command(label="Voir l'histogramme", command=showHist)

menubar.add_cascade(label="Image", menu=imagemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=donothing)
helpmenu.add_command(label="About", command=donothing)

menubar.add_cascade(label="Help", menu=helpmenu)

label = Label(root, text="Select an image...", anchor=CENTER)
label.pack()

root.config(menu=menubar)
root.mainloop()
