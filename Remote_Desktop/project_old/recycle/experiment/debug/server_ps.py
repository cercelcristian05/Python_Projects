import socket

class Server:
    def __init__(self, host='0.0.0.0', port=12505):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        
    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            print(f"Server listening on {self.host}:{self.port}")
            
            self.client_socket, addr = self.server_socket.accept()
            print(f"Connection established from {addr}")
            
            self.send_commands()
            
        except Exception as e:
            print(f"Error starting server: {e}")
        finally:
            if self.client_socket:
                self.client_socket.close()
            self.server_socket.close()
    
    def send_commands(self):
        try:
            while True:
                command = input("Enter a PowerShell command (type 'quit' to exit): ")
                if command.lower() == 'quit':
                    break
                
                self.client_socket.sendall(command.encode('utf-8'))
                response = self.client_socket.recv(4096).decode('utf-8')
                print(f"Command: {command}\nOutput:\n{response}\n")
        except Exception as e:
            print(f"Error sending commands: {e}")

if __name__ == "__main__":
    server = Server()
    server.start()  # Start the server (inputs commands and sends them)