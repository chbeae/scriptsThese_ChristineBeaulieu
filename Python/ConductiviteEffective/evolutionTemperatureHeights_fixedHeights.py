# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:45:17 2018

@author: ChristineB.local

This code plots the temperature of particles at different heights in the bed
versus time.
The geometry is a cube.
The thermocouples are aligned in the middle of the cube in (x,y)
The thermocouples are evenly spaced and start from the top of the bed.
    First thermocouple is at z = maxZ - distance
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import sys
from scipy import stats
import math

print ""
print "Hello! This script reads data from dump files created from LIGGGHTS."
print ""
print "WARNING!!! The particles in dump files must be ordered by ID!!"

"Initialize empty structures"
timeVector = np.array([])

"Faire une liste de tous les fichiers dump dans le dossier à l'étude"
#dossier=input('Enter the directory containing the dump files (between "): ') 
dossier = 'dump' #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
listeDeFichiers=os.listdir(dossier)
#skip = int(raw_input("You want to compute one dump file on how many? "))
#newList = listeDeFichiers[0::skip]
firstTimeStep = 0
print ("")
print ("There are %d files in that dump folder.") %len(listeDeFichiers)
nbPointsStudied = int(raw_input("How many points (timesteps) do you want to calculate? "))
indexVector = np.round(np.linspace(firstTimeStep,len(listeDeFichiers)-1,nbPointsStudied, dtype = 'int'))
newList = list()
for j in indexVector:
    newList.append(listeDeFichiers[j])


"Lire tous les fichiers texte en entier et les mettre dans une matrice"
for index, file in enumerate(newList):    
    print ""
    print "FILE %d: %s" %(index+1, file) 
    os.chdir(dossier)
    donnees=np.loadtxt(file, skiprows=9, unpack=False)
    #donnees = np.genfromtxt(file, skip_header=11, unpack=False)
        
    if donnees.size:
        "Renommer chaque colonne"
        ID=donnees[:,0]
        type_part=donnees[:,1]
        positionxyz=donnees[:,2:5]
        vitessexyz=donnees[:,5:8]
        #forcexyz=donnees[:,8:11]
        #omegaxyz=donnees[:,11:14]
        radius=donnees[:,14]
        density=donnees[:,15]
        #radialPos=donnees[:,16]
        temp = donnees[:,16]
        heatFlux = donnees[:,17]
        
        minX = min(positionxyz[:,0])
        maxX = max(positionxyz[:,0])
        minY = min(positionxyz[:,1])
        maxY = max(positionxyz[:,1]) 
        minZ = min(positionxyz[:,2])
        maxZ = max(positionxyz[:,2])
        
        if index == 0: #Things to do for the FIRST dump
            timestep = float(raw_input("What is the timestep of your simulation? (in seconds) : "))
            #timestep = 1  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            minRadius = min(radius)
            maxRadius = max(radius)  
            nbPart = len(ID)
            nbType = max(type_part)
            
            "Global boolean to separate type 1 and type 2"
            if nbType > 1:
                boolType1 = (type_part == 1)
                nbType1 = sum(boolType1)
                boolType2 = (type_part == 2)
                nbType2 = sum(boolType2)
                radius1 = radius[boolType1][0]
                radius2 =  radius[boolType2][0]
                density1 = density[boolType1][0]
                density2 = density[boolType2][0]
                volume1 = (4 * math.pi* (radius1**3))/3
                volume2 = (4 * math.pi* (radius2**3))/3
                mass1 = volume1 * density1
                mass2 = volume2 * density2
                mass1Tot = nbType1 * mass1
                mass2Tot = nbType2 * mass2
            
            print ""            
            print "************SIMULATION INFORMATIONS**********************"            
            print "There are %d particles in this simulation." %(nbPart)
            print "The domain of particles in x is : %.4f m to %.4f m" \
                %(minX, maxX) 
            print "The domain of particles in y is : %.4f m to %.4f m" \
                %(minY, maxY) 
            print "The domain of particles in z is : %.4f m to %.4f m" \
               %(minZ, maxZ)
            print ""
                
            if nbType > 1:
                print "There are %d types of particles in this simulation." \
                %(nbType)
                print "The radius 1 is : %.6f m"  %radius[boolType1][0] 
                print "The radius 2 is : %.6f m"  %radius[boolType2][0]
                print "The density 1 is : %.1f m"  %density[boolType1][0]
                print "The density 2 is : %.1f m"  %density[boolType2][0]
            else:
                print "There is %d types of particles in this simulation." \
                %(nbType)
                print "The radius of the MONODISPERSE particles is : %.6f m"  %minRadius 
                print "The density of the MONODISPERSE particles is : %.1f m"  %density[0]

            print ""
            print "The timestep you entered is %.2e seconds." %(timestep)
            print ""
            print "There are %i files to browse." %(len(newList))
            print ""
            
            #T0 = float(raw_input("What is the initial temperature of particles? (in K) : "))
            #Twall = float(raw_input("What is the wall temperature? (in K) : "))
            #drumRadius = float(raw_input("What is the drum radius? (in m) : "))
            boxSize = float(raw_input("What is the cubic box size? (in m) : "))
            #boxSize = 0.20 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!                    
            
            print ("")            
            print ("Info on the thermocouples.")
            nbThermo = int(raw_input("How many thermocouples do you have? "))
            #nbThermo = 3 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #distanceThermo = float(raw_input("What is the distance between each thermocouple (in m)? "))
            #distanceThermo = 0.05 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            heightsVector = np.array([])
            zVector = np.array([])
            for jjg in range(nbThermo):
                print ("Thermocouple %d") %(jjg+1)
                distanceThermo = float(raw_input("What is the distance of the thermocouple from the top (in m)? "))
                #height_jjg = (maxZ+maxRadius) - distanceThermo
                height_jjg = boxSize - distanceThermo
                heightsVector = np.append(heightsVector, height_jjg)
                zVector = np.append(zVector, distanceThermo)
                print ("")
                
#            previousSensor = 0
#            for sensor in range(nbThermo):
#                positionSensor = previousSensor + distanceThermo
#                heightsVector = np.append(heightsVector, positionSensor)
#                previousSensor = positionSensor
                #locals()["thermocouple"+str(sensor+1)] = np.array([])
            print ("The thermocouples are located at (in m): ")
            print heightsVector
            tableTemperatures = np.zeros((nbThermo, len(newList)), dtype=float)
            
            go = str(raw_input("Are you ready to continue? (y/n) "))
            if go == 'n':
                sys.exit('Not ready. You''ll have to start again')
            print ""
            
        "Décortiquer le nom du fichier à l'étude"
        b=file.split('_')
        b=b[1].split('.')
        iteration=int(b[0])
        timeSim = iteration * timestep
        timeVector = np.append(timeVector,timeSim)
            
        #Return to main directory to have access to other output scripts
        os.chdir("..")
                       
        "Go take the temperature of the particles at the good heights"
        execfile("getTemperature.py")
        
tableTemperaturesCelsius = tableTemperatures - 273.15

"Plot the results"
"Control of sizes in all the file"
SMALL_SIZE = 20
MEDIUM_SIZE = 30
BIGGER_SIZE = 40

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
#plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

"""
fig = plt.figure()
ax = plt.subplot(111)
colors=['b', 'g', 'r', 'c', 'm', 'k', 'y','b', 'g', 'r', 'c', 'm']
#symbs=['o', 'v', 's', 'p', 'D', '^', '1','o', 'v', 's', 'p', 'D', '^', '1']
for i in range(nbThermo):
    plt.plot(timeVector, tableTemperatures[i,:], marker='o', color=colors[i], label= 'Thermo %d' %(i+1))
    #plt.plot(timeVector, tableTemperatures[i,:], marker='v', color='g', linestyle='-') 
plt.legend(loc = 0, numpoints = 1)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

"""
fig = plt.figure()
ax = plt.subplot(111)
colors=['orange','b', 'g', 'r', 'c', 'm', 'k', 'y','b', 'g', 'r', 'c', 'm']
symbs=['o', 'v', 's', 'p', 'D', '^', '1','o', 'v', 's', 'p', 'D', '^', '1']
for i in range(nbThermo):
    plt.plot(timeVector, tableTemperaturesCelsius[i,:], marker='o', color=colors[i], label= 'Thermo %d (z=%.3f m)' %((i+1),heightsVector[i]))
    #plt.plot(timeVector, tableTemperaturesCelsius[i,:], marker=symbs[i], color='r', linestyle='-') 
plt.legend(loc = 0, numpoints = 1)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

"""
fig = plt.figure(2)
plt.plot(heightsVector,tableTemperaturesCelsius[:,0], linestyle='', marker='s', color='r')
"""