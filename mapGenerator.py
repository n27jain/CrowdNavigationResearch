
from pickletools import read_uint1
from platform import node
import random
from tkinter import X, Label
import matplotlib.pyplot as plt
from scipy import rand

#Grid  20 x 20 units That means potential for 400 nodes


f = open("Output.txt",'w')

w_grid = 7
h_grid = 7

#Edges


def gaussian():
    x = -1
    while(x < 0 or x > 1):
        x = random.gauss(0.5,0.5/3)
        if(x >= 0 and x <= 1):
            return x

class Edge:
    def __init__(self, node_1, node_2, distance, direction):
        self.node_1 = node_1 # (x,y)
        self.node_2 = node_2 #(x,y)
        self.distance = distance # km
        self.speed = 10 * random.randint(0,5) + 30 # speeds from 30-80 km/h
        self.direction = direction # 0 - X or 1 - Y

        #lets say that there is a 50% chance of any traffic being on any given road
        # and of the 50% the 
        #TODO: Figure out exactly how to distribute the traffic 
        self.traffic = gaussian()

    def printEdge(self):
        out = str(self.node_1) + " | " + str(self.node_2)+ " | " + str(self.distance)+ " | " + str(self.speed)+ " | "+ str(self.direction) 
        f.write(out)
        f.write('\n')

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

    #average cycle time 30 to 120 seconds
    def yellowTime(incomingSpeed):
        if incomingSpeed < 35: return 3
        elif incomingSpeed < 40: return 3.5
        elif incomingSpeed < 50: return 4
        elif incomingSpeed < 60: return 4.5
        else: return 5

    def setLightTimes(self,east,west,south,north):
        #0,1 are east west
        #2,3 are south north
        #Assume equal time for opposite directions and 
        # Green side 1 + yellow side 1 = Red side 2

        self.Y_T[0] = self.yellowTime(east.speed)
        self.Y_T[1] = self.yellowTime(west.speed)

        self.Y_T[0] = max(self.Y_T[0], self.Y_T[1])
        self.Y_T[1] = max(self.Y_T[0], self.Y_T[1])

        self.Y_T[2] = self.yellowTime(south.speed)
        self.Y_T[3] = self.yellowTime(north.speed)

        self.Y_T[2] = max(self.Y_T[2], self.Y_T[3])
        self.Y_T[3] = max(self.Y_T[2], self.Y_T[3])


        cycletime = 60 * gaussian() + 30

        e_w_y = max(self.Y_T[0], self.Y_T[1])
        s_n_y = max(self.Y_T[2], self.Y_T[3])
        e_w_d = east.distance + west.distance
        s_n_d = north.distance + south.distance
        e_w_percent_green  = e_w_d / (e_w_d + s_n_d)

        timeleft = cycletime - e_w_y - s_n_y
        self.G_T[0] = timeleft * e_w_percent_green
        self.R_T[0] = cycletime - self.G_T[0] - self.Y_T[0] 
        self.R_T[2] = self.G_T[0] + self.Y_T[0]
        self.G_T[2] = cycletime - self.R_T[2] - self.Y_T[2] 

        self.G_T[1] = self.G_T[0]
        self.R_T[3] = self.R_T[2]
        self.G_T[1] = self.G_T[0]
        self.R_T[3] = self.R_T[2]


    def printSelf(self):
        out = self.x + self.y + self.R_T




# Nodes
# Contain X Y position
# lets make 100 nodes


def makeNodes(w,h):
    num_nodes =  w*h * 0.5
    nodes = set()
    while len(nodes) < num_nodes:
        #random X location
        x = random.randint(0,w_grid)
        #random Y location
        y = random.randint(0,h_grid)
        #check and see if it exists in collection, if not then ignore
        nodes.add((x,y))
    return nodes

#print(nodes)


def makeEdges(nodes):
    newNodes = set()
    # S-> N
    x_edges = set()
    nodes = sorted(nodes,
        key=lambda element: (element[0], element[1]))

    lastNode = None
    lastNodeX = None
    for node in nodes:
        thisX = node[0]
        if lastNodeX == thisX:
            dis = node[1] - lastNode[1]
            node1 = Node(node[0], node[1])

            #speed = random.randint(30,80) # 30 - 80 km/h 
            edge = Edge(lastNode,node, dis, 0 )

            # print(lastNode,node, dis, speed, 0)
            x_edges.add(edge)
        lastNode = node
        lastNodeX = thisX

    y_edges = set()
    n_nodes = sorted(nodes,
    key=lambda element: (element[1], element[0]))
    lastNode = None
    lastNodeY = None
    for node in n_nodes:
        thisY = node[1]
        if lastNodeY == thisY:
            dis = node[0] - lastNode[0]
            speed = random.randint(30,80) # 30 - 80 km/h 
            edge = Edge(lastNode, node, dis,0 )

            # print(lastNode,node, dis, speed, 0)
            y_edges.add(edge)
            #print(edge)
        lastNode = node
        lastNodeY = thisY
    return x_edges, y_edges


def createFile(x,y,nodes):
    #plt.plot(x_values, y_values)
    f.write("S_N_EDGES: \n")
    f.write("NODE 1| NODE 2  | D | S | Dir| ")
    f.write('\n')
    for edge in x: 
        edge.printEdge()

    f.write("E_W_EDGES: \n ")
    f.write("NODE 1| NODE 2  | D | S | Dir| ")
    f.write('\n')
    for edge in y:
        edge.printEdge()

def makeMap(x_edges, y_edges, nodes ):
    t_val = []
    for edge in x_edges:
        p1 = edge.node_1
        p2 = edge.node_2
        x_val = [p1[0],p2[0]]
        y_val = [p1[1],p2[1]]
        label = " S: " + str(edge.speed) + " " + "D: " + str(edge.distance)
        
        plt.plot(x_val, y_val,label=label)
        
    for edge in y_edges:
        p1 = edge.node_1
        p2 = edge.node_2
        x_val = [p1[0],p2[0]]
        y_val = [p1[1],p2[1]]
        label = " S: " + str(edge.speed) + " " + "D: " + str(edge.distance)
        plt.plot(x_val, y_val, label= label)
    #plt.xlim([0, w_grid+10])
    #plt.ylim([0, h_grid+10])
    #plt.legend()
    for node in nodes:
        # print(node)
        plt.plot(node[0],node[1])

    plt.xlabel("East - West")
    plt.ylabel("South - North")
    plt.savefig('map.png')
    


nodes = makeNodes(w_grid,h_grid)
x_e, y_e = makeEdges(nodes)

createFile(x_e,y_e,nodes)

# makeMap(x_e, y_e, nodes)

l = []
for i in range(100):
    x = -1
    while(x < 0 or x > 1):
        x = random.gauss(0.5,10)
        if(x >= 0 and x <= 1):
            l.append((x))
        # plt.plot(i,x)
    

# plt.show()



nodes = sorted(l)

print(nodes)