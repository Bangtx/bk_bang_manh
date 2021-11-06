from tkinter import *
from PIL import Image, ImageTk
import threading
import cv2
import warnings
import numpy as np
from keras.models import load_model
from pyzbar.pyzbar import decode
from database import DB
import pyttsx3

app_say = 'Please wear a mask'
say_init = pyttsx3.init()

win = Tk()
win.title('Giám Sát Nhiệt Độ')
icon = Image.open('icon/male-student.png')
icon = icon.resize((100, 120), Image.ANTIALIAS)
icon = ImageTk.PhotoImage(icon)

db = DB()
isCheckQrCode = True
id = None

width_screen = win.winfo_screenwidth()
hieght_screen = win.winfo_screenheight()
width = int((width_screen - 1200) / 2)
heigh = int((hieght_screen - 900) / 2)
win.geometry(f'1200x900+{width}+{heigh}')
Label(win, bg='white').place(width=1200, heigh=900, x=0, y=0)

warnings.filterwarnings('ignore')
facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
threshold = 0.90
font = cv2.FONT_HERSHEY_COMPLEX
model = load_model('MyTrainingModel.h5')


def preprocessing(img):
    img = img.astype("uint8")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    img = img / 255
    return img


def get_className(classNo):
    if classNo == 0:
        return "Mask"
    elif classNo == 1:
        return "No Mask"



def main():
    global icon, img_cam, canvas, photo, isCheckQrCode, id, say_init
    Label(win, text='Student').place(width=100, heigh=30, x=0, y=0)
    Label(win, image=icon).place(width=100, heigh=120, x=80, y=100)
    Label(win, text=f"Tên: ", font='times 16').place(width=200, heigh=30, x=30, y=250)
    Label(win, text=f"Lớp: ", font='times 16').place(width=200, heigh=30, x=30, y=300)
    Label(win, text=f"Giới Tính: ", font='times 16').place(width=200, heigh=30, x=30, y=350)

    Label(win, text='Code').place(width=100, heigh=30, x=400, y=0)
    Label(win, image=icon).place(width=100, heigh=120, x=380, y=100)

    list_student = Listbox(win)
    list_student.place(width=550, heigh=450, x=20, y=400)
    canvas = Canvas(win, bg='red')
    # canvas.place(width=550, heigh=450, x=600, y=50)
    cap = cv2.VideoCapture(0)

    def update():
        global photo, name, isCheckQrCode, id, say_init

        sucess, imgOrignal = cap.read()
        faces = facedetect.detectMultiScale(imgOrignal, 1.3, 5)
        if isCheckQrCode == False:
            for x, y, w, h in faces:
                # cv2.rectangle(imgOrignal,(x,y),(x+w,y+h),(50,50,255),2)
                # cv2.rectangle(imgOrignal, (x,y-40),(x+w, y), (50,50,255),-2)
                crop_img = imgOrignal[y:y + h, x:x + h]
                img = cv2.resize(crop_img, (32, 32))
                img = preprocessing(img)
                img = img.reshape(1, 32, 32, 1)
                # cv2.putText(imgOrignal, "Class" , (20,35), font, 0.75, (0,0,255),2, cv2.LINE_AA)
                # cv2.putText(imgOrignal, "Probability" , (20,75), font, 0.75, (255,0,255),2, cv2.LINE_AA)
                prediction = model.predict(img)
                classIndex = np.argmax(prediction, axis=1)
                probabilityValue = np.amax(prediction)
                if probabilityValue > threshold:
                    if classIndex == 0:
                        say_init.say(app_say)
                        say_init.runAndWait()
                        cv2.rectangle(imgOrignal, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.rectangle(imgOrignal, (x, y - 40), (x + w, y), (0, 255, 0), -2)
                        cv2.putText(imgOrignal, str(get_className(classIndex)), (x, y - 10), font, 0.75, (255, 255, 255), 1,
                                    cv2.LINE_AA)
                    elif classIndex == 1:
                        cv2.rectangle(imgOrignal, (x, y), (x + w, y + h), (50, 50, 255), 2)
                        cv2.rectangle(imgOrignal, (x, y - 40), (x + w, y), (50, 50, 255), -2)
                        cv2.putText(imgOrignal, str(get_className(classIndex)), (x, y - 10), font, 0.75, (255, 255, 255), 1,
                                    cv2.LINE_AA)
        else:
            for i in decode(imgOrignal):
                id = i.data.decode('utf-8')
                data_student = db.select_by_id(int(id))
                cv2.putText(imgOrignal, data_student[1], (70, 100), font, 2, (0, 255, 0), 1, cv2.LINE_AA)
                Label(win, text=f"Tên: {data_student[1]}", font='times 16').place(width=200, heigh=30, x=30, y=250)
                Label(win, text=f"Lớp:  {data_student[2]}", font='times 16').place(width=200, heigh=30, x=30,
                                                                                         y=300)
                Label(win, text=f"Giới Tính:  {data_student[3]}", font='times 16').place(width=200, heigh=30, x=30,
                                                                                             y=350)
                isCheckQrCode = False
                id = None


        img_cam = cv2.cvtColor(imgOrignal, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(img_cam).resize((550, 450), Image.ANTIALIAS))
        canvas.create_image(0, 0, image=photo, anchor=NW)
        canvas.place(width=550, heigh=450, x=600, y=50)
        win.after(10, update)
        # cv2.imshow("Result", imgOrignal)
        # k = cv2.waitKey(0)

    t1 = threading.Thread(target=update)
    t1.start()



# openCam()
main()
win.mainloop()