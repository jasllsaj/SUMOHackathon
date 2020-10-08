# This program is to 
# SUMO HACKATHON 2020
# Author: Jason Lai

import speech_recognition as sr
from gtts import gTTS
import os
language = 'en'
from playsound import playsound
import graph
# operating mode
ASK_ITEM = 1
GIVE_DIRECTION = 2
IS_CORRECT_ITEM = 3
ASK_CHECKOUT = 4
PLAY_INIT_PROMPT = 5
PLAY_PICKUP_PROMPT = 6
PLAY_CHECKOUT_PROMPT = 7
THANKYOU = 8

# user prompts
INIT_PROMPT = "What would you like to find?"
CHECKOUT_PROMPT = "Would you like to checkout?"
NOT_FOUND_PROMPT = "Sorry. Your item could not be found."
PICKUP_ITEM = "Please pick up an item from the"

# shelves
SHELVES = ("top", "middle", "bottom")

def speech2text(mode, optarg1, optarg2):
    r = sr.Recognizer()

    if mode == ASK_ITEM:
        # optarg1 is the item catalogue
        # ask what the user would like to find
        playVoice(INIT_PROMPT, PLAY_INIT_PROMPT)
        
        # fetch audio
        # from file source
        #test = sr.AudioFile('Apple.wav')
        #with test as source:
         #   audio = r.record(source)
        #request = r.recognize_google(audio)

        # from microphone
        print('Listening...')
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            request = (r.recognize_google(audio)).lower()
            print(request)
            return request
        except Exception as e:
            print('You said nothing!')
            return   
    elif mode == GIVE_DIRECTION:
        # optarg1 is the correct direction, optarg2 is whether you are turning into the end corridor
        if optarg1 == graph.STRAIGHT:
            return
        elif optarg1 == graph.TURN_BACK:
            direction = "turn around."
        else:
            if optarg1 == graph.TURN_LEFT:
                direction = "turn left into the "
            elif optarg1 == graph.TURN_RIGHT:
                direction = "turn right into the "
            
            if optarg2 == True:
                direction = direction + "end corridor"
            else:
                direction = direction + "aisle"
        print(direction)
        playVoice(direction, mode)
    elif mode == IS_CORRECT_ITEM:
        # optarg1 is whether the item is correct
        if optarg1 == True:
            answer = "This is the correct item"
        else:
            answer = "This is an incorrect item"
        print(answer)
        playVoice(answer, mode)
    elif mode == ASK_CHECKOUT:
        # ask user if they want to checkout
        playVoice(CHECKOUT_PROMPT, PLAY_CHECKOUT_PROMPT)
        # listen to their response
        print('Listening...')
        with sr.Microphone() as source:
            audio = r.listen(source)
        
        request = None
        while not request:
            request = (r.recognize_google(audio)).lower()
        print(request)
        return request
    else:
        print("invalid mode")

def playVoice (response, mode):
    output = gTTS(text=response, lang=language, slow=False)
    if mode == PLAY_INIT_PROMPT:
        output.save('initPrompt.mp3')
        playsound('initPrompt.mp3')
    elif mode == ASK_ITEM:
        output.save('itemRequestResponse.mp3')
        playsound('itemRequestResponse.mp3')
    elif mode == GIVE_DIRECTION:
        output.save('directions.mp3')
        playsound('directions.mp3')
    elif mode == IS_CORRECT_ITEM:
        output.save('itemCheck.mp3')
        playsound('itemCheck.mp3')
    elif mode == PLAY_PICKUP_PROMPT:
        output.save('pickupPrompt.mp3')
        playsound('pickupPrompt.mp3')
    elif mode == PLAY_CHECKOUT_PROMPT:
        output.save('checkoutPrompt.mp3')
        playsound('checkoutPrompt.mp3')
    elif mode == THANKYOU:
        output.save('thankyou.mp3')
        playsound('thankyou.mp3')
    else:
        return
