import mediapipe as mp
import cv2
import numpy as np
from deepface import DeepFace

trusted_images = "./cropped_faces"

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

landmark_indices = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 
                    397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 
                    136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
nose_index = 1  # The index for the nose landmark

cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    refine_landmarks=True
) as face_mesh:
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb_frame)
        
        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                # Get face points
                face_points = []
                for idx in landmark_indices:
                    x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                    y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                    face_points.append((x, y))
                
                # Calculate bounding box
                xs = [p[0] for p in face_points]
                ys = [p[1] for p in face_points]
                x_min = min(xs)
                x_max = max(xs)
                y_min = min(ys)
                y_max = max(ys)

                # Width and height of the face in pixels
                width = x_max - x_min
                height = y_max - y_min

                # Estimate distance (example)
                # Here you might need to calibrate the relation between pixel size and distance
                if width > 0:  # To avoid division by zero
                    estimated_distance = (1000 / width) * 9  # Example calculation, adjust based on calibration

                # Display the results
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                cv2.putText(frame, f"Distance: {estimated_distance:.2f} cm", (10, 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
