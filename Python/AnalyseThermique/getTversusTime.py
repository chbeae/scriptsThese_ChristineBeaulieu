# -*- coding: utf-8 -*-
"""
Created on Wed May 20 22:26:14 2020

*****************HARD-CODED VARIABLES*************************
drumDiameter, cp1, cp2, timestep, dump


This script calculates and plots the total average temperature of the drum
versus time.
The script will ask you for these two next options:
This script can also calculate and plot the radial distribution of the 2 types of particles
in the drum (only once at the first time step)
It can also calculate and plot the average temperature per annulus versus the
adimensional radius for all the times studied.

@author: ChristineB.local
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
from scipy import stats
import math

print ""
print "Hello! This script reads data from dump files created from LIGGGHTS."
print ""
print "WARNING!!! The particles in dump files must be ordered by ID!!"

"Initialize empty structures"
timeVector = np.array([])
meanTempVector = np.array([])
meanTvolumeVector = np.array([])
meanTinertiaVector = np.array([])
meanTinertiaVolVector = np.array([])

"Faire une liste de tous les fichiers dump dans le dossier à l'étude"
#dossier=input('Enter the directory containing the dump files (between "): ') 
dossier = 'dump'
listeDeFichiers=os.listdir(dossier)
nbFilesRaw = len(listeDeFichiers)
print ("There are %d files in that folder.") %nbFilesRaw
skip = int(raw_input("You want to compute one dump file on how many? "))
newList = listeDeFichiers[0::skip]
nbFiles = len(newList)
calculateRadial = raw_input('Do you want to calculate the radial temperature and distribution? (y/n) ')
calculateTempZ = raw_input('Do you want to calculate the temperature profile in Z (versus the depth)? (y/n) ')
calculateTempSpecific = raw_input('Do you want to calculate the evolution of T at a specific position? (y/n) ')
calculateT1T2Diff = raw_input('Do you want to calculate the difference of temperature between types 1 and 2? (y/n) ')

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
        #vitessexyz=donnees[:,5:8]
        #forcexyz=donnees[:,8:11]
        #omegaxyz=donnees[:,11:14]
        radius=donnees[:,14]
        density=donnees[:,15]
        radialPos=donnees[:,16]
        temp = donnees[:,17]
        #heatFlux = donnees[:,17]
        
        
        minX = min(positionxyz[:,0])
        maxX = max(positionxyz[:,0])
        minY = min(positionxyz[:,1])
        maxY = max(positionxyz[:,1]) 
        minZ = min(positionxyz[:,2])
        maxZ = max(positionxyz[:,2])
        
        if index == 0: #Things to do for the FIRST dump
#            footer = len(donnees)
#            header = np.genfromtxt(file, skip_header=3, skip_footer=footer+7, usecols=0, dtype = str)
            #timestep = header.split('_')
#            print "For that simulation, the timestep is :"
#            print header
            #timestep = float(raw_input("What is the timestep of your simulation? (in seconds) : "))
            timestep = 1.0
            #drumDiameter = float(raw_input("What is the drum diameter? (in m) : "))
            drumDiameter = 0.24
            drumRadius = drumDiameter/2.
            #cp1 = float(raw_input("What is the heat capacity of type 1? (in J/kg.K) : "))
            cp1 = 896.0
            #cp2 = float(raw_input("What is the heat capacity of type 1? (in J/kg.K) : "))
            cp2 = 840
            
            if calculateRadial == "y":
                "Info on the drum and on the domain discretization"
                nbAnnuli = int(raw_input("In how many annuli do you want to discretize your drum? "))
                annulusWidth = drumRadius/nbAnnuli
                print ("Each annulus has a width of %.4fm.") %annulusWidth 
                scaledRadius = np.arange(nbAnnuli)
                scaledRadius = (scaledRadius*annulusWidth) 
                scaledRadius = scaledRadius + (annulusWidth/2)
                scaledRadius = scaledRadius/drumRadius
                "Initialize some arrays"
                radialTempTime = np.zeros((nbAnnuli,nbFiles))
                radialTempInertiaTime = np.zeros((nbAnnuli,nbFiles))
                radialTempInertiaVolTime = np.zeros((nbAnnuli,nbFiles))
                
            if calculateTempZ == "y":
                "Info on the discretization"
                nbPaquets = int(raw_input("In how many packages do you want to discretize your drum diameter? "))
                paquetWidth = drumDiameter/nbPaquets
                zTempTime = np.zeros((nbPaquets,nbFiles))
                zMiddleVector = np.zeros(nbPaquets)
                zTempInertiaVolTime = np.zeros((nbPaquets,nbFiles))

            if calculateTempSpecific == "y":
                "Info on the discretization"
                xPosi = float(raw_input("What is the X position? (in m) "))
                yPosi = float(raw_input("What is the Y position? (in m) "))
                zPosi = float(raw_input("What is the Z position? (in m) "))
                tempSpeciVector = np.zeros(nbFiles)
                tempSpeciVolumeVector = np.zeros(nbFiles)
                tempSpeciInertiaVector = np.zeros(nbFiles)
                
            if calculateT1T2Diff == "y":
                temp1Vector = np.zeros(nbFiles)
                temp2Vector = np.zeros(nbFiles)
                tempDiffVector = np.zeros(nbFiles)
            
            minRadius = min(radius)
            maxRadius = max(radius)
            minDiameter = 2*minRadius
            maxDiameter = 2*maxRadius
            nbPart = len(ID)
            nbType = max(type_part)
            Tini = min(temp)
            cpVector = np.zeros(nbPart)
            for indexAB, typep in enumerate(type_part):
                if (typep == 1.0):
                    cpVector[indexAB] = cp1
                elif (typep == 2.0):
                    cpVector[indexAB] = cp2
            
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
                vol1Tot = volume1*nbType1
                vol2Tot = volume2*nbType2
                volTot = vol1Tot + vol2Tot
                xvol1 = vol1Tot / volTot
                xvol2 = vol2Tot / volTot
                mass1 = volume1 * density1
                mass2 = volume2 * density2
                mass1Tot = mass1 * nbType1
                mass2Tot = mass2 * nbType2
                massTot = mass1Tot + mass2Tot
                xmass1 = mass1Tot / massTot
                xmass2 = mass2Tot / massTot
                
#        "Get the norm of the velocities"
#        vitesse = np.zeros((len(vitessexyz),1))
#        for row in range(len(vitessexyz)):
#            vitesse[row,0] = np.linalg.norm(vitessexyz[row,:])
#        if nbType > 1:
#            vitesseType1 = vitesse[boolType1]
#            vitesseType2 = vitesse[boolType2]


            
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
        
        "Get some information about the temperature of all particles in the drum"
        meanTemp=np.mean(temp)
        meanTempVector = np.append(meanTempVector, meanTemp)
        maxTemp=np.max(temp)
        minTemp=np.min(temp)
        
        "Volume averaged"
        volume = (4*math.pi*(radius**3))/3. #vector of all particles
        sumVolumeT = 0
        for iT, tempera in enumerate(temp):
            product = tempera * volume[iT]
            sumVolumeT = sumVolumeT + product
        meanTvolume = sumVolumeT/(sum(volume))
        meanTvolumeVector = np.append(meanTvolumeVector, meanTvolume)
        
        "Inertia tempearture"
        rhoCpT = density * cpVector * temp
        rhoCp = density * cpVector
        sum_rhoCpT = sum(rhoCpT)
        sum_rhoCp = sum(rhoCp)
        averageTinertia = sum_rhoCpT / sum_rhoCp
        meanTinertiaVector = np.append(meanTinertiaVector, averageTinertia)
        
        "Inertia volume temperature"
        rhoCpVT = density * cpVector * volume * temp
        rhoCpV = density * cpVector * volume
        sum_rhoCpVT = sum(rhoCpVT)
        sum_rhoCpV = sum(rhoCpV)
        averageTinertiaV = sum_rhoCpVT / sum_rhoCpV
        meanTinertiaVolVector = np.append(meanTinertiaVolVector, averageTinertiaV)        

        print 'The mean temperature is %.2f K.' %meanTemp
        print 'The maximum temperature is %.2f K.' %maxTemp
        print 'The minimum temperature is %.2f K.' %minTemp
        
        if (index==0) & (calculateRadial=="y"):
            "Get the radial distribution of types 1 and 2"
            execfile("radialDistribution.py")        
        
        if calculateRadial=="y":
            "Get the radial temperature"
            execfile("radialDistributionTemp.py")
    
        if calculateTempZ=="y":
            "Get the radial temperature"
            execfile("profilT_inZ.py")

        if calculateTempSpecific=="y":
            execfile("profilT_specific.py")
            
        if calculateT1T2Diff == "y":
            execfile("differenceT1_T2.py")
        
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

colors=['b', 'g', 'r', 'c', 'm', 'k', 'y', "orange","darkgreen","coral","fuchsia", \
"gold","gray","plum","turquoise","b","g","r","c","m","y","b","orange","darkgreen", \
"coral","fuchsia", "gold","gray","plum","turquoise", 'b', 'g', 'r', 'c', 'm', 'k', \
'y', "orange","darkgreen","coral","fuchsia", \
"gold","gray","plum","turquoise","b","g","r","c","m","y","b","orange","darkgreen", \
"coral","fuchsia", "gold","gray","plum","turquoise", 'b', 'g', 'r', 'c', 'm', 'k', \
'y', "orange","darkgreen","coral","fuchsia", \
"gold","gray","plum","turquoise","b","g","r","c","m","y","b","orange","darkgreen", \
"coral","fuchsia", "gold","gray","plum","turquoise", 'b', 'g', 'r', 'c', 'm', 'k', \
'y', "orange","darkgreen","coral","fuchsia", \
"gold","gray","plum","turquoise","b","g","r","c","m","y","b","orange","darkgreen", \
"coral","fuchsia", "gold","gray","plum","turquoise", 'b', 'g', 'r', 'c', 'm', 'k', \
'y', "orange","darkgreen","coral","fuchsia", \
"gold","gray","plum","turquoise","b","g","r","c","m","y","b","orange","darkgreen", \
"coral","fuchsia", "gold","gray","plum","turquoise", 'b', 'g', 'r', 'c', 'm', 'k', \
'y', "orange","darkgreen","coral","fuchsia", \
"gold","gray","plum","turquoise","b","g","r","c","m","y","b","orange","darkgreen", \
"coral","fuchsia", "gold","gray","plum","turquoise", 'b', 'g', 'r', 'c', 'm', 'k', \
'y', "orange","darkgreen","coral","fuchsia", \
"gold","gray","plum","turquoise","b","g","r","c","m","y","b","orange","darkgreen", \
"coral","fuchsia", "gold","gray","plum","turquoise", 'b', 'g', 'r', 'c', 'm', 'k', \
'y', "orange","darkgreen","coral","fuchsia", \
"gold","gray","plum","turquoise","b","g","r","c","m","y","b","orange","darkgreen", \
"coral","fuchsia", "gold","gray","plum","turquoise"]
symbs = ["o","v","^","<",">","s","1","2","3","4","x","o","v","^","<",">","s",\
"1","2","3","4","x","o","v","^","<",">","s","1","2","3","4","x", "o","v","^",\
"<",">","s","1","2","3","4","x","o","v","^","<",">","s",\
"1","2","3","4","x","o","v","^","<",">","s","1","2","3","4","x",\
"o","v","^","<",">","s","1","2","3","4","x","o","v","^","<",">","s",\
"1","2","3","4","x","o","v","^","<",">","s","1","2","3","4","x", "o","v","^",\
"<",">","s","1","2","3","4","x","o","v","^","<",">","s",\
"1","2","3","4","x","o","v","^","<",">","s","1","2","3","4","x",\
"o","v","^","<",">","s","1","2","3","4","x","o","v","^","<",">","s",\
"1","2","3","4","x","o","v","^","<",">","s","1","2","3","4","x", "o","v","^",\
"<",">","s","1","2","3","4","x","o","v","^","<",">","s",\
"1","2","3","4","x","o","v","^","<",">","s","1","2","3","4","x",\
"o","v","^","<",">","s","1","2","3","4","x","o","v","^","<",">","s",\
"1","2","3","4","x","o","v","^","<",">","s","1","2","3","4","x", "o","v","^",\
"<",">","s","1","2","3","4","x","o","v","^","<",">","s",\
"1","2","3","4","x","o","v","^","<",">","s","1","2","3","4","x"]

fig = plt.figure()
plt.plot(timeVector, meanTempVector, marker = 'o', color = 'r', label='Average')
plt.plot(timeVector, meanTvolumeVector, marker = 'o', color = 'b', label='Volume Average')
plt.plot(timeVector, meanTinertiaVector, marker = 'o', color = 'g', label='Inertia Average')
plt.plot(timeVector, meanTinertiaVolVector, marker = 'o', color = 'm', label='Inertia Vol Average')
plt.xlabel('Time (s)')
plt.ylabel('Globa mean temperature (K)')
plt.legend(loc = 0, numpoints=1)

if calculateRadial=="y":
    fig = plt.figure()
    for ii in range(nbFiles):
        plt.plot(scaledRadius, radialTempTime[:,ii], marker = symbs[ii], \
        color = colors[ii], markersize=8, label = 'Time =%.0fs'%timeVector[ii])
        plt.plot(scaledRadius, radialTempInertiaTime[:,ii], marker = symbs[ii], \
        color = colors[ii], markersize=8, label = 'Time =%.0fs'%timeVector[ii])        
    plt.xlabel('Scaled Radius ($r/R_{drum}$)')
    plt.ylabel('Mean Temperature (K)')
    plt.legend(loc = 0, numpoints=1)
    
if calculateTempZ=="y":
    fig = plt.figure(10)
    for ii in range(nbFiles):
        plt.plot(zMiddleVector, zTempTime[:,ii], marker = symbs[ii], \
        color = colors[ii], markersize=8, label = 'Time =%.0fs'%timeVector[ii])
        plt.plot(zMiddleVector, zTempInertiaVolTime[:,ii], marker = symbs[ii], \
        color = colors[ii], markersize=8, label = 'Time =%.0fs'%timeVector[ii])
    plt.xlabel('z (m)')
    plt.ylabel('Mean Temperature (K)')
    plt.legend(loc = 0, numpoints=1)

if calculateTempSpecific == "y":
    fig = plt.figure()
    plt.plot(timeVector, tempSpeciVector, marker= 'o', color = 'r', label='Average' )
    plt.plot(timeVector, tempSpeciVolumeVector, marker= 'o', color = 'b', label='Volume Average' )
    plt.plot(timeVector, tempSpeciInertiaVector, marker= 'o', color = 'g', label='Inertia Average' )
    plt.xlabel('Time (s)')
    plt.ylabel('Specific mean Temperature (K)')
    plt.figtext(.3, .2, "Position is (%.3f ; %.3f ; %.3f) m" %(xPosi, yPosi, zPosi))
    plt.legend(loc = 0, numpoints=1)
    
if calculateT1T2Diff == "y":
    fig = plt.figure()
    plt.plot(timeVector, tempDiffVector, marker= 'o', color = 'b', label = 'Absolute difference' )
    plt.plot(timeVector, temp1Vector, marker= 'o', color = 'r' , label = 'Type 1')
    plt.plot(timeVector, temp2Vector, marker= 'o', color = 'g' , label = 'Type 2')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (K)')
    plt.legend(loc = 0, numpoints=1)

    
    