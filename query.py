def stockQuery (request, itemList):
    correctItem = None
    print('Searching for',request)
    for key in itemList:
        if key in request:
            correctItem = key
    return correctItem