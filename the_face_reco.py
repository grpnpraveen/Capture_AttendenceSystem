import numpy as np
import pickle
import face_recognition
import cv2
import os


# with open('train_data.pkl', 'rb') as f:
#     train_data = pickle.load(f)

# print("Train Data Loaded")



def compare_test_image(image,encoding):
    test_image_encoding = face_recognition.face_encodings(image)
    #print(test_image_encoding)
    if(len(test_image_encoding)==1):
        result = face_recognition.compare_faces([test_image_encoding[0]],encoding,tolerance=0.55)
        if result[0]==True:
            return 1
        else:
            return 0
    elif(len(test_image_encoding)==0):
        return 2
    elif(len(test_image_encoding)>1):
        return 3


def the_face_recognition(img,regno,train_data):
    # print("the_face_recognition is called....")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    check_number = 0
    # print("after check number")
    for values in train_data:
        if regno == values[1]:
            check_number=1
            check_image = compare_test_image(img,values[4])
            if(check_image==0):
                print("Number and Face Doesnt Match, Please exit try again")
                return("Number and Face Doesnt Match, Please exit try again")
            elif(check_image==1):
                print("Your attendance marked " + str(values[0]))
                return("Your attendance marked " + str(values[0]))
            elif(check_image==2):
                print("Cannot Find Face Properly, Please exit Try Again")
                return("Cannot Find Face Properly, Please exit Try Again")
            elif (check_image == 3):
                print("Multiple Faces Detected, Please exit try again") #Handling Multiple faces can be added
                return("Multiple Faces Detected, Please exit try again") #Handling Multiple faces can be added
    print("afetr loop")
    if(check_number==0):
        print("Number not found")
        return("Number not found")


# cap = cv2.VideoCapture(0)

# regno = input("Enter your Number : ")



# while True:
#     success,img = cap.read()
#     the_face_recognition(img, regno)

#     cv2.imshow("Image",img)
#     cv2.waitKey(1)


