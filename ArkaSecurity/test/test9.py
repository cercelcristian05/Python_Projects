import cv2
from deepface import DeepFace

# Path to the directory with trusted images
trusted_images = "./cropped_faces"

# Open video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break

    # Convert the frame to RGB as DeepFace works with RGB images
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    try:
        # Use DeepFace.find to compare the frame with trusted images
        results = DeepFace.find(img_path=rgb_frame, db_path=trusted_images, enforce_detection=False)
        
        if len(results) > 0:
            # If there's a match, display "Trusted Person"
            cv2.putText(frame, "Trusted Person", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            # If no match, display "Unknown Person"
            cv2.putText(frame, "Unknown Person", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    
    except Exception as e:
        print(f"Error: {e}")

    # Show the frame with results
    cv2.imshow('Face Recognition', frame)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
