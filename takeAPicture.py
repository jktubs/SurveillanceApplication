#!/usr/bin python

print "\nTaking a picture ... "

#https://www.raspberrypi.org/documentation/usage/camera/python/README.md

#import picamera
from imports_and_helper import *

from skimage import io
from skimage.data import data_dir
from skimage.util import img_as_ubyte
from skimage.util import img_as_int
#from skimage.util import img_as_uint
#import numpy
#from skimage.morphology import erosion, dilation, opening, closing, white_tophat
#from skimage.morphology import black_tophat, skeletonize, convex_hull_image
#from skimage.morphology import disk
#import time
#import picamera
#import os
#import datetime
#import fileinput
#import sys

def readInImage(path):
    #image = img_as_int(io.imread(path, as_grey=True))
    image = io.imread(path)
    return image

def setPixelNeighborhood(img, x, y, neighborPixel_x, neighborPixel_y):
    height, width, dim = img.shape
    print "width = %d, height = %d, dim = %d" %(width, height, dim)
    
    for i in range(x, x+neighborPixel_x):
        for j in range(y, y+neighborPixel_y):
            if (i < width) and (j < height):
                img[j,i] = [255, 255, 255] # set the colour white

try:
    camera = picamera.PiCamera()
    camera.resolution = (1920, 1440)
    camera.framerate = 30

    path_image_to_take = '/var/www/images/currentImage/currentImage_org.jpg'
    camera.capture(path_image_to_take)

    image = readInImage(path_image_to_take)
    #set markers for window calibration
    setPixelNeighborhood(image,  620,  300, 20, 20) #1920x1440
    setPixelNeighborhood(image, 1350,  300, 20, 20) #1920x1440
    setPixelNeighborhood(image,  640,  735, 20, 20) #1920x1440
    setPixelNeighborhood(image, 1300, 1065, 20, 20) #1920x1440
    io.imsave('/var/www/images/currentImage/currentImage.jpg', image)

finally:
    print "finally camera.close()"
    camera.close()