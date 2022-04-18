
from MapObjects import *
from MapGenerator import *
from CreatePaths import *
from FindBestSpeed import *

#runCustom(5,5)

#paths = setUpPaths(10, 3)
paths = getPathsFromSaveData()


# i = 0
# for path in paths:
#     paths[0].makeGraph("Path_" +str(i))
#     i +=1 

print("DONE")
solveThisPath(paths[0])

