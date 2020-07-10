# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 14:33:50 2018

@author: ChristineB.local

This script calculates a RSD and a RSDr
This script must be ran AFTER the reading of dump files, because it needs 
    variables such as nbPart

This code calculates the RSD in time like (Lemieux, 2007) and Bahman (exp)
but I added that every sample is weighted with the space occupied by
particles in each cell

The domain is divided in cartesian rectangles

    
N : number of samples
m : number of particles per sample
"""
import numpy as np
import os
import matplotlib.pyplot as plt
import sys
from scipy import stats
import math


"Initialize empty structures"
timeVector = np.array([])
rsdRandomVector = np.array([])
rsdVector = np.array([])
angleVector = np.array([])
angleDifference = np.array([])
criterionAngle = 0

"Faire une liste de tous les fichiers dump dans le dossier à l'étude"
dossier=input('Enter the directory containing the dump files (between "): ') 
listeDeFichiers=os.listdir(dossier)
nbFichiersOriginal = len(listeDeFichiers)
print ("There are %d files in that folder." %nbFichiersOriginal)
skip = int(raw_input("You want to compute one dump file on how many? "))
newList = listeDeFichiers[0::skip]
rotatePart = raw_input('Do you want to calculate the angle and rotate the geometry? (y/n) ')

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
        #heatFlux = donnees[:,18]
        
        minX = min(positionxyz[:,0])
        maxX = max(positionxyz[:,0])
        minY = min(positionxyz[:,1])
        maxY = max(positionxyz[:,1]) 
        minZ = min(positionxyz[:,2])
        maxZ = max(positionxyz[:,2])        
        
        if index == 0: #Things to do for the FIRST dump
            timestep = float(raw_input("What is the timestep of your simulation? (in seconds) : "))

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
            
            drumRadius = float(raw_input("What is the drum radius? (in m) : "))
            drumDiameter = drumRadius*2
            RPM = float(raw_input("What is the drum rotating speed? (in RPM) : "))
            RPS = RPM/60            
            
            go = str(raw_input("Are you ready to continue? (y/n) "))
            if go == 'n':
                sys.exit('Not ready. You''ll have to start again')
            print ""
            
            "Create the mesh"
            nbCellsX = int(raw_input("In how many cells do you want to split the x dimension? "))
            nbCellsY = int(raw_input("In how many cells do you want to split the y dimension? "))
            nbCellsZ = int(raw_input("In how many cells do you want to split the z dimension? "))
            
            "Create the big box and discretize the domain in small boxes"
            xLength = drumDiameter
            zLength = drumDiameter
            yLength = (maxY + minRadius) #- (minY - maxRadius)
            
            cellLengthX = xLength/nbCellsX
            cellLengthY = yLength/nbCellsY
            cellLengthZ = zLength/nbCellsZ
            cellVolume = cellLengthX*cellLengthY*cellLengthZ
            
            print ("")
            print ("*****Info on the grid*****")
            print ("Your grid will have %d by %d by %d cells in x, y and z.") %(nbCellsX, nbCellsY, nbCellsZ)
            print ("The dimensions of each cell will be [%.4f by %.4f by %.4f]m in [x,y,z].") %(cellLengthX, cellLengthY, cellLengthZ)
            
            minXbox = -drumRadius
            maxXbox = drumRadius
            minZbox = -drumRadius
            maxZbox = drumRadius
            minYbox = 0 #minY
            maxYbox = maxY + minRadius
            
        "Décortiquer le nom du fichier à l'étude"
        b=file.split('_')
        b=b[1].split('.')
        iteration=int(b[0])
        timeSim = iteration * timestep
        timeVector = np.append(timeVector,timeSim)

        #Return to main directory to have access to other output scripts
        os.chdir("..")
        
        if rotatePart=='y':
            if criterionAngle < 20 : #5        
                "Calculate the angle of rotation"        
                execfile("calculateAngle.py")
            else:
                meanDynAngle = np.mean(angleVector[-5:])
                angleVector = np.append(angleVector, meanDynAngle)
            "Rotate the position vectors"
            execfile("applyRotation.py")
        
        
        "Calculate the RSD"
        print ("")
        print ("At time %.2fs ") %timeSim
        countType1 = np.zeros((nbCellsX, nbCellsY, nbCellsZ), dtype=int)
        countType2 = np.zeros((nbCellsX, nbCellsY, nbCellsZ), dtype=int)
        lastCellX = False
        lastCellY = False
        lastCellZ = False
        for cellIndexX in range(nbCellsX):
            for cellIndexY in range(nbCellsY):
                for cellIndexZ in range(nbCellsZ):
                    if (cellIndexX == (nbCellsX - 1)): #last cell in X
                        lastCellX = True
                    if (cellIndexY == (nbCellsY - 1)): #last cell in X
                        lastCellY = True
                    if (cellIndexZ == (nbCellsZ - 1)): #last cell in X
                        lastCellZ = True                            
                    lowLimitX = minXbox + (cellIndexX*cellLengthX)
                    highLimitX = minXbox + (cellIndexX+1) * cellLengthX
                    lowLimitY = minYbox + (cellIndexY*cellLengthY)
                    highLimitY = minYbox + ((cellIndexY+1) * cellLengthY)
                    lowLimitZ = minZbox + (cellIndexZ*cellLengthZ)
                    highLimitZ = minZbox + ((cellIndexZ+1) * cellLengthZ)
                    
                    booleanX = np.zeros(nbPart, dtype=bool)
                    booleanY = np.zeros(nbPart, dtype=bool)
                    booleanZ = np.zeros(nbPart, dtype=bool)
                    
                    #Check which particles fit the x-coordinates
                    for particle, position in enumerate(positionxyz[:,0]):
                        if lastCellX & (position >= lowLimitX) & (position <= highLimitX):
                            booleanX[particle]='True'
                        elif (position >= lowLimitX) & (position < highLimitX):
                            booleanX[particle]='True'                            
                    #Check which particles fit the y-coordinates
                    for particle, position in enumerate(positionxyz[:,1]):
                        if lastCellY & (position >= lowLimitY) & (position <= highLimitY):
                            booleanY[particle]='True'
                        elif (position >= lowLimitY) & (position < highLimitY):
                            booleanY[particle]='True'
                    #Check which particles fit the z-coordinates
                    for particle, position in enumerate(positionxyz[:,2]):
                        if lastCellZ & (position >= lowLimitZ) & (position <= highLimitZ):
                            booleanZ[particle]='True'
                        elif (position >= lowLimitZ) & (position < highLimitZ):
                            booleanZ[particle]='True'
                    #Check which particles are in that cell and split between the types
                    booleanTot = booleanX & booleanY & booleanZ
                    nbPartCell = sum(booleanTot)
                    #print ("There are %d particle in the cell (%d,%d,%d).") %(nbPartCell, cellIndexX, cellIndexY, cellIndexZ)
                    boolType1Cell = booleanTot & boolType1
                    boolType2Cell = booleanTot & boolType2
                    nbPart1Cell = sum(boolType1Cell)
                    nbPart2Cell = sum (boolType2Cell)
                    countType1[cellIndexX,cellIndexY,cellIndexZ] = nbPart1Cell
                    countType2[cellIndexX,cellIndexY,cellIndexZ] = nbPart2Cell
                   
        #Calculate the global mass concentration of particles
        volumeTotType1 = nbType1 * volume1
        volumeTotType2 = nbType2 * volume2
        volumeTotSystem = volumeTotType1 + volumeTotType2
        massTotType1 = volumeTotType1 * density1
        massTotType2 = volumeTotType2 * density2
        massTotSystem = massTotType1 + massTotType2
        globalMassConcentration = massTotType1/massTotSystem
                    
        #Convert the number of particles in volumes
        #These variables are arrays representing the matrix of cells
        countTot = countType1 + countType2
        volumeType1 = countType1*volume1
        volumeType2 = countType2*volume2
        volumeTot = volumeType1+volumeType2
        volumeWeight = volumeTot/cellVolume
        volumeWeightVector = np.array([])
        for eachVolume in np.nditer(volumeWeight):
            volumeWeightVector = np.append(volumeWeightVector, eachVolume)
        
        #Convert the volumes in mass
        massType1 = volumeType1*density1
        massType2 = volumeType2*density2
        massTot = massType1 + massType2
        concentration = massType1/massTot
        massWeight = massTot/massTotSystem
        massWeightVector = np.array([])
        for eachMass in np.nditer(massWeight):
            massWeightVector = np.append(massWeightVector, eachMass)
    
        #Calculate the RSDr for that time (the m (nb of particles per sample) can vary)
        numberOfParticlesPerSample = np.array([])
        for item in np.nditer(countTot):
            if item != 0:
                numberOfParticlesPerSample = np.append(numberOfParticlesPerSample, item)
        averageNumberOfParticlesPerSample = np.average(numberOfParticlesPerSample)
        stdDevRandom = math.sqrt((globalMassConcentration * (1-globalMassConcentration))/averageNumberOfParticlesPerSample)
        rsdRandom = stdDevRandom / globalMassConcentration
        rsdRandomVector = np.append(rsdRandomVector, rsdRandom)
        weightedSamplesVector = numberOfParticlesPerSample/nbPart #to know the importance of each sample according to the number of particles within it
        
        #Calculate the RSD index for that time
        numberOfSamplesM = 0
        concentrationDiffSquareVector = np.array([])
        for count, item in enumerate(np.nditer(concentration)):
            if math.isnan(item): #check if the cell is empty
                sigurd=2 # a command for nothing...
            else:
                numberOfSamplesM = numberOfSamplesM + 1
                concentrationDiff = globalMassConcentration - item
                concentrationDiffSquare = concentrationDiff**2
                ponderationCoeff = volumeWeightVector[count] #weighted by VOLUME and not by number (gave too much importance to small particles)
                concentrationDiffSquareWeighted = ponderationCoeff * concentrationDiffSquare
                concentrationDiffSquareVector = np.append(concentrationDiffSquareVector, concentrationDiffSquareWeighted)
        sumOnAllSamples = sum(concentrationDiffSquareVector)
        standardDeviation = math.sqrt(sumOnAllSamples/(numberOfSamplesM-1))
        rsd = standardDeviation/globalMassConcentration    
        rsdVector = np.append(rsdVector,rsd)
        print ("The RSD is %.3f.") %rsd
      
"Plot the segregation index versus time"
SMALL_SIZE = 20
MEDIUM_SIZE = 30
BIGGER_SIZE = 30

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
#plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

fig = plt.figure()
nbRotation = timeVector * RPS
plt.plot(nbRotation, rsdVector, marker = 'o', color = 'r', label = 'RSD')
plt.plot(nbRotation, rsdRandomVector, marker = 'o', color = 'b', label = 'RSDr')
plt.xlabel('Number of rotations')
plt.ylabel('Relative Std Deviation')
plt.legend(loc = 0, numpoints=1)
plt.figtext(.3, .2, "Grid of %d x %d x %d cells." %(nbCellsX, nbCellsY, nbCellsZ))

if rotatePart=='y':
    "Plot the dynamic angle of repose"
    fig = plt.figure()
    meanGlobalDynAngle = np.mean(angleVector[-5:])
    nbRotation = timeVector * RPS
    plt.plot(nbRotation, -angleVector, marker = 'o', color = 'r')
    plt.axhline(y=-meanGlobalDynAngle)
    plt.xlabel('Number of rotations')
    plt.ylabel('(-) Angle calculated (deg)')
    plt.figtext(.2, .2, "Mean Dyn angle on the last 5 files is : %.1f degrees" %meanGlobalDynAngle)
