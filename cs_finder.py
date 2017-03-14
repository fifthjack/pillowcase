# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 21:38:09 2017

Colour Scheme generator using PIL

Python script which accepts an image as input and finds
a colour scheme from that image by creating classes of "similar" colours
sorted by popularity.

@author: Thomas
"""
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image as Im



# Select the image to be processed
im = Im.open("example2.png")

make_coarse = 0

print(im.format) # get image format (PNG, JPG, etc.)
print(im.mode) # get colour mode (RGBA, CMYK etc.)

# get all the colors in an image (handle with care, this takes a lot of memory!)
# print(im.getcolors(im.size[0]*im.size[1]))

# create pixel map [(h,w),(r,g,b,a)] for RGBA types (PNG)
pixelMap = im.load() 



# Size = Total number of pixels in the image
size = im.size[0]*im.size[1]
print(size)




# Create an array with the RGB values (0-255) for each pixel in order
# total array has a LOT of rows (millions for a megapixel image)
# Consider splitting this up nto sections if your system can't handle megahuge arrays
colorMap = np.zeros((size,3))
for ii in range(im.size[0]):
    for jj in range(im.size[1]):
        index = (im.size[1])*ii + jj
        colorMap[index] = pixelMap[ii,jj][0:3]
        #coarse graining of colours into blocks of 32/256 size for each colour
        colorMap[index] = (np.floor(colorMap[index].astype(float)/32)+0.5)*32
        # reduces possible colours to a set of 8^3 = 512 values



if make_coarse == 1:
    
    coarseMap = np.zeros((im.size[1],im.size[0],4))
    
    
    for kk in range(size):
        jj = kk % im.size[1]
        ii = (kk - jj)/im.size[1]
        coarseMap[jj,ii][0:3] = colorMap[kk]
        coarseMap[jj,ii][3] = 255
    coarseMap = np.uint8(coarseMap)
    
    
    
    
    out = Im.fromarray(coarseMap)
    out.save("out.png", "PNG")

#



coor_tuple = [tuple(x) for x in colorMap]
unique_coor = sorted(set(coor_tuple), key=lambda x: coor_tuple.index(x))
unique_count = [coor_tuple.count(x) for x in unique_coor]
unique_index = [coor_tuple.index(x) for x in unique_coor]
#print(unique_coor[0][0], unique_count[0])
#
#print(len(unique_coor))

freqMap = np.zeros((len(unique_coor),4))
for jj in range(len(unique_coor)):
    for kk in range(3):
        freqMap[jj,kk]= unique_coor[jj][kk]
        freqMap[jj,kk] = freqMap[jj,kk].astype(int)
    freqMap[jj,3] = unique_count[jj]
np.set_printoptions(suppress=True)


# A list of colours in order of increasing frequency in the image
freqMap = freqMap[freqMap[:,3].argsort()]

#
#print(freqMap[-7:-1])

Ncol = 7
# take the top 6 colours, the bottom slice of the freqMap
bottom_slice = freqMap[-(Ncol+1):-1]

# extract the frequencies
freqs = np.zeros(Ncol)
for jj in range(Ncol):
    freqs[jj] = bottom_slice[(Ncol-1-jj),3]
freqs = freqs/size # proportional of total pixels


# Consturct a bar chart
ind = np.arange(Ncol) # locations of bars
width = 0.9 # bar width


# set bar colours
#  Convert RGB numbers to hexadecimal string

# taken from StackOverflow, shamelessly stolen
# http://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)
barcolour = ([""]*Ncol)
for jj in range(Ncol):
    red = bottom_slice[(Ncol-1-jj),0]
    green = bottom_slice[(Ncol-1-jj),1]
    blue = bottom_slice[(Ncol-1-jj),2]
    
    barcolour[jj] = rgb_to_hex(red, green,blue)


fig, ax = plt.subplots()
rects1 = ax.bar(ind, freqs, width, color=barcolour)


ax.set_ylabel('Frequency')
ax.set_title('Top colours in the image, sorted by occurence')
ax.set_xticks(ind + width / 2)




plt.show()

##    
