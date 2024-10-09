# import socket
# import threading
# import struct
# import cv2
# import pickle
# import numpy as np

# class Server:
#     def __init__(self, host='0.0.0.0', port=12505):
#         self.host = host
#         self.port = port
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.bind((self.host, self.port))
#         self.server_socket.listen(5)
#         self.client_sockets = []
#         self.statusCamera = False
#         print(f"Server listening on {self.host}:{self.port}")

#     def start(self):
#         while True:
#             client_socket, client_address = self.server_socket.accept()
#             print(f"Connection established with {client_address}")
#             self.client_sockets.append(client_socket)
#             client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
#             client_handler.start()

#     def handle_client(self, client_socket):
#         self.openCamera(client_socket)
#         client_socket.close()
#         self.client_sockets.remove(client_socket)

#     def openCamera(self, client_socket):
#         try:
#             self.statusCamera = True
#             payload_size = struct.calcsize("L")
            
#             while self.statusCamera:
#                 received_data = b""
#                 while len(received_data) < payload_size:
#                     data = client_socket.recv(4*1024)
#                     if not data:
#                         self.statusCamera = False
#                         break
#                     received_data += data
                    
#                 if not received_data:
#                     break
                
#                 packed_msg_size = received_data[:payload_size]
#                 received_data = received_data[payload_size:]
#                 msg_size = struct.unpack("L", packed_msg_size)[0]

#                 while len(received_data) < msg_size:
#                     data = client_socket.recv(4*1024)
#                     if not data:
#                         self.statusCamera = False
#                         break
#                     received_data += data

#                 frame_data = received_data[:msg_size]
#                 received_data = received_data[msg_size:]

#                 frame = pickle.loads(frame_data)
#                 frame = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
#                 cv2.imshow('Client Camera', frame)
#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     self.statusCamera = False
#                     break
                
#         except Exception as e:
#             print(f"Error handling client: {e}")
#         finally:
#             cv2.destroyAllWindows()

# if __name__ == "__main__":
#     server = Server()
#     server.start()

import socket
import threading
import struct
import cv2
import pickle
import numpy as np

class Server:
    def __init__(self, host='0.0.0.0', port=12505):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.client_sockets = []
        self.statusCamera = False
        print(f"Server listening on {self.host}:{self.port}")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection established with {client_address}")
            self.client_sockets.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        self.openCamera(client_socket)
        client_socket.close()
        self.client_sockets.remove(client_socket)

    def openCamera(self, client_socket):
        try:
            self.statusCamera = True
            payload_size = struct.calcsize("L")
            
            while self.statusCamera:
                received_data = b""
                while len(received_data) < payload_size:
                    data = client_socket.recv(4*1024)
                    if not data:
                        self.statusCamera = False
                        break
                    received_data += data
                    
                if not received_data:
                    break
                
                packed_msg_size = received_data[:payload_size]
                received_data = received_data[payload_size:]
                msg_size = struct.unpack("L", packed_msg_size)[0]

                while len(received_data) < msg_size:
                    data = client_socket.recv(4*1024)
                    if not data:
                        self.statusCamera = False
                        break
                    received_data += data

                frame_data = received_data[:msg_size]
                received_data = received_data[msg_size:]

                frame = pickle.loads(frame_data)
                frame = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow('Client Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.statusCamera = False
                    break
                
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    server = Server()
    server.start()
