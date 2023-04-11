import cv2
import face_recognition
import os

sourcedir = 'face/faceImg/source.jpg'
dir = 'face/faceImg'


def addface(userid):
    # Initialize OpenCV video capture
    video_capture = cv2.VideoCapture(0)
    # video_capture = cv2.VideoCapture("rtsp://admin:a12345678@192.168.136.156:554/stream1")

    # Check if video capture is initialized
    if(video_capture.isOpened()):
        print("SUCCESS : Video capture initialized")
    else:
        return False, "FAIL : Error initializing video capture"

    # Take picture using video capture
    ret, frame = video_capture.read()
    target_size = (1080, 1080)
    # resize frame
    frame = cv2.resize(frame, target_size)
    # improve face detection by converting to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_locations = face_recognition.face_locations(frame)
    # just get the face from the frame with a margin of 10 pixels
    for (top, right, bottom, left) in face_locations:
        frame = frame[top-10:bottom+10, left-10:right+10]

    # If no faces are detected, return
    if not face_locations:
        return False, "FAIL : No face detected"

    # Save the face encoding to a file in the faceImg directory
    filename = f'{userid}.jpg'
    filepath = os.path.join(dir, filename)
    cv2.imwrite(filepath, frame)
    return True, f"SUCCESS : New face added: userid:{userid}"


def addface_frompic(userid):

    frame = cv2.imread(sourcedir)
    target_size = (1080, 1080)
    # resize frame
    frame = cv2.resize(frame, target_size)
    # improve face detection by converting to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_locations = face_recognition.face_locations(frame)
    # just get the face from the frame with a margin of 10 pixels
    for (top, right, bottom, left) in face_locations:
        frame = frame[top-10:bottom+10, left-10:right+10]

    # If no faces are detected, return
    if not face_locations:
        return False, "FAIL : No face detected"

    # Save the face encoding to a file in the faceImg directory
    filename = f'{userid}.jpg'
    filepath = os.path.join(dir, filename)
    cv2.imwrite(filepath, frame)
    return True, f"SUCCESS : New face added: userid:{userid}"


def deleteface(userid):
    filename = f'{userid}.jpg'
    filepath = os.path.join(dir, filename)
    os.remove(filepath)
    return f"SUCCESS : Face removed: userid:{userid}"


if __name__ == "__main__":
    print(addface(1))
