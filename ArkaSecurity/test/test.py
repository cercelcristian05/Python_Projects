import os
import json
import cv2

# Function to extract face regions from images using LabelMe JSON annotations
def extract_faces_from_json(json_file_path, image_dir, output_dir):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Get image path
    image_path = os.path.join(image_dir, os.path.basename(data['imagePath']))
    image = cv2.imread(image_path)
    
    for shape in data['shapes']:
        if shape['label'] == 'trusted':  # Assuming 'trusted' is the label for your face
            # Extract bounding box points
            x1, y1 = map(int, shape['points'][0])
            x2, y2 = map(int, shape['points'][1])
            
            # Crop face region
            face_region = image[y1:y2, x1:x2]
            
            # Save cropped face to output directory
            face_filename = os.path.join(output_dir, os.path.basename(image_path))
            cv2.imwrite(face_filename, face_region)
            print(f"Saved cropped face to {face_filename}")

# Directory paths
json_dir = './without_glasses/trusted'  # Path to the folder with your JSON files
image_dir = './without_glasses/'  # Path to the folder with the original images
output_dir = './cropped_faces/'  # Path to save the cropped face images

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop through all JSON files and extract faces
for json_file in os.listdir(json_dir):
    if json_file.endswith('.json'):
        json_file_path = os.path.join(json_dir, json_file)
        extract_faces_from_json(json_file_path, image_dir, output_dir)
