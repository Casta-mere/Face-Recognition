import cv2
import os
import face_recognition
import numpy as np

def detect_faces():
    known_face_encodings = []
    known_face_names = []
    pictures = len(os.listdir('faceImg'))
    for i in range(1, pictures + 1):
        img_path = f'faceImg/{i}.jpg'
        img = face_recognition.load_image_file(img_path)
        face_encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(f'Person {i}')
    # Start the video capture
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()

        # Convert the frame to RGB format
        rgb_frame = frame[:, :, ::-1]

        # Detect the faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each detected face
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare the face encoding with the known face encodings
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Find the known face with the highest confidence
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                if face_distances[best_match_index] < 0.4:
                    name = known_face_names[best_match_index]
                # Calculate confidence
                confidence = 1 - face_distances[best_match_index]

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw the name and confidence above the face
                cv2.rectangle(frame, (left, top - 35), (right, top), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name + ' ' + str(round(confidence * 100, 2)) + '%', (left + 6, top - 6), font, 0.6,
                            (255, 255, 255), 1)

        # Display the video feed
        cv2.imshow('Video', frame)

        # Exit the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture
    cap.release()
    cv2.destroyAllWindows()

detect_faces()
