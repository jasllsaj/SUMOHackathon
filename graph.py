import pandas as pd
import csv
import numpy
import speechtext

# features and corresponding values on occupancy matrix
BMP_WALL = -1
BMP_FLOOR = 0
BMP_ENTRY = -2
BMP_CHECKOUT = -3

# directions in the store map
RIGHT_TUPLE = (1,0)
LEFT_TUPLE = (-1,0)
DOWN_TUPLE = (0,1)
UP_TUPLE = (0,-1)

DIRECTIONS = {
    RIGHT_TUPLE: 0,
    UP_TUPLE: 1,
    LEFT_TUPLE: 2,
    DOWN_TUPLE: 3
}

NUM_DIRECTIONS = 4
STRAIGHT = 0
TURN_LEFT = 1
TURN_RIGHT = 2
TURN_BACK = 3

# where values are stored in boundary list
MIN_X_INDEX = 0
MAX_X_INDEX = 1
MIN_Y_INDEX = 2
MAX_Y_INDEX = 3

class Node:
    def __init__(self,x,y,discovered):
        self.x=x
        self.y=y
        self.discovered=discovered
        self.adjacent=[]
    
    def __str__(self):
        return '({0}, {1})'.format(self.x,self.y)
    
    def appendAdjacent(self, adjNode):
        self.adjacent.append(adjNode)

def createGraph(matrix):
    # create graph object
    floorGraph = {}
    y = 0
    # find nodes and populate graph
    for index, row in matrix.iterrows():
        x = 0
        for col in row:
            if col == BMP_FLOOR or col == BMP_ENTRY or col == BMP_CHECKOUT:
                floorGraph.update({(x,y): Node(x=x,y=y,discovered=False)})
            x += 1
        y += 1
    
    for key in floorGraph:
        above = tuple(map(sum, zip(key, UP_TUPLE)))
        below = tuple(map(sum, zip(key, DOWN_TUPLE)))
        left = tuple(map(sum, zip(key, LEFT_TUPLE)))
        right = tuple(map(sum, zip(key, RIGHT_TUPLE)))
        
        if above in floorGraph:
            floorGraph[key].appendAdjacent(floorGraph[above])
        if below in floorGraph:
            floorGraph[key].appendAdjacent(floorGraph[below])
        if left in floorGraph:
            floorGraph[key].appendAdjacent(floorGraph[left])
        if right in floorGraph:
            floorGraph[key].appendAdjacent(floorGraph[right])
    #for key in floorGraph:
       # print('key: ', key,'adjacent nodes:')
        #for i in floorGraph[key].adjacent:
            #print('(', i.x,', ', i.y, ')')
    return floorGraph

def getItemCoord(floorMap, aisleMap, aisleBlock, itemID):
    # find where it is in the aisle: xy coord system with origin at top left
    # assumption: all aisle blocks are rectangular and there is only one of that item
    yAisle = 0
    itemAisleCoord = (0,0)
    for index, row in aisleMap.iterrows():
        xAisle = 0
        for col in row:
            if col == itemID:
                itemAisleCoord = (xAisle,yAisle) # coordinate within the aisle block
            xAisle += 1
        yAisle += 1
    # find where the top-left corner of the aisle is in the floor map
    yFloor = 0
    aisleCornerCoord = (0,0)
    foundCorner = False
    for index, row in floorMap.iterrows():
        xFloor = 0
        for col in row:
            if col == aisleBlock and not foundCorner:
                foundCorner = True
                aisleCornerCoord = (xFloor,yFloor)
            xFloor += 1
        yFloor += 1
    return tuple(map(sum, zip(itemAisleCoord, aisleCornerCoord)))

# find a node adjacent to where the item is stored
def getDestinationCoord(floorGraph, itemCoord):
    # assume vertically aligned aisle blocks so adjacent nodes on the left/right are favoured
    left = tuple(map(sum, zip(itemCoord, LEFT_TUPLE)))
    right = tuple(map(sum, zip(itemCoord, RIGHT_TUPLE)))
    above = tuple(map(sum, zip(itemCoord, UP_TUPLE)))
    below = tuple(map(sum, zip(itemCoord, DOWN_TUPLE)))

    if left in floorGraph:
        return left
    elif right in floorGraph:
        return right
    elif above in floorGraph:
        return above
    elif below in floorGraph:
        return below
    else:
        # item isn't accessible from anywhere: error state
        sys.exit("Item isn't accessible from anywhere!")

def getEndCoord(floorMap,mode):
    y = 0
    for index, row in floorMap.iterrows():
        x = 0
        for col in row:
            if col == mode:
                return (x,y)
            x += 1
        y += 1

# simple algorithm: go to nearest aisle end, then align x then align y
# isAisleEnd indicates whether the aisle end has been reached yet 
def calculatePath(current, end, floorGraph, boundaries, isAisleEnd, facing):
    print('(',current.x,', ',current.y,')')
    if not isAisleEnd:
        upper = boundaries[MIN_Y_INDEX]
        lower = boundaries[MAX_Y_INDEX]
        if current.y == upper or current.y == lower:
            #print('Reached aisle end')
            isAisleEnd = True
            return current, isAisleEnd, facing
        if current.y <= int((upper+lower)/2):
            # move to top corridor
            #print('Moving towards upper corridor')
            next, turn = nextNode(current, UP_TUPLE, boundaries, floorGraph, facing)
            if turn:
                speechtext.speech2text(speechtext.GIVE_DIRECTION, wayToTurn(UP_TUPLE, facing), False)
                facing = UP_TUPLE
        else:
            # move to bottom corridor
            #print('Moving towards lower corridor')
            if current.y > lower:
                next, turn = nextNode(current, UP_TUPLE, boundaries, floorGraph, facing)
                if turn:
                    speechtext.speech2text(speechtext.GIVE_DIRECTION, wayToTurn(UP_TUPLE, facing), False)
                    facing = UP_TUPLE
            else:
                next, turn = nextNode(current, DOWN_TUPLE, boundaries, floorGraph, facing)
                if turn:
                    speechtext.speech2text(speechtext.GIVE_DIRECTION, wayToTurn(DOWN_TUPLE, facing), False)
                    facing = DOWN_TUPLE
        current, isAisleEnd, facing = calculatePath(next, end, floorGraph, boundaries, isAisleEnd, facing)
    while current.x != end.x:
        if current.x < end.x:
            # move right
            next, turn = nextNode(current, RIGHT_TUPLE, boundaries, floorGraph, facing)
            if next:
                if turn:
                    speechtext.speech2text(speechtext.GIVE_DIRECTION, wayToTurn(RIGHT_TUPLE, facing), True)
                    facing = RIGHT_TUPLE
                current, isAisleEnd, facing = calculatePath(next, end, floorGraph, boundaries, isAisleEnd, facing)
        elif current.x > end.x:
            # move left
            next, turn = nextNode(current, LEFT_TUPLE, boundaries, floorGraph, facing)
            if next:
                if turn:
                    speechtext.speech2text(speechtext.GIVE_DIRECTION, wayToTurn(LEFT_TUPLE, facing), True)
                    facing = LEFT_TUPLE
                current, isAisleEnd, facing = calculatePath(next, end, floorGraph, boundaries, isAisleEnd, facing)
    
    while current.y != end.y:
        if current.y < end.y:
            # move down
            next, turn = nextNode(current, DOWN_TUPLE, boundaries, floorGraph, facing)
            if next:
                if turn:
                    speechtext.speech2text(speechtext.GIVE_DIRECTION, wayToTurn(DOWN_TUPLE, facing), None)
                    facing = DOWN_TUPLE
                current, isAisleEnd, facing = calculatePath(next, end, floorGraph, boundaries, isAisleEnd, facing)
        elif current.y > end.y:
            # move up
            next, turn = nextNode(current, UP_TUPLE, boundaries, floorGraph, facing)
            if next:
                if turn:
                    speechtext.speech2text(speechtext.GIVE_DIRECTION, wayToTurn(UP_TUPLE, facing), None)
                    facing = UP_TUPLE
                current, isAisleEnd, facing = calculatePath(next, end, floorGraph, boundaries, isAisleEnd, facing)
    return current, isAisleEnd, facing
# fetches node at a given coordinate
def getNode(coord, floorGraph):
    for key in floorGraph:
        if coord == key:
            return floorGraph[key]

# fetch adjacent node in a given direction
def nextNode(current, direction, boundaries, floorGraph, facing):
    xMin = boundaries[MIN_X_INDEX]
    xMax = boundaries[MAX_X_INDEX]
    yMin = boundaries[MIN_Y_INDEX]
    yMax = boundaries[MAX_Y_INDEX]
    next = (current.x+direction[0], current.y+direction[1])
    while (getNode(next, floorGraph) not in current.adjacent) and (next[0] <= xMax) and (next[0] >= xMin) and (next[1] >= yMin) and (next[1] <= yMax):
        next = tuple(map(sum, zip(next, direction)))
    if getNode(next, floorGraph) in current.adjacent:
        if facing != direction:
            return getNode(next, floorGraph), True
        else:
            return getNode(next, floorGraph), False
    else:
        return None # passed the boundary

# determine which direction to turn relative to the person
def wayToTurn(direction, facing):
    before = DIRECTIONS[facing]
    after = DIRECTIONS[direction]

    result = (after-before) % NUM_DIRECTIONS
    if result == 1:
        return TURN_LEFT
    elif result == 2:
        return TURN_BACK
    elif result == 3:
        return TURN_RIGHT
    else:
        return STRAIGHT