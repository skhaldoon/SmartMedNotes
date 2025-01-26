import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech (default is 200)
engine.setProperty('volume', 1)  # Volume level (from 0.0 to 1.0)

# Text to convert
text = "Hello, I am your assistant. How can I help you today?"

# Convert text to speech
engine.say(text)

# Wait for speech to finish before closing
engine.runAndWait()
