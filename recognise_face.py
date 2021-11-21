
import face_recognition
import cv2
import pickle


def prepare_image(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    return image


def compare_test_image(image,encoding):
    image = prepare_image(image)
    test_image_encoding = face_recognition.face_encodings(image)
    #print(test_image_encoding)
    if(len(test_image_encoding)==1):
        result = face_recognition.compare_faces([test_image_encoding[0]],encoding,tolerance=0.6)
        #print(result)
        if result[0]==True:
            return 1
        else:
            return 0
    elif(len(test_image_encoding)==0):
        return 2
    elif(len(test_image_encoding)>1):
        return 3


with open('train_data2.pkl', 'rb') as f:
    train_data = pickle.load(f)


def find_compare(number,image):
    check_number = 0

    for values in train_data:
        if(values[1]==number):
            check_number=1


    if(check_number == 1):
        check_image = compare_test_image(image,values[4])
        if(check_image==0):
            return("Number and Face Doesnt Match, Please try again")
        elif(check_image==1):
            return("Your attendance marked " + str(values[0]))
        elif(check_image==2):
            return("Cannot Find Face Properly, Please Try Again")
        elif (check_image == 3):
            return("Multiple Faces Detected, Please try again") #Handling Multiple faces can be added

    else:
        return("Registration number not found")



# image = cv2.imread("Training Images/amir_03.jpg") #input Image




number = input("Enter your Number : ")
cap = cv2.VideoCapture(0)

while True:
    success,img = cap.read()
    a = find_compare(number,img)

    cv2.imshow("Image",img)
    cv2.waitKey(1)

    print(a)


#Show Image
# cv2.imshow("Image",image)
# cv2.waitKey(0)



