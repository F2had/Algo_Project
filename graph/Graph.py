import json
from collections import defaultdict


class Edge(tuple):
    def __init__(self,edge):
        self.from_point=edge['from_point']
        self.to_point=edge['to_point']
        self.weight=edge['distance']
        self.transit_mode=edge['travel_mode']

    def __new__(cls, e1, e2):
        return tuple.__new__(cls, (e1, e2))

    def __repr__(self):
        return "Edge(%s, %s)" % (repr(self[0]), repr(self[1]))


    def __repr__(self):
        return "Edge(%s, %s,%s)" % (repr(self.from_point), repr(self.to_point), repr(self.transit_mode))

    __str__ = __repr__


class Vertex:
    def __init__(self,name,edge):
        self.name=name
        if edge['from_point']==self.name:
            self.latitude = edge['start_lat']
            self.longtitude = edge['start_lng']
        elif edge['to_point']==self.name:
            self.latitude = edge['end_lat']
            self.longtitude = edge['end_lng']

    def getPointName(self):
        return self.name

    def getPointPosition(self):
        pass

    def __repr__(self):
        return 'GraphPoint(%s,%s,%s)' % (repr(self.name),repr(self.latitude),repr(self.longtitude))

    __str__ = __repr__


class Graph(dict):
    def __init__(self,result=None):
        self.vertices = set([])
        self.edges={}
        self._graph = defaultdict(list)
        if result:
            for e in result:
                edge=Edge(e)
                print(edge)
                self.add_edge(edge,e)

    def __str__(self):
        """
        a: ['b', 'c']
        b: ['a']
        c: ['a', 'c']
        """
        return '\n'.join(['%s: %s' % (str(k), str(v)) for k, v in self._graph.items()])

    def add_edge(self,edge,e):

        #print("add edge from {} to {}, weight {},transit_mode{} ".format(edge.from_point, edge.to_point, edge.weight,edge.transit_mode))
        #edge = set(edge)
        #print(edge)
        node1 = Vertex(edge.from_point, e)
        self.vertices.add(node1)
        #print(node1)
        if edge.to_point:
            node2 = Vertex(edge.to_point, e)
            print(node2)
            #print(node2.name)
            #self.add_vertex(node1).append(self.add_vertex(node2))
            self._graph[node1].append(self._graph[node2])
            self._graph[node2].append(self._graph[node1])
            #self.add_vertex(node2).append(self.add_vertex(node1))
        #else:
           #self._graph[node1].append(node1)
        #self.add_vertex(node1).append(self.add_vertex(node1))

    def nodes(self):
        """Return a list of all nodes in the graph."""
        return list(self._graph)

    def add_vertex(self,node):
        if node not in self.edges:
            self.edges[node] = []

    def vertices(self):
        pass

    def edges(self):
        edge_pairs = []
        for node, edges in self._graph.items():
            for edge in edges:
                edge_pairs.append((node, edge))
        return edge_pairs

    def generate_edges(self):
        pass

    def __len__(self):
        return len(self._graph)




if __name__ == '__main__':
    with open('result.json', 'r') as fp:
        result= json.load(fp)
    g = Graph(result)
   # print(g.edges())










