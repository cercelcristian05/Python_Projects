import cv2
from deepface import DeepFace

# Path to your database of known faces
db_path = "./cropped_faces"

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the original frame to RGB for face recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Try to find a match from the database using the RGB frame
    try:
        results = DeepFace.find(img_path=rgb_frame, db_path=db_path, enforce_detection=False)

        # If results are found, draw rectangles around faces
        if results and len(results[0]) > 0:
            for i, result in results[0].iterrows():
                # Get the face's bounding box coordinates from the result
                top_x, top_y, bottom_x, bottom_y = result['source_x'], result['source_y'], result['source_x'] + result['source_w'], result['source_y'] + result['source_h']

                # Draw a rectangle around the detected face on the frame
                cv2.rectangle(frame, (top_x, top_y), (bottom_x, bottom_y), (0, 255, 0), 2)  # Green rectangle with thickness 2

                # Optionally, label the face as "Match Found" or whatever label you prefer
                label = "Match Found"
                cv2.putText(frame, label, (top_x, top_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)  # Text above the rectangle

        else:
            label = "No Match"
    
    except ValueError as e:
        # If no face is detected, handle it gracefully
        label = "No Face Detected"
    
    except Exception as e:
        print(f"Error detecting or recognizing face: {str(e)}")
        label = "Error"

    # Display the frame with the rectangle around the face (if any)
    cv2.imshow('Face Recognition with Rectangle', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
