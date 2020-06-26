##############################################################################
#
#   CSE 231 Honors Option Part 1
#
#       Dots & Boxes
#
#       generateGrid
#           Generates new game board with specificed size
#
#       printGrid
#           Prints the game board to a file or console
#
#       makeMove
#           Takes user input for a requested move to draw a line
#           then passes to placeLine
#
#       makeMoveAI
#           Compiles list of avaiable moves and picks one at random
#           passes to placeLineAI
#
#       placeLineAI
#           Places a line in the array used to store the lines on the game board
#           passes to checkForBoxes
#
#       placeLine
#           Places a line the the array used to store the lines on the game board
#           passes to checkForBoxes
#
#       checkForBoxes
#           Checks to see if the line thar has just been places has formed
#           any boxes on the game board, if it has then it fills in the correct
#           letter on the board and passes to addScore
#
#       addScore
#           Adds one to the score of spceified player
#
#       checkGameOver
#           Checks game board to see if there are any moves left to be made
#
#       regularPlay
#           Plays a game between two humans
#
#       humanVsAI
#           Plays a game between a human and a Random Player
#
#       singlePlayAI
#           Plays one game between two Random Players and outputs everything to
#           a .txt file
#
#       multiplePlayAI
#           Plays spceified number of games with two Random Players and returns stats
#
#
##############################################################################



import math
import random

def generateGrid(size=4):
    
    grid = []
    row = []
    scoringTable = []
    lineTable = []

    gridCounter=0

    for i in range(0, size):
        for i in range(0, size):
            row.append(gridCounter)
            gridCounter+=1
        grid.append(row)
        row = []
    #Generates a 2D array containing the grid of numbers
        
        
    for i in range(0, size-1):
        for i in range(0, size-1):
            row.append(' ')
        scoringTable.append(row)
        row = []
    #Generates an empty 2D array for storing the letters for marking boxes when they're formed
        
        
    for i in range(0, size):
        for i in range(0, size-1):
            row.append(' ')
        lineTable.append(row)
        row = []
        for i in range(0, size):
            row.append(' ')
        lineTable.append(row)
        row = []
        
    del lineTable[len(lineTable)-1]
    #Generates an empty 2D array for storing all the lines for marking the board
    
    scores = [0, 0] #List for keeping track of scores
    
    turn = 'A' #Sets the starting turn to player A
        
    return grid, scoringTable, lineTable, scores, turn

def printGrid(tables, fp=None):
    
    scoringTableIndex = 0
    gridTableIndex = 0
    formatString = ''
    
    for i in range(0, len(tables[0][0])+len(tables[2][0])):
        formatString+='{:2s} '
    formatString.strip()
    #Makes the format string "{:2s}" repeated adaptavely for the size of the board
    #For printing the grid
    
    for row in range(0, len(tables[2])):
        printQ = [] #The Print Queue
        if row%2 == 0:
            #Go here if the row is even
            printQ.append(str(tables[0][gridTableIndex][0]))
            for i in range(0, len(tables[2][row])):#Tables 2 is the line table, Tables 0 is the numbers table
                printQ.append(str(tables[2][row][i]))
                printQ.append(str(tables[0][gridTableIndex][i+1]))
            gridTableIndex+=1 #Incrememnt a seprate counter for the numbers
            #Add the numbers, and horizontal lines to the print queue
        else:
            #Go here if the row is odd
            printQ.append(tables[2][row][0])
            for i in range(0, len(tables[2][row])-1):#Tables 1 is the letters table, Tables 2 is the numbers table
                printQ.append(str(tables[1][scoringTableIndex][i]))
                printQ.append(str(tables[2][row][i+1]))
            scoringTableIndex+=1#Increment a seperate counter for the letters
            #Add the letters and vertical lines to the print queue
        print(formatString.format(*printQ), file=fp)#Print the print queue with the format string
            
    
def makeMove(size, tableData):
    
    validMove = False
    
    while(not validMove):
    
        move = input("Player {} Make Your Move: ".format(tableData[4])).split(" ")
        
        if(move[0] == 'q'):
            crashyTimeBoi = int("Stop it... Get some help...")#This is just for if you want to quit a game it'll just crash the program
    
        try:
            move[0] = int(move[0])
            move[1] = int(move[1])
            validMove = True
            #Try to convert player's move into an int
            if(len(move) != 2):
                validMove = False
            #If there's more than 2 numbers then move in invalid
        except:
            validMove = False
            print("Move Not Valid")
            #If move isn't an int then move is invalid
            
    #Above code is for error checking the player's requested move
    
    move.sort()#Sort the moves so the smaller number is always first
    
    validMove = True
    
    x1 = move[0]%size
    y1 = move[0]//size
    
    x2 = move[1]%size
    y2 = move[1]//size
    
    #Above is for converting the numbers on the screen into a coordnate system
    #representing where the numbers are on the screen with (0, 0) being the number 0
    #this is done for both numbers entered by the player
    
    if(int(move[0]) < 0 or int(move[0]) > (size**2)-1):
        validMove = False
    elif(int(move[1]) < 0 or int(move[1]) > (size**2)-1):
        validMove = False
        
    #More move validation, checks to make sure move is actually a number on the screen
    
    dist = math.fabs(math.sqrt(((x2-x1)**2)+((y2-y1)**2)))
    
    if(dist > 1):
        validMove = False
        
    #Even more move validation
    #Checks to make sure moves are next to each other using the distance fourmlia
    #Can be done because moves where converted into coordnates
    
    validMove = placeLine(tableData, x1, y1, x2, y2, size)
    #Attempts to place the line, if there's a line there already then move is invalid
    
    if(not validMove):
        print("Move Not Valid")
        makeMove(size, tableData)
    #If move isn't valid then recurse back into makeMove and try again




def makeMoveAI(size, tableData, fp=None):
    
    print("AI Moving For Player {}: ".format(tableData[4]), file=fp)
    
    lineTable = tableData[2]
    
    moveOptions = []
    
    for y in range(len(lineTable)):
        for x in range(len(lineTable[y])):
            if(lineTable[y][x] == ' '):
                moveOptions.append([y, x])
    #Finds all the places in the array containing the lines that are empty
    #As there are all the possable moves the AI could make
    
    choice = random.randrange(0, len(moveOptions))
    
    choice = moveOptions[choice]
    #Picks one of the possable choices that where compiled
    
    placeLineAI(size, tableData, choice, fp)
    #Places line at that point
    
def placeLineAI(size, tableData, choice, fp=None):
    
    lineTable = tableData[2]
    
    if(choice[0]%2 == 0):
        lineTable[choice[0]][choice[1]] = '-'#Places a - if it's on an even line
        lineDirection = "right"
        print("Line Placed Between {} and {}".format((choice[0]//2)*(size)+choice[1], (choice[0]//2)*(size)+choice[1]+1), file=fp)
        #Converts the coordnate system used by the array storing the lines into the numbers that the line was placed between
    else:
        lineTable[choice[0]][choice[1]] = '|'#Places a | if it's on an odd line
        lineDirection = "down"
        print("Line Placed Between {} and {}".format(((choice[0]-1)//2)*size+choice[1], ((choice[0]+1)//2)*size+choice[1]), file=fp)
        #Converts the coordnate system used by the array storing the lines into the numbers that the line was placed between
    
    checkForBoxes(tableData, choice[0], choice[1], lineDirection, size, True, fp)
    #Checks to see if any boxes were made
    
    
def placeLine(tableData, x1, y1, x2, y2, size):
    
    lineTable = tableData[2]
    
    lineDirection = ""
    
    if(x1 == x2):
        lineDirection = "down"
    elif(y1 == y2 and x1 < x2):
        lineDirection = "right"
    #If the x coords of the two numbers the player picked are the same then the line goes right
    #If the y coords are the same then it goes down
    #This will always be true because we're always looking at the smaller number entered
        
    if(lineDirection == "down"):
        if(lineTable[(2*y1)+1][x1] == "|"):#The math here is to do the conversion from a general coordnate system to the one used by the line array
            return False
        #If there's already a line there return false
        else:
            lineTable[(2*y1)+1][x1] = "|"
            checkForBoxes(tableData, (2*y1)+1, x1, lineDirection, size)
            return True
        #If there isn't a line there return true and check for boxes
    elif(lineDirection == "right"):
        if(lineTable[2*y1][x1] == "-"):
            return False
        #If there's already a line there return false
        else:
            lineTable[2*y1][x1] = "-"
            checkForBoxes(tableData, 2*y1, x1, lineDirection, size)
            return True
        #If there isn't a line there return true and check for boxes

        
def checkForBoxes(tableData, y, x, lineDirection, size, AI=False, fp=None):
    
    lineTable = tableData[2]
    scoringTable = tableData[1]
    
    box1 = [False, 0, 0]
    box2 = [False, 0, 0]
    #It's possable to make 2 boxes in a turn
    
    box1OutOfBounds = True
    box2OutOfBounds = True
    
    if(lineDirection == "right"):
        if(y-2 >= 0 and y-1 >= 0):
            box2OutOfBounds = False
    elif(lineDirection == "down"):
        if(x-1 >= 0 and y-1 >= 0):
            box1OutOfBounds = False
        if(y-1 >= 0):
            box2OutOfBounds = False
    #Checks to see if checking for a box would make python check a negative array index
    #If it does then we know the box goes out of bounds of the board
    
    
    if(lineDirection == "right"):
        try:
            if(lineTable[y+2][x] != ' ' and lineTable[y+1][x] != ' ' and lineTable[y+1][x+1] != ' '):
                box1[0] = True#Records that there is a box formed here
                box1[1] = (y//2)#Coordnate conversion
                box1[2] = (x)#Coordnate conversion (Not nessicery for this one)
        except:
            box1[0] = False
        try:
            if(lineTable[y-2][x] != ' ' and lineTable[y-1][x] != ' ' and lineTable[y-1][x+1] != ' ' and box2OutOfBounds == False):
                box2[0] = True
                box2[1] = (int((y/2)-1))
                box2[2] = (int(x))
        except:
            box2[0] = False
    elif(lineDirection == "down"):
        try:
            if(lineTable[y][x-1] != ' ' and lineTable[y-1][x-1] != ' ' and lineTable[y+1][x-1] != ' ' and box1OutOfBounds == False):
                box1[0] = True
                box1[1] = (int((y-1)/2))
                box1[2] = (x-1)
        except:
            box1[0] = False
        try:
            if(lineTable[y][x+1] != ' ' and lineTable[y-1][x] != ' ' and lineTable[y+1][x] != ' ' and box2OutOfBounds == False):
                box2[0] = True
                box2[1] = (int((y-1)/2))
                box2[2] = (x)
        except:
            box2[0] = False
            
    #All of the above code checks the three spaces next to the line that's just been drawn that would need to be filled to make a box
    #It does this for both directions that a box could be made in for the new line (Above and below it or to the left or right of it)
    #And then it records the coordnates of the newly made box in the coordnate system used by the array that stores the scoring letters
            
    if(box1[0] == True and scoringTable[box1[1]][box1[2]] == ' '):
        if(tableData[4] == 'A'):
            scoringTable[box1[1]][box1[2]] = "A"
            addScore(1, tableData)
        else:
            scoringTable[box1[1]][box1[2]] = "B"
            addScore(2, tableData)
    if(box2[0] == True and scoringTable[box2[1]][box2[2]] == ' '):
        if(tableData[4] == 'A'):
            scoringTable[box2[1]][box2[2]] = "A"
            addScore(1, tableData)
        else:
            scoringTable[box2[1]][box2[2]] = "B"
            addScore(2, tableData)
            
    #The block above checks to see if a box was made, if it was it adds the approaprate letter to the scoring array
    #and adds one to the score for that player
    #Repeat to check for the second box
            
    if((box1[0] or box2[0]) and not checkGameOver(tableData)):
        printGrid(tableData, fp)
        print("Score is A:{} and B:{}".format(tableData[3][0], tableData[3][1]), file=fp)
        if(not AI):
            print(file=fp)
            makeMove(size, tableData)
        else:
            if(box1[0] and box2[0]):
                print("2 Boxes Made This Turn! Player {} Taking Another Turn".format(tableData[4]), file=fp)
            else:
                print("1 Box Made This Turn! Player {} Taking Another Turn".format(tableData[4]), file=fp)
            
            print(file=fp)
            makeMoveAI(size, tableData, fp)
        
    #If a box was made and the game hasn't ended then the above block will proceed to the next turn without changing players
    #Giving any player who has made a box an extra turn

def addScore(player, tableData):
    score = tableData[3]
    
    score[player-1]+=1
    #Adds one to the score of specified player


def checkGameOver(tableData):
    
    scoringTable = tableData[1]
    
    gameOver = True
    
    for i in scoringTable:
        for n in i:
            if n == ' ':
                gameOver = False
                
    #Scans every line of the scoring table (The letters)
    #If one is empty then the game isn't over
    
    return gameOver


def regularPlay(size, tableData):

    gameOver = False
    
    print("Player {} Goes First!".format(tableData[4]))
    
    printGrid(tableData)
    
    while(not gameOver):

        makeMove(size, tableData)
    
        printGrid(tableData)
    
        print("Score is A:{} and B:{}".format(tableData[3][0], tableData[3][1]))
        print()
    
        if(tableData[4] == 'A'):
            tableData[4] = 'B'
        else:
            tableData[4] = 'A'
            
        #Change who's turn it is
            
        gameOver = checkGameOver(tableData)
        
    #As long as the game isn't over this code loops and lets 2 humans play against each other


def humanVsAI(size, tableData):
    gameOver = False
    
    print("Player {} Goes First!".format(tableData[4]))
    
    printGrid(tableData)
    
    while(not gameOver):
        
        if(tableData[4] == 'A'):
            makeMove(size, tableData)
            printGrid(tableData)
            
            print("Score is A:{} and B:{}".format(tableData[3][0], tableData[3][1]))
            print()
        #Block of code for human player
        else:
            print("AI Moving For Player B")
            
            makeMoveAI(size, tableData)
            printGrid(tableData)
            
            print("Score is A:{} and B:{}".format(tableData[3][0], tableData[3][1]))
            print()
        #Block of code for AI player
    #If it's player A's turn then a human goes
    #If it's player B's turn then an AI goes
    
        if(tableData[4] == 'A'):
            tableData[4] = 'B'
        else:
            tableData[4] = 'A'
            
        #Change who's turn it is
            
        gameOver = checkGameOver(tableData)
    #Plays a game between an AI and a human
        
        
def singlePlayAI(size, tableData):
    
    fp = open("single_play.txt", 'w')
    
    print("Player {} Goes First!".format(tableData[4]), file=fp)
    
    gameOver = False
    
    printGrid(tableData, fp)
    
    while(not gameOver):

        makeMoveAI(size, tableData, fp)
    
        printGrid(tableData, fp)
    
        print("Score is A:{} and B:{}".format(tableData[3][0], tableData[3][1]), file=fp)
        print(file=fp)
        
    
        if(tableData[4] == 'A'):
            tableData[4] = 'B'
        else:
            tableData[4] = 'A'
            
        gameOver = checkGameOver(tableData)
        
    #Plays a game between 2 AI player
    #The same as regularPlay except uses makeMoveAI
        
        if(gameOver):
            print("Game Over!", file=fp)
            print("Final Score: A:{} B:{}".format(tableData[3][0], tableData[3][1]), file=fp)

            if(tableData[3][0] > tableData[3][1]):
                print("Player A Wins!", file=fp)
            elif(tableData[3][0] < tableData[3][1]):
                print("Player B Wins!", file=fp)
            else:
                print("Tie!", file=fp)
        #Prints the end of game text to a file when the game is over
            fp.close()
            #Close the file
        
        
def multiplePlayAI(size, tableData, games=None):
    
    if(not games):
        games = int(input("Input How Many Games To Play: "))
    #If no amount of games was passed then ask user
    
    gameOver = False
    
    timesWon = [0, 0]
    maxScore = [0, 0]
    minScore = [100, 100]
    scoresA = []
    scoresB= []
    scores = []
    gamesPlayed = 0
    #Set up for recording stats
    
    fp = open("multiple_play.txt", 'w')
    
    while(games > 0):

        makeMoveAI(size, tableData, fp)
    
        if(tableData[4] == 'A'):
            tableData[4] = 'B'
        else:
            tableData[4] = 'A'
        #Change who's turn it is
            
        gameOver = checkGameOver(tableData)
        
        if(gameOver):
            games-=1
            gameOver = False
            
            #When the game ends remove one from the games counter and reset the gameOver flag
            
            scoresA.append(tableData[3][0])
            scoresB.append(tableData[3][1])
            scores.append(tableData[3][0])
            scores.append(tableData[3][1])
            
            if(tableData[3][0] > tableData[3][1]):
                timesWon[0]+=1
            else:
                timesWon[1]+=1
                
                
            if(tableData[3][0] > maxScore[0]):
                maxScore[0] = tableData[3][0]
            if(tableData[3][1] > maxScore[1]):
                maxScore[1] = tableData[3][1]
                
            if(tableData[3][0] < minScore[0]):
                minScore[0] = tableData[3][0]
            if(tableData[3][1] < minScore[1]):
                minScore[1] = tableData[3][1]
                
            gamesPlayed+=1
            
            #Update Stats
            
            tableData = list(generateGrid(size))
            
            cointoss = random.randrange(1, 3, 1)
            
            if(cointoss == 1):
                tableData[4] = 'A'
            else:
                tableData[4] = 'B'
                
            #Set up the next game
            
    return timesWon, maxScore, scoresA, scoresB, scores, gamesPlayed, fp, minScore         
    #Return all stats
                     
    
print("Game modes:")
print("1. 2 Human players")
print("2. 1 Human vs random COM")
print("3. 2 Random AI (Single Play)")
print("4. 2 Random AI (Multiple Play)")
print("5. 2 Random AI (Single Play + Multiple Play)")
#Print the gamemode selection menu

gameMode = None

while(gameMode != 1 and gameMode != 2 and gameMode != 3 and gameMode!= 4 and gameMode != 5):

    try:
        gameMode = int(input("Select Game Mode (1-5): "))
    except:
        print("Enter a number 1-5")
        continue
        
    if(gameMode > 0 and gameMode < 6):
        continue
    else:
        print("Enter a number 1-5")
#Error checking for game mode selection
    
    
size = input("Grid Size (Default is 4): ")
#Ask for board size
try:
    size = int(size)
except:
    size = 4
#Error checking for board size
#If there's an error just set size to 4

tableData = list(generateGrid(size))
#Generate the board

try:
    seed = int(input("Enter a seed for the coin flip: "))
except:
    seed = None
#Ask for random number generator seed

if(seed):
    random.seed(seed)
else:
    random.seed()

cointoss = random.randrange(1, 3)
#Make the cointoss for who goes first

if(cointoss == 1):
    tableData[4] = 'A'
else:
    tableData[4] = 'B'
#Sets who plays first


if(gameMode == 1):
    regularPlay(size, tableData)
if(gameMode == 2):
    humanVsAI(size, tableData)
if(gameMode == 3):
    singlePlayAI(size, tableData)
if(gameMode == 4):
    data = multiplePlayAI(size, tableData)
if(gameMode == 5):
    games = int(input("Input How Many Games To Play: "))
    singlePlayAI(size, tableData)
    tableData = list(generateGrid(size))
    cointoss = random.randrange(1, 3)
    if(cointoss == 1):
        tableData[4] = 'A'
    else:
        tableData[4] = 'B'
    data = multiplePlayAI(size, tableData, games)
    #First runs single play, then resets board and runs multi play
#Runs each game mode based on selection made
    
    
if(gameMode == 4 or gameMode == 5):
    timesWon = data[0]
    maxScore = data[1]
    scoresA = data[2]
    scoresB = data[3]
    scores = data[4]
    gamesPlayed = data[5]
    fp = data[6]
    minScore = data[7]
    
    fp.close()
    
    fp = open("multiple_play.txt", 'w')
    
    total = 0
    
    for i in scores:
        total+=i
        
    total/=2
    total/=gamesPlayed
    overallAVG = total
    #Calculate the overall average score
    
    total=0
    for i in scoresA:
        total+=i
    
    total/=gamesPlayed
    avgA = total
    
    total=0
    for i in scoresB:
        total+=i
    
    total/=gamesPlayed
    avgB = total
    
    #Calculate average scores for players A and B
    
    scores.sort()
    medianScore = scores[len(scores)//2]
    
    scoresA.sort()
    medianScoreA = scoresA[len(scoresA)//2]
    
    scoresB.sort()
    medianScoreB = scoresB[len(scoresB)//2]
    #Calculate median scores
    #Sort the scores then pick out the one in the middle
    
    print("Number Of Rounds Played: {}".format(gamesPlayed), file=fp)
    print("Overall AVG Score: {}".format(overallAVG), file=fp)
    print("AVG Score For Player A: {}".format(avgA), file=fp)
    print("AVG Score For Player B: {}".format(avgB), file=fp)
    print("Times Player A Won: {}".format(timesWon[0]), file=fp)
    print("Times Player B Won: {}".format(timesWon[1]), file=fp)
    print("Overall Median Score: {}".format(medianScore), file=fp)
    print("Median Score For Player A: {}".format(medianScoreA), file=fp)
    print("Median Score For Player B: {}".format(medianScoreB), file=fp)
    print("Highest Score For Player A: {}".format(maxScore[0]), file=fp)
    print("Lowest Score For Player A: {}".format(minScore[0]), file=fp)
    print("Highest Score For Player B: {}".format(maxScore[1]), file=fp)
    print("Lowest Score For Player B: {}".format(minScore[1]), file=fp)
    #Print all the stats to file

    fp.close()
#If multi play was run then compile stats and print to a file
    
if(gameMode == 1 or gameMode == 2):

    print("Game Over!")
    print("Final Score: A:{} B:{}".format(tableData[3][0], tableData[3][1]))

    if(tableData[3][0] > tableData[3][1]):
        print("Player A Wins!")
    elif(tableData[3][0] < tableData[3][1]):
        print("Player B Wins!")
    else:
        print("Tie!")
        
#If the game mode has a human in it then print all the end of game data

    