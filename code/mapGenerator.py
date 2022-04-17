
from http.client import IM_USED
import json
from pickletools import read_uint1
from platform import node
import random
from tkinter import N, W, X, Label
from cv2 import add
import matplotlib.pyplot as plt
from scipy import rand
from SavingMap import SavingMap
#Grid  20 x 20 units That means potential for 400 nodes
from MapObjects import *

    


w_grid = 7
h_grid = 7

map = None

# Nodes
# Contain X Y position
# lets make 100 nodes
def makeNodes(w,h):
    num_nodes =  w*h * 0.5
    nodes = set()
    checkExists  = set ()
    while len(nodes) < num_nodes:
        x = random.randint(0,w_grid)
        y = random.randint(0,h_grid)
        #check and see if it exists in collection, if not then ignore
        if  not ((x,y) in checkExists):
            nodes.add(Node(x,y))
            checkExists.add((x,y))
    return sorted(nodes,key=lambda node: (node.x, node.y))


def makeEdges(nodes):
    #using only the co

    x_e = []
    sortedNodes = sorted(nodes,key=lambda node: (node.x, node.y))
    lastNodes = []

    for node in sortedNodes:
        thisX = node.x
        if(len(lastNodes) > 0 ):
            l_node = lastNodes.pop(-1)
            lastX = l_node.x
            if thisX == lastX:
                d =  node.y - l_node.y
                edge = edge = Edge((l_node.x,l_node.y), (node.x,node.y), d, 0 )
                x_e.append(edge)
                l_node.north = edge
                node.south = edge
               
                lastNodes.append(l_node) 
                lastNodes.append(node) 
            else:
                lastNodes.append(l_node)
                lastNodes.append(node) 
        else:
            lastNodes.append(node)

    y_e = []
    sortedNodes = sorted(lastNodes,key=lambda node: (node.y, node.x))
    lastNodes = []


    for node in sortedNodes:
        thisY = node.y
        if(len(lastNodes) > 0 ):
            l_node = lastNodes.pop(-1)
            lastY = l_node.y
            if thisY == lastY:
                d =  node.x - l_node.x
                edge = edge = Edge((l_node.x,l_node.y), (node.x,node.y), d, 1 )
                y_e.append(edge)
                l_node.east = edge
                node.west = edge
                lastNodes.append(l_node) 
                lastNodes.append(node) 
            else:
                #add it back because it doesnt need to be updated
                lastNodes.append(l_node)
                lastNodes.append(node) 
        else:
            lastNodes.append(node)

        sortedNodes = sorted(lastNodes,key=lambda node: (node.x, node.y))
    return x_e, y_e, sortedNodes
   

def makeMap(x_edges, y_edges, nodes ):
    t_val = []
    for edge in x_edges:
        p1 = edge.node_1
        p2 = edge.node_2
        x_val = [p1[0],p2[0]]
        y_val = [p1[1],p2[1]]
        label = " S: " + str(edge.speed) + " " + "D: " + str(edge.distance)
        plt.plot(x_val, y_val, label= label)
        
    for edge in y_edges:
        p1 = edge.node_1
        p2 = edge.node_2
        x_val = [p1[0],p2[0]]
        y_val = [p1[1],p2[1]]
        label = " S: " + str(edge.speed) + " " + "D: " + str(edge.distance)
        plt.plot(x_val, y_val, label= label)


    plt.xlabel("East - West")
    plt.ylabel("South - North")
    plt.savefig('map.png')
    plt.close()
    
def createFile(x,y,nodes):
    f = open("output.txt",'w')
    #plt.plot(x_values, y_values)
    f.write("____________________NODES:______________________")

    f.write("\n Pos |eastGreenOffset|   Go_T E,W,S,N     | Stop_T  |Cycle Times")
    f.write('\n')
    for node in nodes:
        f.write(node.printSelf())
        f.write("\n")
    f.write("____________________EDGES:______________________")
    f.write("\n____________________South - North:______________________\n")
    f.write("\nPOINT1 |  POINT2 | D | S  | Direction | traffic_factor")
    for e in x:
        f.write(e.printSelf())
        f.write("\n")
    f.write("\n____________________East - West:______________________\n")   
    f.write("\nPOINT1 |  POINT2 | D | S  | Direction | traffic_factor")
    for e in y:
        f.write(e.printSelf())
        f.write("\n")

def setLights(nodes):
    for node in nodes:
        node.setLightTimes()


def run():        
    nodes = makeNodes(w_grid,h_grid)
    x_e, y_e, nodes = makeEdges(nodes)
    makeMap(x_e,y_e,nodes)
    setLights(nodes)
    createFile(x_e,y_e,nodes=nodes)
    SM = SavingMap()
    SM.saveData(x_e,y_e,nodes)
    
    # i = x_e[0]
    # jsonStr = json.dumps(nodes[0].__dict__)
    # print(jsonStr)





def runCustom(g_w, g_h,filename = None):
    nodes = makeNodes(g_w,g_h)
    x_e, y_e, nodes = makeEdges(nodes)
    makeMap(x_e,y_e,nodes)
    setLights(nodes)
    createFile(x_e,y_e,nodes=nodes)
    SM = SavingMap()
    SM.saveData(x_e,y_e,nodes)

def seeData():
    SM = SavingMap()
    x,y,n = SM.open()
    # createFile(x,y,n)
    # print(x,y,n)
    return x,y,n

# run()
# x,y,n = seeData()

# for node in n :
#     print(node.printSelf())
