import cv2
from flask import Flask,render_template,Response,request,redirect,url_for,jsonify
import os
import datetime, time
import numpy as np

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
            regisno=request.form.get('regisno')
    return redirect(url_for('index'))

@app.route('/checkpin',methods=['POST','GET'])
def checkpin():
    if request.method == 'POST':
        global pin,data,camera
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
    camera.release()
if (__name__=='__main__'):
    app.run()
