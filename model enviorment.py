import random

width = 25
height = 25
grid =[]

def celltype():
    n = random.randint(0,10)
    if n >= 6:
        return 0
    else:
        return 1

def rowgen():  
    maze_row =[]
    while len(maze_row) < height:
        maze_row.append(celltype())
    return maze_row 

def mazegen(maze):
    while len(maze) < width:
        maze.append(rowgen())
    maze[0][0] = 0
    maze[0][-1] = 0
    maze[50][0] = 0
    maze[50][-1] = 0
    maze[25][25] = 0

def mazeprinter(maze):
    for line in maze:
        print(line)

#def cell_loc((x)):




mazegen(grid)
mazeprinter(grid) 







