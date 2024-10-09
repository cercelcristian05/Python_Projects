import socket
import cv2
import numpy as np
import threading

class ScreenMirrorServer:
    def __init__(self, host='0.0.0.0', port=8765):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.is_receiving = False

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server started at {self.host}:{self.port}, waiting for connection...")

        self.client_socket, client_address = self.server_socket.accept()
        print(f"Client connected from {client_address}")

        self.is_receiving = True
        self.display_thread = threading.Thread(target=self.receive_and_display)
        self.display_thread.start()

    def receive_and_display(self):
        while self.is_receiving:
            try:
                # Receive frame size
                frame_size_bytes = self.client_socket.recv(4)
                if len(frame_size_bytes) < 4:
                    break
                frame_size = int.from_bytes(frame_size_bytes, byteorder='big')

                # Receive frame data
                frame_data = b''
                while len(frame_data) < frame_size:
                    packet = self.client_socket.recv(frame_size - len(frame_data))
                    if not packet:
                        break
                    frame_data += packet

                # Decode frame
                if len(frame_data) == frame_size:
                    nparr = np.frombuffer(frame_data, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    if frame is not None:
                        cv2.imshow('Screen Mirror', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                else:
                    print("Incomplete frame received")

            except Exception as e:
                print(f"Error receiving or decoding frame: {e}")
                break

        self.client_socket.close()
        cv2.destroyAllWindows()
        print("Streaming stopped and client connection closed.")

if __name__ == "__main__":
    server = ScreenMirrorServer(host='DESKTOP-I1O0U7L', port=8765)
    server.start()
