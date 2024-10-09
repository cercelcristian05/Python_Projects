    def __init__(self, host='0.0.0.0', port=8765):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.capture_thread = None
        self.is_streaming = False

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")

        self.client_socket, client_address = self.server_socket.accept()
        print(f"Client connected from {client_address}")

        self.is_streaming = True
        self.capture_thread = threading.Thread(target=self.stream_screen)
        self.capture_thread.start()

    def stream_screen(self):
        screen_capture = cv2.VideoCapture(0)  # Change to 1, 2, ... for different cameras
        while self.is_streaming:
            ret, frame = screen_capture.read()
            if ret:
                encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
                try:
                    self.client_socket.sendall(encoded_frame)
                except Exception as e:
                    print(f"Error sending frame: {e}")
                    break
            else:
                print("Failed to capture frame")
                break

        screen_capture.release()
        self.client_socket.close()
        print("Streaming stopped and client connection closed.")

if __name__ == "__main__":
    server = ScreenMirrorServer()
    server.start()