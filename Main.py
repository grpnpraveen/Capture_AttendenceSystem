import cv2
from flask import Flask,render_template,Response,request,redirect,url_for,jsonify
import os
import datetime, time
import numpy as np
import face_recognition
import pickle

with open('train_data.pkl', 'rb') as f:
    train_data = pickle.load(f)


def prepare_image(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    return image


def compare_test_image(image,encoding):
    image = prepare_image(image)
    test_image_encoding = face_recognition.face_encodings(image)
    #print(test_image_encoding)
    if(len(test_image_encoding)==1):
        result = face_recognition.compare_faces([test_image_encoding[0]],encoding)
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
                return("Number and Face Doesnt Match, Please try again")
            elif(check_image==1):
                return("Your attendance marked " + str(values[0]))
            elif(check_image==2):
                return("Cannot Find Face Properly, Please Try Again")
            elif (check_image == 3):
                return("Multiple Faces Detected, Please try again") #Handling Multiple faces can be added

    if(check_number==0):
        return("Registration number not found")



global capture,regisno,pin,data
capture=0
regisno=None
pin=None
data=0
#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')


# camera = cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    global capture,regisno,camera
    while True:
        success, frame = camera.read() 
        if success:   
            if(capture):
                capture=0
                now = datetime.datetime.now()

                p = os.path.sep.join(['shots', "{}.png".format(str(pin)+"_"+str(regisno).lower())])
                cv2.imwrite(p, frame)
                camera.release() 
        try:
            train_faceLoc = face_recognition.face_locations(frame)[0]
            cv2.rectangle(frame,(train_faceLoc[3],train_faceLoc[0]),(train_faceLoc[1],train_faceLoc[2]),(255,255,0),2)
            encoding = face_recognition.face_encodings(frame)[0]

            output_for_user=find_compare(regisno,frame)
            print(output_for_user)
        except:
            print("Face not recognised properly!")
            pass  # write face not recognised
 
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/tasks',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture,regisno
            capture=1
            # regisno=request.form.get('regisno')
            
    return redirect(url_for('index'))

@app.route('/checkpin',methods=['POST','GET'])
def checkpin():
    if request.method == 'POST':
        global pin,data,camera,regisno
        regisno=request.form.get('regis')
        if request.form.get('pin') == '1234':
            pin=request.form.get('pin')
            camera = cv2.VideoCapture(0)
            global capture
            capture=0
            data=0
            return redirect(url_for('capture'))
        else:
            data=1
            return redirect(url_for('index'))
            # return redirect(url_for('index.html'))
            # data = {'name': 'nabin khadka'}
            # return Response

@app.route('/')
def index():
    global data
    return render_template('index.html',data=data)

@app.route('/capture')
def capture():
    return render_template('capture.html')
@app.route('/camerarelease',methods=['POST','GET'])
def camclose():
    print("in cameraclose")
    camera.release()
    status={"ok":"200"}
    return jsonify(status)
if (__name__=='__main__'):
    app.run()
