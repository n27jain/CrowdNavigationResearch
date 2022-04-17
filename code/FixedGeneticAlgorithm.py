from hashlib import new
from operator import index
import random
import copy
from time import sleep

from MapObjects import *



class GeneticAlgorithm:
    def __init__(self,population=50,generations = 150, pc = 0.6, pm =0.4):
        self.population = population
        self.generations = generations
        self.pc = pc
        self.pm = pm
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
        self.X = []
        self.Score = []
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

                if (i + 1 ) != len(self.D):
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
    def generateNewSol(self):
        solutions = [] 
        for i in range(self.population):
            x = []
            for j in range(self.N):
                if i == 0 : 
                    x.append(self.S [j])
                else:
                    x.append(random.randint(1, round(self.S[j], 0)))
            solutions.append(x)
        
        self.X = solutions
        return self.X
                            
    




            
