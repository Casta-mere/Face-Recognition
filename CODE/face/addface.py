import cv2
import dlib
import csv
import pandas as pd
import sys

sys.path.append(sys.path[0]+'/..')
from Log import log as l

source_pic_dir = 'face/faceImg/source.jpg'
source_csv_dir = 'face/faceImg/features.csv'
imgdir = 'face/faceImg'
npydir = 'face/facenpy'

log = l.classlog("addface")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('face/data_dlib/shape_predictor_68_face_landmarks.dat')
face_reco_model = dlib.face_recognition_model_v1("face/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

def get_features(frame):
    faces = detector(frame, 1)
    if len(faces) != 0:
        shape = predictor(frame, faces[0])
        face_descriptor = face_reco_model.compute_face_descriptor(frame, shape)
    else:
        face_descriptor = 0
    return face_descriptor

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
    msg=f"ALERT : Face file for {userid} not found"
    state=False

    csv_rd = pd.read_csv(source_csv_dir, header=None)
    for i in range(csv_rd.shape[0]):
        if csv_rd.iloc[i][0] == userid:
            csv_rd.drop(i, inplace=True)
            csv_rd.to_csv(source_csv_dir, index=False, header=False)
            msg = f"SUCCESS : Face file removed: userid : {userid}"
            state = True
            break
    log.log(msg)
    return state, msg

if __name__ == "__main__":
    pass