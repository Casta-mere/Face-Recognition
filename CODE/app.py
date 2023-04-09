from flask import Flask, render_template, request,Response,jsonify,redirect,url_for
from flask_cors import CORS
import json
import cv2
import numpy
import base64
app = Flask(__name__) 
CORS(app)
@app.route('/')
def hello_world():
    return render_template('index.html')
 
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)