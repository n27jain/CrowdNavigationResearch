def __init__(self,population=50,generations = 150, pc = 0.6, pm =0.25):
        self.population = population
        self.generations = generations
        self.pc = pc
        self.pm = pm
        self.chromosomes = []


def f(self): # this is the f function. it is the score we want to minimize
    return

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