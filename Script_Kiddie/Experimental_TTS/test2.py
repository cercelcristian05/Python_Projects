import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Set properties: volume, rate, and voice
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Get the available voices and select one (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Use the first available voice

# Text to be spoken
text = """XXXDDDDDDD"""

# Convert the text to speech
engine.say(text)

# Run and wait until the speech is finished
engine.runAndWait()
