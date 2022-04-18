# given a map
# give a route
# we must minimize travel time by adjusting out speed
# Delay = time at traffic light + expect start up delay 
#Let’s assume that there is an additional penalty for stopping at a red light. There usually is a 2 second delay reaction before cars can reach the expected average speed of the coming road.

from itertools import cycle
from time import time

from numpy import append
from MapGenerator import *
from MapObjects import *
from SavingMap import SavingMap
from FixedGeneticAlgorithm import GeneticAlgorithm



def findNode(coordinate, nodes):
    for node in nodes:
        if node.x == coordinate[0] and node.y == coordinate[1]: 
            return node
    return None

def findEdge(node1, node2, edges):
    for edge in edges:
        if edge.node_1 == node1 and edge.node_2 == node2:
            return edge
    return None

def createFile(edges,nodes, path):
    f = open("solve.txt",'w')
    f.write("____________________NODES:______________________")
    f.write("\n Pos |isGreen|   Go_T E,W,S,N     | Stop_T  |Cycle Times")
    f.write('\n')
    for node in nodes:
        f.write(node.printSelfClear())
        f.write("\n")
    f.write("____________________EDGES:______________________")
    f.write("\nPOINT1 |  POINT2 | D | S  | Direction | traffic_factor")
    f.write("\n")
    for e in edges:
        f.write(e.printSelf())
        f.write("\n")

    f.write("_________IMPORTANT DATA ____________")

    for i in range(len(edges)):
        f.write("\n")
        f.write("__EDGE__ "+ str(edges[i].node_1) + str(edges[i].node_2))
        f.write("\n")
        f.write("D: "+ str(edges[i].distance))
        f.write("\n")

        f.write("S: "+ str(edges[i].speed * (1 - edges[i].traffic)))
        f.write("\n")

        f.write("C: "+ str(nodes[i+1].cycletime))
        f.write("\n")

        f.write("Tg: "+ str(nodes[i+1].Go_T[path[i]]))
        f.write("\n")

        f.write("Tr: "+ str(nodes[i+1].Stop_T[path[i]]))
        f.write("\n")
        
        if (path[i] == 0 or path[i] == 1):

            f.write("Rt_0: " + str(nodes[i+1].greenOffset) )
            f.write("\n")
           
        else:
            if nodes[i+1].greenOffset >= 0 :
                f.write("Rt_0: 0 ")
                f.write("\n")
                
            else:
                f.write("Rt_0: 1 ")
                f.write("\n")
      




def prepareSolutions(S,n):
    # prepare an array SOL, with X solution lists
    # using the S array, find out the max speeds a driver can drive on each edge
    # Using S randomly select a speed (Rounded to a whole number)
    # check and make sure that the solution did not exist in pool, 
    return
def directionsToData(start_pos, directions):
    # node stat =  start_pos
    # get edge from start_pos and directions
    # no
    return
    
def setUp():

    # normally we ignore the traffic light when we take a right turn (possible 1 second delay)
    # so for now we will combine right turns with the next node upgrade.
    
    SM = SavingMap()
    x,y,n = SM.open()
    e = x + y # all edges list
    nodes = []
    Tg = []
    Tr = []
    C = []
    edges = []
    S =[]
    D =[]
    Rt_0 = []
    path = [] #  ~ E,E,E,E
    # Example 1 : all going straight
    # nodes.append(findNode((0,1), n)) # Start go North
    nodes.append(findNode((0,3), n)) # go East
    edges.append(findEdge((0,3),(1,3), e)) 
    path.append(0)
    nodes.append(findNode((1,3), n)) # go East
    edges.append(findEdge((1,3),(2,3), e))
    path.append(0)
    nodes.append(findNode((2,3), n)) # go East 
    edges.append(findEdge((2,3),(4,3), e)) 
    path.append(0)
    nodes.append(findNode((4,3), n)) # go East - > Destination
    createFile(edges, nodes, path)
    

   
    for i in range(len(edges)):
        D.append(edges[i].distance)
        S.append(edges[i].speed * (1 - edges[i].traffic))
        C.append(nodes[i+1].cycletime)
        Tg.append(nodes[i+1].Go_T[path[i]])
        Tr.append(nodes[i+1].Stop_T[path[i]])
        if (path[i] == 0 or path[i] == 1):
            Rt_0.append(nodes[i+1].greenOffset)
        else:
            if nodes[i+1].isGreenAtT_0 == 1:
                Rt_0.append(0)
            else:
                Rt_0.append(1)
    
    gA = GeneticAlgorithm()
    gA.setVars(len(edges),D,C,Tr,Tg, Rt_0, S)
    gA.runSolver()



def solveThisPath(path):
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
        # TODO: path has edges that are not complete. Missing speed limit change
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

    gA = GeneticAlgorithm()
    gA.setVars(N ,D ,S , C, G_T ,R_T , G_Offset, motion, path)
    gA.run()
    # print("path.q_Seq" , path.q_Seq)

    # print( "N:" , N)
    # print( "D:" , D)
    # print( "S:" , S)
    # print( "C:" , C)
    # print( "G_T:" , G_T)
    # print( "R_T:" , R_T)
    # print( "G_Offset:" , G_Offset)
    


    # print( "solX:" , solX)
    # print( "time:" , time)
    # print( "fuel:" , fuel)
    # return time, fuel
    

