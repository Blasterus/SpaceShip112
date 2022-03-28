#################################################
#This is the main file for all of the graphics, as well as manipulating the board
#including inputting ships and playing the game
#the graphics include a lot of menus, buttons and grids
#################################################

from random import randint
from cmu_112_graphics import *
from datetime import datetime

import AI

#################################################
# Writing the txt files
#################################################


lines2 = ['Past Winners']
with open('GamesHistory.txt', 'w') as f:
    for line in lines2:
        f.write(line)
        f.write('\n')

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def makeBoard(x):
    #cols = rows = 8
    return [ ([0] * int(x)) for row in range(int(x)) ]

#################################################
# Variables
#################################################


def appStarted(app):
    app.gameState = 'Main Menu'
    app.AiMode = None
    app.textState = None

    #app.width
    #app.height

    #from https://wallpaperaccess.com/retro-space
    app.MainMenuBackground = app.loadImage("space.jpg")
    #from https://www.istockphoto.com/video/retro-8-bit-arcade-game-space-in-loop-gm962000126-262715347
    app.image = app.loadImage("space2.jpg")
    app.image2 = app.scaleImage(app.image, 2)

    app.margin = 150

    app.ShipListP1 = []
    app.ShipListP2 = []
    
    app.anchorsP1 = []
    app.anchorsP2 = []

    app.shipSizesP1 = []
    app.shipSizesP2 = []

    app.solutionBoardP1 = []
    app.solutionBoardP2 = []

    app.guessBoardP1 = []
    app.guessBoardP2 = []

    app.guessListP1 = []
    app.guessListP2 = []

    #this is for ships that have been hit
    #for example, hitListP1 represents the P1 ships that have been hit by P2
    app.hitListP1 = []
    app.hitListP2 = []

    app.currLenP1 = 0
    app.currLenP2 = 0


    app.textNickname1 = []
    app.textNickname2 = []
    app.textNumShip = []
    app.textGridSize = []

    app.selection = (-1,-1)


    app.shootAgain = False

    app.games = []



#############################
# V to M and M to V for grids
#############################


def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))


#from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
def getCellBounds(app, row, col):
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)

    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + gridWidth * col / num
    x1 = app.margin + gridWidth * (col+1) / num
    y0 = app.margin + gridHeight * row / num
    y1 = app.margin + gridHeight * (row+1) / num
    return (x0, y0, x1, y1)

def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)

    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / num
    cellHeight = gridHeight / num

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

    return (row, col)


def pointInGrid1(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin <= x <= app.width/2-app.margin) and
            (app.margin <= y <= app.height-app.margin))


#from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
def getCellBounds1(app, row, col):
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)

    gridWidth  = app.width/2 - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + gridWidth * col / num
    x1 = app.margin + gridWidth * (col+1) / num
    y0 = app.margin + gridHeight * row / num
    y1 = app.margin + gridHeight * (row+1) / num
    return (x0, y0, x1, y1)

def getCell1(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)

    if (not pointInGrid1(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width/2 - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / num
    cellHeight = gridHeight / num

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

    return (row, col)


def pointInGrid2(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return (((app.width/2)+app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))


#from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
def getCellBounds2(app, row, col):
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)

    gridWidth  = app.width/2 - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.width/2 + app.margin + gridWidth * col / num
    x1 = app.width/2 +app.margin + gridWidth * (col+1) / num
    y0 = app.margin + gridHeight * row / num
    y1 = app.margin + gridHeight * (row+1) / num
    return (x0, y0, x1, y1)

def getCell2(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)

    if (not pointInGrid2(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width/2 - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / num
    cellHeight = gridHeight / num

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin-app.width/2) / cellWidth)

    return (row, col)

#################################################
# Button clicks
#################################################

def clickPlay(ex, ey, app):
    x0, y0, x1, y1 = app.width/4, app.height/3, 3*app.width/4, app.height/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)


def clickOptions(ex, ey, app):
    x0, y0, x1, y1 = app.width/4, (app.height/2)+25, 3*app.width/4, (2*app.height/3)+25
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickQuit(ex, ey, app):
    x0, x1 = app.width/4, 3*app.width/4
    y0, y1 = app.height/2, 3*app.height/4
    x0, y0, x1, y1 = app.width/4, (2*app.height/3)+50, 3*app.width/4, app.height-66
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def click2Player(ex, ey, app):
    x0, y0, x1, y1 = app.width/4, app.height/3, 3*app.width/4, app.height/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)


def clickVSAI(ex, ey, app):
    x0, y0, x1, y1 = app.width/4, (app.height/2)+25, 3*app.width/4, (2*app.height/3)+25
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickNickname1(ex, ey, app):
    x0 = 0
    y0 = 0
    x1 = app.width/2
    y1 = app.height/2

    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickNickname2(ex, ey, app):
    x0 = app.width/2
    y0 = 0
    x1 = app.width
    y1 = app.height/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickNumShip(ex, ey, app):
    x0 = 0
    y0 = app.height/2
    x1 = app.width/2
    y1 = app.height
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickGridSize(ex, ey, app):
    x0 = app.width/2
    y0 = app.height/2
    x1 = app.width
    y1 = app.height
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickConfirm(ex, ey, app):
    x0, y0, x1, y1 = 3*app.width/8, 3*app.height/8, 5*app.width/8, 5*app.height/8
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickConfirmShips(ex, ey, app):
    x0, y0, x1, y1 = app.width/4, (2*app.height/3)+100, 3*app.width/4, app.height-16
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickBack(ex, ey, app):
    x0, y0, x1, y1 = 0, 0, 120, 70
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickEasy(ex, ey, app):
    x0, y0, x1, y1 = 20, app.height/3, app.width/2-20, app.height/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickMedium(ex, ey, app):
    x0, y0, x1, y1 = app.width/2, app.height/3, app.width-20, app.height/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickHard(ex, ey, app):
    x = app.height/2 - app.height/3
    x0, y0, x1, y1 = 20, app.height/2+20, app.width/2-20, app.height/2+20+x
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickImpossible(ex, ey, app):
    x = app.height/2 - app.height/3
    x0, y0, x1, y1 = app.width/2, app.height/2+20, app.width-20, app.height/2+20+x
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickNickname1AI(ex, ey, app):
    x0 = 0
    y0 = 0
    x1 = app.width
    y1 = app.height/2

    return (x0 <= ex <= x1) and (y0 <= ey <= y1)


#################################################
# Background code
#################################################

def convertShips(app, num):

    app.solutionBoardP1 = makeBoard(num)

    app.solutionBoardP2 = makeBoard(num)

    app.guessBoardP1 = makeBoard(num)
    app.guessBoardP2 = makeBoard(num)

    for ship in app.ShipListP1:
        x = ship[0]
        y = ship[1]
        app.solutionBoardP1[x][y] = 1

    for ship2 in app.ShipListP2:
        x = ship2[0]
        y = ship2[1]
        app.solutionBoardP2[x][y] = 1

def isHit(app, player):

    coord = app.guessListP1[-1]

    if player == 1:
        if coord in app.ShipListP2:
            app.hitListP2.append(coord)
            return True
        else:
            return False
    elif player == 2:
        if coord in app.ShipListP1:
            app.hitListP1.append(coord)
            return True
        else:
            return False

def didYouWin(app, player):

    if player == 1:
        for ship in app.ShipListP2:
            if ship not in app.guessListP1:
                return False

        return True
    elif player == 2:
        for ship in app.ShipListP1:
            if ship not in app.guessListP2:
                return False

        return True

def shipLegal(app, size, row, col, shipSize):
    around = [(row, col-(shipSize-1)), (row, col+(shipSize-1)), (row+(shipSize-1), col), (row-(shipSize-1), col)]

    for i in range(len(around)):
        if size-1 >= around[i][0] >= 0 and size-1 >= around[i][1] >=0:
            return True
    return False

def AIShipRandom(app, num, size):

    for i in range(num):
        while(True):
            row = randint(0, size)
            col = randint(0, size)

            shipSize = randint(2,5)

            if shipLegal(app, size, row, col, shipSize):
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




#################################################
# Rotating ships
#################################################

def rotateLegal(app, player):

    if len(app.ShipListP1) >= 2:
        lastShip1 = app.ShipListP1[-1]
        lastShip12 = app.ShipListP1[-2]

    if len(app.ShipListP2) >= 2:
        lastShip2 = app.ShipListP2[-1]
        lastShip22 = app.ShipListP2[-2]

    size = ''
    for digit in app.textGridSize:
        size += digit
    
    size = int(size)

    if player == 1:
        if size-1 >= lastShip1[0] >= 0 and size-1 >= lastShip1[1] >= 0 \
            and size-1 >= lastShip12[0] >= 0 and size-1 >= lastShip12[1] >= 0:

            return True

        else:
            return False
    
    if player == 2:
        if size-1 >= lastShip2[0] >= 0 and size-1 >= lastShip2[1] >= 0 \
            and size-1 >= lastShip22[0] >= 0 and size-1 >= lastShip22[1] >= 0:
            return True

        else:

            return False



        
def orientation(app, player):

    around = [(0, -1), (0, +1), (+1, 0), (-1, 0)]

    if player == 1:
        lastShips1 = []

        for i in range(1, app.shipSizesP1[-1]+1):
            lastShips1.append(app.ShipListP1[-i])

        lastShips1.reverse()
        lastShips1 = lastShips1[0:2]

        lastShip1 =lastShips1[-1]
        lastShip2 = lastShips1[-2]
    
    elif player ==2:
        lastShips1 = []

        for i in range(1, app.shipSizesP2[-1]+1):
            lastShips1.append(app.ShipListP2[-i])

        lastShips1.reverse()
        lastShips1 = lastShips1[0:2]

        lastShip1 =lastShips1[-1]
        lastShip2 = lastShips1[-2]

    
    drow = lastShip1[0] - lastShip2[0]
    dcol = lastShip1[1] - lastShip2[1]

    coord = (drow, dcol)

    if coord == around[0]:
        return "left"
    elif coord == around[1]:
        return "right"
    elif coord == around[2]:
        return "down"
    elif coord == around[3]:
        return "up"
    
def rotateShip(app, orientation, player):

    if player == 1: 

        lastShips1 = app.ShipListP1[-(app.shipSizesP1[-1]):]


    elif player == 2:
        
        lastShips1 = app.ShipListP2[-(app.shipSizesP2[-1]):]

    for k in range(len(lastShips1)):
        
        if k == len(lastShips1):
            continue

        else:
            row = lastShips1[k][0]
            col = lastShips1[k][1]

            if orientation == "left":
                row -= k
                col += k
                
            elif orientation == "right":
                row += k
                col -= k
            elif orientation == "down":
                row -= k
                col -= k
            elif orientation == "up":
                row += k
                col += k


            lastShips1[k] = (row,col)

    if player == 1:

        app.ShipListP1[-(app.shipSizesP1[-1]):] = lastShips1

    elif player == 2:
        
        app.ShipListP2[-(app.shipSizesP2[-1]):] = lastShips1
    

def unrotateShip(app, orientation, player):


    if player == 1: 

        lastShips1 = app.ShipListP1[-(app.shipSizesP1[-1]):]


    elif player == 2:
        
        lastShips1 = app.ShipListP2[-(app.shipSizesP2[-1]):]

    for k in range(len(lastShips1)):
        
        if k == len(lastShips1):
            continue

        else:
            row = lastShips1[k][0]
            col = lastShips1[k][1]

            if orientation == "left":
                row += k
                col += k
        
            elif orientation == "right":
                row -= k
                col -= k
            elif orientation == "down":
                row -= k
                col += k
            elif orientation == "up":
                row += k
                col -= k

            lastShips1[k] = (row,col)

    if player == 1:

        app.ShipListP1[-(app.shipSizesP1[-1]):] = lastShips1

    elif player == 2:
        
        app.ShipListP2[-(app.shipSizesP2[-1]):] = lastShips1



#################################################
# Mouse pressed event
#################################################

def mousePressed(app, event):

    ex, ey = event.x, event.y

    if app.gameState == 'Main Menu':
        if clickPlay(ex, ey, app):
            app.gameState = 'Choose Mode'
        if clickOptions(ex, ey, app):
            app.gameState = 'Options'
        if clickQuit(ex,ey,app):
            app.quit()
            print("Thanks for playing!")

    elif app.gameState == "Options":
        if clickBack(ex, ey, app):
            app.gameState = "Main Menu"

    elif app.gameState == 'Choose Mode':
        if click2Player(ex, ey, app):
            app.gameState = 'Input 2'
        if clickVSAI(ex, ey, app):
            app.gameState = 'Choose AI'
        if clickBack(ex, ey, app):
            app.gameState = "Main Menu"

    elif app.gameState == 'Input 2':
        if clickNickname1(ex, ey, app):
            app.textState = 'Nickname1'
        if clickNickname2(ex, ey, app):
            app.textState = 'Nickname2'
        if clickNumShip(ex, ey, app):
            app.textState = 'NumShip'
        if clickGridSize(ex, ey, app):
            app.textState = 'GridSize'
        if clickConfirm(ex, ey, app):

            if len(app.textNickname1) < 1 or len(app.textNickname2)<1 or len(app.textNumShip)<1 or  len(app.textGridSize) < 1:
                app.gameState = 'Input 2'
            else:
                app.gameState = 'Two Player Ship P1'
        
        if clickBack(ex, ey, app):
            app.gameState = "Choose Mode"

#################################################
# 2 Player Mode
#################################################
    
    elif app.gameState == 'Two Player Ship P1':
        (row, col) = getCell(app, ex, ey)
        
        num = ''
        for letter in app.textNumShip:
            num += letter

        num = int(num)

        size = ''
        for digit in app.textGridSize:
            size += digit
        size = int(size)

        if pointInGrid(app, ex, ey):
            if len(app.anchorsP1) < num:
                app.selection = (row, col)

                shipSize = randint(2,5)

                if shipLegal(app, size, row, col, shipSize):
                    around = [(row, col-(shipSize-1)), (row, col+(shipSize-1)), (row+(shipSize-1), col), (row-(shipSize-1), col)]

                    for i in range(len(around)):
                        if size-1 >= around[i][0] >= 0 and size-1 >= around[i][1] >=0:
                            
                            app.ShipListP1.append((row,col))
                            app.anchorsP1.append((row,col))

                            for j in range(shipSize):
                                if i == 0:
                                    app.ShipListP1.append((row,col-j))
                                elif i == 1:
                                    app.ShipListP1.append((row,col+j))
                                elif i == 2:
                                    app.ShipListP1.append((row+j,col))
                                elif i == 3:
                                    app.ShipListP1.append((row-j,col))
                            
                            app.shipSizesP1.append(shipSize)
                            break
                    

        if clickConfirmShips(ex,ey,app):
            if len(app.anchorsP1) >= num:
                app.gameState = 'Two Player Ship P2'
            else:
                app.gameState = 'Two Player Ship P1'

    elif app.gameState == 'Two Player Ship P2':
        (row, col) = getCell(app, ex, ey)
        
        num = ''
        for letter in app.textNumShip:
            num += letter

        num = int(num)

        size = ''
        for digit in app.textGridSize:
            size += digit
        size = int(size)

        if pointInGrid(app, ex, ey):
            if len(app.anchorsP2) < num:
                app.selection = (row, col)

                shipSize = randint(2,5)

                if shipLegal(app, size, row, col, shipSize):
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
                    

        if clickConfirmShips(ex,ey,app):
            if len(app.anchorsP2) >= num:
                app.gameState = 'Two Player Player 1'
            else:
                app.gameState = 'Two Player Ship P2'


    
    elif app.gameState == 'Two Player Player 1':
        (row, col) = getCell2(app, ex, ey)


        num = ''
        for letter in app.textNumShip:
            num += letter

        num = int(num)

        if pointInGrid2(app, ex, ey):
            if app.currLenP1 < 1:
                app.selection = (row, col)
                app.guessListP1.append((row,col))
                app.currLenP1 += 1

        if clickConfirmShips(ex,ey,app):

            if isHit(app, 1):
                if didYouWin(app, 1):
                    app.gameState = "Player 1 Win"
                else:
                    app.shootAgain = True
                    app.gameState = 'Two Player Player 1'
                    app.currLenP1 = 0
            else:
                app.shootAgain = False
                app.gameState = 'Two Player Player 2'
                app.currLenP2 = 0

    elif app.gameState == 'Two Player Player 2':
        (row, col) = getCell2(app, ex, ey)

        num = ''
        for letter in app.textNumShip:
            num += letter

        num = int(num)

        if pointInGrid2(app, ex, ey):
            if app.currLenP2 < 1:
                app.selection = (row, col)

                app.guessListP2.append((row,col))

                app.currLenP2 += 1

        if clickConfirmShips(ex,ey,app):
            if isHit(app, 2):
                if didYouWin(app, 2):
                    app.gameState = "Player 2 Win"
                else:
                    app.shootAgain = True
                    app.gameState = 'Two Player Player 2'
                    app.currLenP2 = 0
            else:
                app.shootAgain = False
                app.gameState = 'Two Player Player 1'
                app.currLenP1 = 0

#################################################
# VS AI
#################################################

    elif app.gameState == 'Choose AI':
        if clickEasy(ex, ey, app):
            app.gameState = 'Input AI'
            app.AiMode = 'Easy'

        if clickMedium(ex, ey, app):
            app.gameState = 'Input AI'
            app.AiMode = 'Medium'

        if clickHard(ex, ey, app):
            app.gameState = 'Input AI'
            app.AiMode = 'Hard'

        if clickImpossible(ex, ey, app):
            app.gameState = 'Input AI'
            app.AiMode = 'Impossible'
        
        if clickBack(ex, ey, app):
            app.gameState = "Main Menu"


    elif app.gameState == 'Input AI':
        if clickNickname1AI(ex, ey, app):
            app.textState = 'Nickname1'
        if clickNumShip(ex, ey, app):
            app.textState = 'NumShip'
        if clickGridSize(ex, ey, app):
            app.textState = 'GridSize'
        if clickConfirm(ex, ey, app):

            if len(app.textNickname1) < 0 or len(app.textNumShip)<0 or  len(app.textGridSize) < 0:
                app.gameState = 'Input AI'
            else:
                app.gameState = 'Input AI Ship'

        if clickBack(ex, ey, app):
            app.gameState = "Choose AI"

    elif app.gameState == "Input AI Ship":
        (row, col) = getCell(app, ex, ey)
        
        num = ''
        for letter in app.textNumShip:
            num += letter

        num = int(num)

        size = ''
        for digit in app.textGridSize:
            size += digit
        size = int(size)

        if pointInGrid(app, ex, ey):
            if len(app.anchorsP1) < num:
                app.selection = (row, col)

                shipSize = randint(2,5)

                if shipLegal(app, size, row, col, shipSize):
                    around = [(row, col-(shipSize-1)), (row, col+(shipSize-1)), (row+(shipSize-1), col), (row-(shipSize-1), col)]

                    for i in range(len(around)):
                        if size-1 >= around[i][0] >= 0 and size-1 >= around[i][1] >=0:
                            
                            app.ShipListP1.append((row,col))
                            app.anchorsP1.append((row,col))

                            for j in range(shipSize):
                                if i == 0:
                                    app.ShipListP1.append((row,col-j))
                                elif i == 1:
                                    app.ShipListP1.append((row,col+j))
                                elif i == 2:
                                    app.ShipListP1.append((row+j,col))
                                elif i == 3:
                                    app.ShipListP1.append((row-j,col))
                            
                            app.shipSizesP1.append(shipSize)
                            break
                    
        
        if clickConfirmShips(ex,ey,app):
            if len(app.anchorsP1) >= num:
                if app.AiMode == 'Easy' or app.AiMode == 'Medium' or app.AiMode == 'Hard':
                    AIShipRandom(app, num, size)
                elif app.AiMode == 'Impossible':
                    AI.placeShipsImpossible(app, num, size)
                #convertShips(app, size)
                app.gameState = 'VS AI P1'
            else:
                app.gameState = 'Input AI Ship'


    elif app.gameState == 'VS AI P1':
        (row, col) = getCell2(app, ex, ey)


        num = ''
        for letter in app.textNumShip:
            num += letter

        num = int(num)

        if pointInGrid2(app, ex, ey):
            if app.currLenP1 < 1:
                app.selection = (row, col)
                app.guessListP1.append((row,col))
                app.currLenP1 += 1

        if clickConfirmShips(ex,ey,app):
            if isHit(app, 1):
                if didYouWin(app, 1):
                    app.gameState = "Player 1 Win"
                else:
                    app.shootAgain = True
                    app.gameState = 'VS AI P1'
                    app.currLenP1 = 0
            else:
                app.shootAgain = False
                app.gameState = 'VS AI P2'
                app.currLenP2 = 0

    elif app.gameState == 'VS AI P2':

        num = ''
        for letter in app.textNumShip:
            num += letter

        num = int(num)

        if app.AiMode == "Easy":
            move = AI.nextMoveEasy(app)
        elif app.AiMode == "Medium":
            move = AI.nextMoveMedium(app)
        elif app.AiMode == "Hard":
            move = AI.nextMoveHard(app)
        elif app.AiMode == "Impossible":
            move = AI.nextMoveImpossible(app)
        

        if app.currLenP2 < 1:
            app.guessListP2.append(move)
            app.currLenP2 += 1

        if clickConfirmShips(ex,ey,app):
            if isHit(app, 2):
                if didYouWin(app, 2):
                    app.gameState = "Player AI Win"
                else:
                    app.shootAgain = True
                    app.gameState = 'VS AI P2'
                    app.currLenP2 = 0
            else:
                app.shootAgain = False
                app.gameState = 'VS AI P1'
                app.currLenP1 = 0

#################################################
# Winning
#################################################

    if app.gameState == 'Player 1 Win':

        nowtime = datetime.now()
        times = nowtime.strftime("%m/%d/%y %H:%M:%S")

        nickname1 = ''
        for letter in app.textNickname1:
            nickname1 += letter


        nummoves = len(app.guessListP1)

        more_lines = ['', times, f'{nickname1} wins in {nummoves} moves!']
        with open('GamesHistory.txt', 'a') as f:
            f.writelines('\n'.join(more_lines))

        if clickOptions(ex, ey, app):
            app.gameState = 'Main Menu'
            app.ShipListP1 = []

            app.textState = None

            app.ShipListP2 = []

            app.anchorsP1 = []
            app.anchorsP2 = []

            app.shipSizesP1 = []
            app.shipSizesP2 = []
            
            app.solutionBoardP1 = []
            app.solutionBoardP2 = []

            app.guessBoardP1 = []
            app.guessBoardP2 = []

            app.guessListP1 = []
            app.guessListP2 = []

            app.hitListP1 = []
            app.hitListP2 = []

            app.currLenP1 = 0
            app.currLenP2 = 0


            app.textNickname1 = []
            app.textNickname2 = []
            app.textNumShip = []
            app.textGridSize = []

            app.selection = (-1,-1)


            app.shootAgain = False


    elif app.gameState == 'Player 2 Win':

        nowtime = datetime.now()
        times = nowtime.strftime("%m/%d/%y %H:%M:%S")

        nickname2 = ''
        for letter in app.textNickname2:
            nickname2 += letter

        nummoves = len(app.guessListP2)

        more_lines = ['', times, f'{nickname2} wins in {nummoves} moves!']
        with open('GamesHistory.txt', 'a') as f:
            f.writelines('\n'.join(more_lines))

        if clickOptions(ex, ey, app):
            app.gameState = 'Main Menu'

            app.textState = None

            app.ShipListP2 = []

            app.anchorsP1 = []
            app.anchorsP2 = []

            app.shipSizesP1 = []
            app.shipSizesP2 = []
            
            app.solutionBoardP1 = []
            app.solutionBoardP2 = []

            app.guessBoardP1 = []
            app.guessBoardP2 = []

            app.guessListP1 = []
            app.guessListP2 = []

            app.hitListP1 = []
            app.hitListP2 = []

            app.currLenP1 = 0
            app.currLenP2 = 0


            app.textNickname1 = []
            app.textNickname2 = []
            app.textNumShip = []
            app.textGridSize = []

            app.selection = (-1,-1)


            app.shootAgain = False
            

    elif app.gameState == 'Player AI Win':

        thisGames = [app.textNumShip, app.textGridSize, app.ShipListP1, app.ShipListP2, app.guessListP1, app.guessListP2, app.hitListP1, app.hitListP2]

        app.games.append(thisGames)

        if clickOptions(ex, ey, app):
            app.gameState = 'Main Menu'

            app.textState = None

            app.ShipListP2 = []

            app.anchorsP1 = []
            app.anchorsP2 = []

            app.shipSizesP1 = []
            app.shipSizesP2 = []
            
            app.solutionBoardP1 = []
            app.solutionBoardP2 = []

            app.guessBoardP1 = []
            app.guessBoardP2 = []

            app.guessListP1 = []
            app.guessListP2 = []

            app.hitListP1 = []
            app.hitListP2 = []

            app.currLenP1 = 0
            app.currLenP2 = 0


            app.textNickname1 = []
            app.textNickname2 = []
            app.textNumShip = []
            app.textGridSize = []

            app.selection = (-1,-1)


            app.shootAgain = False
            
#################################################
# Key Pressed event
#################################################

def keyPressed(app, event):

    key = event.key

    if app.gameState == 'Input 2' or app.gameState == 'Input AI':

        if app.textState == 'Nickname1':
            #app.textNickname1 = []
            if key == "Backspace" and len(app.textNickname1) >0:
                app.textNickname1.pop(-1)
            elif key.isalnum():
                app.textNickname1.append(key.upper())
            
        elif app.textState == 'Nickname2':
            #app.textNickname2 = []
            if key == "Backspace" and len(app.textNickname2) >0:
                app.textNickname2.pop(-1)
            elif key.isalnum():
                app.textNickname2.append(key.upper())
            
        
        elif app.textState == 'NumShip':
            #app.textNumShip = []
            if key == "Backspace" and len(app.textNumShip) >0:
                app.textNumShip.pop(-1)
            elif key.isdigit() == True:
                integer = int(key)
                app.textNumShip.append(key)
            
        
        elif app.textState == 'GridSize':
            #app.textGridSize = []
            if key == "Backspace" and len(app.textGridSize) >0:
                app.textGridSize.pop(-1)
            elif key.isdigit() == True:
                integer = int(key)
                app.textGridSize.append(key)


    elif app.gameState == "Two Player Ship P1":
        lastShip1 = app.ShipListP1[-1]
        lastShip2 = app.ShipListP1[-2]

                #rotating ship
        if(event.key == 'Up'):

            o = orientation(app,1)

            rotateShip(app, o, 1)

            if rotateLegal(app, 1) == False:

                unrotateShip(app, o, 1)

            #print(app.ShipListP1)
            


        if(event.key == 'Down'):

            o = orientation(app,1)

            unrotateShip(app, o, 1)

            if rotateLegal(app, 1) == False:

                rotateShip(app, o, 1)

            #print(app.ShipListP1)

    
    elif app.gameState == "Two Player Ship P2":
        lastShip1 = app.ShipListP2[-1]
        lastShip2 = app.ShipListP2[-2]

        #rotating ship
        if(event.key == 'Up'):

            o = orientation(app,2)

            rotateShip(app, o, 2)

            if rotateLegal(app, 2) == False:

                unrotateShip(app, o, 2)

        if(event.key == 'Down'):

            o = orientation(app, 2)

            unrotateShip(app, o, 2)

            if rotateLegal(app, 2) == False:

                rotateShip(app, o, 2)

    
    elif app.gameState == "Input AI Ship":

        lastShip1 = app.ShipListP1[-1]
        lastShip2 = app.ShipListP1[-2]

    

        #rotating ship
        if(event.key == 'Up'):

            o = orientation(app, 1)

            rotateShip(app, o, 1)

            if rotateLegal(app, 1) == False:

                unrotateShip(app, o, 1)

        if(event.key == 'Down'):

            o = orientation(app, 1)

            unrotateShip(app, o, 1)

            if rotateLegal(app, 1) == False:

                rotateShip(app, o, 1)

                


#################################################
# Drawing Helpers
#################################################

def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

def drawTextBox(app, canvas, x0, y0, x1, y1):

    canvas.create_rectangle(x0, y0, x1, y1, fill='white')


#from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#exampleAddingAndDeletingShapes
def drawBoard(app, canvas):

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)

    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill='white')


def drawButton(app, canvas, x0, y0, x1, y1, buttonName):

    canvas.create_rectangle(x0, y0, x1, y1, fill = 'black', outline = 'white')
    canvas.create_text((x0+x1)//2, (y0+y1)//2, text = buttonName, font = ("Evil Empire", " 45 "), fill = 'white')

def drawNickname1(app, canvas):
    word = ''
    for letter in app.textNickname1:
        word += letter

    #app.Nickname1 = word

    x0 = 0
    y0 = 0
    x1 = app.width/2
    y1 = app.height/2

    if app.textState == "Nickname1":
        fill1 = 'black'
        fill2 = "white"
    else:
        fill1 = 'white'
        fill2 = "black"

    canvas.create_rectangle(x0, y0, x1, y1, fill = fill2,outline = fill1)

    canvas.create_text((x0+x1)//2, (y0+y1)//2-50, text = 'ENTER THE NICKNAME FOR PLAYER 1:', font = ("Evil Empire", " 20 "), fill = fill1)
    canvas.create_text((x0+x1)//2, (y0+y1)//2, text = word, font = ("Lucida Console", " 20 "), fill = fill1)

def drawNickname1AI(app, canvas):

    word = ''
    for letter in app.textNickname1:
        word += letter

    #app.Nickname1 = word

    x0 = 0
    y0 = 0
    x1 = app.width
    y1 = app.height/2

    if app.textState == "Nickname1":
        fill1 = 'black'
        fill2 = "white"
    else:
        fill1 = 'white'
        fill2 = "black"

    canvas.create_rectangle(x0, y0, x1, y1, fill = fill2,outline = fill1)

    canvas.create_text((x0+x1)//2, (y0+y1)//2-50, text = 'ENTER THE NICKNAME FOR PLAYER 1:', font = ("Evil Empire", " 20 "), fill = fill1)
    canvas.create_text((x0+x1)//2, (y0+y1)//2, text = word, font = ("Lucida Console", " 20 "), fill = fill1)

def drawNickname2(app, canvas):
    word = ''
    for letter in app.textNickname2:
        word += letter

    #app.Nickname2 = word

    x0 = app.width/2
    y0 = 0
    x1 = app.width
    y1 = app.height/2

    if app.textState == "Nickname2":
        fill1 = 'black'
        fill2 = "white"
    else:
        fill1 = 'white'
        fill2 = "black"

    canvas.create_rectangle(x0, y0, x1, y1, fill = fill2,outline = fill1)

    canvas.create_text((x0+x1)//2, (y0+y1)//2-50, text = 'ENTER THE NICKNAME FOR PLAYER 2:', font = ("Evil Empire", " 20 "), fill = fill1)
    canvas.create_text((x0+x1)//2, (y0+y1)//2, text = word, font = ("Lucida Console", " 20 "), fill = fill1)
    


def drawNumShip(app, canvas):

    word = ''
    for letter in app.textNumShip:
        word += letter

    #if word != '':
        #app.textNumShip = int(word)

    x0 = 0
    y0 = app.height/2
    x1 = app.width/2
    y1 = app.height

    if app.textState == "NumShip":
        fill1 = 'black'
        fill2 = "white"
    else:
        fill1 = 'white'
        fill2 = "black"

    canvas.create_rectangle(x0, y0, x1, y1, fill = fill2,outline = fill1)

    canvas.create_text((x0+x1)//2, (y0+y1)//2-50, text = 'ENTER THE NUMBER OF SHIPS YOU WISH TO PLAY WITH:', font = ("Evil Empire", " 20 "), fill = fill1)
    canvas.create_text((x0+x1)//2, (y0+y1)//2, text = word, font = ("Lucida Console", " 20 "), fill = fill1)
    

def drawGridSize(app, canvas):

    word = ''
    for letter in app.textGridSize:
        word += letter

    #if word != '':
        #app.textGridSize = int(word)


    x0 = app.width/2
    y0 = app.height/2
    x1 = app.width
    y1 = app.height
    

    if app.textState == "GridSize":
        fill1 = 'black'
        fill2 = "white"
    else:
        fill1 = 'white'
        fill2 = "black"

    canvas.create_rectangle(x0, y0, x1, y1, fill = fill2,outline = fill1)

    canvas.create_text((x0+x1)//2, (y0+y1)//2-50, text = 'ENTER THE SIZE OF THE BOARD YOU WISH TO PLAY WITH:', font = ("Evil Empire", " 20 "), fill = fill1)
    canvas.create_text((x0+x1)//2, (y0+y1)//2, text = word, font = ("Lucida Console", " 20 "), fill = fill1)
    

def drawConfirm(app, canvas):

    drawButton(app, canvas, 3*app.width/8, 3*app.height/8, 5*app.width/8, 5*app.height/8, 'Onwards!')

def drawConfirmShips(app, canvas):

    drawButton(app, canvas, 3*app.width/8, 3*app.height/8, 5*app.width/8, 5*app.height/8, 'Enter Battle!')

def drawBack(app, canvas):
    drawButton(app, canvas, 0, 0, 120, 70, 'Back')

#################################################
# Main drawings
#################################################

def drawMainMenu(app, canvas):

    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.MainMenuBackground))

    canvas.create_text(app.width/2, app.height/4-25, text = 'SPACESHIP!',
                            font = ("Evil Empire", " 100 "), fill = 'black')

    drawButton(app, canvas, app.width/4, app.height/3, 3*app.width/4, app.height/2, 'PLAY!')
    drawButton(app, canvas, app.width/4, (app.height/2)+25, 3*app.width/4, (2*app.height/3)+25, 'HOW TO PLAY')
    drawButton(app, canvas, app.width/4, (2*app.height/3)+50, 3*app.width/4, app.height-66, 'QUIT')
    #drawBack(app, canvas)
    


def drawModeMenu(app, canvas):

    canvas.create_text(app.width/2, app.height/4-25, text = 'CHOOSE YOUR MODE',
                            font = ("Evil Empire", " 100 "), fill = 'black')

    drawButton(app, canvas, app.width/4, app.height/3, 3*app.width/4, app.height/2, '2 Players')
    drawButton(app, canvas, app.width/4, (app.height/2)+25, 3*app.width/4, (2*app.height/3)+25, 'VS AI')

    drawBack(app, canvas)

def drawChooseAI(app, canvas):

    
    canvas.create_text(app.width/2, app.height/4-25, text = 'CHOOSE YOUR AI',
                            font = ("Evil Empire", " 100 "), fill = 'white')

    x = app.height/2 - app.height/3

    drawButton(app, canvas, 20, app.height/3, app.width/2-20, app.height/2, 'EASY')
    drawButton(app, canvas, app.width/2, app.height/3, app.width-20, app.height/2, 'MEDIUM')
    drawButton(app, canvas, 20, app.height/2+20, app.width/2-20, app.height/2+20+x, 'HARD')
    drawButton(app, canvas, app.width/2, app.height/2+20, app.width-20, app.height/2+20+x, 'IMPOSSIBLE')

    drawBack(app, canvas)

def drawInputMenu2(app, canvas):

    drawNickname1(app, canvas)
    drawNickname2(app, canvas)
    drawNumShip(app, canvas)
    drawGridSize(app, canvas)
    drawConfirm(app, canvas)
    drawBack(app, canvas)


def drawInputMenuAI(app, canvas):

    drawNickname1AI(app, canvas)
    drawNumShip(app, canvas)
    drawGridSize(app, canvas)
    drawConfirm(app, canvas)
    drawBack(app, canvas)


#################################################
# Ship Input drawings
#################################################

def drawTwoPlayerShipP1(app, canvas):


    nickname1 = ''
    for letter in app.textNickname1:
        nickname1 += letter

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)
    
    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            
            if (row,col) in app.ShipListP1:

                fill = "orange"  
                
            else:
                fill = "black"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline = "white")

    canvas.create_text(app.width/2, app.height/8, text=f"{nickname1}, please click on the cells to deploy your spaceships.",
                       font=("Lucida Console", " 20 "), fill="white")
    

    drawButton(app, canvas, app.width/4, (2*app.height/3)+100, 3*app.width/4, app.height-16, 'Continue')
    
    
    
def drawTwoPlayerShipP2(app, canvas):

    nickname2 = ''
    for letter in app.textNickname2:
        nickname2 += letter

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)
    
    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            
            if (row,col) in app.ShipListP2:

                fill = "orange"  
                
            else:
                fill = "black"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline = "white")

    
    canvas.create_text(app.width/2, app.height/8, text=f"{nickname2}, please click on the cells to deploy your spaceships.",
                    font=("Lucida Console", " 20 "), fill="white")

        
    
    drawButton(app, canvas, app.width/4, (2*app.height/3)+100, 3*app.width/4, app.height-16, 'Begin Battle!')


def drawVSAIShip(app, canvas):

    nickname1 = ''
    for letter in app.textNickname1:
        nickname1 += letter

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)
    
    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            
            if (row,col) in app.ShipListP1:

                fill = "orange"  
                
            else:
                fill = "black"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline = "white")

    canvas.create_text(app.width/2, app.height/8, text=f"{nickname1}, please click on the cells to deploy your spaceships.",
                       font=("Lucida Console", " 20 "), fill="white")
    

    drawButton(app, canvas, app.width/4, (2*app.height/3)+100, 3*app.width/4, app.height-16, 'Continue')


#################################################
# Drawing the game
#################################################

def drawTwoPlayerP1(app, canvas):

    nickname1 = ''
    for letter in app.textNickname1:
        nickname1 += letter

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)

    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds1(app, row, col)
            
            if (row,col) in app.guessListP2:

                fill = "orange"  

            elif (row,col) in app.hitListP1:

                fill = "red"
                
            else:
                fill = "black"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline = "white")


    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds2(app, row, col)
            
            if (row,col) in app.guessListP1:

                fill2 = "orange"  

            elif (row,col) in app.hitListP2:

                fill2 = "red"
                
            else:
                fill2 = "black"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill2, outline = "white")

    if app.shootAgain == False:
        canvas.create_text(app.width/2, app.height/8, text=f"{nickname1}, choose where to shoot your missile on the enemy galaxy.",
                        font=("Lucida Console", " 20 "), fill="white")
    else:
        canvas.create_text(app.width/2, app.height/8, text=f"{nickname1}, you may shoot again!",
                        font=("Lucida Console", " 20 "), fill="white")

    canvas.create_text(app.width/4, 2*app.height/8, text=f"Your galaxy",
                       font=("Lucida Console", " 20 "), fill="white")
    
    canvas.create_text(3*app.width/4, 2*app.height/8, text=f"Enemy galaxy",
                       font=("Lucida Console", " 20 "), fill="white")
    
    drawButton(app, canvas, app.width/4, (2*app.height/3)+100, 3*app.width/4, app.height-16, 'SHOOT!')

    



def drawTwoPlayerP2(app, canvas):

    nickname2 = ''
    for letter in app.textNickname2:
        nickname2 += letter

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)


    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds1(app, row, col)
            
            if (row,col) in app.guessListP1:

                fill = "orange"  

            elif (row,col) in app.hitListP2:

                fill = "red"
                
            else:
                fill = "black"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline = "white")


    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds2(app, row, col)
            
            if (row,col) in app.guessListP2:

                fill2 = "orange"  

            elif (row,col) in app.hitListP1:

                fill2 = "red"
                
            else:
                fill2 = "black"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill2, outline = "white")

    if app.shootAgain == False:
        canvas.create_text(app.width/2, app.height/8, text=f"{nickname2}, choose where to shoot your missile on the enemy galaxy.",
                        font=("Lucida Console", " 20 "), fill="white")
    else:
        canvas.create_text(app.width/2, app.height/8, text=f"{nickname2}, you may shoot again!",
                        font=("Lucida Console", " 20 "), fill="white")

    canvas.create_text(app.width/4, 2*app.height/8, text=f"Your galaxy",
                       font=("Lucida Console", " 20 "), fill="white")
    
    canvas.create_text(3*app.width/4, 2*app.height/8, text=f"Enemy galaxy",
                       font=("Lucida Console", " 20 "), fill="white")

    drawButton(app, canvas, app.width/4, (2*app.height/3)+100, 3*app.width/4, app.height-16, 'SHOOT!')





def drawVSAIP1(app, canvas):
    nickname1 = ''
    for letter in app.textNickname1:
        nickname1 += letter

    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)

    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds1(app, row, col)
            
            if (row,col) in app.guessListP2:

                fill = "orange"  

            elif (row,col) in app.hitListP1:

                fill = "red"
                
            else:
                fill = "black"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline = "white")


    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds2(app, row, col)
            
            if (row,col) in app.guessListP1:

                fill2 = "orange"  

            elif (row,col) in app.hitListP2:

                fill2 = "red"
                
            else:
                fill2 = "black"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill2, outline = "white")



    if app.shootAgain == False:
        canvas.create_text(app.width/2, app.height/8, text=f"{nickname1}, choose where to shoot your missile on the enemy galaxy.",
                        font=("Lucida Console", " 20 "), fill="white")
    else:
        canvas.create_text(app.width/2, app.height/8, text=f"{nickname1}, you may shoot again!",
                        font=("Lucida Console", " 20 "), fill="white")


    canvas.create_text(app.width/4, 2*app.height/8, text=f"Your galaxy",
                       font=("Lucida Console", " 20 "), fill="white")
    
    canvas.create_text(3*app.width/4, 2*app.height/8, text=f"Computer's galaxy",
                       font=("Lucida Console", " 20 "), fill="white")
    
    drawButton(app, canvas, app.width/4, (2*app.height/3)+100, 3*app.width/4, app.height-16, 'SHOOT!')
    

def drawVSAIP2(app, canvas):



    num = ''
    for letter in app.textGridSize:
        num += letter

    num = int(num)


    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds1(app, row, col)
            
            if (row,col) in app.guessListP2:

                fill = "orange"  

            elif (row,col) in app.hitListP1:

                fill = "red"
                
            else:
                fill = "black"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline = "white")


    for row in range(num):
        for col in range(num):
            (x0, y0, x1, y1) = getCellBounds2(app, row, col)
            
            if (row,col) in app.guessListP1:

                fill2 = "orange"  

            elif (row,col) in app.hitListP2:

                fill2 = "red"
                
            else:
                fill2 = "black"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill2, outline = "white")
    

    if app.shootAgain == False:
        canvas.create_text(app.width/2, app.height/8, text=f"The computer shoots!",
                    font=("Lucida Console", " 20 "), fill="white")
    else:
        canvas.create_text(app.width/2, app.height/8, text=f"The computer shoots again!",
                        font=("Lucida Console", " 20 "), fill="white")

    canvas.create_text(app.width/4, 2*app.height/8, text=f"Your galaxy",
                       font=("Lucida Console", " 20 "), fill="white")
    
    canvas.create_text(3*app.width/4, 2*app.height/8, text=f"Computer's galaxy",
                       font=("Lucida Console", " 20 "), fill="white")

    drawButton(app, canvas, app.width/4, (2*app.height/3)+100, 3*app.width/4, app.height-16, 'Continue')


#################################################
# Winning
#################################################

def drawWin(app, canvas):
    nickname1 = ''
    for letter in app.textNickname1:
        nickname1 += letter
    
    nickname2 = ''
    for letter in app.textNickname2:
        nickname2 += letter

    

    if app.gameState == "Player 1 Win":
        winner = nickname1


    elif app.gameState == "Player 2 Win":
        winner = nickname2

    
    elif app.gameState == "Player AI Win":
        winner = "THE COMPUTER"


    canvas.create_text(app.width/2, app.height/3, text = f'{winner} CLAIMS DOMINANCE OVER THE GALAXY!',
                            font = ("Evil Empire", " 50 "), fill = 'white')
    

    drawButton(app, canvas, app.width/4, (app.height/2)+25, 3*app.width/4, (2*app.height/3)+25, 'RETURN TO MAIN MENU')
    #drawButton(app, canvas, app.width/4, (2*app.height/3)+50, 3*app.width/4, app.height-66, 'QUIT')
    

#################################################
# How to Play
#################################################

def drawOptions(app, canvas):

    margin = 50

    x0 = margin
    x1 = app.width - margin
    y0 = margin
    y1 = app.height - margin

    
    canvas.create_rectangle(x0-10,y0-10,x1+10,y1+10, fill = 'white')
    canvas.create_rectangle(x0,y0,x1,y1, fill = 'black')

    canvas.create_text(app.width/2, app.height/8, text = "> Welcome to SpaceShip! In this game, 2 players compete for             ",
                            font = ("Lucida Console", " 20 "), fill = 'white')
    
    canvas.create_text(app.width/2, 2*app.height/8, text = "> intergalatical dominance as you both shoot dangerous ordinance        ",
                            font = ("Lucida Console", " 20 "), fill = 'white')

    canvas.create_text(app.width/2, 3*app.height/8, text = "> at each other until the better player shoots down the other fleet     ",
                            font = ("Lucida Console", " 20 "), fill = 'white')
    
    canvas.create_text(app.width/2, 4*app.height/8, text = "> You will each place down ships, marked on a grid. You may only shoot  ",
                            font = ("Lucida Console", " 20 "), fill = 'white')

    canvas.create_text(app.width/2, 5*app.height/8, text = "> once per turn, but if you hit a spaceship, then you may shoot again   ",
                            font = ("Lucida Console", " 20 "), fill = 'white')

    canvas.create_text(app.width/2, 6*app.height/8, text = "> A black square = empty, An orange square = attempt, A red square = hit",
                            font = ("Lucida Console", " 20 "), fill = 'white')
    
    canvas.create_text(app.width/2, 7*app.height/8, text = "> When inputting ships, press Up and Down to rotate them                ",
                            font = ("Lucida Console", " 20 "), fill = 'white')
    

    drawBack(app, canvas)


#################################################
# Game Start
#################################################

def redrawAll(app, canvas):

    if app.gameState == 'Main Menu':
        drawMainMenu(app, canvas)
    elif app.gameState == 'Choose Mode':
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
        drawModeMenu(app, canvas)
    elif app.gameState == 'Input 2':
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
        drawInputMenu2(app, canvas)

    
    elif app.gameState == 'Two Player Ship P1':
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
        drawTwoPlayerShipP1(app, canvas)
    elif app.gameState == 'Two Player Ship P2':
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
        drawTwoPlayerShipP2(app, canvas)

    
    elif app.gameState == 'Two Player Player 1':
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
        drawTwoPlayerP1(app, canvas)
    elif app.gameState == 'Two Player Player 2':
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
        drawTwoPlayerP2(app, canvas)


    elif app.gameState == "Choose AI":
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
        drawChooseAI(app, canvas)
    
    elif app.gameState == 'Input AI':
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
        drawInputMenuAI(app, canvas)
        

    elif app.gameState == 'Input AI Ship':
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
        drawVSAIShip(app, canvas)
    
    elif app.gameState == "VS AI P1":
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
        drawVSAIP1(app, canvas)
    
    elif app.gameState == "VS AI P2":
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
        drawVSAIP2(app, canvas)
    



    elif app.gameState == "Player 1 Win":
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.MainMenuBackground))
        drawWin(app, canvas)
    
    elif app.gameState == "Player 2 Win":

        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.MainMenuBackground))
        drawWin(app, canvas)

    elif app.gameState == "Player AI Win":

        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.MainMenuBackground))
        drawWin(app, canvas)
    
    elif app.gameState == "Options":
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.MainMenuBackground))
        drawOptions(app, canvas)



runApp(width=1280, height=650)