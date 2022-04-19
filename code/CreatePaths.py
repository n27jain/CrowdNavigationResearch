from SavingMap import SavingMap
from MapGenerator import *
from MapObjects import *
import random
from random import choice


def findNode(coordinate, nodes):
    for node in nodes:
        if node.x == coordinate[0] and node.y == coordinate[1]: 
            return node
    return None
def findEdge(startNode, endNode, edges):
    for edge in edges:
        if edge.node_1 == startNode and node.node_2 == endNode: 
            return edge
    return None

def createPath(path_min_len, x,y,n):
    try:
        allEdges = x + y
        i = 0
        #1.) checked nodes is none
        checkedNodes = []
        path =  Path(path_min_len) #2. start a new path
        start_node = None
        options = []
        east = None
        west = None
        south = None
        north = None

        start_node =  n[random.randint(0,len(n) - 1)] # select a randome start node

        while (start_node.isIsolated): # while the node discovered has no edges
            start_node =  n[random.randint(0,len(n) - 1)] # select a randome start node
            checkedNodes.append((start_node.x, start_node.y))

        path.nodes.append(start_node)
        path.directions.append(None) # the first direction travelled is null
        path.motion.append(None) # first node no motion
        
        j = 0

        while j < path_min_len:
            #3.) we will check each node to see if it has edges
            #4.) if it doesnt we will back track
            #5.) if it does, then we will move to the next node 
            #6.) we do not consider reversing our path as an option

                # direction
            # 0 - East
            # 1 - West
            # 2 - South 
            # 3 - North
            if len(path.nodes)  == 0: # we backtracked all the way to the begining
                return None
            curNode = path.nodes[-1] # get the last appeneded node
            lastDir = path.directions[-1] # get the last direction travelled
            exclude  = []
            options = [ curNode.east, curNode.west, curNode.south, curNode.north] # NOTE HERE east and north are 0 , 1 
            
            if lastDir == 0:
                options[1] == None # dont go west if u came from the east
                
            elif lastDir == 1:
                options[0] == None
                
            elif lastDir == 2:
                options[3] == None
                
            elif lastDir == 3:
                options[2] == None
                
            # Exlcude the nodes already visited or nodes that are isolated
            if (options[0] != None):
                test = findNode(options[0].node_2,n)
                if  options[0].node_2 in checkedNodes or test.isIsolated:
                    options[0] = None
                
            if options[1] != None: 
                test = findNode(options[1].node_1,n)
                if (options[1].node_1 in checkedNodes) or test.isIsolated:
                    options[1] = None

            if options[2] != None: 
                test = findNode(options[2].node_1,n)
                if (options[2].node_1 in checkedNodes) or test.isIsolated:
                    options[2] = None

            if options[3] != None: 
                test = findNode(options[3].node_2,n)
                if (options[3].node_2 in checkedNodes) or test.isIsolated:
                    options[3] = None

            for i in range(4):
                if options[i] == None : exclude.append(i)
            if len(exclude) == 4: # time to backtrack
                path.nodes.pop() # remove the last node we found
                if path.directions:
                    path.directions.pop()
                if path.edges:
                    path.edges.pop()
                if path.motion:
                    path.motion.pop()
                j = j - 1
                if j < 0: 
                    print("Bad run get new route")
                    return None
            else:

                # motion
                # 0 - straight
                # 1 - right
                # 2 - left 
                randSide = choice([p for p in range(0,3) if p not in exclude])
                if options[randSide] != None: 
                    lastDirection  = path.directions[-1]
                    lastMotion  = path.motion[-1]
                    path.directions.append(randSide)
                    if lastMotion == None:
                        path.motion.append(0) # moving straight
                    elif lastDirection ==  randSide:
                        path.motion.append(0) # moving straight
                    elif lastDirection == 0: #east
                        if randSide == 2: 
                            path.motion.append(1) # EN Left
                        if randSide == 3: 
                            path.motion.append(2) # ES Right
                    elif lastDirection == 1: #west
                        if randSide == 2: 
                            path.motion.append(2) # WN 
                        if randSide == 3: 
                            path.motion.append(1) # WS 
                    elif lastDirection == 2: #south
                        if randSide == 0: 
                            path.motion.append(2) # SE
                        if randSide == 1:
                            path.motion.append(1) # SW
                    elif lastDirection == 3: #north
                        if randSide == 0: 
                            path.motion.append(1) # NE
                        if randSide == 1: 
                            path.motion.append(2) # NW

                    # Get the updated edge instead of the pointer edge.
                    #newEdge =  findEdge()
                    # this_edge  = options[randSide]
                    # newEdge =  findEdge(this_edge.node_1, this_edge.node_2, allEdges)

                    # if (newEdge == None) : 
                    #     print("FATAL ERROR. NO such edge exists")
                    
                    # path.edges.append(newEdge)

                    path.edges.append(options[randSide])
                    newNode = None
                    if randSide == 0 or randSide == 3: # east or north
                        #this means look at the second node of the edge
                        newNodeCor =  options[randSide].node_2
                    
                    elif randSide == 1 or randSide == 2:  # west or south
                        # this means that we look at the first node of the edge to travel to
                        newNodeCor =  options[randSide].node_1
                    
                    newNode = findNode(newNodeCor,n)
                    if newNode == None: print("Fatal error. Node searched but does not exist")
                    path.nodes.append(newNode)
                    checkedNodes.append(newNodeCor)
                    j = j + 1
        return path
    except Exception as e:
        print("error : ", e)
        return None

def setUpPaths(path_dir, numPaths, pathLen, xmax = None, ymax =  None):
    SM = SavingMap()
    x,y,n = SM.open()
    paths = []
    path_seq = []
    i = 0
    while i < numPaths:
        path = None
        while path == None:
            path = createPath(pathLen, x,y,n)
        for select_node in path.nodes:
                path.q_Seq.append((select_node.x, select_node.y))
        if not path.q_Seq in path_seq:
            i += 1
            paths.append(path)
            path_seq.append(path.q_Seq)

    for i in range(len(paths)):
        paths[i].printSelf()
        title = path_dir + "path" + str(i)
        paths[i].makeGraph(title, xmax, ymax)
        
    createPathFile(paths)
    return paths

def createPathFile(paths):
    SM = SavingMap()
    SM.savePaths(paths)
    # f = open("paths/paths.txt",'w')
    # for i in range(len(paths)):
    #      f.write(paths[i].writeSelf())

def getPathsFromSaveData():
    SM = SavingMap()
    paths = SM.openPaths()
    return paths


