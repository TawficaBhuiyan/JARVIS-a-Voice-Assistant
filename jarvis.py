import speech_recognition as sr
import pyttsx3
import logging
import datetime
import wikipedia
import webbrowser
import random
import subprocess
import os
import google.generativeai as genai 
#Logging configuration
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO
)

#We are using functional programming instead of scripting programming FOR better code management and readability

# Activating voice from our system
engine = pyttsx3.init("sapi5") #pyttsx3 initializes the speech engine for text-to-speech conversion
voices = engine.getProperty("voices") #returns a list of voices available on the system
engine.setProperty("rate",200)
engine.setProperty("voice", voices[0].id)
# print(voices[0].id) #david
# print(voices[1].id) #zira


# #This is speak function
def speak(text):
    """This function converts text to voice

    Args:
        text 
    returns:
        voice
    """
    engine.say(text)
    engine.runAndWait() #closed the engine after speaking the text





#This function recognizes the speech and converts it to the text

def take_command():                                  # Defines a function to take voice input
    """
    This function takes command and recognizes speech.
    Returns: recognized text as a query.
    """

    r = sr.Recognizer()                              # Creates a Recognizer object to recognize speech and convert it into text

    with sr.Microphone() as source:                  # Uses the microphone as the audio input source
        print("Listening...")                        # Displays a message while waiting for voice input
        r.pause_threshold = 1                        # Considers the command complete after 1 second of silence
        audio = r.listen(source)                     # Records voice input and stores the audio in the audio variable

    try:                                             # Executes code that may cause an error
        print("Recognizing...")                      # Displays a message while converting speech into text
        query = r.recognize_google(audio, language="en-IN")  # Converts recorded audio into text using Google Speech Recognition
        print(f"User said: {query}\n")               # Prints the recognized text

    except Exception as e:                           # Handles any error that occurs in the try block
        logging.info(e)                              # Logs the error for debugging
        print("Say that again please...")            # Asks the user to repeat the command
        return "None"                                # Stops the function and returns the string "None"

    return query        # Returns the recognized text if no error occurs


def play_music():
    music_dir = "E:\\JARVIS-a-Voice-Assistant\\music"
    try:
        songs = os.listdir(music_dir) #returns the musics list as list
        if songs:
            random_song = random.choice(songs)
            speak(f"Playing a random song for you:{random_song}")
            os.startfile(os.path.join(music_dir,random_song))
            logging.info(f"Playing a random song for you:{random_song}")
        else:
            speak("No Music files in your directory.")
    except Exception as e:
        speak("No Music files in your directory.")
        logging.info(e)


def gemini_model_response(user_input):
    GEMINI_API_KEY = "YOUR_API_KEY"
    genai.configure(api_key=GEMINI_API_KEY) #set configuration to use gemini api
    model = genai.GenerativeModel("gemini-3.1-flash-lite")
    prompt = f"Your name is JARVIS and act like JARVIS and Answere the  provided question in short, Question:{user_input}"
    response = model.generate_content(prompt)
    result = response.text

    return result


def  greeting():
    hour = (datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning!")
    elif hour > 12 and hour <= 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")  
    speak("How are you doing today?")                 
    speak("Hello, I am Jarvis.Please tell me how can I help you.")

greeting()

while True:
    query = take_command().lower()                             # Calls the function and stores its returned value in query
    print(query)                                         # Prints the returned value

    if "your name" in query:
        speak("My name is Jarvis")
        logging.info("User asked for assistant's name.")

    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
        logging.info("User asked for current time.")

    elif "how are you" in query:
        speak("I'm Fine.")
        logging.info("User asked for assistant's well-being.")
        
    elif "who made you" in query:
        speak("I was created by Tawfica Bhuiyan!")
        logging.info("User asked for assistant's creator.")
        

    elif "thank you" in query:
        speak("It's my pleasure!")
        logging.info("User expressed grattitude.")

        
    #google opening
    elif "open google" in query:
        speak("ok, please type what do you want to read")
        webbrowser.open("google.com") #webbrowser.open() is a class of method webbrowser
        logging.info("User requested to open google.")
        

    #calculator open
    elif "calculator" in query:
        speak("Opening Calculator")
        subprocess.Popen("calc.exe")  #Launches the Windows Calculator application
        logging.info("User requested to open calculator.")

    #notepad open
    elif "calculator" in query:
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe") #Popen() is a class of subprocess module
        logging.info("User requested to open notepad.")

    #Command Prompt open
    elif "terminal" in query or "cmd" in query:
        speak("Opening Command Prompt Terminal")
        subprocess.Popen("cmd.exe")
        logging.info("User requested to open terminal.")

    #Google Calender
    elif "calendar" in query:
        speak("Opening Windowa Calendar")
        webbrowser.open("https://calendar.google.com") # Opens Google Calendar in the default browser
        logging.info("User requested to open calendar.")

    #Youtube search
    elif "youtube" in query:
        speak("Opening Youtube.")
        query = query.replace("youtube","") # Removes the word "youtube" from the user's command
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")  # Opens YouTube with the remaining query as the search term
        logging.info("User requested to search on youtube.")

    #Open facebook
    elif "facebook" in query:
        speak("Opening Facebook.")
        webbrowser.open("facebook.com") 
        logging.info("User requested to open facebook.")
    
#Open github
    elif "github" in query:
            speak("Opening github.")
            webbrowser.open("github.com") 
            logging.info("User requested to open github.")

    elif "joke" in query:
        jokes = [
            "Why dont programmers like nature? Too many bugs.",
            "I told my computer I needed a break. It said no problem, it will go to sleep.",
            "Why do Java developers wear glasses?  Because they don't C sharp."
        ]
        speak(random.choice(jokes))
        logging.info("User requested a joke.")

    elif "wikipedia" in query:
        speak("Searching Wikipedia")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak(results)
        logging.info("User requested information in wikipedia")

    elif "music" in query:
        play_music()

    elif "exit" in query:
        speak("Thanks for your time")
        logging.info("User exited the program.")
        exit()
        

    else:
        response = gemini_model_response(query)
        speak(response)
        logging.info("User asked for advanced  questions.")


