
import random

from matplotlib import pyplot as plt
from scipy import rand


class Solution():
    def __init__(self, X, fitness,time):
        self.X = X
        self.fitness = fitness
        self.time = time


class Paths(object):
    def __init__(self, paths):
        self.paths = paths
    
class Map(object):
    def __init__(self, x_edges, y_edges, nodes):
        self.x_edges = x_edges
        self.y_edges = y_edges
        self.nodes = nodes

def findNode(coordinate, nodes):
    for node in nodes:
        if node.x == coordinate[0] and node.y == coordinate[1]: 
            return node
    return None
        
def gaussian():
    x = -1
    while(x < 0 or x > 1):
        x = random.gauss(0.5,1)
        if(x >= 0 and x <= 1):
            return x

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
        

        # these are edges
        self.east= None
        self.west = None
        self.south = None
        self.north = None

        self.cycletime = None
        self.isIsolated = False

    #average cycle time 30 to 120 seconds
    def yellowTime(self,incomingSpeed):
        if incomingSpeed < 35: return 3
        elif incomingSpeed < 40: return 3.5
        elif incomingSpeed < 50: return 4
        elif incomingSpeed < 60: return 4.5
        else: return 5

    def setLightTimes(self, random_genetic = False):
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

        self.Y_T[0] = max(self.Y_T[0], self.Y_T[1]) #E
        self.Y_T[1] = max(self.Y_T[0], self.Y_T[1]) #W
        self.Y_T[2] = max(self.Y_T[2], self.Y_T[3]) #S
        self.Y_T[3] = max(self.Y_T[2], self.Y_T[3]) #N

        # get the maximum time needed for yellow light
        self.cycletime = round(60 * gaussian() + 30, 0) # minimum of 30 seconds and maximum of 90 seconds

        e_w_y = self.Y_T[0]
        s_n_y = self.Y_T[2]
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

        if e_w_d == 0 and s_n_d == 0: # this node is isolated
            self.isIsolated = True
            return
        if e_w_d == 0 :
            # there is no x direction road
            # we need to set the cycle time to -1
            # this node is always green for y direction
            self.cycletime = -1
            self.Go_T[0] = -1
            self.Go_T[1] = -1
            self.Go_T[2] = 0
            self.Go_T[3] = 0
            return
        
        if random_genetic:
            e_w_percent_green = 0.2 + random.uniform(0,0.6)
        else:
            e_w_percent_green  =  e_w_d / (e_w_d + s_n_d)

       
        self.G_T[0] = self.cycletime * e_w_percent_green - e_w_y

        self.G_T[1] = self.G_T[0]
        self.R_T[0] = self.cycletime - self.G_T[0] - self.Y_T[0] 
        self.R_T[1] = self.R_T[0]
        
        self.G_T[2] = self.cycletime * (1 - e_w_percent_green) - s_n_d
        self.G_T[3] = self.G_T[2]
        self.R_T[2] = self.cycletime - self.G_T[2] - self.Y_T[2] 
        self.R_T[3] = self.R_T[2]

        if self.east: 
            self.Go_T[0] = self.G_T[0] + self.Y_T[0]
            self.Stop_T[0] = self.R_T[0] 
        if self.west: 
            self.Go_T[1] = self.G_T[1] + self.Y_T[1]
            self.Stop_T[1] = self.R_T[1] 
        if self.south: 
            self.Go_T[2] = self.G_T[2] + self.Y_T[2]
            self.Stop_T[2] = self.R_T[2] 
        if self.north: 
            self.Go_T[3] = self.G_T[3] + self.Y_T[3]
            self.Stop_T[3] = self.R_T[3]
            
        self.greenOffset =  random.randint(0,1) # this is for the X intersection. Opposite for the Y intersection
        if self.greenOffset == 0:
            self.greenOffset = 1
        else: self.greenOffset = -1 
        self.greenOffset = -1 * random.randint( 0,int( min( self.Go_T[0], self.Go_T[2] ) ) )
           
    def printSelf(self):
        
        out = "( " + str(self.x) + " " + str(self.y) + " )  |  " + str(self.greenOffset)+ " | " + str(self.Go_T) + " | " + str(self.Stop_T) + " | " + str(self.cycletime)
        if self.north:
            # out += "\n north  : "
            e = self.north.printSelf()
            out += "\n" 
            out = out + " N: " + e
        if self.east:
            # out += "\n east  : "
            e = self.east.printSelf()
            out += "\n" 
            out = out + " E: " + e
        if self.south:
            # out += "\n south  : "
            e = self.south.printSelf()
            out += "\n" 
            out = out + " S: " + e
        if self.west:
            # out += "\n west  : "
            e = self.west.printSelf()
            out += "\n" 
            out = out + " W: " + e
        return out

    def printSelfClear(self):
        out = "NODE: ( " + str(self.x) + " " + str(self.y) + " )  | \n "
        out += "    greenOffset : " + str(self.greenOffset)+ " | \n " 
        out += "    G_E: " + str(self.Go_T[0]) + " | \n" 
        out += "    G_W: " + str(self.Go_T[1]) + " | \n" 
        out += "    G_S: " + str(self.Go_T[2]) + " | \n" 
        out += "    G_N: " + str(self.Go_T[3]) + " | \n" 
        out += "    S_E: " + str(self.Stop_T[0]) + " | \n" 
        out += "    S_W: " + str(self.Stop_T[1]) + " | \n" 
        out += "    S_S: " + str(self.Stop_T[2]) + " | \n" 
        out += "    S_N: " + str(self.Stop_T[3]) + " | \n" 
        out += "    C: " + str(self.cycletime) + "\n"
        out += "_________Edges__________"
        if self.north:
            # out += "\n north  : "
            e = self.north.printSelf()
            out += "\n" + "    "
            out = out + " N: " + e
        if self.east:
            # out += "\n east  : "
            e = self.east.printSelf()
            out += "\n" + "    "
            out = out + " E: " + e
        if self.south:
            # out += "\n south  : "
            e = self.south.printSelf()
            out += "\n" + "    "
            out = out + " S: " + e
        if self.west:
            # out += "\n west  : "
            e = self.west.printSelf()
            out += "\n" + "    "
            out = out + " W: " + e
        return out 
    
    def printNodeExclusive(self):
        out = "NODE: ( " + str(self.x) + " " + str(self.y) + " )  | \n "
        out += "    greenOffset : " + str(self.greenOffset)+ " | \n " 
        out += "    G_E: " + str(self.Go_T[0]) + " | \n" 
        out += "    G_W: " + str(self.Go_T[1]) + " | \n" 
        out += "    G_S: " + str(self.Go_T[2]) + " | \n" 
        out += "    G_N: " + str(self.Go_T[3]) + " | \n" 
        out += "    S_E: " + str(self.Stop_T[0]) + " | \n" 
        out += "    S_W: " + str(self.Stop_T[1]) + " | \n" 
        out += "    S_S: " + str(self.Stop_T[2]) + " | \n" 
        out += "    S_N: " + str(self.Stop_T[3]) + " | \n" 
        out += "    C: " + str(self.cycletime) + "\n"
        return out
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
        self.traffic = gaussian() * random.randint(0,1) 

    def printSelf(self):
        #str(self.node_1) + " | " + str(self.node_2)+ " | " +
        out = " ( " + str(self.node_1[0]) + "," + str(self.node_1[1])+ " ) ---> " 
        out += " ( " + str(self.node_2[0]) + "," + str(self.node_2[1]) + " ) | "
        out += str(self.distance) + " | " 
        out += str(self.speed)+ " | "
        out += str(self.direction) + " | " 
        out += str(self.traffic)
        return out


class Path:
    def __init__(self, minSize):
        self.minSize = minSize
        self.nodes = []
        self.edges = []
        self.q_Seq = [] # quick sequence of coordinates travelled for testing purposes
        self.directions = [] 
        self.motion = []

        # motion
        # 0 - straight
        # 1 - right
        # 2 - left 
        # direction
        # 0 - East
        # 1 - West
        # 2 - South 
        # 3 - North

    def writeSelf(self):
        out = ("Size: " + str(self.minSize) + " \n")
        out += ("Nodes:  \n ")
        for node in self.nodes:
            out += (node.printSelf() + "\n")
        
        print("Edges:  \n ")
        for edge in self.edges:
            out += (edge.printSelf() + "\n")
        print("Motion:  \n ")
        for d in self.motion:
            if d == 0:
                out += ("straight \n")
            elif d == 1:
                 out += ("right \n")
            elif d == 2:
                 out += ("left \n")
            else:
                print("NONE \n")
        out += ("Directions:  \n ")
        for m in self.directions:
            if m == 0:
                 out += ("east \n")
            elif m == 1:
                 out += ("west \n")
            elif m == 2:
                 out += ("south \n")
            elif m == 3:
                 out += ("north \n")
            else:
                 out += ("NONE \n")
        return out

    def printSelf(self):
        print("Size: ",  self.minSize)
        print("Nodes:  \n ")
        for node in self.nodes:
            print (node.printSelf())
        
        print("Edges:  \n ")
        for edge in self.edges:
            print(edge.printSelf())
        print("Motion:  \n ")
        for d in self.motion:
            if d == 0:
                print("straight")
            elif d == 1:
                print("right")
            elif d == 2:
                print("left")
            else:
                print("NONE")
        print("Directions:  \n ")
        for m in self.directions:
            if m == 0:
                print("east")
            elif m == 1:
                print("west")
            elif m == 2:
                print("south")
            elif m == 3:
                print("north")
            else:
                print("NONE")
    def makeGraph(self, name, xmax = None, ymax =  None):
      
        x, y = zip(*self.q_Seq)
        plt.plot(x, y, '-o')
        if xmax != None :
            plt.axis([0,xmax, 0, ymax])
        plt.xlabel("East - West")
        plt.ylabel("South - North")
        plt.savefig(name + ".png")
        plt.close()
        
        print("DONE making path map")
