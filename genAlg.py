    # -*- coding: utf-8 -*-
"""
Created on Thu May 17 10:59:46 2018

@author: anoopscoop
"""
import xlwings as xw
import random
import operator
from itertools import permutations
from collections import defaultdict
import matplotlib.pyplot as plt


#references for much of the code was taken from docs.python.org
#much of the code was modified for this project's purposes from https://blog.sicara.com/getting-started-genetic-algorithms-python-tutorial-81ffa1dd72f9
#another valuable source from which code was modified was https://gist.github.com/NicolleLouis/d4f88d5bd566298d4279bcb69934f51d
#another reference used was https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.choice.html
#0 represents A station
#1 represents B station
#2 represents AB station

def generateRandomStations():
    stationVector = [2]

    for i in range(1,5):
        
        
        
        stationVector.append(random.randint(0,2))        
        
    #stationVector.append(2) #to make sure that the beginning and end of the stationVector are AB stations
    print('checkpoint 3')
    return stationVector
    
def generatePopulation(populationSize):
    populationStationVector = []
    print('checkpoint 2')
    for i in range(1,populationSize+1):
        populationStationVector.append(generateRandomStations())
        
    return populationStationVector

#print(list(permutations(["Wiehle-Reston East","Spring Hill", "Greensboro","Tysons Corner", "McLean"],2)))
def timeBetweenStations(origin,destination):
    standardTravelTime = 0 
    
    for i in range(21):  #find the standard travel time of that OD pair from spreadsheet
            if (xw.Range('E1:E20').value[i]==origin and xw.Range('F1:F20').value[i]==destination):
                
                standardTravelTime = xw.Range('J1:J20').value[i]
                
    return standardTravelTime
#############################################################  

def travelTime(stations):   #this is the fitness function
    
    
   
    totalTravelTime=0 #note that this is not a true totalTravelTime, it is a cost that includes the OD demand by each OD pair

    stationNamesVector=["Wiehle","Spring Hill", "Greensboro","Tysons Corner", "McLean"]   #vector with names of stations in order from left to right 
    #compute waiting time by finding the time saved for each possible trip combination

    #print(permutations(stations),2)
    passengerDemand =0
     
    stationPermut = list(permutations(stationNamesVector,2)) #permutations of stationNames vector(for all possible OD combinations)
    #print(stationPermut)
    for val in stationPermut: #iterate through the OD pairs
        
        #print(val)
        origin = val[0]
        #print(totalTravelTime)
        
        #print(origin)
        destination = val[1]
        originindex = stationNamesVector.index(origin)
        #print(originindex)
        #print(destination)
        destinationindex= stationNamesVector.index(destination)
        #print(destinationindex)
        standardTravelTime=0
        
        optimizedTravelTime=0
        print(origin)
        print(destination)
        #standard travel time is sourced directionally dependent
        for i in range(21):  #find the standard travel time of that OD pair from spreadsheet
            print('its working' )
            if (xw.Range('E1:21').value[i]==origin and xw.Range('F1:F21').value[i]==destination):
                
                standardTravelTime = xw.Range('G1:G21').value[i]
                passengerDemand = xw.Range('H1:H21').value[i]
        #print(passengerDemand)
        originStationType=stations[originindex] #find station type of origin
        #print(destinationindex)        
        destinationStationType=stations[destinationindex] #find station type of destination

        #Both are AB stations; this also chooses the most rational choice of train (lowest travel time)
        if(originStationType*destinationStationType==4):
            acount=0
            bcount=0
            abcount=0
            
            if(originindex>destinationindex):
                for i in range(destinationindex+1,originindex):   #count the number of stops between the AB station that can be skipped
                    if(stations[i]==0):
                        acount=acount+1
                    
                    if(stations[i]==1):
                        bcount=bcount+1
                        
                    if(stations[i]==2):
                        abcount=abcount+1
                    
            else:   
                for z in range(originindex+1,destinationindex):   #no need to subtract one from destinationindex because range always goes 1 less than upper bound anyways
                    if(stations[z]==0):
                        acount=acount+1
                    
                    if(stations[z]==1):
                        bcount=bcount+1
                        
                    if(stations[z]==2):
                        abcount=abcount+1
            
            if(bcount>acount):
              
                optimizedTravelTime = standardTravelTime-bcount #assuming waiting time is only one minute, however this does not include the savings from not having to accelerate and decelerate
            else:
                optimizedTravelTime = standardTravelTime-acount #assuming waiting time is only one minute, however this does not include the savings from not having to accelerate and decelerate
            
            totalTravelTime = (totalTravelTime)+ (optimizedTravelTime*passengerDemand)#converts the time into a cost
                
        #Both are same type of station (AA or BB), this excludes AB to AB trips however
        if((originStationType-destinationStationType==0) and originStationType*destinationStationType<4):
            
            acount=0
            bcount=0
            abcount=0
            
            if(originindex>destinationindex):
                for i in range(destinationindex+1,originindex):   #count the number of stops between the AB station that can be skipped
                    if(stations[i]==0):
                        acount=acount+1
                    
                    if(stations[i]==1):
                        bcount=bcount+1
                        
                    if(stations[i]==2):
                        abcount=abcount+1
                    
            else:   
                for z in range(originindex+1,destinationindex):   #no need to subtract one from destinationindex because range always goes 1 less than upper bound anyways
                    if(stations[z]==0):
                        acount=acount+1
                    
                    if(stations[z]==1):
                        bcount=bcount+1
                        
                    if(stations[z]==2):
                        abcount=abcount+1
            
            if(bcount>acount):
              
                optimizedTravelTime = standardTravelTime-bcount #assuming waiting time is only one minute, however this does not include the savings from not having to accelerate and decelerate
            else:
                optimizedTravelTime = standardTravelTime-acount #assuming waiting time is only one minute, however this does not include the savings from not having to accelerate and decelerate
            
            totalTravelTime = (totalTravelTime)+ (optimizedTravelTime*passengerDemand)
             #adding the travel time from this OD pair to the total travel time
        
            
        #both are different types of stations, excluding AB to A or AB to B and vice versa
        #transfer cost
        if(not(originStationType==destinationStationType) and not(destinationStationType==2) and not(originStationType==2)): 
            optimizedTravelTime = 0 #in this case this "optimized" travel time would likely be more than the regular travel time because of the transfer cost
         
            #go from initial station to AB station so that they can transfer
            acount=0 #number of A stations between the origin and the AB station
            bcount=0 #number of B stations between the origin and the AB station
            abcount=0
            abindex = 0
            
            if(originindex>destinationindex):  #this means that the trip is going from east to west
                    for i in range(destinationindex+1,originindex): #count the number of stops between the AB station that can be skipped
                        reversedstations= list(reversed(stations))                 
                        
                        if(reversedstations[i]==2):
                            abindex= len(stations)-1-i#reversed(list(enumerate(stations))) #returns the index of the first ab station bewteen the two different stations in the original index 
                            break
                        
                    for i in range(abindex, originindex): #counts the number of a and b stations between the origin and the AB station that the person gets off of 
                        
                        if(stations[i]==0):
                            acount=acount+1
                    
                        if(stations[i]==1):
                            bcount=bcount+1
                        
                    if(originStationType==0):                       
                        optimizedTravelTime = optimizedTravelTime + timeBetweenStations(stationNamesVector[originindex],stationNamesVector[abindex])-bcount

            
                    if(originStationType==1):
                        optimizedTravelTime = optimizedTravelTime + timeBetweenStations(stationNamesVector[originindex],stationNamesVector[abindex])-acount

            else:   #this means that the trip is going from west to east because the destination station index is greater than the origin station index 
                for z in range(originindex+1,destinationindex): 
                        
                            
                        if(stations[z]==2):
                            abindex=z
                            break  #first index of AB station
                            
                             
                            
                optimizedTravelTime = optimizedTravelTime + timeBetweenStations(stationNamesVector[originindex],stationNamesVector[abindex])
                for i in range(originindex,abindex):
                      
                     if(stations[i]==0):
                            acount=acount+1
                    
                     if(stations[i]==1):
                            bcount=bcount+1
                            
                if(originStationType==0):                       
                    optimizedTravelTime = optimizedTravelTime + timeBetweenStations(stationNamesVector[originindex],stationNamesVector[abindex])-bcount

            
                if(originStationType==1):
                    optimizedTravelTime = optimizedTravelTime + timeBetweenStations(stationNamesVector[originindex],stationNamesVector[abindex])-acount
        
        #now from the AB transfer station to the destination station.
            #This is basically the same thing as the code below
        
        #go from initial station to AB station so that they can transfer
            acountone=0 #number of A stations between the origin and the AB station
            bcountone=0 #number of B stations between the origin and the AB station
            abcountone=0
                  
            if(abindex>destinationindex):
                for i in range(destinationindex+1,originindex):   #count the number of stops between the AB station that can be skipped
                    if(stations[i]==0):
                        acountone=acountone+1
                    
                    if(stations[i]==1):
                        bcountone=bcountone+1
                        
                    if(stations[i]==2):
                        abcountone=abcountone+1   
                     
            else:   
                for z in range(abindex+1,destinationindex):   #no need to subtract one from destinationindex because range always goes 1 less than upper bound anyways
                    if(stations[z]==0):
                        acountone=acountone+1
                    
                    if(stations[z]==1):
                        bcountone=bcountone+1
                        
                    if(stations[z]==2):
                        abcountone=abcountone+1
            
            #so now we have the number of a, b, and ab stations between the two stations
            #next what we need is which stations will be skipped. This is based on the one non AB station in the OD pair
            #the standard travel time is assumed to be the same in either direction            
            if(destinationStationType==0): #if origin station is an AB station and destination is an A station
                
                optimizedTravelTime =optimizedTravelTime+ standardTravelTime-bcount #assuming waiting time is only one minute, however this does not include the savings from not having to accelerate and decelerate
            
            if(destinationStationType==1):  #if origin station is an AB station and destination is an B station
                optimizedTravelTime = optimizedTravelTime + standardTravelTime-acount #assuming waiting time is only one minute, however this does not include the savings from not having to accelerate and decelerate
            
            totalTravelTime= totalTravelTime + (optimizedTravelTime*passengerDemand)
        #from A to AB or B to AB and vice versa
        if(originindex==2 or destinationindex ==2 and not(originindex==destinationindex)):
            optimizedTravelTime = 0 #in this case this "optimized" travel time would likely be more than the regular travel time because of the transfer cost
         
            #go from initial station to AB station so that they can transfer
            acount=0 #number of A stations between the origin and the AB station
            bcount=0 #number of B stations between the origin and the AB station
            abcount=0
                  
            if(originindex>destinationindex):
                for i in range(destinationindex+1,originindex):   #count the number of stops between the AB station that can be skipped
                    if(stations[i]==0):
                        acount=acount+1
                    
                    if(stations[i]==1):
                        bcount=bcount+1
                        
                    if(stations[i]==2):
                        abcount=abcount+1   
                     
            else:   
                for z in range(originindex+1,destinationindex):   #no need to subtract one from destinationindex because range always goes 1 less than upper bound anyways
                    if(stations[z]==0):
                        acount=acount+1
                    
                    if(stations[z]==1):
                        bcount=bcount+1
                        
                    if(stations[z]==2):
                        abcount=abcount+1
            
            #so now we have the number of a, b, and ab stations between the two stations
            #next what we need is which stations will be skipped. This is based on the one non AB station in the OD pair
            #the standard travel time is assumed to be the same in either direction            
            if(originStationType==2 and destinationStationType==0): #if origin station is an AB station and destination is an A station
                
                optimizedTravelTime = standardTravelTime-bcount #assuming waiting time is only one minute, however this does not include the savings from not having to accelerate and decelerate
            
            if(originStationType==2 and destinationStationType==1):  #if origin station is an AB station and destination is an B station
                optimizedTravelTime = standardTravelTime-acount #assuming waiting time is only one minute, however this does not include the savings from not having to accelerate and decelerate
            
            if(originStationType==0 and destinationStationType==2):  #if origin station is an A station and destination station is an AB station
                optimizedTravelTime = standardTravelTime-bcount #assuming waiting time is only one minute, however this does not include the savings from not having to accelerate and decelerate
            
            if(originStationType==1 and destinationStationType==2):  #if origin station is a B station and destination station is an AB station
                optimizedTravelTime = standardTravelTime-acount #assuming waiting time is only one minute, however this does not include the savings from not having to accelerate and decelerate
            
            totalTravelTime = (totalTravelTime)+ (optimizedTravelTime*passengerDemand) #increment the totalTravelTime value for the function by the optimizedTraveLTime value for each OD pair, creating a totalTravelTime (cost) for the entire stationVector
    
    return totalTravelTime
    

##fitness function done!    
      
################################################################################################   

def populationPerformance(population):
    
    populationPerf = {}
    #print(population)
    for individual in population:
        #print(population)    
        #convert to string
        stringlist = ''.join(str(e) for e in individual)
        #print(individual)
        #print(stringlist)
        #print(travelTime(individual))
        populationPerf[stringlist] = travelTime(individual) #this is a dictionary putting the station vectors and its travelTime as key value pairs
        
    
    print(sorted(populationPerf.items(), key=operator.itemgetter(1), reverse =True))
    print('checkpoint 6')    
    return sorted(populationPerf.items(), key=operator.itemgetter(1), reverse =True)  #gets the second element of each dictionary entry, which is the fitness, and sorts based on that
 #reverse=True returns the values in descending order       
        

def populationSelection(randomIndi,bestIndi,sortedPopulation):
        nextGeneration=[]
        print(len(sortedPopulation))
        for i in range(bestIndi):
            
            print(sortedPopulation)
            
            nextGeneration.append(sortedPopulation[i][0]) #0 because you are getting the vectors, not the fitness values from the dictionary

        for i in range(randomIndi):
            nextGeneration.append(random.choice(sortedPopulation)[0])
        
        random.shuffle(nextGeneration)
        print(nextGeneration)
        return nextGeneration

def createChild(individual1,individual2):
    
    child = []

    for i in range(len(individual1)):
        if(int(100*random.random())<50):
            child.append(individual1[i])
        
        else:
            child.append(individual2[i])
            
    return child
    
def createChildren(breeders,numberofChildren):
    nextPopulation= []
    
    for i in range(int(len(breeders)/2)):
        for j in range(numberofChildren):
                nextPopulation.append(createChild(breeders[i],breeders[len(breeders)-i-1])) #it appears that you add a child made from the first breeder and the last breeder
    #since it breeds the beginning with the end, the range only needs to go until HALF the length of the breeders vector.
        return nextPopulation

def mutateStation(stationVec):
    
    #choose a random index in the station vector and randomly assign it an integer from 0-2 (which are the possible types of stations)
    index_modification = int(random.randint(1,len(stationVec)-1))
    mutatedStationVec=stationVec
    mutatedStationVec[index_modification] = int(random.random()*3)
    
    return mutatedStationVec

def mutatePopulation(population, chance_of_mutation):
	for i in range(len(population)):
		if random.random() * 100 < chance_of_mutation:
			population[i] = mutateStation(population[i])
	return population  
#variables to be input 

def nextGeneration (firstGeneration, best_sample, lucky_few, number_of_child, chance_of_mutation):
     
     populationSorted = populationPerformance(firstGeneration)
     print('checkpoint 5')
     print(populationSorted)
     nextBreeders = populationSelection(lucky_few,best_sample,populationSorted)
     nextPopulation = createChildren(nextBreeders, number_of_child) #requires an input of an int
     nextGeneration = mutatePopulation(nextPopulation, chance_of_mutation) 
     return nextGeneration

def multipleGeneration(number_of_generation, size_population, best_sample, lucky_few, number_of_child, chance_of_mutation):
    historic = []
    print('checkpoint 1')
    historic.append(generatePopulation(size_population))
    for i in range (number_of_generation):
        print('checkpoint 4')
        
        historic.append(nextGeneration(historic[i], best_sample, lucky_few, number_of_child, chance_of_mutation)) #problem line 
    
    return historic


#print result:
def printSimpleResult(historic, number_of_generation): #bestSolution in historic. Caution not the last
	result = getListBestIndividualFromHistoric(historic)[number_of_generation-1]
	print ("solution: \"" + result[0] + "\" with fitness: " + str(result[1]))

def getBestIndividualFromPopulation (population):
	return populationPerformance(population)[0]

def getListBestIndividualFromHistoric(historic):
	bestIndividuals = []
	for population in historic:
		bestIndividuals.append(getBestIndividualFromPopulation(population))
	return bestIndividuals
#graph
def evolutionBestFitness(historic):
	plt.axis([0,len(historic),0,105])
	plt.title("Best travel time cost in each generation by iteration")
	
	evolutionFitness = []
	for population in historic:
		evolutionFitness.append(getBestIndividualFromPopulation(population)[1])
	plt.plot(evolutionFitness)
	plt.ylabel('fitness best individual')
	plt.xlabel('generation')
	plt.show()

def evolutionAverageFitness(historic, size_population):
	plt.axis([0,len(historic),0,105])
	plt.title("Average travel time cost by generation")
	
	evolutionFitness = []
	for population in historic:
		populationPerf = populationPerformance(population)
		averageFitness = 0
		for individual in populationPerf:
			averageFitness += individual[1]
		evolutionFitness.append(averageFitness/size_population)
	plt.plot(evolutionFitness)
	plt.ylabel('Average fitness')
	plt.xlabel('generation')
	plt.show() 
#variables

size_population = 100
best_sample = 20
lucky_few = 20
number_of_child =5
number_of_generation = 50
chance_of_mutation = 5

#program
if ((best_sample + lucky_few) / 2 * number_of_child != size_population):
	print ("population size not stable")
else:
	historic = multipleGeneration(number_of_generation, size_population, best_sample, lucky_few, number_of_child, chance_of_mutation)
	
	printSimpleResult(historic, number_of_generation)
	
	evolutionBestFitness(historic)
	evolutionAverageFitness(historic, size_population)

