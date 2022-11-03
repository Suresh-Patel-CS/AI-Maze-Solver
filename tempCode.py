import random
import math
from pprint import pprint
from collections import deque
import csv
import numpy as np

dim = 51 #set the size of the maze
q = 0.1 #set the flammability

###########################################################################################################################

#the function that creates the random maze
def generateMaze(width, height):
    grid = []
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(random.randint(0, 1))
        grid.append(line)
 
    #set the corners to 0 (unblocked)
    grid[0][0] = 0
    grid[0][dim-1] = 0
    grid[dim-1][0] = 0
    grid[dim-1][dim-1] = 0
 
    #set the center to 0 (unblocked)
    mid = math.floor(dim / 2)
    grid[mid][mid] = 0
 
    #return the maze
    return grid

#this will check if the maze that was generated was valid and useable
def validMaze(grid): 
    #measure the dimnesion of the grid
   row = len(grid)
   column = len(grid[0])

   #visited array to keep track of the visited positions, initiallt filled with falses
   visited = [[False] * row for i in range(column)]

   #distance array, initially filled with 0s
   path = [[0] * row for i in range(column)]
   q = deque()
   q.append((0,0)) #append starting position
   visited[0][0] = True #set the visited position to true

   #while the queue is not empty
   while len(q):
       x,y = q.popleft() #get the x, y coordinates of the current position

       #for each of the directions in moves, get the x and y coordinates
       for dx,dy in moves:
           new_x = x + dx #calculates the new cell to move 
           new_y = y + dy #new position we want to go to

           #check if the new position is within the bounds of the grid and hasn't been visited
           if new_x >= 0 and new_x < row and new_y >= 0 and new_y < column and not visited[new_x][new_y]and grid[new_x][new_y]==0:
               q.append((new_x,new_y)) #append the new position
               visited[new_x][new_y] = True #set the visited to true
               path[new_x][new_y] = path[x][y] + 1 #increase the distance by 1

    #if we have not visited the goal not return false else return true
   if not visited[row - 1][column - 1]: 
       return False
   else:
        return True



###########################################################################################################################

#calculates the manhattan distance
def heuristic(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1-x2) + abs(y1-y2)
 
 
def a_star(grid, start, goal, moves):
 
    cost_goal = []#stores how much it cost to the goal node
    val = 1
    
    #keeps track of all the visited positions
    visited = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    visited[start[0]][start[1]] = 1
 
    #keeps track of the path the algorithm take
    path = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    path[start[0]][start[1]] = 0
 
    x = start[0] #start position
    y = start[1]
    g_score = 0
    f_score = g_score + heuristic(start, goal) 
 
    minList = [f_score, g_score, x, y]
 
    while minList[2:] != goal: #while we are not at goal
        for i in range(len(moves)): #for each move in moves
            x2 = x + moves[i][0] #calculate new position
            y2 = y + moves[i][1]   
            if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]): #check if its in the bounds
                if visited[x2][y2] == 0 and grid[x2][y2] == 0: #check if its visited or not and its the position is unblocked
                    g2_score = g_score + 1 #calculate the new g score
                    f2_score = g2_score + heuristic([x2, y2], goal) #calculate the new f score
                    cost_goal.append([f2_score, g2_score, x2, y2])
                    visited[x2][y2] = 1

        if not cost_goal:
            return False
 
        del minList[:]
        minList = min(cost_goal)
        cost_goal.remove(minList)
        x = minList[2]
        y = minList[3]
        g_score = minList[1]
        path[x][y] = val
        val += 1

    return True

###########################################################################################################################

firespread = []
checkforfire =[]

def startFire(maze,h,w):
    maze [int((h-1)/2)] [int((w-1)/2)] = 2
    firespread.append((int((h-1)/2),int((w-1)/2)))

#will set the center block on fire 6

def fireProb(maze,list):
    for (x,y) in list:
        k = neighborCell(maze,x,y)
        blaze = 1 - (1-q)**k
        fire = arson(blaze)
        if fire == True:
            maze[x][y] = 2
            firespread.append((x,y))
            checkforfire.pop()

#create the number used to see if the block will catch on fire 

def fireSpread(maze):
    firespread = [(ix,iy) for ix, row in enumerate(maze) for iy, i in enumerate(row) if i == 2]
#will run after every player move 
def neighborCell(maze,x,y):
        size = []
        try:
            if maze[x-1][y] == 2:
                size.append((x-1,y))
        except IndexError:
            pass
        try:
            if maze[x+1][y] == 2:
                size.append((x+1,y))
        except IndexError:
            pass
        try:
            if maze[x][y+1] == 2:
                size.append((x,y+1))
        except IndexError:
            pass
        try:  
            if maze[x][y-1] == 2:
                size.append((x,y-1))
        except IndexError:
            pass
        if len(size) == None:
            return 0
        else:
            return len(size)
            

def cellNeighbor(maze,list):
   for (x,y) in list:
        try: 
            if maze[x-1][y] == 0:
                checkforfire.append((x-1,y))
        except IndexError:
            pass  
        try:    
            if maze[x+1][y] == 0:
                checkforfire.append((x+1,y))
        except IndexError:
            pass  
        try:
            if maze[x][y+1] == 0:
                checkforfire.append((x,y+1))
        except IndexError:
            pass
        try:
            if maze[x][y-1] == 0:
                checkforfire.append((x,y-1))
        except IndexError:
            pass
            
#will return with a list of the cordinates of the 4 cells around thje center block
#then it will check the cordinates to see if there is an empty block if there is then it will add it to the list of on fire

def fireCheck():
    pass
# a queue of all the cells that will need to be ran against the prob to see if they will catch on fire

def updateFire():
    pass
# runs through every cell in matrix and checks against the fire spread list to see if its in there and if it is not it appends it to the list
# creates alot of time delay so we will see if i want to implement it or not

def arson(prob):
    x = random.random()
    if prob >= x:
        return True
    else:
        return False
# will actually set the blocks on fire

def mazeprinter(maze):
    for line in maze:
        print(line)
    print()
# prints the maze in a readable manner

def fireStep(maze):
    cellNeighbor(maze,firespread)
    fireProb(maze,checkforfire)
# step method to use every step

###########################################################################################################################

def agent1(grid): 
    #measure the dimnesion of the grid
   row = len(grid)
   column = len(grid[0])

   #visited array to keep track of the visited positions, initiallt filled with falses
   visited = [[False] * row for i in range(column)]

   #distance array, initially filled with 0s
   path = [[0] * row for i in range(column)]
   q = deque()
   q.append((0,0)) #append starting position
   visited[0][0] = True #set the visited position to true

   #while the queue is not empty
   while len(q):
       x,y = q.popleft() #get the x, y coordinates of the current position

       #for each of the directions in moves, get the x and y coordinates
       for dx,dy in moves:
           new_x = x + dx #calculates the new cell to move 
           new_y = y + dy #new position we want to go to

           #check if the new position is within the bounds of the grid and hasn't been visited
           if new_x >= 0 and new_x < row and new_y >= 0 and new_y < column and not visited[new_x][new_y]and grid[new_x][new_y] == 0 :
               q.append((new_x,new_y)) #append the new position
               fireStep(grid)
               visited[new_x][new_y] = True #set the visited to true
               path[new_x][new_y] = path[x][y] + 1 #increase the distance by 1

    #if we have not visited the goal not return false else return true
   if not visited[row - 1][column - 1]: 
       return False
   else:
        return True


def agent2(grid, start, goal, moves):
 
    cost_goal = []#stores how much it cost to the goal node
    val = 1
    
    #keeps track of all the visited positions
    visited = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    visited[start[0]][start[1]] = 1
 
    #keeps track of the path the algorithm take
    path = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    path[start[0]][start[1]] = 0
 
    x = start[0] #start position
    y = start[1]
    g_score = 0
    f_score = g_score + heuristic(start, goal) 
 
    minList = [f_score, g_score, x, y]
 
    while minList[2:] != goal: #while we are not at goal
        for i in range(len(moves)): #for each move in moves
            x2 = x + moves[i][0] #calculate new position
            y2 = y + moves[i][1]   
            if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]): #check if its in the bounds
                if visited[x2][y2] == 0 and grid[x2][y2] == 0: #check if its visited or not and its the position is unblocked
                    fireStep(grid)
                    g2_score = g_score + 1 #calculate the new g score
                    f2_score = g2_score + heuristic([x2, y2], goal) #calculate the new f score
                    cost_goal.append([f2_score, g2_score, x2, y2])
                    visited[x2][y2] = 1

        if not cost_goal:
            return False
 
        del minList[:]
        minList = min(cost_goal)
        cost_goal.remove(minList)
        x = minList[2]
        y = minList[3]
        g_score = minList[1]
        path[x][y] = val
        val += 1

    return True

def agent3(grid, start, goal, moves):
 
    cost_goal = []#stores how much it cost to the goal node
    val = 1
    
    #keeps track of all the visited positions
    visited = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    visited[start[0]][start[1]] = 1
 
    #keeps track of the path the algorithm take
    path = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    path[start[0]][start[1]] = 0
 
    x = start[0] #start position
    y = start[1]
    g_score = 0
    f_score = g_score + heuristic(start, goal) 
 
    minList = [f_score, g_score, x, y]
 
    while minList[2:] != goal: #while we are not at goal
        fireStep(grid)
        fireStep(grid)
        fireStep(grid)
        for i in range(len(moves)): #for each move in moves
            x2 = x + moves[i][0] #calculate new position
            y2 = y + moves[i][1]   
            if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]): #check if its in the bounds
                if visited[x2][y2] == 0 and grid[x2][y2] == 0: #check if its visited or not and its the position is unblocked
                    g2_score = g_score + 1 #calculate the new g score
                    f2_score = g2_score + heuristic([x2, y2], goal) #calculate the new f score
                    cost_goal.append([f2_score, g2_score, x2, y2])
                    visited[x2][y2] = 1
 
        if not cost_goal:
            return False
 
        del minList[:]
        minList = min(cost_goal)
        cost_goal.remove(minList)
        x = minList[2]
        y = minList[3]
        g_score = minList[1]
        path[x][y] = val
        val += 1

    return True

#Our agent 4 has the ability to remove certain number of obstacles
def agent4(maze, start, num):
    row, column = len(maze), len(maze[0])
    lives = [[-1 for i in range(column)] for j in range(row)] #lives matrix which is the same dimnesion as our grid
    q = deque()
    x = start[0] #start position
    y = start[1]
    q.append([x,y, num]) #append the starting position and the number of obstacles agent is allowed to remove

    #start of the BFS search
    while len(q) > 0:
        currentRow, currentColumn, currentLives = q.popleft() #remove the top element of the queue

        #check if we are at the goal node
        #if currentRow == row - 1 and currentColumn == column - 1:
        #   print("Agent 4 made it to the goal node")
        #   break

        #if we encounter a obstacle then remove it
        if maze[currentRow][currentColumn] == 1:
            currentLives -= 1

        #loop through each of the 4 directions
        for move in moves:
            newRow, newColumn = currentRow + move[0], currentColumn + move[1] #take a step to the new position
            if 0 <= newRow < row and 0 <= newColumn < column and lives[newRow][newColumn] < currentLives:
                #if the new postion is inbound then add it to the queue
                q.append([newRow, newColumn, currentLives])
                fireStep(grid)
                lives[newRow][newColumn] = currentLives  
    if currentRow == row - 1 and currentColumn == column - 1:
        return True
    else:              
        return False

###########################################################################################################################
mazevalid = False
grid = generateMaze(dim, dim)

def main(dim,grid):


    while mazevalid == False:
        mazevalid = validMaze(grid)

    datalist = []
    startFire(grid,dim,dim)

    start = [0, 0] # start position
    goal = [len(grid) - 1, len(grid[0]) - 1] #goal position
    
    #all the possible moves
    moves = [[-1, 0],[1, 0],[0, -1],[0, 1]]

    datalist.append(q)

    if agent1(grid) == False:
        print("Agent 1 could not find a path")
        datalist.append(False)
    else:
        print("Agent 1 made it to the goal node")
        datalist.append(True)

    if agent2(grid, start, goal, moves) == False:
        print("Agent 2 could not find a path")
        datalist.append(False)
    else:
        print("Agent 2 made it to the goal node")
        datalist.append(True)

    if agent3(grid, start, goal, moves) == False:
        print("Agent 3 could not find a path")
        datalist.append(False)
    else:
        print("Agent 3 made it to the goal node")
        datalist.append(True)


    datalist.append(agent4(grid, start, 1))
    return datalist


