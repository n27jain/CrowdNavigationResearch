
from MapObjects import *
from MapGenerator import *
from CreatePaths import *
from Solve import *



# Build a new Experiment

#Shortest Trip Time Planning

def experiment_1():
    # a 8x8 map
    # 5 paths, each path will have a length of 3
    paths = setUpPaths(5,3,xmax = 8, ymax = 8)
    # paths = getPathsFromSaveData()

    bases = []
    results = []

    population=50
    generations = 100
    pc = 0.6
    pm =0.4
    i = 0
    for path in paths:
        base, results = solveThisPath(path,population,generations,pc,pm)
        fname = "Experiment1/Experiment_1_1_Test" + str(i) + "_" + ".txt" 
        title  = "population: " + str(population)
        "generations: " + str(generations)
        "pc: " + str(pc)
        "pm: "+ str(pm)                    
        announcement = "No Variation \n"
        title = announcement + title       
        prepareFile(fname,base,results,title)
        bases.append(base)
        results.append(results)
        i +=1 
    
    # variation in populations
    population=20


    
    for path in paths:
        base, results = solveThisPath(path,population,generations,pc,pm)
        fname = "Experiment1/Experiment_1_2_Test" + str(i) + "_" + ".txt" 
        title  = "population: " + str(population)
        "generations: " + str(generations)
        "pc: " + str(pc)
        "pm: "+ str(pm)                                            
        announcement = "Variation in Population = 20 \n"
        title = announcement + title
        prepareFile(fname,base,results,title)
        bases.append(base)
        results.append(results)
        i +=1 

    population=100



    # variation in generations
    for path in paths:
        base, results = solveThisPath(path,population,generations,pc,pm)
        fname = "Experiment1/Experiment_1_2_Test" + str(i) + "_" + ".txt" 
        title  = "population: " + str(population)
        "generations: " + str(generations)
        "pc: " + str(pc)
        "pm: "+ str(pm)                                      
        announcement = "Variation in Population = 100 \n"
        title = announcement + title
        prepareFile(fname,base,results,title)
        bases.append(base)
        results.append(results)
        i +=1 
    
    population=50
    generations = 30


    for path in paths:
        base, results = solveThisPath(path,population,generations,pc,pm)
        fname = "Experiment1/Experiment_1_3_Test" + str(i) + "_" + ".txt" 
        title  = "population: " + str(population)
        "generations: " + str(generations)
        "pc: " + str(pc)
        "pm: "+ str(pm)                                           
        announcement = "Variation in Generations = 30 \n"
        title = announcement + title
        prepareFile(fname,base,results,title)
        bases.append(base)
        results.append(results)
        i +=1 

    
    generations = 150


    # variation in generations
    for path in paths:
        base, results = solveThisPath(path,population,generations,pc,pm)
        fname = "Experiment1/Experiment_1_3_Test" + str(i) + "_" + ".txt" 
        title  = "population: " + str(population)
        "generations: " + str(generations)
        "pc: " + str(pc)
        "pm: "+ str(pm)                                               
        announcement = "Variation in Generations = 150 \n"
        title = announcement + title
        prepareFile(fname,base,results,title)
        bases.append(base)
        results.append(results)
        i +=1 
    

    generations = 100
    pc = 0.2


    # variation in pc
    for path in paths:
        base, results = solveThisPath(path,population,generations,pc,pm)
        fname = "Experiment1/Experiment_1_4_Test" + str(i) + "_" + ".txt" 
        title  = "population: " + str(population)
        "generations: " + str(generations)
        "pc: " + str(pc)
        "pm: "+ str(pm)                                               
        announcement = "Variation in PC = 0.2 \n"
        title = announcement + title
        prepareFile(fname,base,results,title)
        bases.append(base)
        results.append(results)
        i +=1 

    pc = 0.8
    # variation in pc
    for path in paths:
        base, results = solveThisPath(path,population,generations,pc,pm)
        fname = "Experiment1/Experiment_1_4_Test" + str(i) + "_" + ".txt" 
        title  = "population: " + str(population)
        "generations: " + str(generations)
        "pc: " + str(pc)
        "pm: "+ str(pm)                                               
        announcement = "Variation in PC = 0.8 \n"
        title = announcement + title
        prepareFile(fname,base,results,title)
        bases.append(base)
        results.append(results)
        i +=1 

    pc = 0.6
    pm = 0.2

    # variation in pm
    for path in paths:
        base, results = solveThisPath(path,population,generations,pc,pm)
        fname = "Experiment1/Experiment_1_5_Test" + str(i) + "_" + ".txt" 
        title  = "population: " + str(population)
        "generations: " + str(generations)
        "pc: " + str(pc)
        "pm: "+ str(pm)                                               
        announcement = "Variation in PM = 0.2 \n"
        title = announcement + title
        prepareFile(fname,base,results,title)
        bases.append(base)
        results.append(results)
        i +=1 
    
    pm = 0.6
    # variation in pm
    for path in paths:
        base, results = solveThisPath(path,population,generations,pc,pm)
        fname = "Experiment1/Experiment_1_5_Test" + str(i) + "_" + ".txt" 
        title  = "population: " + str(population)
        "generations: " + str(generations)
        "pc: " + str(pc)
        "pm: "+ str(pm)                                               
        announcement = "Variation in PM = 0.6 \n"
        title = announcement + title
        prepareFile(fname,base,results,title)
        bases.append(base)
        results.append(results)
        i +=1 
    
def experiment_2():
    #same 8x8 map
    # 10 paths each with a length of 6
    # variation in pm, pc, generation, populations 
    return

def STTP():
    runCustom(8,8)
    experiment_1()


#Adaptive Traffic Light System
def experiment_3():
    #same 8x8 map
    # 10 paths each with a length of 6
    # variation in take pm, pc, generation and population from experiment 2
    # run experiment on traffic lights 
    # variation in pm, pc, generation, populations 
    # compare results
    return


def prepareFile(f_name, base, results, title  ):
    f = open(f_name,'w')
    f.write(title + '\n')
    f.write(" ____________________Base_______________________ \n ")

    f.write(str(base) + '\n')

    f.write(" ____________________Best Solution Per Generation_______________________ \n ")
    for result in results:
        f.write(str(result) + '\n')


STTP()



