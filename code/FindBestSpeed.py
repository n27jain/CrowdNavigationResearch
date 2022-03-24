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
    f.write("\n")
    for e in edges:
        f.write(e.printSelf())
        f.write("\n")

def f(n,X,D,C,Tr,Tg, Rt_0): # n is size of edges
    t = 0
    Penalty = 1

    for i in range(n):
        t_t = t + D[i]/ X[i] # the temporary time to check
        if Rt_0[i] == 0:
            #case 1
            if t_t < Tg[0]: # move on to the next node
                t = t_t 
                continue
            else:
                A = t_t/C[i]
                B = A * C[i]
                if t_t < B:
                    t += B + Penalty
                elif t_t >= B + Tg[i]:
                    t += C[i] * (A + 1) + Penalty
                else:
                    #timeArrival <= B + t_go and timeArrival > B
                    # move on to the next node
                    t = t_t 
                    
        else:
            #case 2
            A = t_t/C[i]
            rightside = (A+1) * C[i]
            leftside = C[i] * A + Tr[i]
            if t_t <= leftside:
                t += (leftside + Penalty)
            elif t_t > rightside:
                t += ((C[i] * (A+1)) + Tr[i])
            else:
                t = t_t 
    return t


def prepareSolutions(S,n):
    # prepare an array SOL, with X solution lists
    # using the S array, find out the max speeds a driver can drive on each edge
    # Using S randomly select a speed (Rounded to a whole number)
    # check and make sure that the solution did not exist in pool, 


    
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
    nodes.append(findNode((0,3), n)) # go East 
    nodes.append(findNode((1,3), n)) # go North
    nodes.append(findNode((2,3), n)) # Destination

    edges = []
    edges.append(findEdge((0,1),(0,3), e)) # go North
    edges.append(findEdge((0,3),(1,3), e)) # go East 
    edges.append(findEdge((1,3),(2,3), e)) # go North
    createFile(edges, nodes)

    maxSpeeds = []
    for edge in edges:
        maxSpeeds.append(edge.speed * (1 - edge.traffic))
    
    for s in maxSpeeds:
        print(s)
    # testNode = nodes[0]
    # dangerousTest(testNode)
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

