import sys
import time

MAX_INT = 2**31-1

def create_weights_matrix(matrix):
    # The original matrix contains 0 for an empty cell and 1 for a walled one.
    # We change them to positive numbers 1 and 1000 respectively.
    # This allows to calculate shortest paths based on the sum of the weights
    # preferring the 1 options always (since the mazes used by the google foo bar challenge are max 20 in size and the sum of empty cells
    # will never exceed 1000).

    EMPTY_CELL_WEIGHT = 1
    WALLED_CELL_WEIGHT = 1000

    number_rows = len(matrix)
    number_columns = len(matrix[0])

    weights_matrix = [[0 for j in range(number_columns)] for i in range(number_rows)]

    for i in range(0, number_rows):
        for j in range(0, number_columns):
            if matrix[i][j] == 0:
                weights_matrix[i][j] = EMPTY_CELL_WEIGHT
            else:
                weights_matrix[i][j] = WALLED_CELL_WEIGHT

    return weights_matrix


def find_adjacents_of_a_cell(x, y, number_columns, number_rows):
    # Simply returns an array of coordinates of cells
    # that are adjacent to a given one passed as parameter (x,y).
    # Also requires the size of the containg matrix to take bonduaries into consideration.

    
    if x >= number_rows or y >= number_columns:
        return []

    # transform into indexes
    number_columns = number_columns - 1
    number_rows = number_rows - 1

    if x == 0 and y == 0:
        return [(x, y + 1), (x + 1, y)]
    if x == 0 and 0 < y < number_columns:
        return [(x, y + 1), (x + 1, y), (x, y - 1)]
    if x == 0 and y == number_columns:
        return [(x + 1, y), (x, y - 1)]

    if 0 < x < number_rows and y == 0:
        return [(x - 1, y), (x, y + 1), (x + 1, y)]
    if 0 < x < number_rows and 0 < y < number_columns:
        return [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
    if 0 < x < number_rows and y == number_columns:
        return [(x - 1, y), (x + 1, y), (x, y - 1)]

    if x == number_rows and y == 0:
        return [(x - 1, y), (x, y + 1)]
    if x == number_rows and 0 < y < number_columns:
        return [(x - 1, y), (x, y + 1), (x, y - 1)]
    if x == number_rows and y == number_columns:
        return [(x - 1, y), (x, y - 1)]


def BFS(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    weights = create_weights_matrix(matrix)

    # keeps track of the cells that have been visited by the BFS procedure
    visited_matrix = [[0 for j in range(cols)] for i in range(rows)]

    # populate a new matrix with the paths from the top left corner to the bottom right one
    paths = [[MAX_INT for j in range(cols)] for i in range(rows)]

    # top left corner is always 1, this is also required for the procedure to start properly
    paths[0][0] = 1

    # queue of nodes to visit next
    queue = [(0, 0)]

    while len(queue) > 0:
        node = queue.pop(0)
        nodeX = node[0]
        nodeY = node[1]

        visited_matrix[nodeX][nodeY] = 1

        adjacents = find_adjacents_of_a_cell(nodeX, nodeY, cols, rows)
        for adj in adjacents:
            adjX = adj[0]
            adjY = adj[1]

            new_path_length = paths[nodeX][nodeY] + weights[adjX][adjY]

            if visited_matrix[adjX][adjY] != 1:
                # avoid padding a node to the queue if already present - use a set for performance reasons
                queueSet = set(queue)
                if adj not in queueSet:
                    queue.append(adj)
            if new_path_length < paths[adjX][adjY]:
                paths[adjX][adjY] = new_path_length
                queue.append(adj)

    return paths


def find_removable_walls(paths_matrix):
    # Produces a list of walls that, if removed, could produce a shorter path

    number_cols = len(paths_matrix[0])
    number_rows = len(paths_matrix)

    removableWalls = []

    for i in range(0, number_rows):
        for j in range(0, number_cols):
            # walls that can be removed in a useful way to produce a shorter paths
            # have 2 charateristics: path length between 1000 and 2000 and are adjacent to a cell which is 
            # part of an existing path (checked below when we do the paths_matrix[adjX][adjY] < 1000 comparison)

            if 1000 < paths_matrix[i][j] < 2000:  
                adjacents = find_adjacents_of_a_cell(i, j, number_cols, number_rows)
                counter = 0

                for adj in adjacents:
                    adjX = adj[0]
                    adjY = adj[1]

                    if paths_matrix[adjX][adjY] < 1000:
                        counter += 1
                        if counter > 0:
                            removableWalls.append((i, j))
                            break

    return removableWalls

def solution(maze):

    paths_matrix = BFS(maze)

    number_cols = len(paths_matrix[0])
    number_rows = len(paths_matrix)

    # the lenght of the path is stored in the bottom-right corner
    shortestPath = paths_matrix[number_rows - 1][number_cols - 1]

    # the shortest possible path won't be shorter than the longest dimension (number or rows or columns)
    # if we find something as short as that there's no need to search further
    bestAbsolutePath = number_rows
    if number_cols > number_rows:
        bestAbsolutePath = number_cols

    if shortestPath == bestAbsolutePath:
        return shortestPath

    # can we remove some walls to search for a shorter path?
    removableWalls = find_removable_walls(paths_matrix)

    for wall in removableWalls:
        wallX = wall[0]
        wallY = wall[1]

        maze[wallX][wallY] = 0 # remove that wall in the original maze

        paths_matrix = BFS(maze)

        new_shortest_path_length = paths_matrix[number_rows - 1][number_cols - 1]

        if new_shortest_path_length < shortestPath:
            shortestPath = new_shortest_path_length

        if shortestPath == bestAbsolutePath: # again, in this case we have finished, can't do better anyway
            return shortestPath

        maze[wallX][wallY] = 1 # restore the wall before moving to the next one

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