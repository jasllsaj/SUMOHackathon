# This program is to 
# SUMO HACKATHON 2020
# Author: Jason Lai

import speech_recognition as sr
from gtts import gTTS
import os
language = 'en'
from playsound import playsound
# operating mode
ASK_ITEM = 1
GIVE_DIRECTION = 2
IS_CORRECT_ITEM = 3

# directions
LEFT = 1
RIGHT = 2

print("Hello")

def speech2text(mode, optarg1, optarg2):
    r = sr.Recognizer()

    if mode == ASK_ITEM:
        test = sr.AudioFile('test.wav')
        with test as source:
            audio = r.record(source)
        request = "You requested " + r.recognize_google(audio)
        print(request)
        output = gTTS(text=request, lang=language, slow=True)
    elif mode == GIVE_DIRECTION:
        # optarg1 is the correct direction, optarg2 is the aisle
        if optarg1 == LEFT:
            direction = "turn left into aisle. "
        else:
            direction = "turn right into aisle. "
        direction = direction + str(optarg2)
        print(direction)
        output = gTTS(text=direction, lang=language, slow=True)
    elif mode == IS_CORRECT_ITEM:
        # optarg1 is whether the item is correct
        if optarg1 == True:
            answer = "This is the correct item"
        else:
            answer = "This is an incorrect item"
        print(answer)
        output = gTTS(text=answer, lang=language, slow=False)
    else:
        print("invalid mode")
    
    output.save("test.mp3")

speech2text(IS_CORRECT_ITEM, True, 0)