import sys

class Graph():

    def __init__(self,vert):
        self.V = vert
        self.graph = [[0 for column in range(vert)] for row in range(vert)]

    def printSolution(self, dist):
        print ("Vertex \tDistance from Source")
        for node in range(self.V):
            print(node,"\t",dist[node])


    def minDistance(self,dist,sptSet):
        min = sys.maxsize
        for z in range(self.V):
            if dist[z]<min and sptSet[z]==False:
                min = dist[z]
                mindex = z

        return mindex

    def dijkstra(self,src):
        dist = [sys.maxsize] * self.V
        dist[src]=0
        sptSet = [False]*self.V
        
        for cout in range(self.V):
            u =self.minDistance(dist,sptSet)
            sptSet[u]=True
            for v in range(self.V):
                if self.graph[u][v]>0 and sptSet[v]==False and dist[v] > dist[u]+self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]

        self.printSolution(dist)
g.dijkstra(0)