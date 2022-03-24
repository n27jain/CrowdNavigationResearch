from pickletools import read_uint1
from platform import node
import random
from cv2 import add
import matplotlib.pyplot as plt
from scipy import rand
import pickle


class Map(object):
    def __init__(self, x_edges, y_edges, nodes):
        self.x_edges = x_edges
        self.y_edges = y_edges
        self.nodes = nodes




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

class SavingMap:
    def saveData(self,x,y,n):
        print("TRYING: to save data")
        with open('map_data.pkl', 'wb') as outp:
            map1 = Map(x,y,n)
            pickle.dump(map1,outp,pickle.HIGHEST_PROTOCOL)
    
    def open(self):
        print("TRYING: to get data")
        with open('map_data.pkl', 'rb') as inp:
            map1 = pickle.load(inp)
            print(map1.x_edges[0].node_1)
            return map1.x_edges, map1.y_edges , map1.nodes 


nodes  = []
edges =  []
for i in range(100):
    edge = Edge((0,0), (1,1), 100, 1)
    node = Node(0,0)
    node.east = edge

    nodes.append(node)
    edges.append(edge)


map = Map(edges, edges, nodes)

#Save the data
SM = SavingMap()
SM.saveData(edges, edges, nodes)

# now try and open it
x,y,n = SM.open()

for e in x:
    e.showEdge()
for e in y:
    e.showEdge()
for e in n:
    print(e.x)


