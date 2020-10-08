import pandas as pd
import csv
import numpy

BMP_WALL = -1
BMP_FLOOR = 0
BMP_ENTRY = -2
BMP_CHECKOUT = -3

RIGHT_TUPLE = (1,0)
LEFT_TUPLE = (-1,0)
DOWN_TUPLE = (0,1)
UP_TUPLE = (0,-1)

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
    for key in floorGraph:
        print('key: ', key,'adjacent nodes:')
        for i in floorGraph[key].adjacent:
            print('(', i.x,', ', i.y, ')')
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

# simple algorithm: align x then align y
def calculatePath(current, end, floorGraph, boundaries):
    print('(',current.x,', ',current.y,')')
    while current.x != end.x:
        if current.x < end.x:
            # move right
            next = nextNode(current, RIGHT_TUPLE, boundaries, floorGraph)
            if next:
                print('moving right')
                current = calculatePath(next, end, floorGraph, boundaries)
        elif current.x > end.x:
            # move left
            next = nextNode(current, LEFT_TUPLE, boundaries, floorGraph)
            if next:
                print('moving left')
                current = calculatePath(next, end, floorGraph, boundaries)
    
    while current.y != end.y:
        if current.y < end.y:
            # move down
            next = nextNode(current, DOWN_TUPLE, boundaries, floorGraph)
            if next:
                print('moving down')
                current = calculatePath(next, end, floorGraph, boundaries)
        elif current.y > end.y:
            # move up
            next = nextNode(current, UP_TUPLE, boundaries, floorGraph)
            if next:
                print('moving up')
                current = calculatePath(next, end, floorGraph, boundaries)
    return current
# fetches node at a given coordinate
def getNode(coord, floorGraph):
    for key in floorGraph:
        if coord == key:
            return floorGraph[key]

# fetch adjacent node in a given direction
def nextNode(current, direction, boundaries, floorGraph):
    xMin = boundaries[MIN_X_INDEX]
    xMax = boundaries[MAX_X_INDEX]
    yMin = boundaries[MIN_Y_INDEX]
    yMax = boundaries[MAX_Y_INDEX]
    next = (current.x+direction[0], current.y+direction[1])
    while (getNode(next, floorGraph) not in current.adjacent) and (next[0] <= xMax) and (next[0] >= xMin) and (next[1] >= yMin) and (next[1] <= yMax):
        next = tuple(map(sum, zip(next, direction)))
    
    if getNode(next, floorGraph) in current.adjacent:
        return getNode(next, floorGraph)
    else:
        return None # passed the boundary