from flask import Flask, render_template, request,redirect,url_for,abort,session
import json
import cv2
import numpy
import base64
import control
import os

def secretKey():
    key_bytes = os.urandom(16)
    key = key_bytes.hex()
    return key

app = Flask(__name__) 
app.secret_key = secretKey()
ctrl = control.control()

# 初始化
@app.route('/',methods=['GET','POST'])
def hello_world():
    
    session['loginState']=0
    session['password']="123456"
    session['retry']=0
    session['deleteName']=""
    session['msg']=""
    session['ip']=control.IP_ADDR
    session['id'],client=ctrl.add_client()
    session['port']=str(session['id'])
    # def m():
    #     while True:
    #         with app.test_request_context('/'):
    #             for i in client.get_msg():
    #                 session['msg']=i
    #                 session.modified = True
    #                 print(id(session['msg']),1)
    #                 print(session['msg'])

    # t=threading.Thread(target=m)
    # t.start()
    # app.app_context().push()

    # return redirect(url_for('home'))
    return redirect(url_for('settings'))

# 选择设备
@app.route('/settings',methods=['GET','POST'])
def settings():
    return render_template('initialDev.html')

@app.route('/chooseDev',methods=['GET','POST'])
def chooseDevice():
    return render_template(
        'devSettings.html',
        who="chooseDev",
        create=0
        )

@app.route('/newDev',methods=['GET','POST'])
def newDevice():
    return render_template(
        'devSettings.html',
        who="newDev",
        create=1
        )

@app.route('/startDev',methods=['GET','POST'])
def startDev():
    page_url = request.headers.get('from')
    raw_data=list(request.args.to_dict().keys())[0]
    data=json.loads(raw_data)
    if page_url=="/chooseDev":
        devID=data['chooseDev']
        print(devID)
    elif page_url=="/newDev":
        devName=data['devName']
        devType=data['devType']
        print(devName)
        print(devType)
    msg="here0000"
    return msg

# 首页
@app.route('/Home',methods=['GET','POST'])
def home():
    try:
        ipContent="wss://"+session['ip']+":"+session['port']
        return render_template(
            'firstPage.html',
            state=session['loginState'],
            ip=ipContent
            )
    except:
        return redirect(url_for('hello_world'))

@app.route('/getState',methods=['GET','POST'])
def getState():
    return ctrl.get_msg(session['id'])

# 录入人脸界面
@app.route('/imgUpload',methods=['GET','POST'])
def imageUpload():
    if session['loginState']==0:
        abort(403)
    return render_template('faceRecog.html')

# 接收人脸图片并保存
@app.route('/receiveImage', methods=["POST"])
def receive_image():
 
    if request.method == "POST":
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        # Start
        str_image = json_data["imgData"]
        img = base64.b64decode(str_image)
        img_np = numpy.frombuffer(img, dtype='uint8')
        new_img_np = cv2.imdecode(img_np, 1)
        # end
        try:
            cv2.imwrite('face/faceImg/source.jpg',new_img_np)
            print('SUCCESS : {}'.format('load image success!'))
        except:
            print('ERROR : {}'.format('take photo failed!'))
        
    return 'upload'

# 填姓名+邮箱并录入
@app.route('/sendInfo',methods=['POST','GET'])
def sendInfo():
    data=list(request.args.to_dict().keys())[0]
    data=json.loads(data)
    # print(data)
    name=data['name']
    email=data['stuid']
    con,msg=ctrl.adduser(name,email)
    print(msg)
    return msg
    # return redirect(url_for('hello_world'))
 
# 删除信息
@app.route('/manageInfo',methods=['GET','POST'])
def manageInfo():
    if session['loginState']==0:
        abort(403)
    # 列举所有学生信息
    stuInfo = ctrl.get_users()
    return render_template(
        'manageInfo.html',
        stuInfo = stuInfo
        )

# 显示信息
@app.route('/deleteInfo',methods=['GET','POST'])
def deleteInfo():
    if session['loginState']==0:
        abort(403)
    name=list(request.args.to_dict().keys())[0]
    name=json.loads(name)
    name=name['delInfo']
    # con,msg=ctrl.deleteuser(name)
    msg="here"
    return msg

# 登录界面
@app.route('/login',methods=['POST','GET'])
def login():
    if session['loginState']==0:
        return render_template(
            'login.html',
            retry=session['retry']
            )
    else:
        return redirect(url_for('adminPage'))

# 检查是否为管理员
@app.route('/loginCheck',methods=['GET','POST'])
def loginCheck():
    password=request.values.get('password')
    # print(password)
    if session['password']==password:
        session['loginState']=1
        session.modified = True
        return redirect(url_for('adminPage'))
    else:
        session['retry']=1
        return redirect(url_for('login'))

# 管理员页面
@app.route('/adminPage',methods=['GET','POST'])
def adminPage():
    if session['loginState']==0:
        abort(403)
    return render_template(
        'adminPage.html'
        )


if __name__ == '__main__':
    # app.run(debug=False, use_reloader=False,host='0.0.0.0',port=8500)
    # app.run(debug=True, use_reloader=False,host='0.0.0.0',port=8500)
    app.run(debug=True, use_reloader=False,host='0.0.0.0',port=8500,ssl_context=('static/servercert/server-cert.pem', 'static/servercert/server-key.pem'))