import socket
import cv2
import numpy as np
import pyautogui

class ScreenMirrorClient:
    def __init__(self, host='DESKTOP-I1O0U7L', port=8765):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")
        self.stream_screen()

    def stream_screen(self):
        try:
            while True:
                # Capture the screen
                screenshot = pyautogui.screenshot()
                
                # Convert the screenshot to OpenCV format (BGR)
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                
                # Encode frame to JPEG
                ret, jpeg = cv2.imencode('.jpg', frame)
                if not ret:
                    continue
                
                # Convert JPEG to bytes
                jpeg_bytes = jpeg.tobytes()

                # Send the size of the frame
                frame_size = len(jpeg_bytes)
                self.client_socket.sendall(frame_size.to_bytes(4, byteorder='big'))

                # Send the frame itself
                self.client_socket.sendall(jpeg_bytes)

        except Exception as e:
            print(f"Failed to capture or send frame: {e}")
        finally:
            self.client_socket.close()
            print("Streaming stopped and connection closed.")

if __name__ == "__main__":
    client = ScreenMirrorClient(host='DESKTOP-I1O0U7L', port=8765)
    client.start()
