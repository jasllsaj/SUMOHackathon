import speechtext
import query
import configparser
import pandas as pd
import numpy

BMP_WALL = -1
BMP_FLOOR = 0
BMP_ENTRY = -2

if __name__ == '__main__':
    
    # read in floor and aisle plans stored as an occupancy matrix
    with open('./plans/floormap.csv') as csvfile:
        floorMap = pd.read_csv(csvfile, delimiter=',') 
    
    config = configparser.ConfigParser()
    config.read('config.cfg')
    numAisles = config['SHOPMAP']['numAisles']
    numLevels = config['SHOPMAP']['numLevels']

    items = dict(config['ITEMS'])
    checkout = False
    # keep asking for items until user wants to go to checkout
    while not checkout:
        # keep asking for an item until there is something in stock
        correctItem = None
        while not correctItem:
            request = speechtext.speech2text(speechtext.ASK_ITEM, items, 0)
            if request:
                correctItem = query.stockQuery(request, items)
            if not correctItem:
                speechtext.playVoice(speechtext.NOT_FOUND_PROMPT, speechtext.ASK_ITEM)
            #print(correctItem)
        
        # prepare graph and nodes for searching algorithm: BFS

        # query store data for item location
        itemLocations = dict(config['AISLES'])
        whichAisle = itemLocations.get(correctItem)
        whichAisle = eval(whichAisle) # config files store dict values as strings
        goalPrompt = 'Your item is in Aisle. ' + str(whichAisle[0]) + '. On the ' + speechtext.SHELVES[whichAisle[1]] + ' shelf. Calculating the best route.'
        speechtext.playVoice(goalPrompt, speechtext.GIVE_DIRECTION)
        # while you are not at the correct location
            # localise (find current location)
            # calculate the best path to the item (path optimisation)
        
        # now at the correct shelf. Give instruction to pick up item
        
        # check if picked up item is correct

        # once correct item is picked up, ask if person would like to go to checkout
            # if NO, repeat the process
        request = speechtext.speech2text(speechtext.ASK_CHECKOUT,0,0)
        if 'yes' in request or 'yea' in request or 'yep' in request:
            checkout = True

    # find best path to checkout
    print('Calculating path to checkout')