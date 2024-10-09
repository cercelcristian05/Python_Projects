import cv2
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (640, 480))
    
    # Convert the image to a 2D array of pixels
    pixels = small_frame.reshape((-1, 3))  # Reshape to a 2D array of pixels

    # Convert to float32 for K-means
    pixels = np.float32(pixels)

    # Define criteria and apply KMeans
    k = 3  # Number of clusters
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back to uint8
    centers = np.uint8(centers)
    
    # Map labels to center colors
    segmented_image = centers[labels.flatten()]

    # Reshape back to the original image
    segmented_image = segmented_image.reshape(small_frame.shape)

    # Display the segmented image
    cv2.imshow("Segmented Image", segmented_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
