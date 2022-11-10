# from cProfile import label
# from turtle import right
import face_recognition as fr
import cv2 
from tkinter import BOTTOM, Tk
from tkinter.filedialog import askopenfilename
import os
import time
Tk().withdraw()
load_image = askopenfilename()

target_image = fr.load_image_file(load_image)
target_encoding = fr.face_encodings(target_image)


# Searches for occurrences of this face

def encode_faces(folder):
    list_people_encoding = []

    for filename in os.listdir(folder):

        known_image = fr.load_image_file(f'{folder}{filename}')

        known_encoding = fr.face_encodings(known_image)[0]

        list_people_encoding.append((known_encoding, filename))

    return list_people_encoding


def find_target_face():
    face_location = fr.face_locations(target_image)


    for person in encode_faces('people/'):

        encoded_face = person[0]

        filename = person[1]

        is_target_face = fr.compare_faces(encoded_face, target_encoding, tolerance=0.55)
        print(f' {is_target_face} {filename}')

        if face_location:
            face_number = 0
            for location in face_location:

                if is_target_face[face_number]:
                    label = filename
                    create_frame(location, label)


            face_number +=1

        



def create_frame(location,label):
        top, right, bottom, left = location
        cv2.rectangle(target_image, (left,top), (right,bottom),(255,0,0), 2)
        cv2.rectangle(target_image, (left,bottom+20), (right,bottom),(255,0,0), cv2.FILLED)
        cv2.putText(target_image, label, (left + 3, bottom + 14), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255,255,255), 1)

def render_image():
    # if img_path != None:
    #     print(f"[INFO] Working with image: {img_path}")
    #     frame = cv2.imread(img_path)

    rgb_img = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
    cv2.imshow('Face Recognition', rgb_img)
    cv2.waitKey(0)

find_target_face()
render_image()
