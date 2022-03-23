
import json
from pickletools import read_uint1
from platform import node
import random
from tkinter import N, W, X, Label
from cv2 import add
import matplotlib.pyplot as plt
from scipy import rand
import pickle
from SavingMap import SavingMap
#Grid  20 x 20 units That means potential for 400 nodes


f = open("Output.txt",'w')

w_grid = 5
h_grid = 5

map = None

class Map(object):
    def __init__(self, x_edges, y_edges, nodes):
        self.x_edges = x_edges
        self.y_edges = y_edges
        self.nodes = nodes

#Edges


# def loadMap():
#     with open('map_data.pkl', 'rb') as inp:
#         map = pickle.load(inp)
#         print(map.x_edges)
#         print(map.y_edges)
# def saveMap(x,y,nodes):
#     with open('map_data.pkl', 'wb') as outp:
#         map = Map(x,y,nodes)
#         pickle.dump(map, outp, pickle.HIGHEST_PROTOCOL)

def gaussian():
    x = -1
    while(x < 0 or x > 1):
        x = random.gauss(0.5,1)
        if(x >= 0 and x <= 1):
            return x

class Edge:
    def __init__(self, node_1, node_2, distance, direction):
        self.node_1 = node_1 # (x,y)
        self.node_2 = node_2 #(x,y)
        self.distance = distance # km
        self.speed = 10 * random.randint(0,5) + 30 # speeds from 30-80 km/h
        self.direction = direction # 0 - s_n or 1 - e_w

        #lets say that there is a 50% chance of any traffic being on any given road
        # and of the 50% the 
        #TODO: Figure out exactly how to distribute the traffic 
        self.traffic = gaussian()

    def printEdge(self):
        #str(self.node_1) + " | " + str(self.node_2)+ " | " +
        out = " ( " + str(self.node_1[0]) + "," + str(self.node_1[1])+ " ) ---> " 
        out += " ( " + str(self.node_2[0]) + "," + str(self.node_2[1]) + " ) | "
        out += str(self.distance) + " | " 
        out += str(self.speed)+ " | "
        out += str(self.direction) + " | " 
        out += str(self.traffic)
        f.write(out)
        f.write('\n')
        #return out
    def showEdge(self):
        out = " ( " + str(self.node_1[0]) + "," + str(self.node_1[1])+ " ) ---> " 
        out += " ( " + str(self.node_2[0]) + "," + str(self.node_2[1]) + " ) | "
        out += str(self.distance) + " | " 
        out += str(self.speed)+ " | "
        out += str(self.direction) + " | " 
        out += str(self.traffic)
        return out
class Node:
    #Typical cycle times - 30s to 120s.
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.R_T = [0,0,0,0]
        self.Y_T = [0,0,0,0]
        self.G_T = [0,0,0,0]
        self.Go_T = [0,0,0,0]
        self.Stop_T = [0,0,0,0]
        self.east= None
        self.west = None
        self.south = None
        self.north = None
        self.cycletime = None

    #average cycle time 30 to 120 seconds
    def yellowTime(self,incomingSpeed):
        if incomingSpeed < 35: return 3
        elif incomingSpeed < 40: return 3.5
        elif incomingSpeed < 50: return 4
        elif incomingSpeed < 60: return 4.5
        else: return 5

    def setLightTimes(self):
        #0,1 are east west
        #2,3 are south north
        #Assume equal time for opposite directions and 
        # Green side 1 + yellow side 1 = Red side 2
        if(self.east):
            self.Y_T[0] = self.yellowTime(self.east.speed)
        else: self.Y_T[0] = 0

        if(self.west):
            self.Y_T[1] = self.yellowTime(self.west.speed)
        else: self.Y_T[1] = 0


        if(self.south):
            self.Y_T[2] = self.yellowTime(self.south.speed)
        else: self.Y_T[2] = 0

        if(self.north):
            self.Y_T[3] = self.yellowTime(self.north.speed)
        else: self.Y_T[3] = 0

        self.Y_T[0] = max(self.Y_T[0], self.Y_T[1])
        self.Y_T[1] = max(self.Y_T[0], self.Y_T[1])
        self.Y_T[2] = max(self.Y_T[2], self.Y_T[3])
        self.Y_T[3] = max(self.Y_T[2], self.Y_T[3])

        self.cycletime = 60 * gaussian() + 30

        e_w_y = max(self.Y_T[0], self.Y_T[1])
        s_n_y = max(self.Y_T[2], self.Y_T[3])

        e_d = 0
        w_d = 0
        s_d = 0
        n_d = 0
        if self.east: e_d = self.east.distance
        if self.west: w_d = self.west.distance
        if self.south: s_d = self.south.distance
        if self.north: n_d = self.north.distance
        e_w_d = max(e_d, w_d)
        s_n_d = max(n_d, s_d)
        e_w_percent_green  = e_w_d / (e_w_d + s_n_d)

        timeleft = self.cycletime - e_w_y - s_n_y
        self.G_T[0] = timeleft * e_w_percent_green
        self.R_T[0] = self.cycletime - self.G_T[0] - self.Y_T[0] 
        self.R_T[2] = self.G_T[0] + self.Y_T[0]
        self.G_T[2] = self.cycletime - self.R_T[2] - self.Y_T[2] 

        self.G_T[1] = self.G_T[0]
        self.R_T[3] = self.R_T[2]
        self.G_T[1] = self.G_T[0]
        self.R_T[3] = self.R_T[2]


    def printSelf(self):
        
        out = "( " + str(self.x) + " " + str(self.y) + " )  " + str(self.R_T) + " " + str(self.Y_T) +" " + str(self.G_T) + " " +str(self.Go_T) +" " + str(self.Stop_T)
        if self.north:
            # out += "\n north  : "
            e = self.north.showEdge()
            out += "\n" 
            out = out + " N: " + e
        if self.east:
            # out += "\n east  : "
            e = self.east.showEdge()
            out += "\n" 
            out = out + " E: " + e
        if self.south:
            # out += "\n south  : "
            e = self.south.showEdge()
            out += "\n" 
            out = out + " S: " + e
        if self.west:
            # out += "\n west  : "
            e = self.west.showEdge()
            out += "\n" 
            out = out + " W: " + e
        f.write(out)
        f.write('\n')

        return out 



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
                l_node.west = edge
                node.east = edge
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
    

def createFile(x,y,nodes):

    print("doing this shit")
    #plt.plot(x_values, y_values)
    f.write("____________________NODES:______________________")

    f.write("\n Pos |R_T: E,W,S,N   |   Y_T   |     G_T    | Go_T    | Stop_T  |")
    f.write('\n')
    for node in nodes:
        node.printSelf()

    f.write("____________________EDGES:______________________")
    f.write("\n____________________South - North:______________________\n")
    f.write("\nPOINT1 |  POINT2 | D | S  | Direction | traffic_factor")
    for e in x:
        e.printEdge()
    f.write("\n____________________East - West:______________________\n")   
    f.write("\nPOINT1 |  POINT2 | D | S  | Direction | traffic_factor")
    for e in y:
        e.printEdge()

def setLights(nodes):
    for node in nodes:
        node.setLightTimes()




def run():        
    nodes = makeNodes(w_grid,h_grid)
    x_e, y_e, nodes = makeEdges(nodes)
    makeMap(x_e,y_e,nodes)
    # setLights(nodes)
    createFile(x_e,y_e,nodes=nodes)
    
    # mp = SavingMap()
    # mp.saveData(x_e,y_e,nodes)
    # i = x_e[0]
    # jsonStr = json.dumps(nodes[0].__dict__)
    # print(jsonStr)

# def seeData():
#     print("Lets try this thing")
#     mp = SavingMap()
#     x,y,n = mp.open()
#     print(x.node_1[0])
#     print(n)

run()
#seeData()
