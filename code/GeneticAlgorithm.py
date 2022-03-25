
class GeneticAlgorithm:
    def __init__(self,population=50,generations = 150, pc = 0.6, pm =0.25):
        self.population = population
        self.generations = generations
        self.pc = pc
        self.pm = pm
        self.chromosomes = []
        self.n = None
        self.D = []
        self.C = []
        self.Tr = []
        self.Tg = []
        self.Rt_0 = []
        self.speed = []

    def setVars(self,n,D,C,Tr,Tg, Rt_0, speed):
        self.n = n
        self.D = D
        self.C = C
        self.Tr = Tr
        self.Tg = Tg
        self.Rt_0 = Rt_0
        self.speed = speed

    def f(self,X): # this is the f function. it is the score we want to minimize
        t = 0
        Penalty = 1

        for i in range(self.n):
            t_t = t + self.D[i]/ X[i] # the temporary time to check
            if self.Rt_0[i] == 1: # we are green on t = 0
                #case 1
                if t_t < self.Tg[0]: # move on to the next node
                    t = t_t 
                    continue
                else:
                    A = t_t/self.C[i]
                    B = A * self.C[i]
                    if t_t < B:
                        t += B + Penalty
                    elif t_t >= B + self.g[i]:
                        t += self.C[i] * (A + 1) + Penalty
                    else:
                        #timeArrival <= B + t_go and timeArrival > B
                        # move on to the next node
                        t = t_t 
                        
            else:
                #case 2
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

    def russianRoulette(self): 
        # of the n number of chromosomes select the 2 with the lowest time
        # then of the remaining n -2, we must select the surviours by their ratio of likelyhood
        # return the number of chromosomes for the next iteration
        return

    def crossOver(self):
            # cross over chromosomes 
            # exclude the 2 fittest solutions
            # crossover produces 2 childern who switch their chromosome values at a pivot point
            
            #self.chromosomes = cloneList
            return

    def mutation(self):
        # for each chromosome (excluding the best fit pair) run a randome number generator 
        # if the number is less than the ratio then randomly select a speed value.
        # do this for each speed value in a solution X
        # return the children 
        return

    def runSolver(self):
        return
        # self.generateStart() #create 50 random solutions to begin with
        # for i in range(self.generations):
        #     self.getAllFitness() #update the array with the fitness value 
        #     self.russianRoulette()#sort chromosomes by fitness and select surviors (first 2 are the best fit)
        #     self.crossOver() #cross-over the the surviors 
        #     self.mutation() #mutate the surviors    