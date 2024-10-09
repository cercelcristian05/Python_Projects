from deepface import DeepFace
import os
import numpy as np
import joblib

# Directory with cropped face images
cropped_faces_dir = './cropped_faces/'

# Lists to hold embeddings and labels
embeddings = []
labels = []

# Loop through each face image in the directory
for img_file in os.listdir(cropped_faces_dir):
    img_path = os.path.join(cropped_faces_dir, img_file)
    
    try:
        # Extract face embedding using DeepFace
        embedding = DeepFace.represent(img_path, model_name="Facenet", enforce_detection=False)[0]['embedding']
        embeddings.append(embedding)
        labels.append("trusted")  # Label all embeddings as your name
    except Exception as e:
        print(f"Error processing {img_file}: {str(e)}")

# Convert embeddings and labels to NumPy arrays
X = np.array(embeddings)
y = np.array(labels)

# Save embeddings and labels for future use
np.save('face_embeddings.npy', X)
np.save('face_labels.npy', y)
