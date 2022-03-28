#################################################
#This is the file for the four types of AI
#################################################

from random import randint


def nextMoveEasy(app):

    num = ''
    for letter in app.textNumShip:
        num += letter

    num = int(num)

    size = ''
    for digit in app.textGridSize:
        size += digit
    
    size = int(size)

    while(True):
        x = randint(0, size)
        y = randint(0, size)

        if (x, y) not in app.guessListP2:
            return (x, y)
        else:
            continue



def nextMoveMedium(app):


    num = ''
    for letter in app.textNumShip:
        num += letter

    num = int(num)

    size = ''
    for digit in app.textGridSize:
        size += digit
    
    size = int(size)

    while(True):
        x = randint(0, size)
        y = randint(0, size)


        if app.shootAgain == True:
            lastCoord = app.guessListP2[-1]
            lastX = lastCoord[0]
            lastY = lastCoord[1]
            aroundLastCoord = [(lastX, lastY-1), (lastX+1, lastY-1), (lastX+1, lastY), (lastX+1, lastY+1), (lastX, lastY+1), (lastX-1, lastY+1), (lastX-1, lastY), (lastX-1, lastY-1)]
            for a in aroundLastCoord:
                if a[0] > size or a[1] > size or a[0] < size or a[1] < size:
                    aroundLastCoord.remove(a)
            
            x = aroundLastCoord[0][0]
            y = aroundLastCoord[0][1]

        if (x, y) not in app.guessListP2:
            return (x, y)
        else:
            continue

def shipLegalSim(app, size, row, col, shipSize, simList):

    around = [(row, col-(shipSize-1)), (row, col+(shipSize-1)), (row+(shipSize-1), col), (row-(shipSize-1), col)]

    temp = []

    for i in range(len(around)):
        if size-1 >= around[i][0] >= 0 and size-1 >= around[i][1] >=0:
            temp.append((row,col))

            for j in range(shipSize):
                if i == 0:
                    temp.append((row,col-j))
                elif i == 1:
                    temp.append((row,col+j))
                elif i == 2:
                    temp.append((row+j,col))
                elif i == 3:
                    temp.append((row-j,col))
            
            for element in temp:
                if element in app.guessListP2 or element in simList:
                    return False
            
            return True

    return False

    
#run a 1000 simulations
#place n number of ships, all random size
#see where they would be
#take the most appearing coordinate

def nextMoveHard(app):

    hits = app.hitListP1

    P1Ships = app.ShipListP1

    shipsLeft = []

    for ship in P1Ships:
        if ship not in hits:
            shipsLeft.append(ship)

    numOfCoord = len(shipsLeft)


    size = ''
    for digit in app.textGridSize:
        size += digit
    
    size = int(size)

    grid = size*size


    allResults = []

    #a thousand simulations!
    for a in range(1000):

        simList = []

        
        for i in range(numOfCoord):
            while(True):
                row = randint(0, size)
                col = randint(0, size)

                shipSize = randint(2,5)

                if shipLegalSim(app, size, row, col, shipSize, simList):
                    around = [(row, col-(shipSize-1)), (row, col+(shipSize-1)), (row+(shipSize-1), col), (row-(shipSize-1), col)]

                    for i in range(len(around)):
                        if size-1 >= around[i][0] >= 0 and size-1 >= around[i][1] >=0:
                            
                            simList.append((row,col))

                            for j in range(shipSize):
                                if i == 0:
                                    simList.append((row,col-j))
                                elif i == 1:
                                    simList.append((row,col+j))
                                elif i == 2:
                                    simList.append((row+j,col))
                                elif i == 3:
                                    simList.append((row-j,col))
                            
                            break

                    break



        allResults.extend(simList)

    counter = 0
    maxCoord = ()

    for coord in allResults:
        
        curr = allResults.count(coord)
        if(curr > counter):
            counter = curr

            maxCoord = coord


    return maxCoord


def mostfrequentguesses(app):

    #app.textNumShip, app.textGridSize, app.ShipListP1, app.ShipListP2, app.guessListP1, app.guessListP2, app.hitListP1, app.hitListP2

    numOfGames = len(app.games)

    P1guesses = []
    frequent = []

    for game in app.games:
        if type(game) == str:
            continue
        else:
            P1guesses.extend(game[4])


    nodups = list(set(P1guesses))

    for guess in nodups:
        x = P1guesses.count(guess)
        #if you guessed this coord in over half of the games
        if x > (numOfGames/2):
            frequent.append(guess)


    return frequent

def shipLegal(app, size, row, col, shipSize):
    around = [(row, col-(shipSize-1)), (row, col+(shipSize-1)), (row+(shipSize-1), col), (row-(shipSize-1), col)]

    for i in range(len(around)):
        if size-1 >= around[i][0] >= 0 and size-1 >= around[i][1] >=0:
            return True
    return False

#places the ships so its not where you would usually guess
def placeShipsImpossible(app, num, size):

    frequent = mostfrequentguesses(app)

    for i in range(num):
        while(True):
            row = randint(0, size)
            col = randint(0, size)

            shipSize = randint(2,5)

            if shipLegal(app, size, row, col, shipSize) and (row,col) not in frequent:
                around = [(row, col-(shipSize-1)), (row, col+(shipSize-1)), (row+(shipSize-1), col), (row-(shipSize-1), col)]

                for i in range(len(around)):
                    if size-1 >= around[i][0] >= 0 and size-1 >= around[i][1] >=0:
                        
                        app.ShipListP2.append((row,col))
                        app.anchorsP2.append((row,col))

                        for j in range(shipSize):
                            if i == 0:
                                app.ShipListP2.append((row,col-j))
                            elif i == 1:
                                app.ShipListP2.append((row,col+j))
                            elif i == 2:
                                app.ShipListP2.append((row+j,col))
                            elif i == 3:
                                app.ShipListP2.append((row-j,col))
                        
                        app.shipSizesP2.append(shipSize)
                        break
                break


#would take your previous ship placements
#then checks which zone was the most frequent
#shoot in that zone
#if the zone is all filled up, then shoot in the next frequent

def mostFrequentQuad(app):


    #extracts data from the AIData.txt

    #app.textNumShip, app.textGridSize, app.ShipListP1, app.ShipListP2, app.guessListP1, app.guessListP2, app.hitListP1, app.hitListP2
    
    
    topLeftList = []
    topRightList = []
    botLeftList = []
    botRightList = []

    num = ''
    for letter in app.textNumShip:
        num += letter

    num = int(num)

    size = ''
    for digit in app.textGridSize:
        size += digit
    size = int(size)

    
    mostfrequentquad = []

    for game in app.games:
        textNum = game[0]
        textGrid = game[1]

        currNum = ''
        for letter in textNum:
            currNum += letter
        currNum = int(currNum)

        currSize = ''
        for digit in textGrid:
            currSize += digit
        currSize = int(currSize)



        if currSize%2 == 0:
            midX = midY = (currSize//2) -1

            topLeft = [(0,0), (midX, midY)]
            topRight = [(0,midY+1), (midX, currSize-1)]
            botLeft = [(midX+1,0), (currSize-1, midY)]
            botRight = [(midX+1,midX+1), (currSize-1, currSize-1)]

        elif currSize%2 == 1:
            midX = midY = currSize//2

            topLeft = [(0,0), (midX, midY)]
            topRight = [(0,midY), (midX, currSize-1)]
            botLeft = [(midX,0), (currSize-1, midY)]
            botRight = [(midX,midY), (currSize-1, currSize-1)]


        for coord in game[2]:
            x = coord[0]
            y = coord[1]

            if topLeft[0][0] <= x <= topLeft[1][0] and topLeft[0][1] <= y <= topLeft[1][1]:
                topLeftList.append(coord)

            elif topRight[0][0] <= x <= topRight[1][0] and topRight[0][1] <= y <= topRight[1][1]:
                topRightList.append(coord)

            elif botLeft[0][0] <= x <= botLeft[1][0] and botLeft[0][1] <= y <= botLeft[1][1]:
                botLeftList.append(coord)

            elif botRight[0][0] <= x <= botRight[1][0] and botRight[0][1] <= y <= botRight[1][1]:
                botRightList.append(coord)

        listOfCoords = {'topLeft': len(topLeftList), 'topRight': len(topRightList), 'botLeft': len(botLeftList), 'topRight': len(botRightList)}

        mostfrequentquad.append(max(listOfCoords))




    return mostfrequentquad


def filled(app, size):

    sizeOfQuadrant = ((size//2)+1)**2

    if size%2 == 0:
        midX = midY = (size//2) -1

        topLeft = [(0,0), (midX, midY)]
        topRight = [(0,midY+1), (midX, size-1)]
        botLeft = [(midX+1,0), (size-1, midY)]
        botRight = [(midX+1,midX+1), (size-1, size-1)]

    elif size%2 == 1:
        midX = midY = size//2

        topLeft = [(0,0), (midX, midY)]
        topRight = [(0,midY), (midX, size-1)]
        botLeft = [(midX,0), (size-1, midY)]
        botRight = [(midX,midY), (size-1, size-1)]

    
    TLcount = 0
    TRcount = 0
    BLcount = 0
    BRcount = 0

    for guess in app.guessListP2:

        x = guess[0]
        y = guess[1]

        if topLeft[0][0] <= x <= topLeft[1][0] and topLeft[0][1] <= y <= topLeft[1][1]:
            TLcount +=1

        elif topRight[0][0] <= x <= topRight[1][0] and topRight[0][1] <= y <= topRight[1][1]:
            TRcount +=1

        elif botLeft[0][0] <= x <= botLeft[1][0] and botLeft[0][1] <= y <= botLeft[1][1]:
            BLcount +=1

        elif botRight[0][0] <= x <= botRight[1][0] and botRight[0][1] <= y <= botRight[1][1]:
            BRcount +=1

    if TLcount == sizeOfQuadrant or TRcount == sizeOfQuadrant or BLcount == sizeOfQuadrant or BRcount == sizeOfQuadrant:
        return True
    else:
        return False

def nextMoveImpossible(app):


    most = mostFrequentQuad(app)

    counter = {}
    for coord in most:
        if coord in counter:
            counter[coord] += 1
        else:
            counter[coord] = 1

    highest = sorted(counter, key = counter.get, reverse = True)
    

    num = ''
    for letter in app.textNumShip:
        num += letter

    num = int(num)

    size = ''
    for digit in app.textGridSize:
        size += digit
    
    size = int(size)

    if size%2 == 0:
        midX = midY = (size//2) -1

        topLeft = [(0,0), (midX, midY)]
        topRight = [(0,midY+1), (midX, size-1)]
        botLeft = [(midX+1,0), (size-1, midY)]
        botRight = [(midX+1,midX+1), (size-1, size-1)]

    elif size%2 == 1:
        midX = midY = size//2

        topLeft = [(0,0), (midX, midY)]
        topRight = [(0,midY), (midX, size-1)]
        botLeft = [(midX,0), (size-1, midY)]
        botRight = [(midX,midY), (size-1, size-1)]

    while(True):
        x = randint(0, size)
        y = randint(0, size)

        quadrant = None

        if topLeft[0][0] <= x <= topLeft[1][0] and topLeft[0][1] <= y <= topLeft[1][1]:
            quadrant = "topLeft"

        elif topRight[0][0] <= x <= topRight[1][0] and topRight[0][1] <= y <= topRight[1][1]:
            quadrant = "topRight"

        elif botLeft[0][0] <= x <= botLeft[1][0] and botLeft[0][1] <= y <= botLeft[1][1]:
            quadrant = "botLeft"

        elif botRight[0][0] <= x <= botRight[1][0] and botRight[0][1] <= y <= botRight[1][1]:
            quadrant = "botRight"

        if filled(app, size) == True:
            highest.pop(0)
            continue
        
        elif quadrant == highest[0] and (x, y) not in app.guessListP2:
            return (x, y)
        else:
            continue