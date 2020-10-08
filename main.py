import speechtext
import query
import graph
import configparser
import pandas as pd
import numpy



if __name__ == '__main__':
    
    # read in floor and aisle plans stored as an occupancy matrix
    with open('./plans/floormap.csv') as csvfile:
        floorMap = pd.read_csv(csvfile, delimiter=',',header=None) 
    
    config = configparser.ConfigParser()
    config.read('config.cfg')
    numAisles = int(config['SHOPMAP']['numAisles'])
    numLevels = int(config['SHOPMAP']['numLevels'])

    # read in aisle plans
    aislePlan = {}
    for i in range(1,numAisles):
        for j in range(1,numLevels):
            filePath = './plans/aisle_'+str(i)+'_'+str(j)+'.csv'
            with open(filePath) as csvfile:
                aislePlan.update({(i,j): pd.read_csv(csvfile, delimiter=",",header=None)})
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
        floorGraph = graph.createGraph(floorMap)
        
        # query store data for item location
        itemLocations = dict(config['AISLES'])
        whichAisle = itemLocations.get(correctItem)
        whichAisle = eval(whichAisle) # config files store dict values as strings
        goalPrompt = 'Your item is in Aisle. ' + str(whichAisle[0]) + '. On the ' + speechtext.SHELVES[whichAisle[1]] + ' shelf. Calculating the best route.'
        speechtext.playVoice(goalPrompt, speechtext.GIVE_DIRECTION)

        aisleNum = whichAisle[0]
        shelfNum = whichAisle[1]
        itemCoord = graph.getItemCoord(floorMap, aislePlan[(aisleNum, shelfNum+1)], aisleNum, int(items[correctItem])) # add one to shelf number since csv maps start from 1
        print('item is at: ',itemCoord)
        destCoord = graph.getDestinationCoord(floorGraph, itemCoord)
        print('destination is at: ',destCoord)
        # get store entry coordinate
        startCoord = graph.getEndCoord(floorMap,graph.BMP_ENTRY)
        print('start is at: ',startCoord)
        # while you are not at the correct location
        # localise (find current location) NOT DONE AS HARDWARE REQUIRED
        # calculate the best path to the item (path optimisation)
        # for simple model: align vertically i.e. change x first then move to correct y
        start = graph.getNode(startCoord, floorGraph)
        dest = graph.getNode(destCoord, floorGraph)
        # calculate boundaries
        minX = int(config['SHOPMAP']['minX'])
        maxX = int(config['SHOPMAP']['maxX'])
        minY = int(config['SHOPMAP']['minY'])
        maxY = int(config['SHOPMAP']['maxY'])
        boundaries = [minX, maxX, minY, maxY]
        path = graph.calculatePath(start, dest, floorGraph, boundaries)

        # now at the correct shelf. Give instruction to pick up item
        
        # check if picked up item is correct

        # once correct item is picked up, ask if person would like to go to checkout
            # if NO, repeat the process
        request = speechtext.speech2text(speechtext.ASK_CHECKOUT,0,0)
        if 'yes' in request or 'yea' in request or 'yep' in request:
            checkout = True

    # find best path to checkout
    print('Calculating path to checkout')
    checkoutCoord = graph.getEndCoord(floorMap,graph.BMP_CHECKOUT)
    print(checkoutCoord)