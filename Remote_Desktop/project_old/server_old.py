import socket
import threading
import cv2, pickle, struct, numpy as np

class Server:
    def __init__(self, host='0.0.0.0', port=12505):
        self.host = host
        self.port = port
        self.client_sockets = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        
        self.statusChat = False
        self.statusCmd = False
        self.statusCamera = False
        self.statusMicrophone = False
        
        print(f"[ Server listening on {self.host}:{self.port} ]")
        
    def commandChat(self, client_socket):
        self.statusChat = True
        
        while self.statusChat:
            server_message = input('Server to Client > ')
            client_socket.send(server_message.encode())
            
            if server_message == '/0c':
                self.statusChat = False
                print(f"[ Chat mode has been closed ]")
                break
    
    def commandPrompt(self, client_socket):
        self.statusCmd = True
        
        while self.statusCmd:
            server_message = input('Client\'s CMD > ')
            
            if server_message.lower() == '/0cmd':
                client_socket.send('quit'.encode())
                print("[ Command mode has been closed ]")
                self.statusCmd = False
                break 
            elif server_message.strip() == '':
                print("[ Blank message received ]")
                continue

            client_socket.send(server_message.encode())
            client_response = client_socket.recv(4096).decode()
            print(f"Client response:\n{client_response}")
            
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
        
    def establishClient(self, client_socket, addr):
        print(f"[ Connection established with {addr} ]")
        try:
            while True:
                server_message = input('Server > ')
                client_socket.send(server_message.encode())
                
                if server_message == '/0q':
                    print(f"[ {addr} has been closed ]")
                    break
                elif server_message == '/chat':
                    print(f"[ Chat activated ]")
                    self.commandChat(client_socket)  # Call commandChat method
                elif server_message == '/cmd':
                    print(f"[ Command Prompt activated ]")
                    self.commandPrompt(client_socket)  # Call commandPrompt 
                elif server_message == '/play':
                    client_socket.send('/play'.encode())
                elif server_message == '/stop':
                    client_socket.send('/stop'.encode())
                elif server_message == '/help':
                    help_message = (
                        "/0q - Kill connection with client\n"
                        "---------------------------------\n"
                        "/chat - Activate chat mode\n"
                        "/0c - Exit the chat mode\n"
                        "---------------------------------\n"
                        "/cmd - Activate command prompt mode\n"
                        "/0cmd - Exit the command prompt mode"
                    )
                    print(help_message)
                elif server_message == '/camera':
                    self.openCamera(client_socket)
                else:
                    print(f"[Required command specified. For details, input\"/help\"]")
                
        except ConnectionResetError:
            print(f"[ Connection reset by {addr} ]")
        finally:
            client_socket.close()
            print("[ Searching . . .]")
            
    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            client_thread = threading.Thread(target=self.establishClient, args=(client_socket, addr))
            client_thread.start()
            
if __name__ == "__main__":
    server = Server()
    server.start()
