import mediapipe as mp
import cv2
import numpy as np
import tempfile
import os
from deepface import DeepFace

trusted_images = "./cropped_faces"

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

landmark_indices = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 
                    397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 
                    136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

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
                face_points = []
                for idx in landmark_indices:
                    x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                    y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                    face_points.append((x, y))
                    
                xs = [p[0] for p in face_points]
                ys = [p[1] for p in face_points]
                
                x_min = min(xs)
                x_max = max(xs)
                y_min = min(ys)
                y_max = max(ys)
                
                width = x_max - x_min
                height = y_max - y_min
                
                if width > 0:
                    distance = (1000 / width) * 9

                if distance <= 40:
                    cv2.putText(frame, f"X: {x}  Y: {y}  Z: Too close, move away from screen", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                elif distance >= 90:
                    cv2.putText(frame, f"X: {x}  Y: {y}  Z: Too far, move closer to camera.", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, f"X: {x}  Y: {y}  Z: {distance:.2f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


                mask = np.zeros_like(frame)
                cv2.fillConvexPoly(mask, np.array(face_points, dtype=np.int32), (255, 255, 255))

                face_only = cv2.bitwise_and(frame, mask)
                cv2.imshow('Computer Perspective', face_only)
                
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                        temp_file_path = temp_file.name
                        cv2.imwrite(temp_file_path, rgb_frame)
                    
                    retrieve_validation = DeepFace.find(temp_file_path, './cropped_faces/', model_name="Facenet", enforce_detection=True, detector_backend="mediapipe")
                    first_identity = str(retrieve_validation[0]["identity"][0])  
                    
                    next_result = DeepFace.verify(temp_file_path, first_identity, model_name="Facenet", enforce_detection=True, detector_backend="mediapipe")

                    if next_result["verified"]:
                        cv2.putText(frame, "Trusted Person", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                except Exception as e:
                    print(f"Verification error: {e}")
                    cv2.putText(frame, "Unknown Intruder", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            os.remove(temp_file_path)            
        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
