import cv2
import face_recognition
import os
import dlib
import csv
import numpy as np
import time
import sys

sys.path.append(sys.path[0]+'/..')
from Log import log as l

source_pic_dir = 'face/faceImg/source.jpg'
source_csv_dir = 'face/faceImg/features.csv'
imgdir = 'face/faceImg'
npydir = 'face/facenpy'

log = l.classlog("addface")

# t1=time.time()
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('face/data_dlib/shape_predictor_68_face_landmarks.dat')
face_reco_model = dlib.face_recognition_model_v1("face/data_dlib/dlib_face_recognition_resnet_model_v1.dat")
# print(f"load model time : {time.time()-t1}")


def get_features(frame):
    faces = detector(frame, 1)
    if len(faces) != 0:
        shape = predictor(frame, faces[0])
        face_descriptor = face_reco_model.compute_face_descriptor(frame, shape)
    else:
        face_descriptor = 0
    return face_descriptor


def addface(userid):
    # Initialize OpenCV video capture
    video_capture = cv2.VideoCapture(0)

    # Check if video capture is initialized
    if (video_capture.isOpened()):
        print("SUCCESS : Video capture initialized")
    else:
        return False, "ERROR : Error initializing video capture"

    # Take picture using video capture
    ret, frame = video_capture.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    # If no faces are detected
    if not face_locations:
        return False, "ERROR : No face detected"
    if len(face_locations) > 1:
        return False, "ERROR : More than one face detected"

    # Save numpy array
    filename = f'{userid}.npy'
    filepath = (f"{npydir}/{filename}")
    face_encoding = face_recognition.face_encodings(rgb_frame)[0]
    np.save(filepath, face_encoding)

    # Save face image
    for (top, right, bottom, left) in face_locations:
        frame = frame[top-10:bottom+10, left-10:right+10]
    filename = f'{userid}.jpg'
    filepath = os.path.join(imgdir, filename)
    cv2.imwrite(filepath, frame)

    return True, f"SUCCESS : New face added: userid:{userid}"


def addface_frompic(userid):

    frame=cv2.imread(source_pic_dir)
    with open(source_csv_dir,"a+",newline='') as csvfile:
        writer =csv.writer(csvfile)
        features=get_features(frame)
        if features==0:
            msg="ERROR : No face detected"
            log.log(msg)
            return False,msg
        else:
            features_list=list(features)
            features_list.insert(0,userid)
            writer.writerow(features_list)
    csvfile.close()
    msg=f"SUCCESS : New face added ! userid : {userid}"
    log.log(msg)
    return True,msg
            

def deleteface(userid):
    msg = ""
    state = True

    # Delete face image
    try:
        filename = f'{userid}.jpg'
        filepath = os.path.join(imgdir, filename)
        os.remove(filepath)
    except:
        msg += f"ALERT : Face image file not found: userid : {userid}"
        state = False

    # Delete face numpy file
    try:
        filename = f'{userid}.npy'
        filepath = os.path.join(npydir, filename)
        os.remove(filepath)
    except:
        if (not state):
            msg += "\n"
        msg += f"ALERT : Face numpy file not found: userid : {userid}"
        state = False

    if (state):
        msg = f"SUCCESS : Face file removed: userid : {userid}"

    return state, msg


if __name__ == "__main__":
    pass