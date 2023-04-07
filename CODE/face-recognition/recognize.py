import cv2
import os
import face_recognition
import numpy as np
import threading
# Define the desired size for face detection and recognition
# target_size = (128, 128)
# target_size = (300, 300)
target_size = (1500, 1500)
frame_stack = []
width = 0
height = 0

def get_video():
    global width, height, frame_stack
    # Initialize video capture from RTSP stream
    cap = cv2.VideoCapture("rtsp://admin:a12345678@192.168.136.156:554/stream1")
    # get the width and height of frame
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # create a thread to read frames from the video stream and push int to frame_stack
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_stack.append(frame)
    cap.release()

def response(state,name,confidence):
    if state == True:
        print(name + " " + str(confidence))
    else:
        print("no face")

def detect_faces():
    global frame_stack, width, height
    # Load face images from faceImg folder
    known_face_encodings = []
    known_face_names = []
    pictures = len(os.listdir('faceImg'))
    for i in range(1, pictures + 1):
        img_path = f'faceImg/{i}.jpg'
        img = face_recognition.load_image_file(img_path)
        face_encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(f'Person {i}')
    # create a thread to read frames from the frame_stack and detect faces
    t = threading.Thread(target=get_video)
    t.daemon = True
    t.start()
    while True:
        # Resize the frame to the desired size for face detection and recognition
        if len(frame_stack) == 0:
            continue
        frame = frame_stack.pop()
        frame_stack = []
        small_frame = cv2.resize(frame, target_size)
        # Find all the faces in the resized frame
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        # Loop through each detected face and check if it matches any of the known faces, if so, call response function,no need to draw rectangle
        # if no face detected, call response function with state = False
        if len(face_locations) == 0:
            response(False,"",0)
        else:
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare the face encoding with the known face encodings
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Find the known face with the highest confidence
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                # calculate confidence,if confidence is higher than 0.5, call response function with state = True
                confidence = 1 - face_distances[best_match_index]
                if matches[best_match_index] and confidence > 0.5:
                    name = known_face_names[best_match_index]
                    response(True,name,confidence)
                else:
                    response(True,"unknown",confidence)

detect_faces()
