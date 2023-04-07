import cv2
import face_recognition
import os
def addface():
    # Initialize OpenCV video capture
   # video_capture = cv2.VideoCapture(0)
    video_capture = cv2.VideoCapture("rtsp://admin:a12345678@192.168.136.156:554/stream1")
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
        print("No face detected")
        return
    # Save the face encoding to a file in the faceImg directory
    num_faces = len(os.listdir('faceImg'))
    filename = f'{num_faces + 1}.jpg'
    filepath = os.path.join('faceImg', filename)
    cv2.imwrite(filepath, frame)
    print(f"New face added: {filename}")

addface()