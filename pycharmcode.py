import numpy as np
import pickle
import face_recognition
import cv2
import os

#path = "Train"
#train_data = []
#myList = os.listdir(path)

with open('train_data.pkl', 'rb') as f:
    train_data = pickle.load(f)

print("Train Data Loaded")


def prepare_image(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    return image


def compare_images(image1,image2):
    pass


def compare_test_image(image,encoding):
    image = prepare_image(image)
    test_image_encoding = face_recognition.face_encodings(image)
    #print(test_image_encoding)
    if(len(test_image_encoding)==1):
        result = face_recognition.compare_faces([test_image_encoding[0]],encoding,tolerance=0.55)
        #print(result)
        if result[0]==True:
            return 1
        else:
            return 0
    elif(len(test_image_encoding)==0):
        return 2
    elif(len(test_image_encoding)>1):
        return 3




def find_compare(number,image):
    check_number = 0

    for values in train_data:
        if number == values[1]:
            check_number=1
            check_image = compare_test_image(image,values[4])
            if(check_image==0):
                print("Number and Face Doesnt Match, Please try again")
            elif(check_image==1):
                print("Your attendance marked " + str(values[0]))
            elif(check_image==2):
                print("Cannot Find Face Properly, Please Try Again")
            elif (check_image == 3):
                print("Multiple Faces Detected, Please try again") #Handling Multiple faces can be added

    if(check_number==0):
        print("Number not found")


cap = cv2.VideoCapture(0)

number = input("Enter your Number : ")


while True:
    success,img = cap.read()
    find_compare(number, img)

    cv2.imshow("Image",img)
    cv2.waitKey(1)

    # image = cv2.imread("Test/harshith_img.jpg") #input Image





#Show Image
# cv2.imshow("Image",image)
# cv2.waitKey(0)



