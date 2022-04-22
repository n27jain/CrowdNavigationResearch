# given a map
# give a route
# we must minimize travel time by adjusting out speed
# Delay = time at traffic light + expect start up delay 
#Let’s assume that there is an additional penalty for stopping at a red light. There usually is a 2 second delay reaction before cars can reach the expected average speed of the coming road.


from MapGenerator import *
from MapObjects import *
from GeneticAlgorithm import GeneticAlgorithm


def solveThisPath(path,pop,gen,pc,pm):
    N = len(path.edges)
    D = []
    S = []
    C = []
    G_T = []
    R_T = []
    G_Offset = []
    motion = path.motion
    nodes = path.nodes

    for edge in path.edges:
        D.append(edge.distance)
        S.append(edge.speed * (1 - edge.traffic))
    for i in range( 0,len(path.nodes) - 1 ): # we can ignore the last light as it is the destination
        node = path.nodes[i]
        direction = path.directions[i+1]
        C.append(node.cycletime)
        G_T.append(node.Go_T[direction])
        R_T.append(node.Stop_T[direction])
        
        offset = node.greenOffset
        if direction > 1:
            offset *= -1 # reverse the offset value because we are waiting for N or S light
        G_Offset.append(offset)

    gA = GeneticAlgorithm(population= pop,generations =  gen, pc =  pc, pm = pm)
    gA.setVars(N ,D ,S , C, G_T ,R_T , G_Offset, motion, path)
    return gA.run()
    

def solveAdaptive(paths):
    nodes = []

    for path in paths:
        nodes.extend(path.nodes)
    # convert set of nodes to     
    nodes = list(set(nodes))

    base = []
    results = []

    # now solve each path 
    for path in paths:
       
        N = len(path.edges)
        D = []
        S = []
        C = []
        G_T = []
        R_T = []
        G_Offset = []
        motion = path.motion
        nodes = path.nodes

        for edge in path.edges:
            D.append(edge.distance)
            S.append(edge.speed * (1 - edge.traffic))
        for i in range( 0,len(path.nodes) - 1 ):
            node = path.nodes[i]
            direction = path.directions[i+1]
            C.append(node.cycletime)
            G_T.append(node.Go_T[direction])
            R_T.append(node.Stop_T[direction])
            
            offset = node.greenOffset
            if direction > 1:
                offset *= -1 # reverse the offset value because we are waiting for N or S light
            G_Offset.append(offset)
            gA = GeneticAlgorithm()
            gA.setVars(N ,D ,S , C, G_T ,R_T , G_Offset, motion, path)


    # now for each path we need to update the value based off the nodes list.


