from random import randrange

def isEmpty(queue):

    if (len(queue) == 0):
        return True
    return False

# detect circle with breadth first search on choosen edges
def detectCircle(edges_arr):

    for i in range(len(edges_arr)):

        queue = []
        
        start = edges_arr[i][0]
        dest = edges_arr[i][1]
        queue.append([start, dest])

        while (False == isEmpty(queue)):
            point = queue.pop(0)
            pos_source = point[0]
            pos_dest = point[1]
 
            if (pos_dest == start):
                return True

            for j in range(len(edges_arr)):
                if(pos_dest == edges_arr[j][0]):
                    if (not ((edges_arr[j][1] == pos_source) & (edges_arr[j][0] == pos_dest))):
                        queue.append(edges_arr[j])

    return False

def feasibleSolution(pointArr, vertex_n):

    # if the subset does not contain any edge it is not feasible
    if (len(pointArr) == 0):
        return False

    if (len(pointArr) < (vertex_n - 1)):
        return False

    # Check duplicate in solution space
    for i in range(len(pointArr)):
        
        dup_source = pointArr[i][0]
        dup_dest = pointArr[i][1]

        for j in range(len(pointArr)):
            if ((pointArr[j][0] == dup_dest) & (pointArr[j][1] == dup_source)):
                return False

    # fill the visited table
    visited = [False] * vertex_n
    for i in range(len(pointArr)):
        posX = pointArr[i][0]
        posY = pointArr[i][1]
        visited[posX] = True
        visited[posY] = True

    # if did not visit all vertexes it is not feasible
    for i in range(len(visited)):
        if (False == visited[i]):
            return False

    # permutate and fill array with all point of visited edge
    # to detect circle
    permutatedPointArr = []
    for i in range(len(pointArr)):
        permutatedPointArr.append([pointArr[i][0], pointArr[i][1]])
        permutatedPointArr.append([pointArr[i][1], pointArr[i][0]])
    
    # detect circle
    return (not detectCircle(permutatedPointArr))

def getAllEdges(graph, INF):

    edgeArr = []

    if (len(graph) == 0):
        return edgeArr
    
    for i in range(len(graph)):
        for j in range(len(graph[len(graph) - 1])):
            if (graph[i][j] != INF):
                edgeArr.append([i, j, graph[i][j]])

    return edgeArr

# the random construct the array
def randomConstruct(vertex, arr:list):

    returnArr = []
    rand_size = vertex - 1

    while (rand_size > 0):
        idx = randrange(len(arr))
        returnArr.append(arr[idx])
        arr.pop(idx)
        rand_size -= 1

    return returnArr

def edgesCost(arr):

    cost = 0
    for i in range(len(arr)):
        cost += arr[i][2]

    return cost

def returnMinimizedNeighboor(solution, grph, edgesCache):

    returnArr = []
    cost = edgesCost(solution)

    for i in range(len(solution)):
        for j in range(len(edgesCache)):
            temp = solution[i]
            solution[i] = edgesCache[j]

            if (True == feasibleSolution(solution, len(grph))):
                tempCost = edgesCost(solution)

                if (tempCost < cost):
                    cost = tempCost
                    returnArr.clear()
                    for idx in range(len(solution)):
                        returnArr.append(solution[idx])

            solution[i] = temp

    return returnArr

def localSearch(graph, INF):

    allEdges = getAllEdges(graph, INF)
    solution = randomConstruct(len(graph), allEdges)

    while (False == feasibleSolution(solution, len(graph))):
        for i in range(len(solution)):
            allEdges.append(solution[i])
        solution = randomConstruct(len(graph), allEdges)
    
    return returnMinimizedNeighboor(solution, graph, allEdges)

INF = float("-inf")