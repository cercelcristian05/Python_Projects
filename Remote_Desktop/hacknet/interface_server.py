import socket
import threading
import time
from customtkinter import *

class Interface(CTk):
    def __init__(self, size):
        super().__init__()
        self.title("Hacknet")
        self.geometry(f'{size[0]}x{size[1]}')
        self.resizable(False, False)
        self.iconbitmap('./hacknet/Hacknet.ico')
        
        self.message = None
        self.message_lock = threading.Lock()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.server = None

    def GUI(self):
        self.bar = CTkFrame(self, corner_radius=0)
        self.bar.pack(fill="both")

        self.client_ip = "Disconnected"
        self.client = f"Client: {self.client_ip}"
        self.home_ip = ""
        self.home = f"Home: {self.home_ip}"

        self.bar_window = CTkLabel(self.bar,
                                   text=f"{self.client}\n{self.home}",
                                   text_color="white",
                                   bg_color="#cb662f",
                                   font=CTkFont(weight="bold", size=8),
                                   anchor='e',
                                   justify='right',
                                   padx=10,
                                   height=16
                                   )
        self.bar_window.pack(fill="x")

        self.frame_resource = CTkFrame(self, corner_radius=0)
        self.frame_resource.pack(fill=BOTH, side=LEFT)
        self.bar_resource = CTkLabel(self.frame_resource,
                                     text="Resource",
                                     width=256,
                                     height=16,
                                     text_color="white",
                                     font=CTkFont(weight="bold", size=8),
                                     bg_color="#224e76")
        self.bar_resource.pack(fill=BOTH)

        self.frame_terminal = CTkFrame(self, corner_radius=0)
        self.frame_terminal.pack(fill=BOTH, side=RIGHT)
        self.bar_terminal = CTkLabel(self.frame_terminal,
                                     text="Terminal",
                                     text_color="white",
                                     bg_color="#224e76",
                                     font=CTkFont(weight="bold", size=8),
                                     height=16,
                                     width=384)
        self.bar_terminal.pack()
        self.box_terminal = CTkTextbox(self.frame_terminal,
                                       width=384,
                                       corner_radius=0,
                                       border_color="#405570",
                                       border_width=1,
                                       height=656,
                                       fg_color="#090e11",
                                       text_color="white",
                                       state=DISABLED,
                                       scrollbar_button_color="#224e76",
                                       font=CTkFont(size=10))
        self.box_terminal.pack()
        self.input_terminal = CTkEntry(self.frame_terminal,
                                       width=384,
                                       corner_radius=0,
                                       border_color="#405570",
                                       height=32,
                                       border_width=1,
                                       fg_color="#090e11",
                                       text_color="white")
        self.input_terminal.pack()
        self.input_terminal.bind("<Return>", self.InputTerminal)

        self.frame_display = CTkFrame(self, corner_radius=0)
        self.frame_display.pack(fill=BOTH, expand=True)
        self.bar_display = CTkLabel(self.frame_display,
                                    height=16,
                                    text="Display",
                                    font=CTkFont(weight="bold", size=8),
                                    text_color="white",
                                    bg_color="#224e76")
        self.bar_display.pack(fill=BOTH)

        self.frame_connection = CTkFrame(self, corner_radius=0)
        self.frame_connection.pack(fill=BOTH, expand=True)
        self.bar_connnection = CTkLabel(self.frame_connection,
                                        height=16,
                                        text="Connection",
                                        font=CTkFont(weight="bold", size=8),
                                        text_color="white",
                                        bg_color="#224e76")
        self.bar_connnection.pack(fill=BOTH)

    def InputTerminal(self, event):
        user_input = self.input_terminal.get()
        self.statusTerminal(f"> {user_input}")
        self.input_terminal.delete(0, 'end')
        with self.message_lock:
            self.message = user_input

    def getMessage(self):
        with self.message_lock:
            return self.message

    def clearMessage(self):
        with self.message_lock:
            self.message = None

    def UpdateSC(self, client_ip, home_ip):
        self.client_ip = client_ip
        self.home_ip = home_ip
        self.home = f"Home: {self.home_ip}"
        self.client = f"Client: {self.client_ip}"
        self.bar_window.configure(text=f"{self.client}\n{self.home}")

    def statusTerminal(self, text):
        self.box_terminal.configure(state="normal")
        self.box_terminal.insert("end", f"{text}\n")
        self.box_terminal.configure(state="disabled")
        self.box_terminal.yview("end")

    def on_closing(self):
        if self.server:
            self.server.server_socket.close()
            for client_socket in self.server.client_sockets:
                client_socket.close()
            self.quit()

    def start(self):
        self.mainloop()

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
        self.interface_server.GUI()
        self.interface_server.statusTerminal("[ The server has started ]\n> Searching connection to client . . .\n")

        self.hostname = socket.gethostname()
        self.interface_server.home_ip = socket.gethostbyname(self.hostname)
        self.interface_server.UpdateSC('Disconnected', self.interface_server.home_ip)
        
        self.statusCmd = False
        self.statusPs = False

    def connectionClient(self, client_socket, addr):
        self.interface_server.statusTerminal(f"> Connection established with {addr} !")
        print(f"> Connection established with {addr} !")
        self.interface_server.UpdateSC(addr[0], self.interface_server.home_ip)

        try:
            while True:
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

                time.sleep(0.1)

        except ConnectionResetError:
            self.interface_server.statusTerminal(f"[ Connection reset by {addr} ]")
            self.interface_server.UpdateSC('Disconnected', self.interface_server.home_ip)
        finally:
            client_socket.close()
            self.interface_server.statusTerminal("[ Searching . . .]")
            self.interface_server.UpdateSC('Disconnected', self.interface_server.home_ip)

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
