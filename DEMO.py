from optparse import Values
from sre_constants import SUCCESS
from traceback import print_last
import cv2
from mysqlx import SqlStatement
import numpy as np
import face_recognition
import os
import mysql.connector
#from mysqlx import SqlStatement

MyDB = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "123405",
    database = "Tutorial"
)


MyCursor = MyDB.cursor()

#MyCursor.execute("""CREATE TABLE IF NOT EXISTS Images (id INTEGER(45) NOT NULL AUTO_INCREMENT PRIMARY KEY, Photo LONGBLOB NOT NULL, Name VARCHAR(30)""")
MyCursor.execute('''CREATE TABLE IF NOT EXISTS images(id INTEGER(45) NOT NULL AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(30))''')

# Insert Images
def InsertBlob(name):
    #print(path,namelist)
    #name1=list(name)
    SQLStatement1 = "INSERT INTO images (Name) VALUES (%s)"
    MyCursor.execute(SQLStatement1, list(name))
    #MyCursor.execute(f'''INSERT INTO images (Name) VALUES {namelist}''')
    MyDB.commit()

# Retrieve Images
def RetrieveBlob():
    MyCursor.execute('''SELECT * FROM images ORDER BY id DESC LIMIT 1;''')
    MyResult = MyCursor.fetchone()[1]
    #print(MyResult)
    return MyResult

def fun(name):
    s = RetrieveBlob()
    print(s)
    if s not in namelist:
        InsertBlob(name)
        #print(name)
    elif s in namelist:
        return None

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

#def main1(img):
cap = cv2.VideoCapture('webcam_facemask_result.avi')
    #cap = img
while True:
    success, img = cap.read()
        # img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            
            namelist=[]
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            namelist.append(name)
            #print(name)
            fun(namelist)  
                
                    
            # markAttendance(name)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()










# InsertBlob(imgB)



#RetrieveBlob(id)