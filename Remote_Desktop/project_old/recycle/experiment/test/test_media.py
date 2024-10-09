import ffmpeg
import soundfile as sf
import sounddevice as sd
from pytube import YouTube

def download_video(url):
    try:
        youtube_object = YouTube(url)
        video_stream = youtube_object.streams.get_highest_resolution()
        input_video_path = "input_video.mp4"  # Specify the input video path
        video_stream.download(filename=input_video_path)
        print(f"Downloaded video saved at: {input_video_path}")
        return input_video_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

def convert_to_wav(input_video_path, output_audio_path):
    try:
        (
            ffmpeg
            .input(input_video_path)
            .output(output_audio_path, format='wav', acodec='pcm_s16le', ar=44100, ac=2)
            .overwrite_output()
            .run()
        )
        print(f"Converted {input_video_path} to {output_audio_path}")
        return True
    except ffmpeg.Error as e:
        print(f"Error converting {input_video_path} to WAV: {e.stderr}")
        return False

def play_audio(output_audio_path):
    try:
        # Open the WAV file using soundfile
        wave_data, fs = sf.read(output_audio_path, dtype='float32')

        # Play the audio
        sd.play(wave_data, fs)
        print(f"Now playing: {output_audio_path}")

        return True
    except Exception as e:
        print(f"Error playing audio: {e}")
        return False

def stop_audio():
    try:
        sd.stop()
        print("Audio playback stopped.")
        return True
    except Exception as e:
        print(f"Error stopping audio: {e}")
        return False

# URL of the YouTube video
url = "https://youtu.be/m7GoofKA2VA?si=bDzH4D1i0Hb4jyy4"

# Download the video
input_video_path = download_video(url)

if input_video_path:
    output_audio_path = "output_audio.wav"  # Specify the output audio path

    # Convert to WAV
    if convert_to_wav(input_video_path, output_audio_path):
        # Play the audio
        if play_audio(output_audio_path):
            # Wait for user input to stop the audio (for demonstration purposes)
            input("Press Enter to stop playback...")
            stop_audio()
        else:
            print("Error occurred while playing audio.")
    else:
        print("Error occurred while converting video to WAV.")
else:
    print("Error occurred while downloading video.")
