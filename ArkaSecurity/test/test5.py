import cv2
from deepface import DeepFace

# Path to your database of known faces
db_path = "./cropped_faces"

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to RGB format for DeepFace
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Save the current frame temporarily for recognition
    temp_img_path = "./cropped_faces/captured_image_300.jpg"
    cv2.imwrite(temp_img_path, rgb_frame)

    # Use DeepFace to find a match from the database
    try:
        results = DeepFace.find(img_path=temp_img_path, db_path=db_path, enforce_detection=True)

        # If results are found, draw rectangles around faces
        if results and len(results[0]) > 0:
            for i, result in results[0].iterrows():
                top_x, top_y, bottom_x, bottom_y = result['source_x'], result['source_y'], result['source_x'] + result['source_w'], result['source_y'] + result['source_h']

                # Draw a rectangle around the detected face on the frame
                cv2.rectangle(frame, (top_x, top_y), (bottom_x, bottom_y), (0, 255, 0), 2)  # Green rectangle with thickness 2

                # Optionally, label the face
                label = result['identity']
                cv2.putText(frame, label, (top_x, top_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        else:
            label = "No Match"
            cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # Red text for no match

    except ValueError as e:
        # If no face is detected, handle it gracefully
        cv2.putText(frame, "No Face Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    except Exception as e:
        print(f"Error detecting or recognizing face: {str(e)}")
        cv2.putText(frame, "Error", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame with rectangles around detected faces
    cv2.imshow('Face Recognition', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
