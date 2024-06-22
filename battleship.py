"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["no_of_rows"]=50
    data["no_of_cols"]=50
    data["board_size"]=50
    data["cell_size"]=50
    data["computer_Ships"]=5
    data["user_Ships"]=5
    data["computer_board"]=emptyGrid(data["no_of_rows"],data["no_of_cols"])
    data["user_board"]=emptyGrid(data["no_of_rows"],data["no_of_cols"])
    # data["user_board"]=test.testGrid()
    data["computer_board"]=addShips(data["computer_board"],data["computer_Ships"])
    # data["temp_board"]=test.testShip()
    data["temp_ship"]=[]
    data["userAddedship"]=0
    data["winner"]=None
    data["max_turns"]=50
    data["current_turns"]=0
    # data["user_board"]=addShips(data["user_board"],data["user_Ships"])
    return data


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data,userCanvas,data["user_board"],True) 
    drawGrid(data,compCanvas,data["computer_board"],False)
    drawShip(data,userCanvas,data["temp_ship"])
    drawGameOver(data, userCanvas)
    # if data["winner"]=="user": 
    #     drawGameOver(data,userCanvas) 
    # elif data["winner"]=="comp": 
    #     drawGameOver(data,compCanvas)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    # if event:
    #     makeModel(data)
    # return
    if event.keysym == "Return": 
        makeModel(data)
    return


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    cell=getClickedCell(data,event) 
    if board=="user": 
        clickUserBoard(data,cell[0],cell[1])
    elif board=="comp":
        runGameTurn(data,cell[0],cell[1])
    return

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid=[]
    for i in range(rows):
        x=[]
        for j in range(cols):
            x.append(EMPTY_UNCLICKED)
        grid.append(x)
    return grid

'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    row=random.randint(1,8)
    col=random.randint(1,8)
    corner=random.randint(0,1)
    ship=[]
    if corner==0:
        ship=[[row-1,col],[row,col],[row+1,col]]  #vertical
    else: 
        ship=[[row,col-1],[row,col],[row,col+1]]  #horizontal
    return ship


'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    count=0
    for i in ship:
        if grid[i[0]][i[1]]==EMPTY_UNCLICKED:
            count+=1
            if count==len(ship):
                return True
        else:
            return False


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count=0
    while count<numShips:
        ship=createShip()
        if checkShip(grid, ship)==True:
            for i in ship:
                grid[i[0]][i[1]]=SHIP_UNCLICKED
            count=count+1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    z=data["cell_size"]
    for row in range(data["no_of_rows"]):
        for col in range(data["no_of_cols"]):
            if grid[row][col]==SHIP_UNCLICKED: 
                canvas.create_rectangle(z*col,z*row,z*(col+1),z*(row+1),fill="yellow") 
            elif grid[row][col]==EMPTY_UNCLICKED:
                canvas.create_rectangle(z*col,z*row,z*(col+1),z*(row+1),fill="blue")
            elif grid[row][col]==SHIP_CLICKED:
                canvas.create_rectangle(z*col,z*row,z*(col+1),z*(row+1),fill="red")
            elif grid[row][col]==EMPTY_CLICKED:
                canvas.create_rectangle(z*col,z*row,z*(col+1),z*(row+1),fill="white")
            if grid[row][col]==SHIP_UNCLICKED and showShips==False:
                canvas.create_rectangle(z*col,z*row,z*(col+1),z*(row+1),fill="blue")
    return

### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    if ship[0][1]==ship[1][1]==ship[2][1]:
        ship.sort()
        if ship[0][0]+1==ship[1][0]==ship[2][0]-1:
            return True
    return False


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    if ship[0][0]==ship[1][0]==ship[2][0]:
        ship.sort()
        if ship[0][1]+1==ship[1][1]==ship[2][1]-1:
            return True
    return False


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    x_coordinate=int(event.x/data["cell_size"]) 
    y_coordinate=int(event.y/data["cell_size"]) 
    return [y_coordinate,x_coordinate]


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    a=data["cell_size"]
    for i in ship:
        x=i[1]*data["cell_size"]
        y=i[0]*data["cell_size"]
        canvas.create_rectangle(x, y, x+a, y+a ,fill="white")
    return


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship)==3: 
        if checkShip(grid,ship) and (isVertical(ship) or (isHorizontal(ship))): 
            return True 
    return False



'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["user_board"],data["temp_ship"]): 
        for ship in data["temp_ship"]: 
            data["user_board"][ship[0]][ship[1]]=SHIP_UNCLICKED 
        data["userAddedship"]=data["userAddedship"]+1 
    else: 
        print("Ship is not valid") 
    data["temp_ship"]=[]
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["userAddedship"]==5: 
        print("You can start the game") 
        return 
    if [row,col] not in data["temp_ship"]: 
        data["temp_ship"].append([row,col]) 
        if len(data["temp_ship"])==3: 
            placeShip(data)
        return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    m=data["computer_board"]
    n=data["user_board"]
    if board== m or n:
        if board[row][col]==SHIP_UNCLICKED:
            board[row][col]=SHIP_CLICKED
        elif board[row][col]==EMPTY_UNCLICKED:
            board[row][col]=EMPTY_CLICKED
    if isGameOver(board): 
        data["winner"]=player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    l=getComputerGuess(data["user_board"])
    m=data["computer_board"]
    if m[row][col]==SHIP_CLICKED or m[row][col]==EMPTY_CLICKED:
        return
    else:
        updateBoard(data,m,row,col,"user")
    updateBoard(data,data["user_board"],l[0],l[1],"comp")
    data["current_turns"]=data["current_turns"]+1
    if data["current_turns"]==data["max_turns"]:
        data["winner"]="draw"
    return


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    while True:
        row=random.randint(0,9)
        col=random.randint(0,9)
        if board[row][col]==SHIP_UNCLICKED or board[row][col]==EMPTY_UNCLICKED:
        #     pass
        # else:
        #     break
            return [row,col]


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in range(len(board)): 
        for col in range(len(board)): 
            if board[row][col]==SHIP_UNCLICKED: 
                return False 
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"]=="user": 
        canvas.create_text(250, 50, text="Congrats! You won!", fill="black", font=("Times_New_Roman 25 bold"))
        canvas.create_text(300, 100, text="Press ENTER to play again", fill="black", font=("Times_New_Roman 20 bold"))
    if data["winner"]=="comp": 
        canvas.create_text(250, 50, text="Try Again! You Lost!", fill="black", font=("Times_New_Roman 25 bold"))
        canvas.create_text(300, 100, text="Press ENTER to play again", fill="black", font=("Times_New_Roman 20 bold"))
    if data["winner"]=="draw":
        canvas.create_text(250, 50, text="It's a Draw! Out of Moves!", fill="black", font=("Times_New_Roman 25 bold"))
        canvas.create_text(300, 100, text="Press ENTER to play again", fill="black", font=("Times_New_Roman 20 bold"))
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    ## Finally, run the simulation to test it manually ##
    # test.week1Tests
    # test.week2Tests
    runSimulation(500, 500)
    # test.testGetComputerGuess()
    # test.testUpdateBoard()
    # test.testEmptyGrid()
    # test.testCreateShip()
    # test.testMakeModel()
    # test.testGrid()
    # test.testIsVertical()
    # test.testIsHorizontal()
    # test.testGetClickedCell()
    # test.testDrawShip()
