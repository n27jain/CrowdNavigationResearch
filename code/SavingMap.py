
import pickle

f = open("Output.txt",'w')
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
        out = " ( " + str(self.node_1.x) + "," + str(self.node_1.y)+ " ) | " 
        out += " ( " + str(self.node_2.x) + "," + str(self.node_2.y) + " ) | "
        out += str(self.distance) + " | " 
        out += str(self.speed)+ " | "
        out += str(self.direction) + " | " 
        out += str(self.traffic)
        f.write(out)
        f.write('\n')
        #return out
    def showEdge(self):
        out = " ( " + str(self.node_1.x) + "," + str(self.node_1.y)+ " ) | " 
        out += " ( " + str(self.node_2.x) + "," + str(self.node_2.y) + " ) | "
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

class MapObj(object):
        def __init__(self, x_edges, y_edges, nodes):
            self.x_edges = x_edges
            self.y_edges = y_edges
            self.nodes = nodes

class SavingMap:
    def saveData(self,x,y,n):
        print("TRYING: to save data")
        with open('map_data.pkl', 'wb') as outp:
            map1 = MapObj(x,y,n)
            pickle.dump(map1,outp,pickle.HIGHEST_PROTOCOL)
    
    def open(self):
        print("TRYING: to get data")
        with open('map_data.pkl', 'rb') as inp:
            map1 = pickle.load(inp)
            return map1.x_edges, map1.y_edges , map1.nodes 