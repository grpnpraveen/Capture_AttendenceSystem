import pickle
import face_recognition
import cv2
import os

path = "Training Images"
train_data = []

myList = os.listdir(path)

for file_name in myList:
    temp = []
    image = cv2.imread(f'{path}/{file_name}')
    name_number = os.path.splitext(file_name)[0]
    name = name_number.split("_")[0]
    number = name_number.split("_")[1]

    encoding = face_recognition.face_encodings(image)[0] #Need to handle image not found error

    temp.append(name)
    temp.append(number)
    temp.append(file_name)
    temp.append(image)
    temp.append(encoding)
    train_data.append(temp)


output = open('train_data2.pkl', 'wb')
pickle.dump(train_data, output)



