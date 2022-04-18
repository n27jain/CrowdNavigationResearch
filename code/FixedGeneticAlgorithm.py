from hashlib import new
from operator import index
import random
import copy
from time import sleep
from turtle import getscreen

from MapObjects import *



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
        # 5 seconds for waiting on a red light 
        left_penalty = 5 
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
                        n = round(newTime / cur_C,0)
                        lhs = n * cur_C +  offset
                        rhs = n * cur_C + offset + cur_GT

                        if newTime > rhs:
                            delay = cur_C * (n+1) + offset - t_t
                            f_total += self.getFuel(delay + penalty)
                            t_total += cur_C * (n+1) + offset + 5

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
                        n = round(newTime / cur_C, 0)
                        lhs = -1 * offset + cur_TR + n * cur_C
                        rhs = -1 * offset + (n+1) * cur_C
                        if newTime <= lhs:
                            reachTime  = n *  cur_C +cur_TR - offset +1
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
        for x in self.X:
            x[1], x[2] = self.f(x[0])

        self.baseX[3] = self.getScore(self.baseX[1], self.baseX[2])

        for x in self.X:
            x[3] = self.getScore(x[1],x[2])
        self.X = sorted(self.X, key=lambda sol: (sol[3]) )
        self.worst  = self.X[0][3]
        for x in self.X:
            x[3] -= self.worst
        self.baseX[3] -= self.worst
        self.X.append(copy.deepcopy(self.baseX))
        self.X = sorted(self.X, key=lambda sol: (sol[3]) )
        self.convertToFitness()
        
        return


    def generateNewSol(self):
        solutions = []
        for i in range(self.population + 1): # we have an extra one for default route
            x = []
            for j in range(self.N):
                x.append(random.randint(1, round(self.S[j], 0)))
            
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
        print("total: ", total)

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
    
    
    
    
    def run(self):
        self.generateNewSol() #create 50 random solutions to begin with
        self.solveForEachX()
        self.russianRoulette()
        self.crossOver()

        





            
