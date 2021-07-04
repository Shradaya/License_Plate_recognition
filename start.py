from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton,QProgressBar,QLabel,QVBoxLayout,QHBoxLayout,QGroupBox,QDialog,QGridLayout
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import sys
import pygame
import copy
from PyQt5.QtWidgets import QLineEdit
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize 
import subprocess
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
import time

import cv2
import numpy as np
import os
import Main
import DetectChars
import DetectPlates
import PossiblePlate
import FireDatabase

licPlateNumber="N/A"
imageNo=0
status=0

def selfInitiate(number):
    global licPlateNumber
    licPlateNumber = number
    print("The Input License Plate Number is:" + licPlateNumber)
    databaseconstant = FireDatabase.retrieve(licPlateNumber)
    if(databaseconstant==None):
        print("The Vehicle has not been booked for any parking space in this parking station: ACCESS DENIED")
        global status
        status=-1
    else:
        eoe = FireDatabase.checkforentryorexit(licPlateNumber)
        if(eoe==None):
            status=-1
            print("The Vehicle has not been booked for any parking space in this parking station: ACCESS DENIED")
        elif(eoe=='entry'):
            print("**********Access Granted**********")
            status=1
        elif(eoe=='exit'):
            status=0
            print('**********Drive Safely**********')
    return
  

def initiate():
    global imageNo
    if(imageNo==1):
        imgOriginalScene  = cv2.imread("LicPlateImages/1.jpg")
#        imgOriginalScene  = cv2.imread("LicPlateImages/3.png")
    if(imageNo==2):
        imgOriginalScene  = cv2.imread("LicPlateImages/2.jpeg")

    if imgOriginalScene is None:
        print("\nerror: image not read from file \n\n")
        os.system("pause")
        return

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)


    if len(listOfPossiblePlates) == 0:
        print("\nno license plates were detected\n")
    else:

        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)
        licPlate = listOfPossiblePlates[0]


        if len(licPlate.strChars) == 0:
            print("\nno characters were detected\n\n")
            return

        global licPlateNumber
        licPlateNumber = finalPolish(licPlate.strChars)
        licPlate.strChars = licPlateNumber
        print("\nlicense plate read from image = " + licPlateNumber + "\n")
        print("----------------------------------------")
        databaseconstant = FireDatabase.retrieve(licPlateNumber)
        if(databaseconstant==None):
            print("The Vehicle has not been booked for any parking space in this parking station: ACCESS DENIED")
            global status
            status=-1
        else:
            eoe = FireDatabase.checkforentryorexit(licPlateNumber)
            if(eoe==None):
                status=-1
                print("The Vehicle has not been booked for any parking space in this parking station: ACCESS DENIED")
            elif(eoe=='entry'):
                print("**********Access Granted**********")
                status=1
            elif(eoe=='exit'):
                status=0
                print('**********Drive Safely**********')
    return


def finalPolish(number):
    lst = []
    string=number
    if(len(number)<=4):
        string = 'BAA' + number
        finalPolish(string)
    if (len(number)==7):
        for i in range(7):
            lst.append(number[i])
        for i in range(3):
            if(ord(lst[i])>=65 and ord(lst[i])<=90):
                continue
            elif (lst[i] == '4'):
                lst[i]='A'
            elif lst[i] == '8':
                lst[i]='B'
            elif(lst[i]=='1'):
                lst[i]='L'
            elif(lst[i]=='6'):
                lst[i]='B'
        for i in range(3,7):
            if(ord(lst[i])>=48 and ord(lst[i])<=57):
                continue
            elif (lst[i]=='G'):
                lst[i]='0'
            elif (lst[i]=='B' or lst[i]=='K'):
                lst[i]='9'
            elif (lst[i]=='D'):
                lst[i]='6'
            elif(lst[i]=='A'):
                lst[i]='4'
            elif(lst[i]=='H'):
                lst[i]='4'
            elif(lst[i]=='C'):
                lst[i]='6'
        string=''.join(lst)
        print(string)
    return string



pygame.init()
#pygame.mixer.music.load('sound/music.mp3')
#pygame.mixer.music.play(-1)

class Window(QMainWindow,QLabel):
    def __init__(self):
        super().__init__()
        self.title="Automated Parking System"
        self.icon="win.ico"
        self.InitWindow()
        

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setStyleSheet("QMainWindow{background-image:url(image/bg.jpg)}")
        self.setFixedSize(1024,768)
        self.UIcomponents()
        self.show()

    def UIcomponents(self):
        startbtn=QPushButton("START.",self)
        startbtn.move(350,160)
        startbtn.setFixedSize(150,50)
        startbtn.setIcon(QtGui.QIcon("image/start.ico"))
        startbtn.setStyleSheet("QPushButton{color:white;background-color:brown;border-radius:25px;border: 8px solid white;font: bold}"
        "QPushButton:pressed{color:black;background-color:green}")
        startbtn.clicked.connect(self.start1)

        startbtn=QPushButton("START..",self)
        startbtn.move(550,160)
        startbtn.setFixedSize(150,50)
        startbtn.setIcon(QtGui.QIcon("image/start.ico"))
        startbtn.setStyleSheet("QPushButton{color:white;background-color:brown;border-radius:25px;border: 8px solid white;font: bold}"
        "QPushButton:pressed{color:black;background-color:green}")
        startbtn.clicked.connect(self.start2)
        
        recordbtn=QPushButton("LATEST RECORD",self)
        recordbtn.move(425,260)
        recordbtn.setFixedSize(200,50)
        recordbtn.setIcon(QtGui.QIcon("image/record.ico"))
        recordbtn.setStyleSheet("QPushButton{color:white;background-color:brown;border-radius:25px;border: 8px solid white;font: bold}"
        "QPushButton:pressed{color:black;background-color:green}")
        recordbtn.clicked.connect(self.record)

        feedbackbtn=QPushButton("Feedback",self)
        feedbackbtn.setIcon(QtGui.QIcon("image/feedback.png"))
        feedbackbtn.move(450,460)
        feedbackbtn.setFixedSize(150,50)
        feedbackbtn.setStyleSheet("QPushButton{color:white;background-color:brown;border-radius:25px;border: 8px solid white;font: bold}"
        "QPushButton:pressed{color:black;background-color:green}")
        feedbackbtn.clicked.connect(self.feedbackWindow)

        teambtn=QPushButton("Self Input",self)
        teambtn.setIcon(QtGui.QIcon("image/input.png"))
        teambtn.move(450,360)
        teambtn.setFixedSize(150,50)
        teambtn.setStyleSheet("QPushButton{color:white;background-color:brown;border-radius:25px;border: 8px solid white;font: bold}"
        "QPushButton:pressed{color:black;background-color:green}")
        teambtn.clicked.connect(self.selfInput)

        exitbtn=QPushButton("EXIT",self)
        exitbtn.move(450,560)
        exitbtn.setFixedSize(150,50)
        exitbtn.clicked.connect(self.close)
        exitbtn.setIcon(QtGui.QIcon("image/exit.png"))
        exitbtn.setStyleSheet("QPushButton{color:white;background-color:brown;border-radius:25px;border: 8px solid white;font: bold}"
        "QPushButton:pressed{color:black;background-color:green}")

        mutebtn=QPushButton("",self)
        mutebtn.setIcon(QtGui.QIcon("image/mute.png"))
        mutebtn.move(980,670)
        mutebtn.setFixedSize(35,30)
        mutebtn.clicked.connect(self.off)
        mutebtn.setStyleSheet("QPushButton{color:white;background-color:white;border-radius:25px;border: none}"
        "QPushButton:pressed{color:black;background-color:green}")

        musicbtn=QPushButton("",self)
        musicbtn.setIcon(QtGui.QIcon("image/music.png"))
        musicbtn.move(10,670)
        musicbtn.setFixedSize(35,30)
        musicbtn.clicked.connect(self.on)
        musicbtn.setStyleSheet("QPushButton{color:white;background-color:white;border-radius:25px;border: none}"
        "QPushButton:pressed{color:black;background-color:green}")

    def start1(self):
        self.progress = QProgressBar(self)
        self.progress.setGeometry(345, 300, 400, 100)
        self.progress.setStyleSheet("QProgressBar{color:white;font-size:30px}")
        self.completed = 0
        self.progress.show()
        while self.completed < 100:
            self.completed += 0.0001
            self.progress.setValue(self.completed)
            self.progress.show()
        self.progress.hide()
        global imageNo
        imageNo=1
        initiate()
        self.record()
  
    def start2(self):
        self.progress = QProgressBar(self)
        self.progress.setGeometry(345, 300, 400, 100)
        self.progress.setStyleSheet("QProgressBar{color:white;font-size:30px}")
        self.completed = 0
        self.progress.show()
        while self.completed < 100:
            self.completed += 0.0001
            self.progress.setValue(self.completed)
            self.progress.show()
        self.progress.hide()
        
        global imageNo
        imageNo=2
        initiate()
        self.record()

    def close(self):
        sys.exit()
    
    def bookings(self):
        self.f=Feedback()
        self.f.show()
    
    def off(self):
        pygame.mixer.music.stop()
    
    def on(self):
        pygame.mixer.music.play()
    
    def record(self):
        self.r=Message()
        self.r.show()
        #print(licPlateNumber)
    
    def records(self):
        subprocess.call('.\data.csv')
        
    def feedbackWindow(self):
        self.w=Feedback()
        self.w.show()

    def selfInput(self):
        self.w=adminInput()
        self.w.show()
        
 

 

class adminInput(QDialog):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(320, 140))    
        self.setWindowTitle("Input License Plate") 

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Number:')
        self.line = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200,32)
        pybutton.move(80, 60)        

    def clickMethod(self):
        self.close()
        selfInitiate(self.line.text())
        self.r=Message()
        self.r.show()

        

class Records(QLabel,QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("image/record.ico"))
        self.setWindowTitle("Latest Record")
        self.setMinimumSize(QSize(320, 140))
#        self.setFixedSize(500,200)
        vbox=QVBoxLayout()
        record=QLabel("Latest Number Plate : "+ licPlateNumber)
        record.setFont(QtGui.QFont("Sanserif",18))
        vbox.addWidget(record)
        self.setLayout(vbox)
            
class Feedback(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Feedback")
        self.setWindowIcon(QtGui.QIcon("image/feedback.png"))
        self.setGeometry(500,400,400,100)
        self.setStyleSheet("QDialog{}")
        self.createlayout()
        vbox=QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)
    
    def createlayout(self):
        self.groupBox=QGroupBox("How was your experience ?")
        gridlayout=QGridLayout()

        badbtn=QPushButton("Bad",self)
        badbtn.setMinimumHeight(40)
        badbtn.clicked.connect(exit)
        gridlayout.addWidget(badbtn,0,0)

        satisfybtn=QPushButton("Satisfying",self)
        satisfybtn.setMinimumHeight(40)
        satisfybtn.clicked.connect(exit)
        gridlayout.addWidget(satisfybtn,0,1)

        goodbtn=QPushButton("Good",self)
        goodbtn.setMinimumHeight(40)
        goodbtn.clicked.connect(exit)
        gridlayout.addWidget(goodbtn,1,0)

        exgood=QPushButton("Extremely Good",self)
        exgood.setMinimumHeight(40)
        exgood.clicked.connect(exit)
        gridlayout.addWidget(exgood,1,1)

        self.groupBox.setLayout(gridlayout)

class Message(QLabel,QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("image/alert.ico"))
        self.setWindowTitle("Alert")
        self.setMinimumSize(QSize(600, 200))
        vbox=QVBoxLayout()
        global status
        if(status==1):
#            global licPlateNumber
            record=QLabel("*******Access Granted*******\nLicense Plate: "+str(licPlateNumber))
        elif(status==0):
            record=QLabel("*********Drive Safely*********\nLicense Plate: "+str(licPlateNumber))
            #licPlateNumber="N/A"
        elif(status==-1):
            record=QLabel("Denied:Unbooked Vehicle\nLicense Plate: "+str(licPlateNumber))
            #licPlateNumber="N/A"
        elif(status==-2):
            record=QLabel("Latest Record: N/A")
        record.setFont(QtGui.QFont("Sanserif",18))
        vbox.addWidget(record)
        self.setLayout(vbox)



App=QApplication(sys.argv)
window=Window()
sys.exit(App.exec())
