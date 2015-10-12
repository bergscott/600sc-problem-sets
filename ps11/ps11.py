# 6.00 Problem Set 11
#
# ps11.py
#
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
from graph import *

#
# Problem 2: Building up the Campus Map
#
# Write a couple of sentences describing how you will model the
# problem as a graph)
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."
    MITmap = MITmapGraph()
    buildings = {}
    datFile = open(mapFilename, 'r')
    pathList = datFile.readlines()
    datFile.close()
    for path in pathList:
        splitLine = path.strip().split()
        for elem in splitLine[0:4]: print elem,
        for building in splitLine[0:2]:
            if building not in buildings.keys():
                buildings[building] = Node(building)
                MITmap.addNode(buildings[building])
        MITmap.addEdge(BuildingRoute(buildings[splitLine[0]], 
                                     buildings[splitLine[1]],
                                     int(splitLine[2]), int(splitLine[3])))
    print "Done!"
    return MITmap
        

MITmap = load_map('mit_map.txt')
print MITmap
#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints
#

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    allPaths = getallPaths(digraph, digraph.getNode(start), digraph.getNode(end))
    bestPath = None
    bestDist = None
    for p in allPaths:
        if totalDist(p) < maxTotalDist \
                and outdoorDist(p) < maxDistOutdoors \
                and (totalDist(p) < bestDist or bestDist == None):
            bestPath = p
            bestDist = totalDist(p)
    if bestPath == None:
        raise ValueError('No path fits constraints')
    else:
        return [str(p[0]) for p in bestPath]

## def getallPaths(digraph, start, end, visited=[], parents=[], foundPaths=[]):
##     if start == end:
##         return [str(start)]
##     if parents == []:
##         visited = visited + [str(start)]
##     for node in digraph.childrenOf(start):
##         if (str(node) not in visited):
##             if node == end:
##                 foundPaths.append(parents + [str(start), str(node)])
##             else:
##                 visited = visited + [str(node)]
##                 print "Start: {}".format(str(start))
##                 print "Visited: {}".format(visited)
##                 getallPaths(digraph, node, end, visited, 
##                             parents + [str(start)], foundPaths)
##     if parents == []:
##         return foundPaths
##     else: return None
    
def getallPaths(digraph, start, end, parents=[], foundPaths=[]):
    if type(start) == tuple:
        startNode = start[0]
    else:
        parents = [(start, 0, 0)]
        startNode = start
    if startNode == end:
        return start
    for path in digraph.childrenOf(startNode):
        if (path[0] not in [p[0] for p in parents]):
            ## print 'Parents: {}'.format(parents)
            ## print 'In {} checking {}'.format(start, path)
            if path[0] == end:
                foundPaths.append(parents + [path])
            else:
                getallPaths(digraph, path, end, 
                            parents + [path], foundPaths)
    if len(parents) == 1:
        return foundPaths
    else: return None

def totalDist(path):
    tot = 0
    for p in path:
        tot += p[1] 
    return tot

def outdoorDist(path):
    tot = 0
    for p in path:
        tot += p[2] 
    return tot

def test():
    dg = Digraph()
    nodes = {}
    for n in range(1,7):
        nodes[n] = Node(n)
        dg.addNode(nodes[n])
    dg.addEdge(Edge(nodes[1], nodes[2]))
    dg.addEdge(Edge(nodes[1], nodes[3]))
    dg.addEdge(Edge(nodes[2], nodes[4]))
    dg.addEdge(Edge(nodes[2], nodes[5]))
    dg.addEdge(Edge(nodes[3], nodes[5]))
    dg.addEdge(Edge(nodes[3], nodes[6]))
    dg.addEdge(Edge(nodes[6], nodes[5]))
    dg.addEdge(Edge(nodes[5], nodes[4]))
    dg.addEdge(Edge(nodes[2], nodes[1]))
    dg.addEdge(Edge(nodes[2], nodes[3]))
    print getallPaths(dg, nodes[1], nodes[5])

def test2():
    mg = MITmapGraph()
    nodes = {}
    for n in range(1,7):
        nodes[n] = Node(n)
        mg.addNode(nodes[n])
    mg.addEdge(BuildingRoute(nodes[1], nodes[2], 15, 5))
    mg.addEdge(BuildingRoute(nodes[1], nodes[3], 15, 5))
    mg.addEdge(BuildingRoute(nodes[2], nodes[4], 15, 5))
    mg.addEdge(BuildingRoute(nodes[2], nodes[5], 15, 5))
    mg.addEdge(BuildingRoute(nodes[3], nodes[5], 15, 5))
    mg.addEdge(BuildingRoute(nodes[3], nodes[6], 15, 5))
    mg.addEdge(BuildingRoute(nodes[6], nodes[5], 15, 5))
    mg.addEdge(BuildingRoute(nodes[3], nodes[6], 22, 1))
    mg.addEdge(BuildingRoute(nodes[5], nodes[4], 15, 5))
    mg.addEdge(BuildingRoute(nodes[2], nodes[1], 15, 5))
    mg.addEdge(BuildingRoute(nodes[2], nodes[3], 15, 5))
    print getallPaths(mg, nodes[1], nodes[5])

## test()    
## test2()
## print len(getallPaths_v2(MITmap, MITmap.getNode('1'), MITmap.getNode('16')))

print bruteForceSearch(MITmap, '1', '26', 1000, 1000)
#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    bestPaths = getBestPaths(digraph, digraph.getNode(start), 
                             digraph.getNode(end))
    for path in bestPaths:
        if totalDist(digraph, path) < maxTotalDist \
                and outdoorDist(digraph, path) < maxDistOutdoors:
            return [str(p[0]) for p in path]
    else:
        raise ValueError('No path fits constraints')

def getBestPaths(digraph, start, end, parents=[], bestFound=[], bestDist=None,
                 bestOutdoor=None):
    if type(start) == tuple:
        startNode = start[0]
    else:
        parents = [(start, 0, 0)]
        startNode = start
    if startNode == end:
        return start
    for path in digraph.childrenOf(startNode):
        if (path[0] not in [p[0] for p in parents]):
            dist = totalDist(parents + [path])
            outdoor = outdoorDist(parents + [path])
            if bestDist == None or dist <= bestDist or outdoor <=bestOutdoor:
            ## print 'Parents: {}'.format(parents)
            ## print 'In {} checking {}'.format(start, path)
                if path[0] == end:
                    if bestDist == None or \
                            (dist <= bestDist and outdoor <= bestOutdoor):
                        bestFound = parents + [path]
                        bestDist = dist
                        bestOutdoor = outdoor
                    else: #Needs work to get bests
                        bestFound.append(parents + [path])
                        bestDist = min(dist, bestDist)
                        bestOutdoor = min(outdoor, bestOutdoor)
                else:
                    getBestPaths(digraph, path, end, parents + [path], 
                                 bestFound, bestDist, bestOutdoor)
    if len(parents) == 1:
        return foundPaths
    else: return None
 

# Uncomment below when ready to test
##if __name__ == '__main__':
##    # Test cases
##    digraph = load_map("mit_map.txt")
##
##    LARGE_DIST = 1000000
##
##    # Test case 1
##    print "---------------"
##    print "Test case 1:"
##    print "Find the shortest-path from Building 32 to 56"
##    expectedPath1 = ['32', '56']
##    brutePath1 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
##    dfsPath1 = directedDFS(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
##    print "Expected: ", expectedPath1
##    print "Brute-force: ", brutePath1
##    print "DFS: ", dfsPath1
##
##    # Test case 2
##    print "---------------"
##    print "Test case 2:"
##    print "Find the shortest-path from Building 32 to 56 without going outdoors"
##    expectedPath2 = ['32', '36', '26', '16', '56']
##    brutePath2 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, 0)
##    dfsPath2 = directedDFS(digraph, '32', '56', LARGE_DIST, 0)
##    print "Expected: ", expectedPath2
##    print "Brute-force: ", brutePath2
##    print "DFS: ", dfsPath2
##
##    # Test case 3
##    print "---------------"
##    print "Test case 3:"
##    print "Find the shortest-path from Building 2 to 9"
##    expectedPath3 = ['2', '3', '7', '9']
##    brutePath3 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
##    dfsPath3 = directedDFS(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
##    print "Expected: ", expectedPath3
##    print "Brute-force: ", brutePath3
##    print "DFS: ", dfsPath3
##
##    # Test case 4
##    print "---------------"
##    print "Test case 4:"
##    print "Find the shortest-path from Building 2 to 9 without going outdoors"
##    expectedPath4 = ['2', '4', '10', '13', '9']
##    brutePath4 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, 0)
##    dfsPath4 = directedDFS(digraph, '2', '9', LARGE_DIST, 0)
##    print "Expected: ", expectedPath4
##    print "Brute-force: ", brutePath4
##    print "DFS: ", dfsPath4
##
##    # Test case 5
##    print "---------------"
##    print "Test case 5:"
##    print "Find the shortest-path from Building 1 to 32"
##    expectedPath5 = ['1', '4', '12', '32']
##    brutePath5 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
##    dfsPath5 = directedDFS(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
##    print "Expected: ", expectedPath5
##    print "Brute-force: ", brutePath5
##    print "DFS: ", dfsPath5
##
##    # Test case 6
##    print "---------------"
##    print "Test case 6:"
##    print "Find the shortest-path from Building 1 to 32 without going outdoors"
##    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
##    brutePath6 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, 0)
##    dfsPath6 = directedDFS(digraph, '1', '32', LARGE_DIST, 0)
##    print "Expected: ", expectedPath6
##    print "Brute-force: ", brutePath6
##    print "DFS: ", dfsPath6
##
##    # Test case 7
##    print "---------------"
##    print "Test case 7:"
##    print "Find the shortest-path from Building 8 to 50 without going outdoors"
##    bruteRaisedErr = 'No'
##    dfsRaisedErr = 'No'
##    try:
##        bruteForceSearch(digraph, '8', '50', LARGE_DIST, 0)
##    except ValueError:
##        bruteRaisedErr = 'Yes'
##    
##    try:
##        directedDFS(digraph, '8', '50', LARGE_DIST, 0)
##    except ValueError:
##        dfsRaisedErr = 'Yes'
##    
##    print "Expected: No such path! Should throw a value error."
##    print "Did brute force search raise an error?", bruteRaisedErr
##    print "Did DFS search raise an error?", dfsRaisedErr
##
##    # Test case 8
##    print "---------------"
##    print "Test case 8:"
##    print "Find the shortest-path from Building 10 to 32 without walking"
##    print "more than 100 meters in total"
##    bruteRaisedErr = 'No'
##    dfsRaisedErr = 'No'
##    try:
##        bruteForceSearch(digraph, '10', '32', 100, LARGE_DIST)
##    except ValueError:
##        bruteRaisedErr = 'Yes'
##    
##    try:
##        directedDFS(digraph, '10', '32', 100, LARGE_DIST)
##    except ValueError:
##        dfsRaisedErr = 'Yes'
##    
##    print "Expected: No such path! Should throw a value error."
##    print "Did brute force search raise an error?", bruteRaisedErr
##    print "Did DFS search raise an error?", dfsRaisedErr

