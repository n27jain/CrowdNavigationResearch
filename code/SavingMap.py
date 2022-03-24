
import pickle


class Map(object):
    def __init__(self, x_edges, y_edges, nodes):
        self.x_edges = x_edges
        self.y_edges = y_edges
        self.nodes = nodes

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
           
            return map1.x_edges, map1.y_edges , map1.nodes 
