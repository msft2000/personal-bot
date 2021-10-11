from gtts import gTTS
from playsound import playsound
from os import remove
s = gTTS("Sample Text")
s.save('sample.mp3')
playsound('sample.mp3')
remove('./sample.mp3')