import random

grid = []

def celltype():
    n = random.randint(0,10)
    if n >= 6:
        return 0
    else:
        return 1

def rowgen():  
    maze_row =[]
    while len(maze_row) < 51:
        maze_row.append(celltype())
    return maze_row 

def mazegen(maze):
    while len(maze) < 51:
        maze.append(rowgen())

mazegen(grid)
print(grid)