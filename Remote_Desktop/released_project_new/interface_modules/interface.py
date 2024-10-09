import threading; from customtkinter import *

class Interface(CTk):
    def __init__(self, size):
        super().__init__()
        self.configure(bg="#224e76")
        self.title("Hacknet")
        self.geometry(f'{size[0]}x{size[1]}')
        self.resizable(False, False)
        self.iconbitmap('./hacknet/Hacknet.ico')
        
        self.statusConnectionType = "Disconnected"
        self.message = None
        self.message_lock = threading.Lock()
        self.disconnect_requested = False
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.server = None
        self.status_administrator = None
        self.menu_option = None
        self.disconnect_status = StringVar(value='/0q')

    def BarStatus(self):
        self.bar = CTkFrame(self, corner_radius=0)
        self.bar.pack(fill="both")
        
        self.varStr = StringVar(value="File")
        self.optionmenu = CTkOptionMenu(self.bar,
                                        corner_radius=0,
                                        values=["New", "Open"],
                                        command=self.optionmenu_callback(),
                                        variable=self.varStr,
                                        height=16,
                                        bg_color="#cb662f",
                                        fg_color="#cb662f",
                                        button_color="#cb662f",
                                        dropdown_fg_color="#cb662f")
        self.optionmenu.pack(side=LEFT, fill=BOTH)
        
        self.client_ip = "Disconnected"
        self.client = f"Client: {self.client_ip}"
        self.home_ip = ""
        self.home = f"Home: {self.home_ip}"
        
        self.bar_window = CTkLabel(self.bar,
                                   text=f"{self.client}\n{self.home}",
                                   text_color="white",
                                   bg_color="#cb662f",
                                   font=CTkFont(weight="bold", size=8, family="Verdana"),
                                   anchor='e',
                                   justify='right',
                                   padx=10,
                                   height=16
                                   )
        self.bar_window.pack(fill="x")
        
    def optionmenu_callback(choice):
        print("optionmenu dropdown clicked:", choice)
        
    def WindowResource(self):
        self.frame_resource = CTkFrame(self, corner_radius=0, fg_color="#090e11", border_color="#405570", border_width=1)
        self.frame_resource.pack(fill=BOTH, side=LEFT)
        self.bar_resource = CTkLabel(self.frame_resource,
                                     text="Resource",
                                     width=256,
                                     height=17,
                                     text_color="white",
                                     font=CTkFont(weight="bold", size=8, family="Verdana"),
                                     bg_color="#224e76")
        self.bar_resource.pack(fill=BOTH)

    def WindowTerminal(self):
        self.frame_terminal = CTkFrame(self, corner_radius=0)
        self.frame_terminal.pack(fill=BOTH, side=RIGHT)
        self.bar_terminal = CTkLabel(self.frame_terminal,
                                     text="Terminal",
                                     text_color="white",
                                     bg_color="#224e76",
                                     font=CTkFont(weight="bold", size=8, family="Verdana"),
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
                                       font=CTkFont(size=8, family="Verdana"))
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

    def WindowDisplay(self):
        self.frame_display = CTkFrame(self, corner_radius=0, fg_color="#090e11", border_color="#405570", border_width=1, height=480)
        self.frame_display.pack_propagate(0)
        self.frame_display.pack(fill=BOTH)
        self.bar_display = CTkLabel(self.frame_display,
                                    height=17,
                                    text="Display",
                                    font=CTkFont(weight="bold", size=8, family="Verdana"),
                                    text_color="white",
                                    bg_color="#224e76")
        self.bar_display.pack(fill=BOTH)
        
        if self.statusConnectionType:
            self.DisconnectedStatusDisplay()

    def WindowConnection(self):
        self.frame_connection = CTkFrame(self, corner_radius=0, fg_color="#090e11", border_color="#405570", border_width=1, height=240)
        self.frame_connection.pack_propagate(0)
        self.frame_connection.pack(fill=BOTH)
        self.bar_connnection = CTkLabel(self.frame_connection,
                                        height=17,
                                        text="Connection",
                                        font=CTkFont(weight="bold", size=8, family="Verdana"),
                                        text_color="white",
                                        bg_color="#224e76")
        self.bar_connnection.pack(fill=BOTH)

    def ConnectionStatusDisplay(self, status_client):
        if hasattr(self, 'status_disconnected'):
            self.status_disconnected.destroy()
        
        self.status_connected = CTkLabel(self.frame_display, 
                                         corner_radius=0, 
                                         text_color="white",
                                         text=status_client,
                                         font=CTkFont(size=16, weight="bold", family="Verdana"),
                                         height=64)
        self.status_connected.pack(fill="x", padx=1)
        
    def DisconnectedStatusDisplay(self):
        if hasattr(self, 'status_connected'):
            self.status_connected.destroy()
   
        self.status_disconnected = CTkLabel(self.frame_display, 
                                           corner_radius=0, 
                                           fg_color="#224e76",
                                           text=self.statusConnectionType,
                                           text_color="white",
                                           font=CTkFont(size=32, weight="bold", family="Verdana"),
                                           height=64)
        self.status_disconnected.pack(fill="x", padx=1, pady=182)
        
    def AdministratorStatusDisplay(self, status):
        if self.status_administrator is None:
            self.status_administrator = CTkLabel(self.frame_display, 
                                                corner_radius=0, 
                                                fg_color="#cb662f",
                                                text_color="white",
                                                text=status if status else "Not Available",
                                                font=CTkFont(size=16, weight="bold", family="Verdana"),
                                                height=32)
            self.status_administrator.pack(fill="x", padx=1)
        else:
            self.status_administrator.configure(text=status)

    def clearAdministratorStatus(self):
        if self.status_administrator is not None:
            self.status_administrator.destroy()
            self.status_administrator = None
            
    def MenuDisplay(self):
        if self.menu_option is None:
            self.menu_option=CTkFrame(self.frame_display, fg_color="#090e11")
            self.menu_option.pack_propagate(0)
            self.menu_option.pack(fill=X, pady=48, padx=8)
            
            self.button_filesystem = CTkButton(self.menu_option, 
                                               corner_radius=0, 
                                               border_width=1, 
                                               border_color="#405570",
                                               fg_color="#090e11",
                                               text_color="#224e76",
                                               font=CTkFont(size=16, weight="bold", family="Verdana"),
                                               height=16,
                                               text="View FileSystem",
                                               command=self.FileManager
                                               )
            self.button_filesystem.pack(fill=X, padx=96, pady=8)

            self.button_logs = CTkButton(self.menu_option, 
                                               corner_radius=0, 
                                               border_width=1, 
                                               border_color="#405570",
                                               fg_color="#090e11",
                                               text_color="#224e76",
                                               font=CTkFont(size=16, weight="bold", family="Verdana"),
                                               height=16,
                                               text="View Logs",
                                               command=self.LogManager
                                               )
            self.button_logs.pack(fill=X, padx=96)
            
            self.button_disconnect = CTkButton(self.menu_option, 
                                               corner_radius=0, 
                                               border_width=1, 
                                               border_color="#405570",
                                               fg_color="#090e11",
                                               text_color="#224e76",
                                               font=CTkFont(size=16, weight="bold", family="Verdana"),
                                               height=16,
                                               text="Disconnect",
                                               command=self.DisconnectButton
                                               )
            self.button_disconnect.pack(fill=X, padx=96, pady=24)
            
    def FileManager(self):
        print("Filesystem")
        
    def LogManager(self):
        print("Log")
        
    def DisconnectButton(self):
        self.disconnect_requested = True
        self.disconnect_status.set('/0q')
        
    def NoMenuDisplay(self):
        if self.menu_option is not None:
            self.button_disconnect.destroy()
            self.button_logs.destroy()
            self.button_filesystem.destroy()
            self.menu_option.destroy()
            self.menu_option = None
        
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