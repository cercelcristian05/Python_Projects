import cv2

def capture_photo_and_exit():
    # Initialize the camera capture
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera (usually laptop's webcam)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # If frame is read correctly, ret is True
    if ret:
        # Display the captured frame
        cv2.imshow('Captured Photo', frame)
        
        # Save the captured frame to a file (optional)
        cv2.imwrite('captured_photo.jpg', frame)
        
        # Wait for a brief moment and then close the window
        cv2.waitKey(2000)  # Wait for 2 seconds (2000 milliseconds)
        cv2.destroyAllWindows()
    else:
        print("Error: Failed to capture image.")

    # Release the camera and close any open windows
    cap.release()

if __name__ == "__main__":
    capture_photo_and_exit()
