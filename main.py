from _curses import window
from os import pread
from tkinter import *
from PIL import Image, ImageTk
import threading
import cv2
import numpy as np
from keras.backend import update

win = Tk()
win.title('Giám Sát Nhiệt Độ')
icon = Image.open('icon/male-student.png')
icon = icon.resize((70, 100), Image.ANTIALIAS)
print(icon)
icon = ImageTk.PhotoImage(icon)


width_screen = win.winfo_screenwidth()
hieght_screen = win.winfo_screenheight()
width = int((width_screen - 1000) / 2)
heigh = int((hieght_screen - 800) / 2)
win.geometry(f'1000x800+{width}+{heigh}')
# Label(win, bg='white').place(width=1000, heigh=800, x=0, y=0)


def openCam():
    global img_cam
    # facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # threshold = 0.90
    # cap = cv2.VideoCapture(0)
    # cap.set(3, 640)
    # cap.set(4, 480)
    # font = cv2.FONT_HERSHEY_COMPLEX
    # model = load_model('MyTrainingModel.h5')
    cap = cv2.VideoCapture(0)
    sucess, imgOrignal = cap.read()
    img_cam = cv2.cvtColor(imgOrignal, cv2.COLOR_BGR2RGB)
    img_cam = Image.fromarray(img_cam)
    img_cam = ImageTk.PhotoImage(img_cam)


def getCam():
    cap = cv2.VideoCapture(0)
    global img_cam, canvas
    # facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # threshold = 0.90
    # cap = cv2.VideoCapture(0)
    # cap.set(3, 640)
    # cap.set(4, 480)
    # font = cv2.FONT_HERSHEY_COMPLEX
    # model = load_model('MyTrainingModel.h5')
    def update():
        global canvas
        sucess, imgOrignal = cap.read(),
        # img_cam = cv2.cvtColor(imgOrignal, cv2.COLOR_BGR2RGB)
        # img_cam = Image.fromarray(img_cam)
        # img_cam = ImageTk.PhotoImage(img_cam)

        photo = ImageTk.PhotoImage(image=Image.fromarray(imgOrignal))
        canvas =Canvas.create_image(0, 0, image=photo, anchor=NW)

        canvas.place(width=400, heigh=400, x=500, y=100)
        win.after(10, update)


def main():
    global icon, img_cam, canvas, photo
    Label(win, text='Student').place(width=100, heigh=30, x=0, y=0)
    Label(win, image=icon).place(width=70, heigh=100, x=100, y=100)
    Label(win, text=f'name: student name').place(width=150, heigh=30, x=70, y=250)

    Label(win, text='Code').place(width=100, heigh=30, x=300, y=0)
    Label(win, image=icon).place(width=70, heigh=100, x=300, y=100)
    canvas = Canvas(win, bg='red')
    cap = cv2.VideoCapture(0)

    def update():
        global photo
        sucess, imgOrignal = cap.read()
        img_cam = cv2.cvtColor(imgOrignal, cv2.COLOR_BGR2RGB)
        # img_cam = Image.fromarray(img_cam)
        # img_cam = ImageTk.PhotoImage(img_cam)

        photo = ImageTk.PhotoImage(image=Image.fromarray(img_cam))
        canvas.create_image(0, 0, image=photo, anchor=NW)

        canvas.place(width=400, heigh=400, x=500, y=100)
        win.after(10, update)

    t1 = threading.Thread(target=update)
    t1.start()



# openCam()
main()
win.mainloop()