import numpy as np
from DATA_DUMMY import data
from CONFIGURATION import config
from BRKGA import initializePopulation




def transform(population):
    for i in range(len(population)):
        for j in range(len(population[i]['chr'])):
            if population[i]['chr'][j] <= 0.5:
                population[i]['solution'][j]=0
            else: population[i]['solution'][j]=1
    return population



def checkschedule(currentnurse):
    test=0
    sumhours=sum(currentnurse)
    if sumhours < data['minHours'] and sumhours !=0: #Constraint minH
        test=1
    if sumhours > data['maxHours']:   #Constraint maxH
        test=1
    if sumhours != 0:        #Constraints rests and maxPresence
        i=0
        while currentnurse[i]==0:
            i=i+1
        imin=i
        i=len(currentnurse)-1
        while currentnurse[i] == 0:
            i = i - 1
        imax=i
        for i in range(imin, imax):
            if currentnurse[i]==0 and currentnurse[i+1]==0:   #Constraints rests
                test=1
        if imax-imin+1 > data['maxPresence']:       #Constraints maxPresence
            test=1

        compteur=0
        for i in range(imin, imax+1):               #Constraints maxConsec
            if currentnurse[i]==1:
                compteur+=1
            else:
                if compteur > data['maxConsec']:
                    test=1
                compteur = 0
        if compteur > data['maxConsec']:
            test=1
    return test



def compareworkload(workload):
    error=0
    for i in range(0,data['nHours']):
        if workload[i]-data['demand'][i] > 0:
            error+=(1.0*workload[i]-1.0*data['demand'][i])/data['nHours']
        if workload[i]-data['demand'][i] < 0:
            error += 2.0*abs((workload[i] - data['demand'][i])) / data['nHours']
    return error






def decode(population,data):

    population=transform(population)

    for x in range(len(population)):
        population[x]['fitness']=0
        workload=[0]*data['nHours']
        for i in range(0, data['nNurses']):
            currentnurse = []
            for j in range(i*data['nHours'], (i+1)*data['nHours']):
                currentnurse.append(population[x]['solution'][j])
            test=checkschedule(currentnurse)
            population[x]['fitness'] = population[x]['fitness']+(1.5*test/data['nNurses']) #penalize fitess if bad schedule
            for k in range(0, data['nHours']):
                workload[k]+=currentnurse[k]
        #print(workload)
        error=compareworkload(workload)

        population[x]['fitness'] = population[x]['fitness'] + 0.5*error
    return(population)




def infoBestIndividual(bestIndividual):
    workload = [0] * data['nHours']
    for i in range(0, data['nNurses']):
        currentnurse = []
        for j in range(i*data['nHours'], (i+1)*data['nHours']):
            currentnurse.append(bestIndividual['solution'][j])
        test=checkschedule(currentnurse)
        print('Nurse',i,'Test Schedule =',test)
        for k in range(0, data['nHours']):
            workload[k]+=currentnurse[k]
    print('Comp. Workload',workload)
    print('Dema. Workload', data['demand'])
    #error=compareworkload(workload)
    return(bestIndividual)


#def decode(population, data):
 #   for ind in population:
  #      ind['solution']=ind['chr']
   #     res=np.multiply(ind['chr'],range(len(ind['chr'])))
    #    ind['fitness']=sum(res)
    #return(population)
    

