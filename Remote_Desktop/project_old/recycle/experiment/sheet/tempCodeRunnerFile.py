import numpy as np
import pyautogui
import cv2

def stream_remote_desktop():
    # Create a named window for displaying the stream
    cv2.namedWindow('Remote Desktop Stream', cv2.WINDOW_NORMAL)
    
    try:
        while True:
            # Capture the screen
            screenshot = pyautogui.screenshot()
            
            # Convert the screenshot to OpenCV format (BGR)
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Display the frame in the named window
            cv2.imshow('Remote Desktop Stream', frame)
            
            # Refresh the window
            cv2.waitKey(1)  # Adjust delay as needed for smooth playback
    
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C gracefully
    
    finally:
        # Close the OpenCV window
        cv2.destroyAllWindows()

# Start streaming the remote desktop
stream_remote_desktop()
