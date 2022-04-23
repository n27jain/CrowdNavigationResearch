from hashlib import new
from operator import index
import random
import copy
from time import sleep
from turtle import getscreen

from MapObjects import *

import timeit

class GeneticAlgorithm:
    def __init__(self,population=50,generations = 150, pc = 0.6, pm =0.4):

        self.population = population
        self.generations = generations
        self.pc = pc
        self.pm = pm
        self.wage = 30.69
        self.wageValueFactor = 0.5
        self.fuelCost = 1.809 # dollars per liter
        self.chromosomes = []

        # N  = number of nodes
        # D =  distances array
        # S = max speed array
        # C = cycletimes at traffic lights array
        # Tg =  go time for traffic light
        # Tr = stop time for traffic light 
        # Rt_0 = green delay offset.
        self.N = None
        self.D = [] 
        self.C = []
        self.S = []
        self.R_T = []
        self.G_T = []
        self.G_Offset = []
        self.motion  = []

        self.baseX = [] # one array to contain a base solution,
        #  one value that contains the score, 
        #  one value that contains fitness
        #[  [x,x,x,x,] , time, fuel, score, fitness ]
        self.X = []
        self.worst = None

        self.totalFitness = 0
        self.path = None 

        self.listOfPastPathSolutions = {"key": [0,0]}
         #  "[x,x,x,x,]" , [time, fuel]

    def findPastSolIfExists(self, x):
         return self.listOfPastPathSolutions.get(str(x))
    
    def setVars(self, N , D , S , C , G_T , R_T , G_Offset, motion, path ):
        self.N = N
        self.D = D
        self.S = S
        self.C = C
        self.G_T = G_T
        self.R_T = R_T
        self.G_Offset = G_Offset
        self.motion  = motion
        self.path = path
    
    def getFuel(self, time):
        # input time in seconds
        return 1.89/3600 * time

    def f(self, x):
        # this is the function

    
        t_total = 0
        f_total = 0

        penalty = 5
        leftDelay = 5
        
        # node 1 is starting node.
        # if the light is red we must wait for green
        if self.G_Offset[0] > 0:
            # this is a green offset
            # wait time =  time stop -  offset
            wait_time  = self.R_T[0] - self.G_Offset[0] + penalty
            f_total += self.getFuel(wait_time)
            t_total += wait_time
    # else
        # otherwise proceed to the algorithmn as usual
        for i in range(0, len(self.D) ):
            if x[i] == 0: 
                x[i] = 0.1
            t_t = (self.D[i]/ x[i] * 1 * 60 * 60) #time taken on this edge
            
            if (i + 1 ) != len(self.D):
                motion_side = self.motion[i+1]
                if motion_side == 1:
                    # motion is right 
                    # no delay, concat travel time and move to the next edge
                    t_total += t_t
                    # f_total += self.getFuel(t_t)
                else:
                    # check to see if green or if red
                    # if green no delay move forward
                    # if red then wait until completion of time and then add a penalty 
                    # This is not the last edge to travel
                    offset  = self.G_Offset[i+1]
                    cur_GT  = self.G_T[i+1]
                    cur_TR  = self.R_T[i+1]
                    cur_C = self.C[i+1]
                    if cur_GT == 0: # this means we have a light free intersection 
                        #as there is no alternative direction at this node
                        t_total += t_t

                    elif offset <= 0: # we are at green t = 0
                        #extra delay for motion_side == 2 (left)

                        newTime = t_total + t_t
                        n = newTime // cur_C
                        lhs = n * cur_C +  offset
                        rhs = n * cur_C + offset + cur_GT

                        if newTime > rhs:
                            delay = cur_C * (n+1) + offset - newTime
                            f_total += self.getFuel(delay + penalty)
                            t_total = cur_C * (n+1) + offset + penalty

                        elif newTime <= lhs:
                            delay = lhs - newTime
                            f_total += self.getFuel(delay + penalty)
                            t_total = lhs + delay
                        
                        else:
                            # we got to a green light no delay no extra milage 
                            # extra milage for arriving at green light and not at end of red light
                            if motion_side == 2:
                                t_total += t_t 
                                t_total += leftDelay
                                f_total += self.getFuel(leftDelay)

                    elif offset > 0 : # we are at red t = 0

                        newTime = t_total + t_t
                        n = newTime // cur_C
                        lhs = -1 * offset + cur_TR + n * cur_C
                        rhs = -1 * offset + (n+1) * cur_C

                        if newTime <= lhs:
                            reachTime  = lhs
                            delay = reachTime - newTime
                            f_total += self.getFuel(delay + penalty)
                            t_total += reachTime + penalty

                        elif newTime > rhs:
                            newLhs  = -1 * offset + cur_TR + (n+1) * cur_C
                            delay =  newLhs - newTime
                            f_total += self.getFuel(delay + penalty)
                            t_total = newLhs + delay
                        else:
                            # no delay no extra milage
                            t_total += t_t
            else: # this is the last edge to travel. No need to check anything just 
                t_total += t_t
        return t_total, f_total
       
    def solveForEachX(self):
        self.baseX[1], self.baseX[2] = self.f(self.baseX[0])
        self.baseX[3] = self.getScore(self.baseX[1], self.baseX[2])
        for x in self.X:
            # check = self.findPastSolIfExists(x)
            # if check == None:
            #     x[1], x[2] = self.f(x[0])
            #     self.listOfPastPathSolutions.update( {str(x[0]): [x[1], x[2]]})
            # else:
            #     x[1] = check[0]
            #     x[2] = check[1]
            x[1], x[2] = self.f(x[0])
        for x in self.X:
            x[3] = self.getScore(x[1],x[2])

        self.X.append(copy.deepcopy(self.baseX))
        self.X = sorted(self.X, key=lambda sol: (sol[3]) )
        self.worst  = self.X[0][3]
        for x in self.X:
            x[3] -= self.worst
       
        self.X = sorted(self.X, key=lambda sol: (sol[3]) )
        self.convertToFitness()
        
        return


    def generateNewSol(self):
        solutions = []
        for i in range(self.population + 1): # we have an extra one for default route
            x = []
            for j in range(self.N):
                if i == 0:
                    x.append(round(self.S[j], 0))
                else:
                    if self.S[j] > 30:
                        x.append( random.randint(30, round(self.S[j], 0) ) )
                    elif self.S[j] <= 0: # there was an error in this path. go at a steady 0.1 km/h
                        x.append(0.1)
                    elif self.S[j] < 1:
                        x.append( round( random.uniform(0.1, self.S[j]) , 1 ) ) 
                    else:
                        x.append( round( random.uniform(0.1, self.S[j]) , 1 ) ) 

            
            save = [x, -1,-1,-1,-1] # the x solution and null values for the computations
            if i == 0 :
                self.baseX = save
            else:
                solutions.append(save)
        self.X = solutions

                            
    def getScore(self, T, F):
        t_0 = self.baseX[1]
        f_0 = self.baseX[2]
        delta_f =  f_0 - F
        delta_t = t_0 - T
        out = ( delta_f * self.fuelCost) + (self.wage * self.wageValueFactor *  delta_t)
        return out

    def convertToFitness(self):
        tF = 0 # total fitness
        total = 0
        for x in self.X:
            tF += x[3]
        for x in self.X:
            x[4] = x[3]/ tF
            total += x[4]
        self.totalFitness = tF
        self.X = sorted(self.X, key=lambda sol: (sol[4]) , reverse=True )

    def russianRoulette(self): 
        surviors = []

        # keep the best two based off relative fitness including the base solution
        
        surviors.append(copy.deepcopy(self.X[0]))
        surviors.append(copy.deepcopy(self.X[1]))
        
        for i in range(self.population - 2):
            # lets keep it significant by 5 decimal places since there are many possible ties at 
            # 4 decimal places
            # we should also not keep 1 as a possibly randomly generated number. 
            # from experimentation the sum of the surviors is arround 0.9999999999999996
            
            check = round(random.uniform(0, 0.99999999),8)
            concat  = 0
            for j in range(len(self.X)):
                concat += self.X[j][4]
                if concat >= check:
                    surviors.append(copy.deepcopy(self.X[j]))
                    break
        self.X = copy.deepcopy(surviors)

    def crossOver(self):
            # cross over chromosomes 
            # exclude the 2 fittest solutions
            # crossover produces 2 childern who switch their chromosome values at a pivot point
           
            index_swap = []
            cloneList  = copy.deepcopy(self.X)
            index_A = None
            index_B = None
           
            for i in range(2,self.population):

                check = round(random.uniform(0,1),2) #TODO: fix for more nodes

                if check <= self.pc: #this chromosome needs to be crossed over 
                    index_swap.append(i)
        
            if(len(index_swap) <= 1): 
                # only one chromosome to cross over
                #hence do nothing and let the solutions remain the same
                return 

            for j in range(len(index_swap)):
                if j == (len(index_swap)-1): # last element must cross over with the first 
                  
                    index_A = index_swap[j]
                    index_B = index_swap[0]
                else:
                    index_A = index_swap[j]
                    index_B = index_swap[j+1]
                
                crossOverPoint = int(round(random.uniform(1,len(self.X[0][0]) - 1),0))
                
                for k in range(len(self.X[0][0])):
                    if k >= crossOverPoint:
                        cloneList[index_A][0][k] = cloneList[index_B][0][k]
            self.X = copy.deepcopy(cloneList)
    

    def mutation(self):
        # for each chromosome (excluding the 2 best fit pair) run a randome number generator 
        # if the number is less than the ratio then randomly select a speed value.
        # do this for each speed value in a solution X
        # return the children 
        clone = copy.deepcopy(self.X)
        for i in range(2,self.population):
            for j in range(len(self.X[0][0])):
                check = round(random.uniform(0,1),2) 
                if check <= self.pm:

                    if self.S[j] > 30:
                         clone[i][0][j] =  random.randint(30, round(self.S[j], 0) ) 
                    elif self.S[j] <= 0: # there was an error in this path. go at a steady 0.1 km/h
                        clone[i][0][j] = 0.1
                    elif self.S[j] < 1:
                        clone[i][0][j] = round( random.uniform(0.1, self.S[j]) , 1 ) 
                    else:
                        clone[i][0][j] = round( random.uniform(0.1, self.S[j]) , 1 ) 
        self.X = copy.deepcopy(clone)
    
    
    
    def run(self):
        self.generateNewSol() #create 50 random solutions to begin with
        bestSolutions = []
        for i in range(self.generations):
            self.solveForEachX()
            bestSolutions.append(self.X[0])
            self.russianRoulette()
            self.crossOver()
            self.mutation()
        
        return self.baseX , bestSolutions
        

        


class GeneticAlgorithmnAdaptive:
    def __init__(self,population=50,generations = 50, pc = 0.6, pm =0.4):
        self.population = population
        self.generations = generations
        self.pc = pc
        self.pm = pm
        self.wage = 30.69
        self.wageValueFactor = 0.5
        self.fuelCost = 1.809 # dollars per liter
        self.numberTravellersArray = [10,5,5,1,1,1,1,1,]
        
        self.nodesChromosomes = [] # <list> of nodes, scoresum of paths, scoresum of path's fuel consumption
        
        self.baseChromosome = [None,-1,-1,-1,-1] # <list> of nodes, scoresum of paths trip time, scoresum of path's fuel consumption
        self.baseSolutionFound  = False

        self.paths = [] # a list of <path>
        self.bestPathsSol = [] # generation #, solution

        #self.listOfPastPathSolutions = {"key": [0,0]} # key string value deterived from converting a solution array to a string i.e str([n1,n2,n3,..ni])
        # Array value is total time and total fuel .

    def f(self, chromosome):
        # provided the chromosome for the nodes
        # for each path find the best solution
        # then muliply the path solution by the number of travellers
        # store the best solutions for each path
        # sum up their results 
        # return


        total_time = 0
        total_fuel = 0
        q = 0
        for path in self.paths:
            N = len(path.edges)
            D = []
            S = []
            C = []
            G_T = []
            R_T = []
            G_Offset = []
            motion = path.motion
            for edge in path.edges:
                D.append(edge.distance)
                S.append(edge.speed * (1 - edge.traffic))
            
            for i in range( 0,len(path.nodes) - 1 ): # we can ignore the last light as it is the destination
                searchNode = path.nodes[i]
                node = findNode((searchNode.x, searchNode.y), chromosome[0])
                direction = path.directions[i+1]
                C.append(node.cycletime)
                G_T.append(node.Go_T[direction])
                R_T.append(node.Stop_T[direction])
                
                offset = node.greenOffset
                if direction > 1:
                    offset *= -1 # reverse the offset value because we are waiting for N or S light
                G_Offset.append(offset)

            gA = GeneticAlgorithm(generations=50) # reduce the computational time by a factor of 1/3
            gA.setVars(N ,D ,S , C, G_T ,R_T , G_Offset, motion, path)
            basePath , bestSol = gA.run()
            time =  bestSol[-1][1]
            fuel = bestSol[-1][2]
            total_time += (time * self.numberTravellersArray[q])
            total_fuel += (fuel* self.numberTravellersArray[q])
            q += 1
        return total_time, total_fuel
       
    def generateNewSol(self):
        # call setLightTimes(random_genetic = True) for each node in the node list
        # create an array of these nodes.
        # do this the # of population
        # store them in a biggerList
        listOfNodesList = []
        nodesList = []

        for i in range(self.population):
            nodesList = []
            for node in self.baseChromosome[0]:
                newNode  = copy.deepcopy(node)
                newNode.setLightTimes(random_genetic = True)
                nodesList.append(newNode)
            save = [nodesList,-1,-1,-1,-1]
            listOfNodesList.append(save)
        self.nodesChromosomes = listOfNodesList
        return

    def getScore(self,T,F):
        t_0 = self.baseChromosome[1]
        f_0 = self.baseChromosome[2]
        delta_f =  f_0 - F
        delta_t = t_0 - T
        out = ( delta_f * self.fuelCost) + (self.wage * self.wageValueFactor *  delta_t)
        return out

    def convertToFitness(self):
        tF = 0 # total fitness
        total = 0
        for chrome in self.nodesChromosomes:
            tF += chrome[3]
        for chrome in self.nodesChromosomes:
            chrome[4] = chrome[3]/ tF
            total += chrome[4]
        self.nodesChromosomes = sorted(self.nodesChromosomes, key=lambda sol: (sol[4]) , reverse=True )

    
    def solveForEachY(self):
        # solve for the base case first
        if not self.baseSolutionFound:
            time, fuel = self.f(self.baseChromosome)
            self.baseChromosome[1] = time
            self.baseChromosome[2] = fuel
            self.baseChromosome[3] = self.getScore(time,fuel)
            self.baseSolutionFound =  True
        # Then for each nodesList in  nodesChromosomes 
        # run then function and get back the results for each path
        # multiply the results of the path with its number of travellers
        # sum the solutions

        for chrome in self.nodesChromosomes:
            time, fuel = self.f(chrome)
            chrome[1] = time
            chrome[2] = fuel
            chrome[3] = self.getScore(time,fuel)
        self.nodesChromosomes.append(copy.deepcopy(self.baseChromosome))
        self.nodesChromosomes = sorted(self.nodesChromosomes, key=lambda sol: (sol[3]))
        worst = self.nodesChromosomes[0][3]
        for sol in self.nodesChromosomes:
            sol[3] -= worst
        self.nodesChromosomes = sorted(self.nodesChromosomes, key=lambda sol: (sol[3]))
        self.convertToFitness()
        return

    def russianRoulette(self):
        surviors = []
        surviors.append(copy.deepcopy(self.nodesChromosomes[0]))
        surviors.append(copy.deepcopy(self.nodesChromosomes[1]))
        for i in range(self.population -2):
            check = round(random.uniform(0, 0.99999999),8)
            concat  = 0
            for j in range(len(self.nodesChromosomes)):
                concat += self.nodesChromosomes[j][4]
                if concat >= check:
                    surviors.append(copy.deepcopy(self.nodesChromosomes[j]))
                    break
        self.nodesChromosomes = copy.deepcopy(surviors)
        return
    
    def crossOver(self):
            # cross over chromosomes 
            # exclude the 2 fittest solutions
            # crossover produces 2 childern who switch their chromosome values at a pivot point
           
            index_swap = []
            cloneList  = copy.deepcopy(self.nodesChromosomes)
            index_A = None
            index_B = None
           
            for i in range(2,self.population):

                check = round(random.uniform(0,1),2) 

                if check <= self.pc: #this chromosome needs to be crossed over 
                    index_swap.append(i)
        
            if(len(index_swap) <= 1): 
                # only one chromosome to cross over
                #hence do nothing and let the solutions remain the same
                return 

            for j in range(len(index_swap)):
                if j == (len(index_swap)-1): # last element must cross over with the first 
                  
                    index_A = index_swap[j]
                    index_B = index_swap[0]
                else:
                    index_A = index_swap[j]
                    index_B = index_swap[j+1]
                
                crossOverPoint = int(round(random.uniform(1,len(self.nodesChromosomes[0][0]) - 1),0))
                
                for k in range(len(self.nodesChromosomes[0][0])):
                    if k >= crossOverPoint:
                        cloneList[index_A][0][k] = cloneList[index_B][0][k]
            self.nodesChromosomes = copy.deepcopy(cloneList)
    
    def mutation(self):
        # for each chromosome (excluding the 2 best fit pair) run a randome number generator 
        # if the number is less than the ratio then randomly select a speed value.
        # do this for each speed value in a solution X
        # return the children 
        clone = copy.deepcopy(self.nodesChromosomes)
        for i in range(2,self.population):
            for j in range(len(self.nodesChromosomes[0][0])):
                check = round(random.uniform(0,1),2) 
                if check <= self.pm:
                    # now we need to mutate the node
                    clone[i][0][j].setLightTimes(random_genetic = True)
        self.nodesChromosomes = copy.deepcopy(clone)
    


    def run(self):
        start = timeit.default_timer()
        self.generateNewSol()
        bestSolutions = []
        printedBool = False
        for i in range(self.generations):
            startRun = timeit.default_timer()
            if(i >= (self.generations // 2) and printedBool == False ):
                printedBool = True
                print("We are halfway there!")

            self.solveForEachY()
            bestSolutions.append(self.nodesChromosomes[0])
            self.russianRoulette()
            self.crossOver()
            self.mutation()
            print("Run Complete: ", timeit.default_timer() - startRun)
        stop = timeit.default_timer()
        print("Adaptive GA SIM TIME: ", stop-start)
        return self.baseChromosome , bestSolutions

