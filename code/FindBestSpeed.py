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
        if edge.node1 == node1 and edge.node2 == node2:
            return edge
    return None

def test():
    SM = SavingMap()
    x,y,n = SM.open()
    e = x + y # all edges list
    nodes = []
    g_at_t0 = [0,0,0,0]
    Tg = [0,0,0,0]
    Tr = [0,0,0,0]
    Cycle = [0,0,0,0]

    # for node in n:
    #     print(str(node.x) + "," + str(node.y))
    #     if node.x == 0 and node.y == 1: # N
    #         nodes[0] = (node)
    #     elif node.x == 0 and node.y == 2: # E
    #         nodes[1] = (node)
    #     elif node.x == 5 and node.y == 2: # N
    #         nodes[2] = (node)
    #     elif node.x == 5 and node.y == 3:
    #         nodes[3] = (node)
    nodes.append(findNode((0,1), n)) # go North
    nodes.append(findNode((0,2), n)) # go East 
    nodes.append(findNode((5,2), n)) # go North
    nodes.append(findNode((5,3), n)) # Destination

    edges = []
    edges.append(findEdge((0,1),(0,2), e)) # go North
    edges.append(findEdge((0,2),(5,2), e)) # go East 
    edges.append(findEdge((5,2),(5,3), e)) # go North
    

    
    g_at_t0.append(node.isGreenAtT_0)
    Tg.append(node.Go_T)
    Tr.append(node.Stop_T)
    Cycle.append(node.cycletime)

    g_at_t0.append(node.isGreenAtT_0)
    Tg.append(node.Go_T)
    Tr.append(node.Stop_T)
    Cycle.append(node.cycletime)

    g_at_t0.append(node.isGreenAtT_0)
    Tg.append(node.Go_T)
    Tr.append(node.Stop_T)
    Cycle.append(node.cycletime)

    g_at_t0.append(node.isGreenAtT_0)
    Tg.append(node.Go_T)
    Tr.append(node.Stop_T)
    Cycle.append(node.cycletime)




    # print(node1.printSelf())
    # print(node2.printSelf())
    # print(node3.printSelf())
    # print(node4.printSelf())
    # print(x,y,n)

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
test()
#path()

