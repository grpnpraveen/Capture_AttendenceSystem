import cv2
from flask import Flask,render_template,Response,request,redirect,url_for,jsonify
import os
import datetime, time
import numpy as np
import face_recognition
import pickle
from werkzeug.wrappers import response
from pymongo import MongoClient
# import pymongo
global capture,regisno,pin,data,uniqcode,status_info,camera
capture=0
regisno=None
pin=None
data=0
uniqcode=None
status_info="Please wait while marking your Attendence."

def get_database(DB):
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb://localhost:27017"
    CONNECTION_STRING = "mongodb+srv://admin:root@cluster0.cjpup.mongodb.net/crud_mongodb?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client[DB]
    
with open('train_data2.pkl', 'rb') as f:
    train_data = pickle.load(f)


def prepare_image(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    return image


def compare_test_image(image,encoding):
    image = prepare_image(image)
    test_image_encoding = face_recognition.face_encodings(image)
    #print(test_image_encoding)
    if(len(test_image_encoding)==1):
        result = face_recognition.compare_faces([test_image_encoding[0]],encoding,tolerance=0.5)
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
                return("Number and Face Doesnt Match, Please try again")
            elif(check_image==1):
                print("Your attendance marked " + str(values[0]))
                return("Your attendance marked " + str(values[0]))
            elif(check_image==2):
                print("Cannot Find Face Properly, Please Try Again")
                return("Cannot Find Face Properly, Please Try Again")
            elif (check_image == 3):
                print("Multiple Faces Detected, Please try again")
                return("Multiple Faces Detected, Please try again") #Handling Multiple faces can be added

    if(check_number==0):
        print("Registration number not found")
        return("Registration number not found")


#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')


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
        user_entered_pin=request.form.get('pin')
        splitted_user_entered_pin=user_entered_pin.split("_")
        dbname = get_database("getdata")
        collection=dbname[splitted_user_entered_pin[1]]
        item_details=collection.find()
        for item in item_details:
            # This does not give a very readable output
            if item["code"]==user_entered_pin:
                print(item)
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
    global camera
    camera.release()
    print("in cameraclose")
    status={"ok":"200"}
    return status

@app.route('/login')
def login():
    return render_template('faculty_login.html')

@app.route('/interface')
def interface():
    return render_template('faculty_interface.html')

@app.route('/logindirect',methods=['POST','GET'])
def logindirect():
    if request.method == 'POST':
        return redirect(url_for('interface'))

@app.route('/getcode',methods=['POST','GET'])
def getcode():
    global uniqcode
    if request.method == 'POST':
        status={"ok":"200"}
        jsondata=request.get_json()
        uniqcode=jsondata["uniqcode"]
        print(uniqcode)
        splitted_uniqcode=uniqcode.split("_")
        dbname = get_database("getdata")
        collection=dbname[splitted_uniqcode[1]]
        item_1 = {
                "_id":splitted_uniqcode[5],
                "code":uniqcode,
                }
        collection.insert_one(item_1)
        return jsonify(status)

@app.route('/getinfo',methods=['POST','GET'])
def getinfo():
    
    # if request.method == 'GET':
    global status_info
    status={}
    print("there"+str(status_info))
    x=str(status_info)
    status["info"]=x
    return jsonify(status)


# camera = cv2.VideoCapture(0)
def gen_frames():  # generate frame by frame from camera
    global capture,regisno,camera,status_info
    output_for_user=None
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
            if(frame):
                train_faceLoc = face_recognition.face_locations(frame)[0]
                cv2.rectangle(frame,(train_faceLoc[3],train_faceLoc[0]),(train_faceLoc[1],train_faceLoc[2]),(255,255,0),2)
                output_for_user=find_compare(regisno,frame)
                if( output_for_user.find("Your attendance")):
                    dbname = get_database("BML")
                    collection=dbname[str(pin)]
                    item={
                            "_id":regisno,
                            "present":"1"
                    }
                    collection.insert_one(item)
                # status_info=output_for_user
                # print(output_for_user+ status_info)

                # status_info=str(output_for_user)
                # getinfo()
                frame=None

        except:
            # print("Face not recognised properly!")
            pass  # write face not recognised
            
        # try:
        #     ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
        #     frame = buffer.tobytes()
        #     yield (b'--frame\r\n'
        #             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # except Exception as e:
        #     pass

        
        

if (__name__=='__main__'):
    # dbname = get_database()
    app.run()
