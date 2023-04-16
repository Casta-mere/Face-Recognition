from flask import Flask, render_template, request,Response,jsonify,redirect,url_for,globals
import json
import cv2
import numpy
import base64
import threading
import control
app = Flask(__name__) 
 
globals.loginState=0
globals.password="123456"
globals.retry=0
globals.controls=control.control()
globals.deleteName=""
globals.msg=""

def m():
    while True:
        for i in globals.controls.get_msg():
            globals.msg=i

t=threading.Thread(target=m)
t.start()

# 首页
@app.route('/',methods=['GET','POST'])
def hello_world():
    return render_template(
        'firstPage.html',
        state=globals.loginState
        )

@app.route('/getState',methods=['GET','POST'])
def getState():
    return globals.msg

# 录入人脸界面
@app.route('/imgUpload',methods=['GET','POST'])
def imageUpload():
    return render_template('faceRecog.html')

# 接收人脸图片并保存
@app.route('/receiveImage', methods=["POST"])
def receive_image():
 
    if request.method == "POST":
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        str_image = json_data["imgData"]
        img = base64.b64decode(str_image)
        img_np = numpy.frombuffer(img, dtype='uint8')
        new_img_np = cv2.imdecode(img_np, 1)
        try:
            cv2.imwrite('face/faceImg/source.jpg',new_img_np)
            print('SUCCESS : {}'.format('load image success!'))
        except:
            print('FAIL : {}'.format('take photo failed!'))
        
    return 'upload'

# 填姓名+邮箱并录入
@app.route('/sendInfo',methods=['POST','GET'])
def sendInfo():
    data=list(request.args.to_dict().keys())[0]
    data=json.loads(data)
    print(data)
    name=data['name']
    email=data['email']
    con,msg=globals.controls.adduser(name,email)
    print(msg)
    return msg
    # return redirect(url_for('hello_world'))
 
# 删除信息
@app.route('/manageInfo',methods=['GET','POST'])
def manageInfo():
    return render_template('manageInfo.html')

# 显示信息
@app.route('/deleteInfo',methods=['GET','POST'])
def deleteInfo():
    name=list(request.args.to_dict().keys())[0]
    name=json.loads(name)
    name=name['delName']
    print(name)
    con,msg=globals.controls.deleteuser(name)
    return msg
    # return render_template('manageInfo.html')

# 登录界面
@app.route('/login',methods=['POST','GET'])
def login():
    if globals.loginState==0:
        return render_template(
            'login.html',
            retry=globals.retry
            )
    else:
        return redirect(url_for('hello_world'))

# 检查是否为管理员
@app.route('/loginCheck',methods=['GET','POST'])
def loginCheck():
    password=request.values.get('password')
    # print(password)
    if globals.password==password:
        globals.loginState=1
        return redirect(url_for('hello_world'))
    else:
        globals.retry=1
        return redirect(url_for('login'))

# 管理员页面
@app.route('/adminPage',methods=['GET','POST'])
def adminPage():
    return render_template(
        'adminPage.html'
        )


if __name__ == '__main__':
    # app.run(debug=False,)
    app.run(debug=True, use_reloader=False,host='0.0.0.0',port=8500)
