# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

class Node(object):
   def __init__(self, name):
       self.name = str(name)
   def getName(self):
       return self.name
   def __str__(self):
       return self.name
   def __repr__(self):
      return self.name
   def __eq__(self, other):
      return self.name == other.name
   def __ne__(self, other):
      return not self.__eq__(other)

class Edge(object):
   def __init__(self, src, dest):
       self.src = src
       self.dest = dest
   def getSource(self):
       return self.src
   def getDestination(self):
       return self.dest
   def __str__(self):
       return str(self.src) + '->' + str(self.dest)

class BuildingRoute(Edge):
    """
    Represents a one directional path between two MIT buildings.  
    """
    def __init__(self, src, dest, distance, outdoorDistance):
        """
        Creates a new instance of BuildingRoute with source node SRC,
        destination Node DEST, total distance DISTANCE, and outdoor distance
        OUTDOORDISTANCE.
        src: Node
        dest: Node
        distance: int
        outdoorDistance: int
        returns: BuildingRoute
        """
        assert distance >= outdoorDistance
        Edge.__init__(self, src, dest)
        self.distance = distance
        self.outdoor = outdoorDistance

    def getDistance(self):
        return self.distance

    def getOutdoor(self):
        return self.outdoor

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
       self.nodes = set([])
       self.edges = {}
    def addNode(self, node):
       if node in self.nodes:
           raise ValueError('Duplicate node')
       else:
           self.nodes.add(node)
           self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
       return self.edges[node]
    def hasNode(self, node):
       return node in self.nodes
    def getNode(self, name):
        """
        Given name of node, returns that Node if present, otherwise returns
        ValueError
        name: a str
        returns: a Node
        """
        for n in self.nodes:
            if name == n.getName():
                return n
        raise ValueError('Node not in graph')
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = res + str(k) + '->' + str(d) + '\n'
        return res[:-1]

class MITmapGraph(Digraph):
    def addEdge(self, edge):
        """
        Adds BuildingRoute to edge list
        edge: BuildingRoute
        modifies: self.edges
        """
        src = edge.getSource()
        dest = edge.getDestination()
        dist = edge.getDistance()
        outdoor = edge.getOutdoor()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append((dest, dist, outdoor))

