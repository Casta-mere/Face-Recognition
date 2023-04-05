import cv2
import face_recognition
import os

def addface():
    # Initialize OpenCV video capture
    video_capture = cv2.VideoCapture(0)
    # Take picture using video capture
    ret, frame = video_capture.read()
    # resize frame to 1/4 size for faster face recognition processing
    frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # improve face detection by converting to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_locations = face_recognition.face_locations(frame)
    # If no faces are detected, return
    if not face_locations:
        print("No face detected")
        return
    # Save the face encoding to a file in the faceImg directory
    num_faces = len(os.listdir('faceImg'))
    filename = f'{num_faces + 1}.jpg'
    filepath = os.path.join('faceImg', filename)
    cv2.imwrite(filepath, frame)
    print(f"New face added: {filename}")

addface()