
import random

def GetNeighbours(node,dim):
    child_nodes = []
    row = int(node / dim)
    column = node % dim    
    if row > 0:
        child_nodes.append(((row - 1) * dim) + column)
    if column > 0:
        child_nodes.append((column - 1) + (row * dim))    
    if row < dim - 1:
        child_nodes.append(((row + 1) * dim) + column)
    if column < dim - 1:
        child_nodes.append((column + 1) + (row * dim))
    return child_nodes

def IsOnFire(maze,node,dim):
    row = int(node / dim)
    column = node % dim
    return (maze[row][column] == 2) 

def GetBurningNeighbours(maze,node,dim):
    nodes_fire = []
    child_nodes = GetNeighbours(node,dim)
    for child in child_nodes:
        if IsOnFire(maze,child,dim):
            nodes_fire.append(child)

    return nodes_fire

def SetNodesOnFire(maze,fire_prob,dim):
    Fire_spread = []
    for row in range(0,dim):
        for col in range(0,dim):
            if fire_prob[row][col] != 0 and fire_prob[row][col] != 1:
                p = fire_prob[row][col]
                val = random.randint(0,100)
                if val <= p * 100:
                    fire_prob[row][col] = 1
                    maze[row][col] = 20
                    Fire_spread.append(row*dim+col)

    return Fire_spread

def UpdateFireperStep(maze,fire_prob,dim):
    for row in range(0,dim):
        for col in range(0,dim):
            if maze[row][col] != 2:
                neighbour_fire = GetBurningNeighbours(maze,row*dim+col,dim)
                if neighbour_fire:
                    k = len(neighbour_fire)
                    p = 1 - (pow(0.5,k))
                    fire_prob[row][col] = p






#https://github.com/agangal93/Maze-Runner-using-AI