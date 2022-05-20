from tkinter import filedialog
from PoseModule import PoseDetector
import cv2
import numpy as np
from tkinter import*
from PIL import Image, ImageTk
import mediapipe as mp

#### GLOBAL VARIABLES ###
global cap, Analysis
global var1, frame_1
global win, label1, v, q, Next
adit = 0
SajCount = 0

check = False
Draw = False
Analysis = False
Update = False
CheckAgain = True


Prayer = {'Takbir': False, 'Qayam': False, 'Ruku':False, 'Qomah': False, 'Sajdah': False, 'Atahyaat': False}
cap = cv2.VideoCapture(0)
detector = PoseDetector()

mpPose=mp.solutions.mediapipe.python.solutions.pose # From different
mpDraw=mp.solutions.mediapipe.python.solutions.drawing_utils

### FUNCTION TO CALCULATE ANGLES###
def Angle(First, Second, Third):
    Pa_X = lmlist[First][1]
    Pa_Y= lmlist[First][2]

    Pb_X = lmlist[Second][1]
    Pb_Y= lmlist[Second][2]

    Pc_X = lmlist[Third][1]
    Pc_Y= lmlist[Third][2]

    a = [Pa_X, Pa_Y]
    b = [Pb_X, Pb_Y]
    c = [Pc_X, Pc_Y]
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180:
        angle = 360-angle
        
    return angle


### FUNCTION FOR START LIVE BUTTON ###
def Starting():
    global Analysis, Update, wid, heit, label1
    
    wid = 612
    heit = 450
    label1.configure(width = wid, height = heit)
    label1.place(x=450, y=180)
   
    Analysis = True
    Update = True

### FUNCTION FOR START RECORDED BUTTON ###
def RecordedVideo():
    global win, label1, cap, wid, heit, Analysis, Update, check
    cap.release()
    win.filename = filedialog.askopenfilename(initialdir = "/Users/hp/Desktop/Mediapipe",  \
    title = "Select Recorded Videos")

    label1.destroy()
    label1 = Label(frame_1, width = 600, height= 400, bg= "#2C2F33")
    
    if win.filename:
        cap = cv2.VideoCapture(win.filename)
        label1.place(x=450, y=180)
        Analysis = True
        Update = True
        wid = 236
        heit = 400
    else:
        cap = cv2.VideoCapture(0)
        Analysis = False
        check = False
        Update = False
        label1.configure(width = 210, height= 100)
        label1.place(x=860, y=300)
        wid = 140
        heit = 80
        

    LiveVideo()
    select_img()


### FUNCTION FOR EXIT TO MAIN MENU BUTTON
def MMenu():
    global Analysis, DetectionLabel, label1, wid, heit, cap, MainMenu, check, img, rgb, DetectMssg
    global image, Update, DrawScl, NextMssg, Draw 
    
    cap.release()

    DetectionLabel.destroy()
    label1.destroy()
    DrawScl.destroy()
    MainMenu.destroy()
    DetectMssg.destroy()
    NextMssg.destroy()

    Draw = False
    Analysis = False
    check = False
    Update = False
    label1 = Label(frame_1, width = 210, height= 100, bg= "#2C2F33")
    label1.place(x=860, y=300)
    wid = 140
    heit = 80
    cap = cv2.VideoCapture(0)
    LiveVideo()
    welcome()

### fUNCTION FOR DRAW SCALE BUTTON ###
def callback1(value):
    global Draw
    if Draw:
        Draw = False
    else:
        Draw = True


### FUNCTION FOR STARTING VIDEO PROCESING ###
def LiveVideo():
    global cap, img, _, wid, heit, rgb, image, finalImage
    _, img = cap.read()
    img = cv2.resize(img, (wid, heit))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb =cv2.flip(rgb, 1)
    image = Image.fromarray(rgb)
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage
    
### MAIN ANALYSYS FUNCTION ###
def select_img():
    global img, finalImage, image, rgb, _, wid, heit, lmlist, check, Update, label1
    global cap, v, q, pos, Next, CheckAgain, SajCount

    _, img = cap.read()
    img = cv2.resize(img, (wid, heit))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb =cv2.flip(rgb, 1)

    #img = detector.findPose(img)
    #lmlist, bbxInf = detector.findPosition(img, bboxWithHands=True)
    lmlist = []

    if Update:
        AnalysisWinUpdate()
        Update = False
    
    if Analysis:
        detector.results = detector.pose.process(rgb)
        if detector.results.pose_landmarks:
            check = True
            for id, lm in enumerate(detector.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                lmlist.append([id, cx, cy, cz])

                if Draw:
                    detector.mpDraw.draw_landmarks(rgb, detector.results.pose_landmarks, detector.mpPose.POSE_CONNECTIONS)
        else:
            check = False

    #print(check)
    
    if check:
        Nose_Y=lmlist[0][2]

        IndexRight_X=lmlist[20][1]
        IndexRight_Y=lmlist[20][2]

        IndexLeft_X=lmlist[19][1]
        IndexLeft_Y=lmlist[19][2]

        MouthRight_Y=lmlist[10][2]  
        MouthLeft_Y=lmlist[9][2]

        KneeRight_X=lmlist[26][1] 
        KneeRight_Y=lmlist[26][2]

        KneeLeft_X=lmlist[25][1]  
        KneeLeft_Y=lmlist[25][2] 

        HipRight_Y=lmlist[24][2]  
        HipLeft_Y=lmlist[23][2]

        ShoulderRight_Y=lmlist[12][2]  
        ShoulderLeft_Y=lmlist[11][2]

        AnkleRight_X=lmlist[28][1] 
        AnkleRight_Y=lmlist[28][2]

        AnkleLeft_X=lmlist[27][1]   
        AnkleLeft_Y=lmlist[27][2]

        ToeRight_X =lmlist[32][1]   
        ToeLeft_X = lmlist[31][1]

        KneeAngle = int(Angle(23, 25, 27))
        ElbowAngle = int(Angle(11, 13, 15))

        adit = abs(ShoulderRight_Y - HipRight_Y)
        adit = adit/2

        if IndexRight_Y<ShoulderRight_Y and IndexLeft_Y<ShoulderLeft_Y:
            Prayer['Takbir'] = True
        else:
            Prayer['Takbir'] = False

        if IndexRight_X>IndexLeft_X and (KneeAngle > 165):
            Prayer['Qayam'] = True
        else:
            Prayer['Qayam'] = False

        if ((IndexRight_Y>(HipRight_Y + (KneeRight_Y-HipRight_Y)/2) or \
            (IndexLeft_Y>(HipLeft_Y + (KneeLeft_Y-HipLeft_Y)/2))) and \
            ((KneeAngle) > 165)):
            Prayer['Ruku'] = True
        else:
            Prayer['Ruku'] = False

        if IndexRight_Y>HipRight_Y and IndexLeft_Y>HipRight_Y and ((KneeAngle) > 165):
            Prayer['Qomah'] = True
        else:
            Prayer['Qomah'] = False

        if (ToeLeft_X < AnkleLeft_X) or (ToeRight_X < AnkleRight_X):
            if  ((Nose_Y > ShoulderRight_Y) or (Nose_Y > ShoulderLeft_Y)) and \
            ((HipRight_Y < ShoulderRight_Y) or (HipLeft_Y < ShoulderLeft_Y)) and \
            ((IndexRight_X > KneeRight_X) or (IndexLeft_X > KneeLeft_X)) and \
            (KneeAngle < 80) and (ElbowAngle < 100):
                Prayer['Sajdah'] = True
            else:
                Prayer['Sajdah'] = False
        
        if (ToeLeft_X > AnkleLeft_X) or (ToeRight_X > AnkleRight_X):
            if  ((Nose_Y > ShoulderRight_Y) or (Nose_Y > ShoulderLeft_Y)) and \
            ((HipRight_Y < ShoulderRight_Y) or (HipLeft_Y < ShoulderLeft_Y)) and \
            ((IndexRight_X < KneeRight_X) or (IndexLeft_X < KneeLeft_X)) and \
            (KneeAngle < 80) and (ElbowAngle < 100):
                Prayer['Sajdah'] = True
            else:
                Prayer['Sajdah'] = False

        if (((HipRight_Y > (AnkleRight_Y - adit)) or (HipLeft_Y > (AnkleLeft_Y - adit))) \
            and ((KneeAngle) < 30)):
            Prayer['Atahyaat'] = True
        else:
            Prayer['Atahyaat'] = False

        if Prayer['Takbir']:
            v.set("Takbir")
        elif Prayer['Sajdah']:
            v.set("Sajdah")
        elif Prayer['Ruku']:
            v.set("Ruku")
        elif Prayer['Atahyaat']:
            v.set("Atahyaat")
        elif Prayer['Qomah']:
            v.set("Qomah")
        elif Prayer['Qayam']:
            v.set("Qayam")
        else:
            v.set("None")

        if Prayer["Sajdah"] and CheckAgain:
            SajCount += 1
            CheckAgain = False
        if (not Prayer["Sajdah"]) and Prayer["Atahyaat"]:
            CheckAgain = True


        pos = v.get()
        pos = "Your current position is " + pos
        q.set(pos)

        pos = "The next position should be "
        if v.get() == 'Takbir':
            nex = "Qayam"
        elif v.get() == 'Qayam':
            nex = "Ruku"
        elif v.get() == 'Ruku':
            nex = "Qomah"
        elif v.get() == 'Qomah':
            nex = "Sajdah"
        elif v.get() == 'Sajdah':
            nex = "Atahyaat"
        elif v.get() == 'Atahyaat' and SajCount == 1:
            nex = "Sajdah"
        elif v.get() == 'Atahyaat' and SajCount>1:
            nex = "Salam"
        else:
            pos = ""
            nex = ""
        pos = pos + nex
        Next.set(pos)

    
    image = Image.fromarray(rgb)
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage
    win.after(1, select_img)

def welcome():
    global StartLive, welc1, welc2, welc3, welc4, label1, wid, heit, WelcMsg, Exit, win, StartRecord

    WelcMsg = StringVar()
    WelcMsg.set("WELCOME TO THE PRAYER ANALYSIS MEDIAPIPE PROJECT")
    welc1 = Message(win, justify = CENTER, textvariable = WelcMsg, font = ("Times", 20), bg = "#2C2F33", \
    fg = "green", relief = FLAT, width = 1000)
    welc1.place(x = 220, y = 20)

    welc2 = Message(win, justify = CENTER, font = ("Times", 18), bg = "#2C2F33", fg = "green", \
    text= "A Project by Mechatronics Department, University of Engineering and Technology, Lahore",\
    width = 1000,relief = FLAT)
    welc2.place(x = 170, y = 80)

    welc3 = Message(win, justify = CENTER, text= "Press START to begin your analysis", \
    font = ("Times", 14), bg = "#2C2F33", fg = "green", relief = FLAT,\
    width = 1000)
    welc3.place(x = 480, y = 420)

    welc4 = Message(win, justify = CENTER, text= "Developers:                      Awais Zafar (2020-MC-02)\
                                        Fawaz Mahmood Mughal (2020-MC-26)", \
    font = ("Times", 16), bg = "#2C2F33", fg = "green", relief = FLAT, width = 1000)
    welc4.place(x = 20, y = 600)


    StartLive=Button(win,text='Start Live Video', width = 14, fg = "#88B04B", bg = "#DD4124", padx=10,pady=10,\
    command= Starting, relief = RAISED)
    StartLive.place(x = 450, y = 475)

    StartRecord =Button(win,text='Start Recorded Video', width = 14, fg = "#88B04B", bg = "#DD4124",\
    padx=10,pady=10, relief = RAISED, command = RecordedVideo)
    StartRecord.place(x = 685, y = 475)

    Exit = Button(win,text='Exit Program', width = 10, fg = "#88B04B", bg = "#DD4124", padx=10,pady=10,\
    command= win.destroy, relief = RAISED)
    Exit.place(x = 580, y = 530)

    
def AnalysisWinUpdate():
    global v, q, pos, wid, heit, label1, StartLive, welc1, welc2, welc3, welc4
    global DetectionLabel, MainMenu, DrawScl, WelcMsg, DetectMssg, NextMssg, Next

    StartLive.destroy()
    StartRecord.destroy()
    welc2.destroy()
    welc3.destroy()
    welc4.destroy()
    Exit.destroy()

    WelcMsg.set("Prayer Analysis Project")
    welc1.config(font = ("Times", 25))
    welc1.place(x = 460, y = 20)

    DetectionLabel=Label(win,width=40,borderwidth=5, height = 2, font = ("Times", 21), \
    bg = "#99AAB5", fg= "#5865F2", textvariable= v, relief=FLAT)
    DetectionLabel.place(x = 452, y = 104)

    if (wid == 236 and heit == 400):
        DetectionLabel.place(x = 634, y = 104)
        DetectionLabel.configure(width = 15)

    MainMenu=Button(win,text='Exit to Main Menu', width = 14, fg = "#88B04B", bg = "#DD4124",\
    padx=10,pady=10, relief = RAISED, command = MMenu, font = ("Times", 15))
    MainMenu.place(x = 70, y = 550)

    DrawScl = Scale(win, label="Draw Landmarks", from_ =0, to=1, orient=HORIZONTAL, command = callback1,\
    activebackground='#339999', bg = "#B7410E", length= 170, font = ("Times", 15), fg = "#88B04B",\
    troughcolor= "#798EA4", relief= FLAT)
    DrawScl.set(0)
    DrawScl.place(x=70, y=455)
    
    DetectMssg = Message(win, justify = CENTER, font = ("Times", 18), bg = "#2C2F33", fg = "green", \
    textvariable= q, width = 200,relief = FLAT)
    DetectMssg.place(x = 70, y = 100)

    NextMssg = Message(win, justify = CENTER, font = ("Times", 18), bg = "#2C2F33", fg = "green", \
    textvariable= Next, width = 200,relief = FLAT)
    NextMssg.place(x = 70, y = 220)

win = Tk()
wid = win.winfo_screenwidth()
heit = win.winfo_screenheight()
win.geometry("%dx%d" % (wid, heit))
win.title('Prayer Analysis Project')
frame_1 = Frame(win, width=wid, height=heit, bg= "#2C2F33").place(x=0, y=0)
label1 = Label(frame_1, width = 600, height= 400, bg= "#2C2F33")
label1.place(x=700, y=160)
wid = 110
heit = 60

v = StringVar()
q = StringVar()
Next = StringVar()
if not Analysis:
    welcome()

select_img() 
win.mainloop()