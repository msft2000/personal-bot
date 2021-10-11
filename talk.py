from gtts import gTTS
from playsound import playsound
from os import remove
def talk(sentence):
    s = gTTS(sentence)
    s.save('aux.mp3')
    playsound('aux.mp3')
    remove('./aux.mp3')
