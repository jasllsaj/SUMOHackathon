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

# initial user prompt
INIT_PROMPT = "What would you like to find?"

def speech2text(mode, optarg1, optarg2):
    r = sr.Recognizer()

    if mode == ASK_ITEM:

        # ask what the user would like to find
        prompt = gTTS(text=INIT_PROMPT, lang=language)
        prompt.save('prompt.mp3')
        playsound('prompt.mp3')
        # optarg1 is the item catalogue
        test = sr.AudioFile('Apple.wav')
        with test as source:
            audio = r.record(source)
        request = r.recognize_google(audio)

        # find if the requested item is available
        foundItem = False
        correctItem = None
        for key in optarg1:
            if key in request:
                request = "You requested. " + key
                foundItem = True
                correctItem = key
        if not foundItem:
            request = "Sorry, item could not be found"
        output = gTTS(text=request, lang=language, slow=False)
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
    playsound('test.mp3')
    return correctItem