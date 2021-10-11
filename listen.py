import speech_recognition as sr
import sys
from talk import talk
def listen(question):
    r = sr.Recognizer() 
    VALID_VOICE= True
    while VALID_VOICE:
            with sr.Microphone() as source:
                talk(question)
                audio = r.listen(source)
                try:
                    text = r.recognize_google(audio)
                    VALID_VOICE=False
                except:
                    talk('Sorry could not hear')
    if text.lower()=="goodbye jarvis":
        talk("Bye have a nice day")
        sys.exit()
    return text