import random

file=open("NEWAISearchfile021.txt","r")
filearray=file.readlines()
populationSize=50

#collect data from file in an array
data=[]
num1=""
for i in range(2, len(filearray) ):
    for j in range(0,len(filearray[i]) ):
        if filearray[i][j].isdigit():
            num1 = num1 + filearray[i][j]
            if i==(len(filearray)-1) and j==(len(filearray[i])-1):
                data.append(num1)
        else:
            if num1 != "":
                data.append(num1)
                num1=""

#find the number of cities
secondline=filearray[1]
size=""
for char in secondline:
    if char.isdigit():
        size=size+char

n=int(size)
file.close()

n+=1
matrix = [0] * n
for i in range(n):
    matrix[i] = [0] * n

#populate matrix from array
k=0
n=n-1
for i in range(1,n):
    for j in range(i+1,n+1):
        if i!=j:
            matrix[i][j]=int(data[k])
            matrix[j][i]=int(data[k])
            k+=1

def createRoute(n):
    route=random.sample(range(1,n+1),n)
    return route


def createInitialPopulation(populationSize,n):
    population=[]
    for i in range(0,populationSize):
        population.append(createRoute(n))
    return population

#creates initial population where each succesor tour is better than the previous tour
def createInitialPopulation2(populationSize,n):
    population=[]
    population.append(createRoute(n))
    for i in range(0,populationSize):
        valid=False
        while valid==False:
            r=createRoute(n)
            if findPathDistance(r)<findPathDistance(population[i]):
                population.append(r)
                valid=True
            else:
                valid=False
        population.append(r)
    print("initial pop created")
    return population

def findPathDistance(route):
    distance=0
    for i in range(0, len(route)-1):
        distance=distance+matrix[route[i]][route[i+1]]
    #add the initial node to the distance as well 
    distance+=matrix[route[len(route)-1]][route[0]]
    return distance


def calculateFitness(pop):
    fitness=[]
    for i in range(0, populationSize):
        fitness.append(1/findPathDistance(pop[i]))
    return fitness

def normalizeFitness(fitness):
    sum=0
    normFitness=[0]*len(fitness)
    for i in range(0, len(fitness)):
        sum+=fitness[i]
    for i in range(0, len(fitness)):
        normFitness[i]=fitness[i]/sum
    return normFitness


def findBestRoute(pop):
    recordDistance=findPathDistance(pop[0])
    bestEver=pop[0]
    for i in range(0, populationSize):
        d=findPathDistance(pop[i])
        if d<recordDistance:
            recordDistance=d
            bestEver=pop[i]
    return bestEver

def findBestDist(pop):
    recordDistance=findPathDistance(pop[0])
    for i in range(0, populationSize):
        d=findPathDistance(pop[i])
        if d<recordDistance:
            recordDistance=d
            bestEver=pop[i]
    return recordDistance


def pickOne(list, prob):
    index=0
    r=random.uniform(0,1)
    while r>0:
        r=r-prob[index]
        index+=1
    index-=1
    return list[index]

def swap(b,m,n):
    newArray=[]
    for i in range(len(b)):
        newArray.append(b[i])
    temp=newArray[m]
    newArray[m]=newArray[n]
    newArray[n]=temp
    return newArray

def reverseMutate(route,mutationRate):
    genRand=random.uniform(0,1)
    temp=[]
    if genRand<=mutationRate:
        start=random.randint(0,len(route)-1)
        end=random.randint(start,len(route)-1)
        for i in range(start,end+1):
            temp.append(route[i])
        z=1
        for i in range(start,end+1):
            route[i]=temp[len(temp)-z]
            z+=1
    return route


def mutate(route,mutationRate):
    genRand=random.uniform(0,1)
    if genRand<=mutationRate:
 #       print(genRand)
 #       print("i've been mutated")
        accept=False
        while accept==False:
            indexA=random.randint(0,len(route)-1)
            indexB=random.randint(0,len(route)-1)
            if indexA!=indexB:
                mRoute=swap(route,indexA,indexB)
                accept=True
            else:
                accept=False
        return mRoute
    return route

def orderCrossOverX(orderA,orderB):
    start=random.randint(0,len(orderA)-1)
    end=random.randint(start,len(orderA)-1)

    copyOrderA=[]
    copyOrderB=[]
    for i in range(len(orderA)):
        copyOrderA.append(orderA[i])
        copyOrderB.append(orderB[i])

    child1=[0]*len(orderA)
    child2=[0]*len(orderB)
#create child 1
    for i in range (start,end):
        child1[i]=orderA[i]
        copyOrderB.remove(child1[i])
    x=0
    for i in range(len(child1)):
        if child1[i]==0:
            child1[i]=copyOrderB[x]
            x+=1
#create child 2
    for i in range (start,end):
        child2[i]=orderB[i]
        copyOrderA.remove(child2[i])
    x=0
    for i in range(len(child2)):
        if child2[i]==0:
            child2[i]=copyOrderA[x]
            x+=1

    if findPathDistance(child1)>findPathDistance(child2):
        return child2
    else:
        return child1



def SimpleCrossOver(orderA,orderB):
    accept=False
    while accept==False:
        start=random.randint(0,len(orderA)-1)
        end=random.randint(start,len(orderA)-1)
        if start!=end:
            accept=True
    newOrder=orderA[start:end]

#   left=n-len(newOrder)
    for i in range(len(orderB)):
        city=orderB[i]
        if city not in newOrder:
            newOrder.append(city)

    return newOrder

#one-point crossover 
def crossOver(routeA,routeB):
    childOne=[]
    childTwo=[]
    childOnePrefix=[]
    childOneSuffix=[]
    childTwoPrefix=[]
    childTwoSuffix=[]
    delimiter=random.randint(0,len(routeA)-1)
    for i in range(len(routeA)):
        if i <=delimiter:
            childOnePrefix.append(routeA[i])
        else:
            childOneSuffix.append(routeA[i])
    for i in range(len(routeB)):
        if i <=delimiter:
            childTwoPrefix.append(routeB[i])
        else:
            childTwoSuffix.append(routeB[i])
    for i in childOnePrefix:
        for j in childTwoSuffix:
            if j==i:
                childTwoSuffix.remove(j)
    for k in childTwoPrefix:
            if k not in childOnePrefix and k not in childTwoSuffix:
                childTwoSuffix.append(k)
    childOne=childOnePrefix+childTwoSuffix
    for i in childTwoPrefix:
        for j in childOneSuffix:
            if j==i:
                childOneSuffix.remove(j)
    for k in childOnePrefix:
            if k not in childTwoPrefix and k not in childOneSuffix:
                childOneSuffix.append(k)
    childTwo=childTwoPrefix+childOneSuffix
    if findPathDistance(childOne)>findPathDistance(childTwo):
        fittestChild=childTwo
    else:
        fittestChild=childOne
    return fittestChild


def nextGeneration(prevPopulation,normFit):
    newPopulation=[]
    for i in range(0, populationSize):
        orderA=pickOne(prevPopulation,normFit)
#        print("parent 1 has dist " ,findPathDistance(orderA))
        orderB=pickOne(prevPopulation,normFit)
#        print("parent 2 has dist " ,findPathDistance(orderB))
        for i in range(10):
            orderA1=pickOne(prevPopulation,normFit)
            orderB1=pickOne(prevPopulation,normFit)
            if findPathDistance(orderA1)<findPathDistance(orderA):
                orderA=orderA1           
            if findPathDistance(orderB1)<findPathDistance(orderB):
                orderB=orderB1    

        order=SimpleCrossOver(orderA,orderB)
        for i in range(10):
            order1=orderCrossOverX(orderA,orderB)
            if findPathDistance(order1)<findPathDistance(order):
                order=order1

        newOrder=reverseMutate(order,0.1)
#        print("child has dist " ,findPathDistance(newOrder))
        newPopulation.append(newOrder)
    return newPopulation

def averagepopulationsize(p):
    total=0
    for i in range(len(p)):
        total=total+findPathDistance(p[i])
    averagePopulationSize=total/populationSize
    return averagePopulationSize


p=createInitialPopulation(populationSize,n)

bestestRoute=[]
bestOverall=findBestDist(p)
noOfGenerations=1000
i=0
while i<noOfGenerations:
    f=calculateFitness(p)
    nf=normalizeFitness(f)
    p=nextGeneration(p,nf)
#    print(averagepopulationsize(p))
    best=findBestDist(p)
    bestRoute=findBestRoute(p)
    if best<bestOverall:
        bestOverall=best
        bestestRoute=bestRoute
    for z in range(int(populationSize//10)):
        rand=random.randint(0,populationSize-1)
        p[rand]=bestestRoute
    print(100*i/noOfGenerations, "% completed")
    i+=1

print(bestOverall)
print(bestestRoute)
