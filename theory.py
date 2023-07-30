from RPi.GPIO import GPIO
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from picamera import PiCamera

path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]
    encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

camera = PiCamera()

baseURL = 'https://api.thingspeak.com/update?api_key=MI7DQFJ0OTMK4UFF&field1=0'

while True:
    
    now=datetime.now()
    dt=now.strftime("%d%m%Y%H:%M:%S")
    name=dt+".jpg"
    imgS = camera.capture(name)
    print("captured")
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
     
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
     
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
    #print(faceDis)
    
    if np.min(faceDis)<=0.5:
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex]
            print(name)
            att=[]
            for i range(len(classNames)):
                if(i!=matchIndex):
                    att.append(0)
                else:
                    att.append(1)
                
            conn = urlopen(baseURL + '&field1=%s ' % (att[0]))
            conn = urlopen(baseURL + '&field2=%s ' % (att[1]))
            conn = urlopen(baseURL + '&field3=%s ' % (att[2]))
            conn = urlopen(baseURL + '&field4=%s ' % (att[3]))
            conn = urlopen(baseURL + '&field5=%s ' % (att[4]))
            
            conn.close()
    else:   
        print("Person not identified")