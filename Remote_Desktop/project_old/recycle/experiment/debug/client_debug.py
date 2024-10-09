# import socket
# import cv2
# import pickle
# import struct

# class VideoAndAudio:
#     def __init__(self, client_socket):
#         self.client_socket = client_socket
#         self.statusCamera = False
#         self.video = cv2.VideoCapture(0)
        
#     def startCamera(self):
#         try:
#             self.statusCamera = True
#             while self.statusCamera:
#                 ret, frame = self.video.read()
#                 if ret:
#                     # Resize frame for faster transmission
#                     frame = cv2.resize(frame, (640, 480))
#                     # Encode frame as JPEG
#                     _, buffer = cv2.imencode('.jpg', frame)
#                     data = pickle.dumps(buffer)
#                     message_size = struct.pack("L", len(data))
#                     self.client_socket.sendall(message_size + data)
#                 cv2.imshow('DEBUG', frame)
#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     self.statusCamera = False
#                     break
#         except Exception as e:
#             print(f"Error starting camera: {e}")
#         finally:
#             self.stopCamera()
    
#     def stopCamera(self):
#         self.statusCamera = False
#         self.video.release()
#         cv2.destroyAllWindows()

# class Client:
#     def __init__(self, host='localhost', port=12505):
#         self.host = host
#         self.port = port
#         self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client_socket.connect((self.host, self.port))
#         self.camera = VideoAndAudio(self.client_socket)
        
#     def start(self):
#         try:
#             self.camera.startCamera()
#         except ConnectionResetError:
#             print("Connection reset by server.")
#         finally:
#             self.client_socket.close()

# if __name__ == "__main__":
#     client = Client()
#     client.start()

import socket
import cv2
import pickle
import struct
import time

class VideoAndAudio:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.statusCamera = False
        self.video = cv2.VideoCapture(0)
        
    def startCamera(self):
        try:
            self.statusCamera = True
            while self.statusCamera:
                ret, frame = self.video.read()
                if ret:
                    # Reduce frame rate
                    time.sleep(0.1)  # Send 10 frames per second

                    # Resize frame for faster transmission
                    frame = cv2.resize(frame, (640, 480))
                    
                    # Encode frame as JPEG
                    _, buffer = cv2.imencode('.jpg', frame)
                    data = pickle.dumps(buffer)
                    message_size = struct.pack("L", len(data))
                    
                    self.client_socket.sendall(message_size + data)
        except Exception as e:
            print(f"Error starting camera: {e}")
        finally:
            self.stopCamera()
    
    def stopCamera(self):
        self.statusCamera = False
        self.video.release()
        cv2.destroyAllWindows()

class Client:
    def __init__(self, host='localhost', port=12505):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.camera = VideoAndAudio(self.client_socket)
        
    def start(self):
        try:
            self.camera.startCamera()
        except ConnectionResetError:
            print("Connection reset by server.")
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    client = Client(host='localhost')  # Replace with your server's IP address
    client.start()
