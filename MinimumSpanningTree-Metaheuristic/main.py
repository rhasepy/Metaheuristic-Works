from PSO_MST import PSO_Mst
from PSO_Sort import PSOSort
from ACO_SORT import ACO_Sort, arrayCost
from backtrack_sorting import backtracking_sort
from brute_force_sorting import bruteforce
from bruteforce_MST import bruteforce_MST
from GeneticAlgorithmSorting import geneticSort
from greedy_MST import greedy_MST_APPLY
from greedy_sorting import greedy_algorithm_sorting
from local_search_MST import localSearch
from local_search_sorting import localSearch_Sorting
from simulated_MST import simulatedAnnealing_MST
from simulated_sorting import simulatedAnnealingSorting
from TabuSearchSorting import tabuSort
from TabuMST import tabuMST
from VariableNeighboor_MST import VNS_MST
from VariableNeighboor_sort import VNS_Sort
import matplotlib.pyplot as plt

def MST_Solution_Print(sol_Px):
    
    total_cost = 0
    for i in range(len(sol_Px)):
        if (sol_Px[i][0] != sol_Px[i][1]):
            print("Edge: {}, Source: {}, Dest: {}, Cost: {}".format(i, sol_Px[i][0], sol_Px[i][1], sol_Px[i][2]))
            total_cost += sol_Px[i][2]

    print("Total Cost: {}".format(total_cost))

def convert_chr_int_arr(arr):
    for i in range(len(arr)):
        arr[i] = int(arr[i])

    return arr

def convert_chr_int_graph(arr, INF):
    for i in range(len(arr)):
        if (int(arr[i]) == 0):
            arr[i] = INF
        else:
            arr[i] = int(arr[i])
    return arr

def graphPrint(graph):
    print("-----Graph-----")
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            print(graph[i][j], end = " ")
        print("\n", end = "")
    print("---------------")

def BuildCopyArr(arr):
    temp = []
    for j in range(len(arr)):
        temp.append(arr[j])

    return temp

file = open("./TestResource/171044033_CSE454_Test_Array.txt", "r")
lines = file.readlines()
arr = []
for line in lines:
    arr.append(convert_chr_int_arr(line.split(" ")))

greedySort_old = []
greedySort_new = []

backtrakingSort_old = []
backtrakingSort_new = []

localSearch_old = []
localSearch_new = []

SASort_old = []
SASort_new = []

VNSSort_old = []
VNSSort_new = []

GASort_old = []
GASort_new = []

greedySort_old = []
greedySort_new = []

TSSort_old = []
TSSort_new = []

PSOSort_old = []
PSOSort_new = []

for i in range(len(arr)):
    """print("Bruteforce Test Cases: {}".format(i))
    temp = BuildCopyArr(arr[i])
    print("Unsorted: {}".format(temp))
    bruteforce(temp)
    print("Sorted: {}".format(temp))"""

    print("-----------------------Greedy Test Cases: {}-----------------------".format(i))
    temp = BuildCopyArr(arr[i])
    greedySort_old.append(arrayCost(temp))
    print("Unsorted: {}".format(temp))
    temp = greedy_algorithm_sorting(temp)
    print("Sorted: {}".format(temp))
    greedySort_new.append(arrayCost(temp))

    print("-----------------------Backtracking Test Cases: {}-----------------------".format(i))
    temp = BuildCopyArr(arr[i])
    backtrakingSort_old.append(arrayCost(temp))
    print("Unsorted: {}".format(temp))
    temp = backtracking_sort(temp)
    print("Sorted: {}".format(temp))
    backtrakingSort_new.append(arrayCost(temp))

    print("-----------------------Local Search Test Cases: {}-----------------------".format(i))
    temp = BuildCopyArr(arr[i])
    localSearch_old.append(arrayCost(temp))
    print("Unsorted: {}".format(temp))
    temp = localSearch_Sorting(temp)
    print("Sorted: {}".format(temp))
    localSearch_new.append(arrayCost(temp))

    print("-----------------------Simulated Annealing Test Cases: {}-----------------------".format(i))
    temp = BuildCopyArr(arr[i])
    SASort_old.append(arrayCost(temp))
    print("Unsorted: {}".format(temp))
    temp = simulatedAnnealingSorting(temp)
    print("Sorted: {}".format(temp))
    SASort_new.append(arrayCost(temp))

    print("-----------------------VNS Test Cases: {}-----------------------".format(i))
    temp = BuildCopyArr(arr[i])
    VNSSort_old.append(arrayCost(temp))
    print("Unsorted: {}".format(temp))
    temp = VNS_Sort(temp)
    print("Sorted: {}".format(temp))
    VNSSort_new.append(arrayCost(temp))

    print("-----------------------Genetic Test Cases: {}-----------------------".format(i))
    temp = BuildCopyArr(arr[i])
    GASort_old.append(arrayCost(temp))
    print("Unsorted: {}".format(temp))
    temp = geneticSort(temp)
    print("Sorted: {}".format(temp))
    GASort_new.append(arrayCost(temp))

    print("-----------------------Tabu Test Cases: {}-----------------------".format(i))
    temp = BuildCopyArr(arr[i])
    TSSort_old.append(arrayCost(temp))
    print("Unsorted: {}".format(temp))
    temp = tabuSort(temp)
    print("Sorted: {}".format(temp))
    TSSort_new.append(arrayCost(temp))

    print("-----------------------PSO Test Cases: {}-----------------------".format(i))
    temp = BuildCopyArr(arr[i])
    PSOSort_old.append(arrayCost(temp))
    print("Unsorted: {}".format(temp))
    temp = PSOSort(temp)
    print("Sorted: {}".format(temp))
    PSOSort_new.append(arrayCost(temp))

###################################################################
print("\n---------------MST TESTS---------------")
INF = float("inf")
file = open("./TestResource/171044033_CSE454_Test_Graph.txt", "r")
graphs = []
graph = []
lines = file.readlines()
for line in lines:
    line_ = line.split(" ")
    if (len(line_) == 1):
        temp = []
        for i in range(len(graph)):
            temp.append(graph[i])

        graphs.append(temp)
        graph.show()

    else:
        graph.append(convert_chr_int_graph(line_, INF))

for i in range(len(graphs)):
    print("----------GREEDY MST----------")
    graph = graphs[i]
    graphPrint(graph)
    solPx = greedy_MST_APPLY(graph, INF)
    MST_Solution_Print(solPx)

for i in range(len(graphs)):
    print("----------LOCAL SRCH----------")
    graph = graphs[i]
    graphPrint(graph)
    solPx = localSearch(graph, INF)
    MST_Solution_Print(solPx)

for i in range(len(graphs)):
    print("----------BRUTEFORCE----------")
    graph = graphs[i]
    graphPrint(graph)
    solPx = bruteforce_MST(graph, INF)
    print("The edges of MST: {}\nTotal Cost: {}".format(solPx[0], solPx[1]))

for i in range(len(graphs)):
    print("----------SIMULATED ANNEALING----------")
    graph = graphs[i]
    graphPrint(graph)
    solPx = simulatedAnnealing_MST(graph, INF)
    MST_Solution_Print(solPx)

for i in range(len(graphs)):
    print("----------VNS----------")
    graph = graphs[i]
    graphPrint(graph)
    solPx = VNS_MST(graph, INF)
    MST_Solution_Print(solPx)

for i in range(len(graphs)):
    print("----------TABU----------")
    graph = graphs[i]
    graphPrint(graph)
    solPx = tabuMST(graph, INF)
    MST_Solution_Print(solPx)

for i in range(len(graphs)):
    print("----------PSO----------")
    graph = graphs[i]
    graphPrint(graph)
    solPx = PSO_Mst(graph, INF)
    MST_Solution_Print(solPx)