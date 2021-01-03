from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image

from tools.image_process import *


def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()


def openImage():
    global label
    global imageFile

    imageFile = filedialog.askopenfilename(initialdir="~/Pictures", title="Open an image",
                                           filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png")))

    img = ImageTk.PhotoImage(Image.open(imageFile))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def rotateImage(direction):
    global label
    global imageFile

    angle = 90

    if direction == "RIGHT":
        angle *= -1

    image = rotate(cv2.imread(imageFile), angle)

    img = ImageTk.PhotoImage(Image.fromarray(image))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def binarizeImage():
    global label
    global imageFile

    image = binarize(cv2.imread(imageFile), 128)
    img = ImageTk.PhotoImage(Image.fromarray(image))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def inverseImage():
    global label
    global imageFile

    image = inverse(cv2.imread(imageFile))
    img = ImageTk.PhotoImage(Image.fromarray(image))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def adjustConImage():
    global label
    global imageFile

    image = equalizeHist(cv2.imread(imageFile))
    img = ImageTk.PhotoImage(Image.fromarray(image))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def adjustLumImage():
    global label
    global imageFile

    image = stretchHist(cv2.imread(imageFile), 64, 192)
    img = ImageTk.PhotoImage(Image.fromarray(image))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def blurImage():
    global label
    global imageFile

    image = blur(cv2.imread(imageFile))
    img = ImageTk.PhotoImage(Image.fromarray(image))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def edgeImage():
    global label
    global imageFile

    image = edge(cv2.imread(imageFile))
    img = ImageTk.PhotoImage(Image.fromarray(image))

    label.pack_forget()
    label = Label(image=img, anchor=CENTER)
    label.image = img
    label.pack()


def showHist():
    global imageFile

    hist = computeHist(cv2.imread(imageFile))
    plt.plot(hist)
    plt.xlabel('Gray level')
    plt.ylabel('Count')
    plt.title("Histogram of the image in gray level")
    plt.show()


root = Tk()
root.title("AIVO")
root.geometry("800x600")
# root.resizable(width=False, height=False)

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openImage)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Close", command=donothing)
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
imagemenu.add_command(label="BW color", command=binarizeImage)
imagemenu.add_command(label="Negative color", command=inverseImage)
imagemenu.add_command(label="Blur image", command=blurImage)
imagemenu.add_command(label="Edge detect", command=edgeImage)
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
