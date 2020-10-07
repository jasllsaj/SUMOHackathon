import speechtext
import configparser
import pandas as pd
import numpy

BMP_WALL = -1
BMP_FLOOR = 0
BMP_ENTRY = -2

if __name__ == '__main__':
    
    # ask for an item
    #speechtext.speech2text(speechtext.ASK_ITEM, 0, 0)
    
    # read in floor and aisle plans stored as an occupancy matrix
    with open('./plans/floormap.csv') as csvfile:
        floorMap = pd.read_csv(csvfile, delimiter=',') 
    
    config = configparser.ConfigParser()
    config.read('config.cfg')
    numAisles = config['SHOPMAP']['numAisles']
    numLevels = config['SHOPMAP']['numLevels']

    items = dict(config['ITEMS'])
    for key in items:
        print(key)

