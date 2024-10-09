import cv2
import torch
import time
import numpy as np

# Load your pre-trained model (.pt file)
model_path = "./20180402-114759-vggface2.pt"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Load the model
model = torch.load(model_path)
model.eval()  # Set the model to evaluation mode

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

def preprocess_frame(frame):
    """Preprocess the frame before feeding it to the model"""
    # Resize the frame (for example to 160x160 or as required by your model)
    resized_frame = cv2.resize(frame, (160, 160))

    # Convert BGR to RGB since OpenCV uses BGR but most models use RGB
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    # Normalize pixel values (if required by your model)
    # This is an example, adapt it according to your model's requirements
    normalized_frame = rgb_frame / 255.0  # Normalize to [0, 1]
    
    # Convert to PyTorch tensor and move to GPU (if available)
    input_tensor = torch.from_numpy(normalized_frame).float().permute(2, 0, 1).unsqueeze(0).to(device)
    
    return input_tensor

def postprocess_output(output):
    """Postprocess the model output (e.g., to extract bounding boxes or embeddings)"""
    # Example: If output is bounding boxes, process accordingly
    # Assuming output contains [x1, y1, x2, y2, confidence] per face
    # You need to adapt this based on your specific model
    return output.cpu().detach().numpy()

# Measure FPS
frame_count = 0
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    input_tensor = preprocess_frame(frame)

    # Run the model inference
    with torch.no_grad():
        output = model(input_tensor)

    # Postprocess the output
    result = postprocess_output(output)
    
    # Draw results on the frame (example: bounding boxes)
    for box in result:
        x1, y1, x2, y2, confidence = box
        if confidence > 0.5:  # Draw box only if confidence is high
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"{confidence:.2f}", (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Display the frame
    cv2.imshow('Face Detection', frame)

    # Measure FPS
    frame_count += 1
    if frame_count % 30 == 0:
        end_time = time.time()
        fps = frame_count / (end_time - start_time)
        print(f"FPS: {fps:.2f}")
        frame_count = 0
        start_time = time.time()

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
