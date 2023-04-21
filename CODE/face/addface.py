import cv2
import face_recognition
import os
import numpy as np

sourcedir = 'face/faceImg/source.jpg'
imgdir = 'face/faceImg'
npydir = 'face/facenpy'


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

    frame = cv2.imread(sourcedir)
    face_locations = face_recognition.face_locations(frame)

    # just get the face from the frame with a margin of 10 pixels
    for (top, right, bottom, left) in face_locations:
        frame = frame[top-10:bottom+10, left-10:right+10]

    # If no faces are detected, return
    if not face_locations:
        return False, "ERROR : No face detected"
    if len(face_locations) > 1:
        return False, "ERROR : More than one face detected"

    # Save numpy array
    filename = f'{userid}.npy'
    filepath = (f"{npydir}/{filename}")
    face_encoding = face_recognition.face_encodings(frame)[0]
    np.save(filepath, face_encoding)

    # Save face image
    filename = f'{userid}.jpg'
    filepath = os.path.join(imgdir, filename)
    cv2.imwrite(filepath, frame)
    return True, f"SUCCESS : New face added ! userid : {userid}"


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
    print()
