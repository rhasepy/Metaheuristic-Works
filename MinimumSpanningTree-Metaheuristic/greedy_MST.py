# find the vertex from disjoint set
def find_VertexSet(disjoint_set, idx):

    while (disjoint_set[idx] != idx):
        idx = disjoint_set[idx]
    return idx

# union source index and dest index in disjoint set
def union(disjoint_set, s_idx, d_idx):

    source = find_VertexSet(disjoint_set, s_idx)
    dest = find_VertexSet(disjoint_set, d_idx)
    disjoint_set[source] = dest

# greedy algorithm function
def greedy_MST_APPLY(graph, INF):

    disjoint_set = [i for i in range(len(graph))]
    solution = []
    cost = 0
 
    for i in range(len(graph)):
        disjoint_set[i] = i
 
    edge_count = 0
    while (edge_count < (len(graph) - 1)):
        
        min = INF
        source = -1
        dest = -1
        for i in range(len(graph)):
            for j in range(len(graph)):

                # Is there any circle and the choosen edge minimum
                if ((find_VertexSet(disjoint_set, i) != find_VertexSet(disjoint_set, j)) & (graph[i][j] < min)):
                    min = graph[i][j]
                    source = i
                    dest = j
        
        union(disjoint_set, source, dest)
        step = [source, dest, min]
        solution.append(step)
        edge_count += 1
        cost += min
 
    return solution

def MST_Solution_Print(sol_Px):
    
    total_cost = 0
    for i in range(len(sol_Px)):
        print("Edge: {}, Source: {}, Dest: {}, Cost: {}".format(i, sol_Px[i][0], sol_Px[i][1], sol_Px[i][2]))
        total_cost += sol_Px[i][2]

    print("Total Cost: {}".format(total_cost))

def greedy_MST(graph):
    INF = float('inf')
    return greedy_MST_APPLY(graph, INF)

def test_greedy_MST():

    INF = float('inf')
    graph = [[INF, 2, INF, 6, INF],
        [2, INF, 3, 8, 5],
        [INF, 3, INF, INF, 7],
        [6, 8, INF, INF, 9],
        [INF, 5, 7, 9, INF]]

    sol_Px = greedy_MST(graph)
    print("Graph: {}".format(graph))
    MST_Solution_Print(sol_Px)

    graph = [
        [INF, 2, INF, INF, INF, 14, 8],
        [2, INF, 19, INF, INF, 25, INF],
        [INF, 19, 9, 5, 17, INF, INF],
        [INF, INF, 9, INF, 1, INF, INF],
        [INF, INF, 5, 1, INF, 13, INF],
        [14, 25, 17, INF, 13, INF, 21],
        [8, INF, INF, INF, INF, 21, INF]]

    sol_Px = greedy_MST(graph)
    print("-------------------------\nGraph: {}".format(graph))
    MST_Solution_Print(sol_Px)