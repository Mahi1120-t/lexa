import sounddevice as sd
from scipy.io.wavfile import write
import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from gtts import gTTS
import playsound
import musicLibrary
import time

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

recognizer = sr.Recognizer()
news_data = []

def speak(text):
    print("[LEXA] Speaking:", text)
    tts = gTTS(text)
    tts.save("temp.mp3")
    playsound.playsound("temp.mp3")
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

def record_audio(duration=4, filename="input.wav"):
    fs = 44100  # Sample rate
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    write(filename, fs, audio)
    print("Recording saved.")

def listen_and_recognize():
    record_audio()
    with sr.AudioFile("input.wav") as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            print("Recognized:", text)
            return text.lower()
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print("Speech recognition error:", e)
            return ""

def get_news():
    global news_data
    print("Fetching news...")
    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines?country=us&apiKey=94086cd29f834eae80a75842b036b26b"
        )
        if response.status_code == 200:
            data = response.json()
            news_data = data.get('articles', [])[:5]
            if news_data:
                speak("Here are the top 5 headlines.")
                for i, article in enumerate(news_data, 1):
                    title = article.get('title', 'No title')
                    speak(f"Headline {i}: {title}")
            else:
                speak("No news articles found.")
        else:
            speak("Unable to fetch news right now.")
    except Exception as e:
        print("Error fetching news:", e)
        speak("There was an error fetching the news.")

def speak_news_detail(index):
    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines?country=us&apiKey=94086cd29f834eae80a75842b036b26b"
        )
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])[:5]
            if 1 <= index <= len(articles):
                article = articles[index - 1]
                title = article.get('title', 'No title')
                description = article.get('description', 'No description available')
                url = article.get('url')

                speak(f"Headline {index}: {title}")
                speak("Here is the detailed news.")
                speak(description)

                if url:
                    speak("Opening the article in your browser.")
                    webbrowser.open(url)
            else:
                speak("Sorry, I couldn't find that news headline.")
        else:
            speak("Failed to fetch news details.")
    except Exception as e:
        speak("There was an error retrieving the news.")
        print("News detail error:", e)

def processCommand(c):
    print(f"Recognized command: {c}")

    if "open google" in c:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
    elif "open spotify" in c:
        webbrowser.open("https://spotify.com")
        speak("Opening Spotify")
    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")
        speak("Opening Instagram")
    elif "open amazon" in c:
        webbrowser.open("https://amazon.com")
        speak("Opening Amazon")
    elif c.startswith("play"):
        song = c.replace("play", "").strip().lower()
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak(f"Sorry, I couldn't find {song} in your music library.")
    elif "tell me the news" in c:
        get_news()
    elif "headline" in c or "news" in c:
        number_words = {
            "first": 1,
            "second": 2,
            "third": 3,
            "fourth": 4,
            "fifth": 5,
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5
        }
        for word in c.split():
            if word in number_words:
                index = number_words[word]
                speak_news_detail(index)
                break
    elif "exit" in c or "stop" in c:
        speak("Goodbye!")
        exit()

if __name__ == "__main__":
    speak("Initializing Lexa...")

    while True:
        speak("Say 'Lexa' to activate.")
        command = listen_and_recognize()
        if "lexa" in command:
            speak("Yes?")
            c = listen_and_recognize()
            if c:
                processCommand(c)
