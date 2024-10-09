import socket
import threading
import time, ctypes
from interface_modules.interface import Interface

class Server:
    def __init__(self, host='0.0.0.0', port=12505):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        self.client_sockets = []

        self.interface_server = Interface((1280, 720))
        self.interface_server.server = self
        
        self.interface_server.BarStatus()
        self.interface_server.WindowResource()
        self.interface_server.WindowTerminal()
        self.interface_server.WindowDisplay()
        self.interface_server.WindowConnection()
        
        self.interface_server.statusTerminal("[ The server has started ]\n> Searching connection to client . . .\n")
        self.interface_server.statusTerminal("[This is on beta unfortunate]\n")
        self.hostname = socket.gethostname()
        self.interface_server.home_ip = socket.gethostbyname(self.hostname)
        self.interface_server.UpdateSC('Disconnected', self.interface_server.home_ip)
        
        self.statusCmd = False
        self.statusPs = False
        self.statusClient = False

    def commandPrompt(self, client_socket):
        self.statusCmd = True
        
        while self.statusCmd:
            current_message = self.interface_server.getMessage()
            
            if current_message is not None:
                if current_message.lower() == '/0cmd':
                    client_socket.send('quit'.encode())
                    self.interface_server.statusTerminal("[ Command Mode has been closed ]")
                    self.statusCmd = False
                    break 
                elif current_message.strip() == '':
                    self.interface_server.statusTerminal(">")
                    self.interface_server.clearMessage()

                client_socket.send(current_message.encode())
                client_response = client_socket.recv(2048).decode()
                self.interface_server.statusTerminal(f"{client_response}")
                self.interface_server.clearMessage()
                    
            else:
                time.sleep(0.1)
        self.interface_server.clearMessage()
                
    def powerShell(self, client_socket):
        self.statusPs = True
        print("[ Powershell Mode Activated ]")
        
        while self.statusPs:
            current_message = self.interface_server.getMessage()
            
            if current_message is not None:
                if current_message.lower() == '/0ps':
                    client_socket.send('exit'.encode())
                    self.interface_server.statusTerminal("[ Powershell Mode has been closed ]")
                    self.statusPs = False
                    break 
                elif current_message.strip() == '':
                    self.interface_server.statusTerminal(">")
                    self.interface_server.clearMessage()

                try:
                    client_socket.send(current_message.encode('utf-8'))
                    client_response = client_socket.recv(4096).decode('utf-8')
                    print(f"Received from client: {client_response}")
                    self.interface_server.statusTerminal(f"{client_response}")
                except Exception as e:
                    self.interface_server.statusTerminal(f"Error: {str(e)}")
                
                self.interface_server.clearMessage()
            else:
                time.sleep(0.1)

        self.interface_server.clearMessage()
        
    def connectionClient(self, client_socket, addr):
        client_hostname = socket.gethostbyaddr(addr[0])[0]
        self.interface_server.statusTerminal(f"> Connection established with {addr} !")
        print(f"> Connection established with {addr} !")
        
        self.statusClient = True
        if self.statusClient is True:
            self.interface_server.UpdateSC(addr[0], self.interface_server.home_ip)
            self.interface_server.ConnectionStatusDisplay(f"Connected To {client_hostname} @{addr[0]}")

        try:
            admin_status = client_socket.recv(1024).decode('ascii')
            self.interface_server.AdministratorStatusDisplay(admin_status)
            
            self.interface_server.MenuDisplay()
            disconnect_button = self.interface_server.disconnect_status
            
            while True:  
                if self.interface_server.disconnect_requested:
                    break
      
                current_message = self.interface_server.getMessage()
                
                if current_message:
                    client_socket.send(current_message.encode())
                    self.interface_server.clearMessage()
                    if current_message == '/0q':
                        self.interface_server.statusTerminal(f"[ {addr} has been closed ]")
                        break
                    elif current_message == '/cmd':
                        self.interface_server.statusTerminal("[ Command Prompt Mode Activated ]")
                        self.commandPrompt(client_socket)
                    elif current_message == '/ps':
                        self.interface_server.statusTerminal("[ Powershell Mode Activated ]")
                        self.powerShell(client_socket)
                    else:
                        print(f"> Sent message to {addr}: {current_message}")
                    self.interface_server.clearMessage()        
                if disconnect_button == '/0q':
                    self.interface_server.statusTerminal(f"[ {addr} has been closed ]")
                    break
                time.sleep(0.1)

        except ConnectionResetError:
            self.interface_server.DisconnectedStatusDisplay()
            self.interface_server.statusTerminal(f"[ Connection reset by {addr} ]")
            self.interface_server.clearAdministratorStatus()
            self.interface_server.NoMenuDisplay()
            self.interface_server.UpdateSC('Disconnected', self.interface_server.home_ip)
        finally:
            client_socket.close()
            self.interface_server.DisconnectedStatusDisplay()
            self.interface_server.statusTerminal("[ Searching . . .]")
            self.interface_server.clearAdministratorStatus()
            self.interface_server.NoMenuDisplay()
            self.interface_server.UpdateSC('Disconnected', self.interface_server.home_ip)
    
    def start_server(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            client_thread = threading.Thread(target=self.connectionClient, args=(client_socket, addr))
            client_thread.start()

    def start(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

if __name__ == '__main__':
    server = Server()
    server.start()
    server.interface_server.start()
