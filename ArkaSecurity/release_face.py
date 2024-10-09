import mediapipe as mp
import cv2
import numpy as np
import tempfile
import os
import face_recognition  # Import face_recognition

trusted_images_dir = "./cropped_faces"  # Directory with trusted images

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

landmark_indices = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 
                    397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 
                    136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

# Preload trusted encodings for face_recognition
trusted_encodings = []
trusted_names = []

for image_name in os.listdir(trusted_images_dir):
    if image_name.endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(trusted_images_dir, image_name)
        img = face_recognition.load_image_file(img_path)
        img_encodings = face_recognition.face_encodings(img)  # This returns a list of face encodings
        
        # Check if there are face encodings in the image
        if len(img_encodings) > 0:
            img_encoding = img_encodings[0]  # Only take the first encoding (assuming one face per image)
            trusted_encodings.append(img_encoding)
            trusted_names.append(image_name.split('.')[0])  # Use filename as the label

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

                # Create a mask and display just the face region
                mask = np.zeros_like(frame)
                cv2.fillConvexPoly(mask, np.array(face_points, dtype=np.int32), (255, 255, 255))
                face_only = cv2.bitwise_and(frame, mask)
                cv2.imshow('Computer Perspective', face_only)
                
                try:
                    # Save the current frame temporarily for processing
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                        temp_file_path = temp_file.name
                        cv2.imwrite(temp_file_path, rgb_frame)
                    
                    # Load the captured frame and find face encodings
                    current_frame_image = face_recognition.load_image_file(temp_file_path)
                    current_frame_encodings = face_recognition.face_encodings(current_frame_image)

                    if len(current_frame_encodings) > 0:  # If a face was detected
                        current_encoding = current_frame_encodings[0]
                        
                        # Compare current face with trusted encodings
                        matches = face_recognition.compare_faces(trusted_encodings, current_encoding)
                        face_distances = face_recognition.face_distance(trusted_encodings, current_encoding)

                        # Find the best match
                        best_match_index = np.argmin(face_distances)

                        if matches[best_match_index]:
                            name = trusted_names[best_match_index]
                            cv2.putText(frame, f"Trusted Person: {name}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        else:
                            cv2.putText(frame, "Unknown Intruder", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    else:
                        cv2.putText(frame, "No Face Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                except Exception as e:
                    print(f"Verification error: {e}")
                    cv2.putText(frame, "Unknown Intruder", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                finally:
                    os.remove(temp_file_path)  # Clean up temporary file
                
        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
