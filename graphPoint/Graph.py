import json

from graphPoint.database import database

class Edge(tuple):
    def __init__(self,edge):
        self.from_point=edge['from_point']
        self.to_point=edge['to_point']
        self.weight=edge['distance']
        self.transit_mode=edge['travel_mode']
        self.transit=(self.weight,self.transit_mode)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str("Edge(%s, %s,%s)" % (repr(self.from_point), repr(self.to_point), repr(self.transit)))
    __str__ = __repr__


class Vertex:
    def __init__(self,v):

        self.name=v['name']
        self.latitude =v['location'][0]
        self.longtitude =v['location'][1]
        self.location=v['location']

    def __eq__(self, other):
        return self.name==other.name

    def __hash__(self):
        return hash(str(self))

    " Vetrx(name,(latitude,longtitude)) "
    def __repr__(self):
        return str('Vetrx(%s,%s)' % (repr(self.name),repr(self.location)))
    __str__ = __repr__


"""    {
        a: {'b' :(3223,walking ), 'c':(1222,driving)}
        b: {'a':(3212,driving)}
        c: {'a':(1232,waliking), 'c':(1212,waliking)}
        }
"""

class Graph:

    def __init__(self,edges):

        self._graph ={}
        if edges:
            # add connection_database into graph ,and pass each of their connection
            for edge in edges:
                e = Edge(edge)
                self.add_edge(e)


    "add a edge to a graph that connect two node in a graph, edge.transit is a list of two element of connected nodes,  tuple(distance,mode)"
    def add_edge(self,edge):
        node1=Vertex(edge.from_point)
        node2=Vertex(edge.to_point)

        self.add_vertex(node1)
        self._graph[node1][node2]=edge.transit


    "Add new edge to graph. Nodes are automatically added"
    def add_vertex(self,node):
        if node not in self._graph:
            self._graph[node] ={}

    "return a list of all nodes in the graph"
    def nodes(self):
        return list(self._graph)


    "return a list of two element of connected nodes. tuple(src_node,des_node,transit(distance,transit_mode)"
    def path(self):
        edge_pairs = []
        for origin_node in self._graph.keys():
            for des_node in self._graph[origin_node]:
                edge_pairs.append((origin_node, des_node,self._graph[origin_node][des_node]))
        return edge_pairs



if __name__ == '__main__':
    d=database()
    vertex=d.point_database
    edges=d.connection_database
    g=Graph(edges)
    print(g.path())













