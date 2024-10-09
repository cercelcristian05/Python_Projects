import pyaudio
import wave

# Parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the stream for reading the microphone input and playing it back
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("Recording and playing back... Press Ctrl+C to stop.")

try:
    while True:
        # Read audio from the microphone
        data = stream.read(CHUNK)

        # Play back the audio
        stream.write(data, CHUNK)

except KeyboardInterrupt:
    print("Stopped.")

finally:
    # Close the stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    p.terminate()
