import sys
import time

MAX_INT = 2**31-1

def CreateWeightsMatrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    weights = [[0 for j in range(cols)] for i in range(rows)]

    for i in range(0, rows):
        for j in range(0, cols):
            if matrix[i][j] == 0:
                weights[i][j] = 1
            else:
                weights[i][j] = 1000

    return weights


def FindCellAdjacents(x, y, w, h):

    if x >= h or y >= w:
        return []

    w = w - 1  # transform into indexes
    h = h - 1

    if x == 0 and y == 0:
        return [(x, y + 1), (x + 1, y)]
    if x == 0 and 0 < y < w:
        return [(x, y + 1), (x + 1, y), (x, y - 1)]
    if x == 0 and y == w:
        return [(x + 1, y), (x, y - 1)]

    if 0 < x < h and y == 0:
        return [(x - 1, y), (x, y + 1), (x + 1, y)]
    if 0 < x < h and 0 < y < w:
        return [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
    if 0 < x < h and y == w:
        return [(x - 1, y), (x + 1, y), (x, y - 1)]

    if x == h and y == 0:
        return [(x - 1, y), (x, y + 1)]
    if x == h and 0 < y < w:
        return [(x - 1, y), (x, y + 1), (x, y - 1)]
    if x == h and y == w:
        return [(x - 1, y), (x, y - 1)]


def BFS(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    weights = CreateWeightsMatrix(matrix)

    visited = [[0 for j in range(cols)] for i in range(rows)]
    paths = [[MAX_INT for j in range(cols)] for i in range(rows)]
    paths[0][0] = 1

    queue = [(0, 0)]

    while len(queue) > 0:
        node = queue.pop(0)
        nodeX = node[0]
        nodeY = node[1]

        visited[nodeX][nodeY] = 1

        adjacents = FindCellAdjacents(nodeX, nodeY, cols, rows)
        for adj in adjacents:
            adjX = adj[0]
            adjY = adj[1]

            newValue = paths[nodeX][nodeY] + weights[adjX][adjY]

            if visited[adjX][adjY] != 1:
                queueSet = set(queue)
                if adj not in queueSet:
                    queue.append(adj)
            if newValue < paths[adjX][adjY]:
                paths[adjX][adjY] = newValue
                queue.append(adj)

    return paths


def FindRemovableWalls(paths):
    w = len(paths[0])
    h = len(paths)

    removableWalls = []

    for i in range(0, h):
        for j in range(0, w):
            if 1000 < paths[i][j] < 2000:
                adjacents = FindCellAdjacents(i, j, w, h)
                counter = 0

                for adj in adjacents:
                    adjX = adj[0]
                    adjY = adj[1]

                    if paths[adjX][adjY] < 1000:
                        counter += 1
                        if counter > 0:
                            removableWalls.append((i, j))
                            break

    return removableWalls

def solution(maze):

    paths = BFS(maze)

    cols = len(paths[0])
    rows = len(paths)

    shortestPath = paths[rows - 1][cols - 1]
    bestAbsolutePath = rows
    if cols > rows:
        bestAbsolutePath = cols

    if shortestPath == bestAbsolutePath:
        return shortestPath

    removableWalls = FindRemovableWalls(paths)

    for wall in removableWalls:
        wallX = wall[0]
        wallY = wall[1]

        maze[wallX][wallY] = 0
        paths = BFS(maze)
        newPath = paths[rows - 1][cols - 1]
        if newPath < shortestPath:
            shortestPath = newPath

        maze[wallX][wallY] = 1
        if shortestPath == bestAbsolutePath:
            return shortestPath

    return shortestPath



# the  following part is not required for the Google challenge
def milliseconds():
    return int(round(time.time() * 1000))

def main():
    start_time = milliseconds()
    length = solution(maze4)

    end_time = milliseconds()

    print("Route length", length, "in", end_time - start_time, "milliseconds.")

main()



#Test mazes 
maze = [[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]] 
maze1 = [[0, 1, 1], [1, 0, 0], [1, 1, 0]]
maze2 = [[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]
maze3 = [[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]]
maze4 = [[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]