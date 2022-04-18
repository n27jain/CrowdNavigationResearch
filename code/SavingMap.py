
import os
import pickle
from MapObjects import *

class Map(object):
    def __init__(self, x_edges, y_edges, nodes):
        self.x_edges = x_edges
        self.y_edges = y_edges
        self.nodes = nodes

class Paths(object):
    def __init__(self, paths):
        self.paths = paths



class SavingMap:

    def saveData(self,x,y,n):
        with open('map_data.pkl', 'wb') as outp:
            map1 = Map(x,y,n)
            pickle.dump(map1,outp,pickle.HIGHEST_PROTOCOL)

    def open(self):
        with open('map_data.pkl', 'rb') as inp:
            map1 = pickle.load(inp)
            return map1.x_edges, map1.y_edges , map1.nodes 
    
    def savePaths(self, paths):
        with open('path_data.pkl', 'wb') as outp:
            pickle.dump(paths,outp,pickle.HIGHEST_PROTOCOL)

    def openPaths(self):
        with open('path_data.pkl', 'rb') as inp:
            paths = pickle.load(inp)
            return paths 
