import pyttsx3

engine = pyttsx3.init('sapi5')  # Use 'sapi5' for Windows
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Try voices[1] if needed

engine.say("Testing. Lexa should now speak news headlines.")
engine.runAndWait()
