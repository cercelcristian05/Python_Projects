import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Selfie Segmentation
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Resize the frame for faster processing
    small_frame = cv2.resize(frame, (640, 480))

    # Convert the frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Perform segmentation
    results = segmentation.process(rgb_frame)

    # Create a mask where the segmentation model detects the person
    mask = results.segmentation_mask > 0.5

    # Convert mask to uint8 for OpenCV compatibility
    mask = np.uint8(mask * 255)

    # Apply the mask to the frame
    foreground = cv2.bitwise_and(small_frame, small_frame, mask=mask)

    # Invert the mask to get the background (black)
    background_mask = cv2.bitwise_not(mask)
    background = np.zeros_like(small_frame, dtype=np.uint8)

    # Combine the face (foreground) with the black background
    final_frame = cv2.add(foreground, background)

    # Display the resulting frame
    cv2.imshow("Segmented Face", final_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
