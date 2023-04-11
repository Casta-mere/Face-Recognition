from flask import Flask, render_template, request,Response,jsonify,redirect,url_for,globals
from flask_cors import CORS
import json
import cv2
import numpy
import base64
import control
app = Flask(__name__) 
 
globals.loginState=0
globals.password="123456"
globals.retry=0
 
@app.route('/',methods=['GET','POST'])
def hello_world():
    return render_template('firstPage.html')

@app.route('/imgUpload',methods=['GET','POST'])
def imageUpload():
    return render_template('faceRecog.html')

@app.route('/receiveImage', methods=["POST"])
def receive_image():
 
    if request.method == "POST":
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        str_image = json_data["imgData"]
        img = base64.b64decode(str_image)
        img_np = numpy.fromstring(img, dtype='uint8')
        new_img_np = cv2.imdecode(img_np, 1)
        try:
            cv2.imwrite('./CODE/image/rev_image.jpg',new_img_np)
            print('data:{}'.format('success'))
        except:
            print('data:{}'.format('failed'))
        
    return 'upload'

@app.route('/sendInfo',methods=['POST'])
def sendInfo():
    data=request.form.to_dict()
    print(type(data))
    print(data)
    name=data['name']
    email=data['email']
    print('name:{}'.format(name),'email:{}'.format(email))
    return redirect(url_for('hello_world'))
 
@app.route('/manageInfo',methods=['GET','POST'])
def manageInfo():
    return render_template('manageInfo.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if globals.loginState==0:
        return render_template(
            'login.html',
            retry=globals.retry
            )
    else:
        return redirect(url_for('hello_world'))

@app.route('/loginCheck',methods=['POST','GET'])
def loginCheck():
    password=request.form.get('pw')
    print(password)
    if globals.password==password:
        return redirect(url_for('hello_world'))
    else:
        globals.retry=1
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)