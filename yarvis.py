import os
import time
from playsound import playsound
from os import remove
from foto_a_caricatura import cartoon_maker
from talk import talk
from listen import listen
from answer_questions import answer_questions
options={"nothing":"kill jarvis","wait":"pause yarvis for some time","answer something":"answer a question based on a corpus","cartoon":"convert a foto in to a cartoon"}
def main():
    talk("Hi Mateo Yarvis here for you")
    KEEP_HELPING=True
    while KEEP_HELPING:
        action_to_do=listen("What I can do for you now?").lower()
        if action_to_do=="answer something":
            answer_questions()
        elif action_to_do=="i don't know":
            for option in options:
                talk(f"Say {option} for made me  {options[option]}")
        elif action_to_do=="wait":
            time.sleep(int(listen("How many seconds?")))
        elif action_to_do=="cartoon":
            VALIDAR_FOTO=False
            while not VALIDAR_FOTO:
                try: 
                    temp_img=cartoon_maker(f"{listen('Which is the name of the photo?')}.jpg")
                    VALIDAR_FOTO=True
                except:
                    talk("Sorry I donot find it")
            wait_for_photo=listen("how many seconds you want to see the photo?")
            os.system(f"open assets/imgs/{temp_img}")
            time.sleep(int(wait_for_photo))
            os.system(f"close assets/imgs/{temp_img}")
            os.system(f"rm assets/imgs/{temp_img}")
        elif action_to_do=="nothing":
            KEEP_HELPING=False
            talk("Bye have a nice day")
        else:
            talk("Sorry can you repeat it")

if __name__ == "__main__":
    main()
