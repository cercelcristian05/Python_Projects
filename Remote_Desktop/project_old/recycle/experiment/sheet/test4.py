import numpy as np
import pyautogui
import cv2

def stream_and_record_desktop(output_filename='recorded_stream.mp4'):
    # Create a named window for displaying the stream
    cv2.namedWindow('Remote Desktop Stream', cv2.WINDOW_NORMAL)
    
    # Get the screen size
    screen_width, screen_height = pyautogui.size()
    
    # Define a higher resolution for the frame (e.g., 1280x720 for better quality)
    frame_width, frame_height = 1280, 720

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
    out = cv2.VideoWriter(output_filename, fourcc, 20.0, (frame_width, frame_height))
    
    if not out.isOpened():
        print("Error: Could not open video file for writing.")
        return
    
    try:
        while True:
            # Capture the screen
            screenshot = pyautogui.screenshot()
            
            # Convert the screenshot to OpenCV format (BGR)
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            frame = cv2.resize(frame, (frame_width, frame_height))
            
            # Get the current cursor position
            cursor_pos = pyautogui.position()
            
            # Scale cursor position to the resized frame
            scaled_cursor_pos = (int(cursor_pos.x * frame_width / screen_width),
                                 int(cursor_pos.y * frame_height / screen_height))
            
            # Draw a circle to represent the cursor on the frame
            cv2.circle(frame, scaled_cursor_pos, 10, (0, 255, 0), -1)  # Green circle with radius 10
            
            # Display the frame in the named window
            cv2.imshow('Remote Desktop Stream', frame)
            
            # Write the frame to the video file
            out.write(frame)
            
            # Refresh the window
            if cv2.waitKey(1) == 27:  # Exit on ESC key
                break
            
            # Adding a small delay to avoid overloading the system
            cv2.waitKey(10)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Release the video writer and close the OpenCV window
        out.release()
        cv2.destroyAllWindows()
        print(f"Video saved as {output_filename}")

# Start streaming and recording the remote desktop
stream_and_record_desktop()
