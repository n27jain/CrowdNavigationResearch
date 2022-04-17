import imp
from posixpath import pathsep
from SavingMap import SavingMap
from MapObjects import *
from MapGenerator import *
from CreatePaths import *
from FindBestSpeed import *

# runCustom(5,5)

paths = setUpPaths(1, 3)

paths[0].printSelf()

solveThisPath(paths[0])
