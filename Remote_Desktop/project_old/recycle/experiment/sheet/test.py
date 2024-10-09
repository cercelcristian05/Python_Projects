import pyaudio
import numpy as np

CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1  # Mono channel
RATE = 44100  # 44.1kHz sampling rate

def start_stream():
    p = pyaudio.PyAudio()

    # Open input stream (microphone)
    stream_input = p.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)

    # Open output stream (speakers/headphones)
    stream_output = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           output=True,
                           frames_per_buffer=CHUNK)

    print("Streaming audio... Press Ctrl+C to stop.")

    try:
        while True:
            # Read data from the input stream
            data = stream_input.read(CHUNK)
            
            # Write data to the output stream
            stream_output.write(data)
    except KeyboardInterrupt:
        print("Stopping stream...")

    # Stop and close streams
    stream_input.stop_stream()
    stream_input.close()
    stream_output.stop_stream()
    stream_output.close()
    
    # Terminate PyAudio
    p.terminate()

if __name__ == "__main__":
    start_stream()
