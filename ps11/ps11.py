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
        for building in splitLine[0:2]:
            if building not in buildings.keys():
                buildings[building] = Node(building)
                MITmap.addNode(buildings[building])
        MITmap.addEdge(BuildingRoute(buildings[splitLine[0]], 
                                     buildings[splitLine[1]],
                                     int(splitLine[2]), int(splitLine[3])))
    print "Done!"
    return MITmap

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
    for p in allPaths:
        if str(p[0][0]) != start:
            print str(p[0][0])
            break
    bestPath = None
    bestDist = None
    for p in allPaths:
        if totalDist(p) <= maxTotalDist \
                and outdoorDist(p) <= maxDistOutdoors \
                and (bestDist == None or totalDist(p) < bestDist):
            bestPath = p
            bestDist = totalDist(p)
    if bestPath == None:
        raise ValueError('No path fits constraints')
    else:
        return [str(p[0]) for p in bestPath]
    
def getallPaths(digraph, start, end, parents=None, foundPaths=None):
    """
    Returns all paths in DIGRAPH that lead from START node to END node

    digraph: a Digraph
    start: a Node in digraph
    end: a Node in digraph
    parents: a list of tuple (Node, int, int), representing visited Nodes
    foundPaths: a list of list of tuple (Node, int, int), rep list of paths
    returns: a list of paths represented by lists of tuple (Node, int, int)
        Node in tuple represents destination of edge (BuildingRoute class)
        First int in tuple represents total distance of edge
        Second int in tuple represents outdoor distance of edge
    """
    if parents == None: parents = []
    if foundPaths == None: foundPaths = []
    if type(start) == tuple:
        startNode = start[0]
    else:
        assert len(foundPaths) == 0
        parents = [(start, 0, 0)]
        startNode = start
    if startNode == end:
        return start
    for path in digraph.childrenOf(startNode):
        if (path[0] not in [p[0] for p in parents]):
            ## print 'Parents: {}'.format(parents)
            ## print 'In {} checking {}'.format(start, path)
            if path[0] == end:
                ##print parents[0][0]
                foundPaths.append(parents + [path])
            else:
                getallPaths(digraph, path, end, 
                            parents + [path], foundPaths)
    if len(parents) == 1:
        return foundPaths
    else: return None

def totalDist(path):
    """
    Returns the total distance of path, PATH.
    path: a list of tuple (Node, int, int)
    returns: an int
    """
    tot = 0
    for p in path:
        tot += p[1] 
    return tot

def outdoorDist(path):
    """
    Returns the outdoor distance of path, PATH.
    path: a list of tuple (Node, int, int)
    returns: an int
    """
    tot = 0
    for p in path:
        tot += p[2] 
    return tot

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
    bestPaths, bestDist, bestOutdoor = getBestPaths(digraph, 
                                   digraph.getNode(start), digraph.getNode(end))
    bestPaths.sort(key=lambda x: totalDist(x))
    for path in bestPaths:
        if totalDist(path) <= maxTotalDist \
                and outdoorDist(path) <= maxDistOutdoors:
            return [str(p[0]) for p in path]
    else:
        raise ValueError('No path fits constraints')

def getBestPaths(digraph, start, end, parents=None, bestFound=None, 
                 bestDist=None, bestOutdoor=None):
    """
    Returns a list of the best paths in DIGRAPH that lead from START node 
    to END node. A path is considered best if it has the lowest total distance
    or the lowest outdoor distance.  Ties in one attribute are broken by the 
    min of the other attribute.  If two best paths have equal total and
    outdoor distances, they are both included in the returned list.

    digraph: a Digraph
    start: a Node in digraph
    end: a Node in digraph
    parents: list of edge tuple (Node, int, int)
    bestFound: list of paths (lists of edge tuple (Node, int, int))
    bestDist: int
    bestOutdoor: int
    returns: list of paths (lists of edge tuple (Node, int, int))
        Node in tuple represents destination of edge (BuildingRoute class)
        First int in tuple represents total distance of edge
        Second int in tuple represents outdoor distance of edge
    """
    if parents == None: parents = []
    if bestFound == None: bestFound = []
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
            if bestDist == None or dist <= bestDist or outdoor <= bestOutdoor:
                if path[0] == end:
                    bestFound, bestDist, bestOutdoor = get_bests(
                                             parents + [path], dist, outdoor, 
                                             bestFound, bestDist, bestOutdoor)
                else:
                    recurse = getBestPaths(digraph, path, end, parents + [path], 
                                           bestFound, bestDist, bestOutdoor)
                    if recurse == None:
                        continue
                    else:
                        bestFound, bestDist, bestOutdoor = recurse
    if bestFound != None:
        return bestFound, bestDist, bestOutdoor
    else: return None
 
def get_bests(newPath, dist, outdoor, oldBests, bestDist, bestOutdoor):
    """
    Given OLDBESTS, a list of best paths and NEWPATH, a candidate for inclusion,
    returns the new best list from the appropriate combination of inputs.
    An item is included in the returned best list if it is either the shortest
    path in total distance with the least distance outdoors, the path with the
    least distance travelled outdoors with the shortest overall distance, fits
    both of the preceding criteria, or is tied with another path that fits the
    preceding criteria. Also returns new minimum total path distance and new
    minimum outdoor distance.

    newPath: a list of tuple (Node, int, int)
    dist: an int (totalDist of newPath)
    outdoor: an int (outdoorDist of newPath)
    oldBests: a list of list of tuple (Node, int, int) (a list of paths)
    bestDist: an int (min totalDist of paths in oldBests)
    bestOutdoor: an int (min outdoorDist of paths in oldBests)
    returns: a list of list of tuple (Node, int, int), an int, an int
    """
    if bestDist == None or \
            (dist < bestDist and outdoor <= bestOutdoor) or \
            (dist <= bestDist and outdoor < bestOutdoor):
        return [newPath], dist, outdoor
    elif (dist > bestDist and outdoor == bestOutdoor) or \
            (dist == bestDist and outdoor > bestOutdoor):
        newBests = oldBests[:]
        for path in oldBests:
            if totalDist(path) == dist and outdoorDist(path) == outdoor:
                newBests.append(newPath)
                break
        return newBests, bestDist, bestOutdoor
    elif dist == bestDist and outdoor == bestOutdoor:
        newBests = [newPath]
        for path in oldBests:
            if totalDist(path) == dist and outdoorDist(path) == outdoor:
                newBests.append(path)
        return newBests, dist, outdoor
    elif dist < bestDist and outdoor > bestOutdoor:
        newBests = [newPath]
        for path in oldBests:
            if outdoorDist(path) < outdoor:
                newBests.append(path)
        return newBests, dist, bestOutdoor
    elif dist > bestDist and outdoor < bestOutdoor:
        newBests = [newPath]
        for path in oldBests:
            if totalDist(path) < dist:
                newBests.append(path)
        return newBests, bestDist, outdoor
    else:
        return oldBests, bestDist, bestOutdoor
    
#### Test Functions ####
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
    mg.addEdge(BuildingRoute(nodes[1], nodes[2], 10, 5))
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
    print getBestPaths(mg, nodes[1], nodes[5])
                
## MITmap = load_map('mit_map.txt')
## print MITmap
## test()       
## test2()      
## print len(getallPaths_v2(MITmap, MITmap.getNode('1'), MITmap.getNode('16')))
## MITmapstr = str(MITmap)
## print bruteForceSearch(MITmap, '32', '56', 1000000, 1000000)
## assert MITmapstr == str(MITmap)
## print bruteForceSearch(MITmap, '2', '9', 1000000, 1000000)
## print directedDFS(MITmap, '1', '26', 1000, 1000)
                
# Uncomment below when ready to test
if __name__ == '__main__':
    # Test cases
    digraph = load_map("mit_map.txt")
    LARGE_DIST = 1000000
                
    # Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    dfsPath1 = directedDFS(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print "DFS: ", dfsPath1
                
    # Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, 0)
    dfsPath2 = directedDFS(digraph, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    print "DFS: ", dfsPath2
                
    # Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3
                
    # Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(digraph, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4
                
    # Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5
                
    # Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(digraph, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6
                
    # Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:        
        bruteForceSearch(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

    # Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

