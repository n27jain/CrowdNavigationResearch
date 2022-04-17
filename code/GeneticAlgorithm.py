from operator import index
import random
import copy

class Solution():
    def __init__(self, X, fitness,time):
        self.X = X
        self.fitness = fitness
        self.time = time

class GeneticAlgorithm:
    def __init__(self,population=50,generations = 150, pc = 0.6, pm =0.4):
        self.population = population
        self.generations = generations
        self.pc = pc
        self.pm = pm
        self.chromosomes = []
        self.N = None
        self.D = []
        self.C = []
        self.Tr = []
        self.Tg = []
        self.Rt_0 = []
        self.speed = []
        self.X = []
        self.Cost = []
        self.totalFitness = 0

    def setVars(self,N,D,C,Tr,Tg, Rt_0, speed):
        

        self.N = N
        self.D = D
        self.C = C
        self.Tr = Tr
        self.Tg = Tg
        self.Rt_0 = Rt_0
        self.speed = speed

    def f(self, x ): # this is the f function. it is the score we want to minimize
        t = 0
        Penalty = 1

        for i in range(self.n):
            # D is in km
            # x is in km/h
            # t = D km / x km/h = D/x h
            t_t = t + (self.D[i]/ x[i] * 1 * 60 * 60) # seconds in an hour
            if self.Rt_0[i] < 0: # we are green on t = 0
                #case 1
                if t_t < self.Tg[0]: # move on to the next node
                    t = t_t 
                    continue
                else:
                    A = t_t/self.C[i]
                    B = A * self.C[i]
                    if t_t < B + self.Rt_0[i] : # n*C_C < t_t
                        t += B + Penalty
                    elif t_t >= B + self.Tg[i] + self.Rt_0[i]: # 
                        t += self.C[i] * (A + 1) + Penalty
                    else:
                        #timeArrival <= B + t_go and timeArrival > B
                        # move on to the next node
                        t = t_t 
                        
            else:
                #case 2 we are red
                A = t_t/self.C[i]
                rightside = (A+1) * self.C[i]
                leftside = self.C[i] * A + self.Tr[i]
                if t_t <= leftside:
                    t += (leftside + Penalty)
                elif t_t > rightside:
                    t += ((self.C[i] * (A+1)) + self.Tr[i])
                else:
                    t = t_t 
        return t
    def generateNewSol(self):
        # the first solution will have the maximum speed limit maxed out
        solutions = [] 
        for i in range(self.population):
            x = []
            for j in range(self.n):
                if i == 0 : 
                    x.append(self.speed[j])
                else:
                    x.append(random.randint(1, round(self.speed[j])))
            solutions.append(x)
        
        self.X = solutions
        return
    
    def getCost(self):
        self.Cost = [] 
        self.totalFitness = 0
        for x in self.X:
            time = self.f(x)
            fitness = self.convertToFitness(time)
            sol = Solution(x, fitness,time)
            self.Cost.append(sol)
            self.totalFitness += fitness
        self.Cost = sorted(self.Cost, key=lambda sol: (sol.fitness) )

    def convertToFitness(self, cost):
        #F(x) = 1/(1+f(x))
        return 1/(1+ cost)
        
    def russianRoulette(self): 
        # of the n number of chromosomes select the 2 with the lowest time
        # then of the remaining n -2, we must select the surviours by their ratio of likelyhood
        # return the number of chromosomes for the next iteration
    
        rouletteRatio = []
        surviors = []
        # keep the best two
        
        surviors.append(copy.deepcopy(self.Cost[-1].X))
        surviors.append(copy.deepcopy(self.Cost[-2].X))
        last = 0
        for sol in self.Cost:
            last += sol.fitness/self.totalFitness
            rouletteRatio.append(last)
        
        for i in range(self.population - 2):
            # lets keep it significant by 5 decimal places since there are many possible ties at 
            # 4 decimal places
            # we should also not keep 1 as a possibly randomly generated number. 
            # from experimentation the sum of the surviors is arround 0.9999999999999996
            
            check = round(random.uniform(0, 0.99999),5)
            for i in range(len(self.Cost)):
                if rouletteRatio[i] >= check:
                    surviors.append(copy.deepcopy(self.Cost[i].X))
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
                
                crossOverPoint = int(round(random.uniform(1,self.n - 1),0))
                
                for k in range(self.n):
                    if k >= crossOverPoint:
                        cloneList[index_A][k] = cloneList[index_B][k]
            self.X = copy.deepcopy(cloneList)

    def mutation(self):
        # for each chromosome (excluding the 2 best fit pair) run a randome number generator 
        # if the number is less than the ratio then randomly select a speed value.
        # do this for each speed value in a solution X
        # return the children 
        clone = copy.deepcopy(self.X)
        for i in range(2,self.population):
            for j in range(self.n):
                check = round(random.uniform(0,1),2) 
                if check <= self.pm:
                    clone[i][j] = random.randint(1, round(self.speed[j]))
        self.X = copy.deepcopy(clone)
        
    def runSolver(self):
        self.generateNewSol() #create 50 random solutions to begin with
        for i in range(self.generations):
            self.getCost() # update the array with the fitness value 
            self.russianRoulette()# sort chromosomes by fitness and select surviors (first 2 are the best fit)
            self.crossOver() # cross-over the the surviors 
            self.mutation() # mutate the surviors    
        print("Best Solution found: ", self.X[0], self.f(self.X[0]) )