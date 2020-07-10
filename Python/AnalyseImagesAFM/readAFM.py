# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 15:02:31 2020

@author: ChristineB.local

This script aims to read the images from AFM and calculate a roughness
and estimate a parameter m

grayscale : [0 to 2055]

https://www.hackerearth.com/fr/practice/notes/extracting-pixel-values-of-an-image-in-python/

Watch out to be in the good folder (by clicking play up there) to be able
to read the image
"""

from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
#import matplotlib.image as mpimg
#from skimage import io
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy import ndimage
import sys



im = Image.open("VERRE_2mm_50_TOPO.tif", "r") #read the image
im_gray = im.convert("LA") #convert to gray scale

#Show the original image
fig=plt.figure()
imgplot = plt.imshow(im)

#Show the gray image
fig=plt.figure()
imgplot = plt.imshow(im_gray)

#sys.exit('First step')

im_gray_crop = im_gray.crop((10,95,657,742)) #left, top, right, bottom. verre2mm
#im_gray_crop = im_gray.crop((12,97,658,743)) #left, top, right, bottom
#im_gray_crop = im_gray.crop((13,7,268,262)) #left, top, right, bottom. alu10_2e image
#im_gray_crop = im_gray.crop((10,95,657,742)) #left, top, right, bottom. alu2mm
width, height = im_gray_crop.size

minHeight = -250.0 #-663.6 #-750 #-250
maxHeight = 250.0 #664.1 #750.0 #250
rangeHeights = maxHeight - minHeight
rangeGray = 255.0
scaleWindow = 50000.0 #50um (50 000 nm)

#Show the crop image
fig=plt.figure()
imgplot = plt.imshow(im_gray_crop)

pixels = np.array([])
for i in range(0, width):
    for j in range(0, height):
        pixel = im_gray_crop.getpixel((i,j))[0]
        pixels = np.append(pixels, pixel)
        #total += im_grey.getpixel((i,j))[0]
pixelsMatrix = np.resize(pixels,(width,height))
pixelsMatrix = np.transpose(pixelsMatrix)


heights = (rangeHeights/rangeGray)*pixels + minHeight 
heightsMatrix = np.resize(heights,(width,height))
heightsMatrix = np.transpose(heightsMatrix)


X = np.arange(0, width, 1)
Y = np.arange(0, height, 1)
X, Y = np.meshgrid(X, Y)

#Plot the surface in 3D
fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, heightsMatrix, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
# Customize the z axis.
ax.set_zlim(0, 255)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

#Show a color map of the heights
fig = plt.figure()
plt.imshow(heightsMatrix)
plt.colorbar(orientation='vertical')
plt.xlabel('x')
plt.ylabel('y')

"Get the surface parameters"
averageH = np.mean(heights)
heightsZi = heights - averageH
Rq = np.sqrt(np.sum(heightsZi**2)/len(heightsZi))
Ra = (np.sum(np.abs(heightsZi))) / len(heightsZi)
Rv = np.abs(min(heights)) #Maximum valley depth
Rp = max(heights) #Maximum peak height
Rz = Rv + Rp #Maximum height of the profile

"Make an histogram of the heights"
fig=plt.figure()
plt.hist(heights, bins=100)
plt.xlabel('Surface roughness $\sigma$ $(\mu m)$')
plt.ylabel('Number of pixels')
plt.axvline(x=averageH, color='r', linewidth=2, label='Average')
plt.legend()

stdDev = np.std(heights)
relStdDev = stdDev/np.abs(averageH)
mJamal = 1.0/relStdDev

print ("")
print ("The average height is %.1f nm.") %averageH
print ("Rq is : %.1f nm.") %Rq
print ("Ra is : %.1f nm.") %Ra
print ("Rv (max valley depth) is : %.1f nm.") %Rv
print ("Rp (max peak height) is : %.1f nm.") %Rp
print ("Rz (max height of the profile (Rv+Rp)) is : %.1f nm.") %Rz
print ("The inverse of the standard deviation of the heights is %.2e.") %mJamal


"Plot different surface profiles in 2D"
fig=plt.figure()
xVec = range(width)
plt.plot(xVec, heightsMatrix[0,:])
plt.plot(xVec, heightsMatrix[50,:])
plt.plot(xVec, heightsMatrix[100,:])
plt.plot(xVec, heightsMatrix[150,:])
plt.plot(xVec, heightsMatrix[200,:])
plt.plot(xVec, heightsMatrix[250,:])
plt.plot(xVec, heightsMatrix[300,:])
plt.plot(xVec, heightsMatrix[350,:])
plt.plot(xVec, heightsMatrix[400,:])
plt.plot(xVec, heightsMatrix[450,:])


#"Make an histogram of the heights"
#fig=plt.figure()
#plt.hist(heightsGlass, bins=100, color='b', label='Glass')
#plt.hist(heightsSteel, bins=100, color='r', label='Steel')
#plt.hist(heightsAlu, bins=100, color='g', label='Alu')
#plt.legend(loc = 0, numpoints = 1)
#plt.xlabel('Surface roughness $\sigma$ $(\mu m)$')
#plt.ylabel('Number of pixels')

"Get the gradients to calculte the surface slope"
#Get the global gradient
spacing = scaleWindow/width
[sx, sy] = np.gradient(heightsMatrix, spacing)
sGrad = np.hypot(sx, sy)


#Show the contour
fig=plt.figure()
imsx = plt.imshow(sGrad)
plt.colorbar(orientation='vertical')

#Calculate m
thetaMatrix = np.arctan(sGrad)
averageTheta = np.mean(thetaMatrix)
averageThetaDegree = averageTheta * (360.0/(2.0*np.pi))
m = (np.sqrt(2.0/np.pi)) * np.tan(averageTheta)

print ("m calculated with the gradient is %.2e") %m
