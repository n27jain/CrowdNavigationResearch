# given a map
# give a route
# we must minimize travel time by adjusting out speed
# Delay = time at traffic light + expect start up delay 
#Let’s assume that there is an additional penalty for stopping at a red light. There usually is a 2 second delay reaction before cars can reach the expected average speed of the coming road.

from time import time

from numpy import append
from mapGenerator import *
from MapObjects import *
from SavingMap import SavingMap

def doYouMakeIt(c, timeArrival, t_stop, t_go , onStartGreen):
    # 0 - stuck on light
    # 1 - green free to go
    if onStartGreen:
        if timeArrival < t_go:
            return 1
        else:
            A = timeArrival/c
            B = A * c
            if timeArrival <= B + t_go and timeArrival > B:
                return 1
            else:
                return 0

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

def createFile(edges,nodes):
    f = open("solve.txt",'w')
    f.write("____________________NODES:______________________")
    f.write("\n Pos |isGreen|   Go_T E,W,S,N     | Stop_T  |Cycle Times")
    f.write('\n')
    for node in nodes:
        f.write(node.printSelfClear())
        f.write("\n")
    f.write("____________________EDGES:______________________")
    f.write("\nPOINT1 |  POINT2 | D | S  | Direction | traffic_factor")
    for e in edges:
        f.write(e.printSelf())
        f.write("\n")

    
def test():
    SM = SavingMap()
    x,y,n = SM.open()
    e = x + y # all edges list
    nodes = []
    g_at_t0 = [0,0,0,0]
    Tg = [0,0,0,0]
    Tr = [0,0,0,0]
    Cycle = [0,0,0,0]
    nodes.append(findNode((0,1), n)) # go North
    nodes.append(findNode((0,2), n)) # go East 
    nodes.append(findNode((5,2), n)) # go North
    nodes.append(findNode((5,3), n)) # Destination

    edges = []
    edges.append(findEdge((0,1),(0,2), e)) # go North
    edges.append(findEdge((0,2),(5,2), e)) # go East 
    edges.append(findEdge((5,2),(5,3), e)) # go North
    createFile(edges, nodes)
    
    testNode = nodes[0]
    dangerousTest(testNode)
    # g_at_t0.append(node.isGreenAtT_0)
    # Tg.append(node.Go_T)
    # Tr.append(node.Stop_T)
    # Cycle.append(node.cycletime)

    # g_at_t0.append(node.isGreenAtT_0)
    # Tg.append(node.Go_T)
    # Tr.append(node.Stop_T)
    # Cycle.append(node.cycletime)

    # g_at_t0.append(node.isGreenAtT_0)
    # Tg.append(node.Go_T)
    # Tr.append(node.Stop_T)
    # Cycle.append(node.cycletime)

    # g_at_t0.append(node.isGreenAtT_0)
    # Tg.append(node.Go_T)
    # Tr.append(node.Stop_T)
    # Cycle.append(node.cycletime)


def path(nodes):
    # I am making a custom path for testing rn. 
    # This should be calculated by some kind of shortest path algorithm
    #(0,2) ->(0,4) -> (`4`,1)
    node1 =  None
    node2 =  None
    node3 =  None
    for node in nodes:
        if node.x == 2 and node.y == 3:
            node1 = node
        elif node.x == 4 and node.y == 3:
            node2 = node
        elif node.x == 4 and node.y == 1:
            node3 = node
    print(node1.printSelf())
    print(node2.printSelf())
    print(node3.printSelf())


def dangerousTest(node):
    node.setLightTimes()
    
test()


#path()

