# import random  
from random import randint 

from collections import defaultdict
    
alfB = 0.5
alfT = 0.5
alfD = 0.5
alfBUF = 0.5

betaB = 0.5
betaT = 0.5
betaD = 0.5
betaBUF = 0.5

# creating edge class
class Edge:

    def __init__(self):
        # define five variables 
        self.ban =  randint(1, 10) - 0.5 # for bandwidth
        self.stb =  randint(1, 10) - 0.5 # for stability time
        self.buf =  randint(1, 10) - 0.5 # for buffer size
        self.dly =  randint(1, 10) - 0.5 # for network delay
        self.vis = self.visibility() # for visibility

    def printValue(self):
        print(self.ban , self.stb, self.buf, self.dly, self.vis)

    def visibility(self):
        visb = (self.ban**alfB + self.stb**alfT + self.buf**alfBUF) / (self.dly**alfD)
        return visb


e1 = Edge()
e2 = Edge()
e3 = Edge()
e4 = Edge()
e5 = Edge()
e6 = Edge()
e7 = Edge()
e8 = Edge()
e9 = Edge()
e10 = Edge()

antMatrix = [
    [None,e1,None,None,None,e6,None],
    [None,None,e2,None,None,None,e7],
    [None,None,None,e3,None,None,None],
    [None,None,None,None,None,None,None],
    [None,None,None,e4,None,None,None],
    [None,None,None,None,e5,None,e10],
    [None,None,e8,None,e9,None,None],
]

antVisMatrix = [
    [None,e1.vis,None,None,None,e6.vis,None],
    [None,None,e2.vis,None,None,None,e7.vis],
    [None,None,None,e3.vis,None,None,None],
    [None,None,None,None,None,None,None],
    [None,None,None,e4.vis,None,None,None],
    [None,None,None,None,e5.vis,None,e10.vis],
    [None,None,e8.vis,None,e9.vis,None,None],
]

firstVisMatrix = [
    [None,e1.vis,None,None,None,e6.vis,None],
    [None,None,e2.vis,None,None,None,e7.vis],
    [None,None,None,e3.vis,None,None,None],
    [None,None,None,None,None,None,None],
    [None,None,None,e4.vis,None,None,None],
    [None,None,None,None,e5.vis,None,e10.vis],
    [None,None,e8.vis,None,e9.vis,None,None],
]


# print(antVisMatrix)

allPaths = []

# This class represents a directed graph
# using adjacency list representation
class Graph:
    def __init__(self, vertices):
        # No. of vertices
        self.V = vertices

        # default dictionary to store graph
        self.graph = defaultdict(list)

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    '''A recursive function to print all paths from 'u' to 'd'.
	visited[] keeps track of vertices in current path.
	path[] stores actual vertices and path_index is current
	index in path[]'''

    def printAllPathsUtil(self, u, d, visited, path):

        # Mark the current node as visited and store in path
        visited[u]= True
        path.append(u)

        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            print(path)
            arr = []
            for e in path:
                arr.append(e)
            allPaths.append(arr)
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.graph[u]:
                if visited[i]== False:
                    self.printAllPathsUtil(i, d, visited, path)
                    
            # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u]= False

    # Prints all paths from 's' to 'd'
    def printAllPaths(self, s, d):

        # Mark all the vertices as not visited
        visited =[False]*(self.V)

        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        self.printAllPathsUtil(s, d, visited, path)

# Create a graph given in the above diagram
g = Graph(7)
g.addEdge(0, 1)
g.addEdge(0, 5)
g.addEdge(1, 2)
g.addEdge(1, 6)
g.addEdge(2, 3)
g.addEdge(4, 3)
g.addEdge(5, 4)
g.addEdge(5, 6)
g.addEdge(6, 2)
g.addEdge(6, 4)

loop = 100

while loop > 0:
    loop -= 1
    s = randint(0,6)
    d = randint(0,6)

    if s == d:
        continue

    try:
        print ("Following are all different paths from % d to % d :" %(s, d))
        g.printAllPaths(s, d)

        # print("All Paths Matrix")
        # print(allPaths)

        minVis = 999999999
        index = -1
        for i in range (len(allPaths)):
            cost = 0
            for j in range(len(allPaths[i])-1):
                m = allPaths[i][j]
                n = allPaths[i][j+1]
                # print(m,n)
                cost += antVisMatrix[m][n]
            if(minVis>cost) :
                minVis = cost
                index = i

        if minVis == 999999999:
            print("No Path Found")
        else:
            print(minVis)
        # this is the shorts path array
        shortsPath = allPaths[index]
        print(shortsPath)
        # print(antVisMatrix)
        ans = 0
        for j in range(len(shortsPath)-1):
            m = allPaths[index][j]
            n = allPaths[index][j+1]
            ans += antVisMatrix[m][n]

        print(ans)

        minBan = 999999
        minStb = 999999
        minBuf = 999999
        sumDly = 0
        for j in range(len(shortsPath)-1):
            m = allPaths[index][j]
            n = allPaths[index][j+1]
            # print(antMatrix[m][n].ban)
            minBan = min(minBan, antMatrix[m][n].ban)
            minStb = min(minStb, antMatrix[m][n].stb)
            minBuf = min(minBuf, antMatrix[m][n].buf)
            sumDly += antMatrix[m][n].dly

        # print(minBan,minBuf,minStb,sumDly)
        tou = (minBan**betaB + minStb**betaT + minBuf**betaBUF) / (sumDly**betaD)
        print(tou)
        # print(antVisMatrix)
        # update visibility
        for j in range(len(shortsPath)-1):
            m = allPaths[index][j]
            n = allPaths[index][j+1]
            antVisMatrix[m][n] += tou

        # print(antVisMatrix)
        # print(firstVisMatrix)
    except:
        pass


# difference in visibility factor
diffMatrix = []

for i in range (len(firstVisMatrix)):
    arr2 = []
    for j in range(len(firstVisMatrix[i])):
        if firstVisMatrix[i][j] is None:
            arr2.append(0)
        else:
            arr2.append(antVisMatrix[i][j]-firstVisMatrix[i][j])
    diffMatrix.append(arr2) 

print(diffMatrix)
