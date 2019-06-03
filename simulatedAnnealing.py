import random,math


file=open("NEWAISearchfile012.txt","r")
filearray=file.readlines()

#collect "clean" data from file in an array 
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

def createDistanceMatrix(n):
    #create empty matrix
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

    return matrix


def createRandomRoute(n):
    route=random.sample(range(1,n+1),n)
    return route


def findPathDistance(route,a):
    distance=0
    for i in range(0, len(route)-1):
        distance=distance+a[route[i]][route[i+1]]
    #add the initial node to the distance as well 
    distance+=matrix[route[len(route)-1]][route[0]]
    return distance

def swap(b,m,n):
    newArray=[]
    for i in range(len(b)):
        newArray.append(b[i])
    temp=newArray[m]
    newArray[m]=newArray[n]
    newArray[n]=temp
    return newArray

def inverseMutate(route):
    temp=[]
    start=random.randint(0,len(route)-1)
    end=random.randint(start,len(route)-1)
    for i in range(start,end+1):
        temp.append(route[i])
    z=1
    for i in range(start,end+1):
        route[i]=temp[len(temp)-z]
        z+=1
    return route

def mutate(route):
    accept=False
    while accept==False:
        indexA=random.randint(0,len(route)-1)
        indexB=random.randint(0,len(route)-1)
        if indexA!=indexB:
            route=swap(route,indexA,indexB)
            accept=True
        else:
            accept=False
    return route

def acceptanceProbability(currentEnergy,neighbourEnergy,temp):
    if neighbourEnergy<currentEnergy:
        return 1.0
    prob= math.exp((currentEnergy-neighbourEnergy)/temp)
    return prob

def modifiedAcceptanceProbability(currentEnergy,neighbourEnergy,temp):
    delta_E=neighbourEnergy-currentEnergy
    if delta_E<0:
        return 1.0
    else:
        delta_E_prime=findPathDistance(best,matrix)-neighbourEnergy
    prob=(math.e - (delta_E/temp))/(math.e-(delta_E_prime/temp))
    return prob

def setCoolingEnhancer(n):
    coolingEnhancer=0
    if n<30:
        coolingEnhancer=0.5
    elif n<150:
        coolingEnhancer=0.05
    elif n<750:
        coolingEnhancer=0.005
    else:
        coolingEnhancer=0.0005
    return coolingEnhancer

#create distance matrix
matrix=createDistanceMatrix(n)

#set initial temp
temp=1000

#cooling rate
coolingRate=0.00003

#initialize current solution
currentSolution=createRandomRoute(n)

#set current tour as best
best=currentSolution


#loop until system has cooled
while temp>1:
    #swap 2 randomly selected positions in the tour
    newSolution=mutate(currentSolution)
    #get energy of solutions
    currentEnergy=findPathDistance(currentSolution,matrix)
    neighbourEnergy=findPathDistance(newSolution,matrix)
    #decide if we should accept the neighbour
    prob=acceptanceProbability(currentEnergy,neighbourEnergy,temp)
    if prob>random.uniform(0,1):
        currentSolution=newSolution
    #keep track of the best solution found
    if findPathDistance(currentSolution,matrix)<findPathDistance(best,matrix):
        best=currentSolution
#    print(findPathDistance(currentSolution,matrix))
    #cool system
    temp *= (1-coolingRate);
#    temp=temp-coolingRate
print("Final bext solution distance: ", findPathDistance(best,matrix))
print("Tour: " , best )


"""
#use SA with cooling enhancer and modified acceptance probability
#set a cooling enhancer
coolingEnhancer=setCoolingEnhancer(n)
while temp>1:
    #swap 2 randomly selected positions in the tour
    newSolution=mutate(currentSolution)
    #get energy of solutions    
    currentEnergy=findPathDistance(currentSolution,matrix)
    neighbourEnergy=findPathDistance(newSolution,matrix)        
    #decide if we should accept the neighbour
    prob=modifiedAcceptanceProbability(currentEnergy,neighbourEnergy,temp)
    if prob>random.uniform(0,1):
        currentSolution=newSolution
    #keep track of the best solution found
    if findPathDistance(currentSolution,matrix)<findPathDistance(best,matrix):
        best=currentSolution
        print(best)
#    print(findPathDistance(currentSolution,matrix))
    #cool system
    temp *= (1-coolingRate*coolingEnhancer);
#    temp *= (1-coolingRate);
print("Final bext solution distance: ", findPathDistance(best,matrix))
print("Tour: " , best )
"""






