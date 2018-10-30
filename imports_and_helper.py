from skimage import io
from skimage.data import data_dir
from skimage.util import img_as_ubyte
from skimage.util import img_as_int
import numpy
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
from skimage.morphology import black_tophat, skeletonize, convex_hull_image
from skimage.morphology import disk
import time
import picamera
import os
import shutil
import datetime
import fileinput
import sys
import logging
import traceback

import io
import time
import threading
import picamera
from PIL import Image, ImageMath
from skimage import io as skimageio
import numpy

def copyFilesWorker(e, t):
    try:
        """Wait t seconds and then timeout"""
        doExit = False
        LOGFILE = '/media/usb/images/logfileCopyFilesWorker.txt'
        print "check path" 
        if os.path.isfile(LOGFILE):
            print "exists"
            backupFile = LOGFILE + '%s.txt' %(datetime.date.today())
            print backupFile
            os.rename(LOGFILE, backupFile) 
        logfile = open(LOGFILE, 'a')
        logfile.write('CopyFilesWorker:\n')
        while not doExit:
            logfile.write('wait_for_event_timeout starting:\n')
            logging.debug('wait_for_event_timeout starting')
            event_is_set = e.wait(t)
            logging.debug('event set: %s', event_is_set)
            if event_is_set:
                logging.debug('processing event')
                logfile.write('processing event\n')
                doExit = True
            else:
                logging.debug('Check if files to be copied are available.')
                logfile.write('Check if files to be copied are available.\n')
                src_files = os.listdir(path_in)
                for file_name in src_files:
                    full_file_name = os.path.join(path_in, file_name)
                    if (os.path.isfile(full_file_name) and not os.path.exists(os.path.join(path_out, file_name))):
                        logging.debug('copy ' + file_name)
                        logfile.write('copy ' + file_name + '\n')
                        #shutil.copyfile(full_file_name, path_out)
                        shutil.copyfile(full_file_name, os.path.join(path_out, os.path.basename(full_file_name)))
        logging.debug('Leaving copyFilesWorker()')
        logfile.write('Leaving copyFilesWorker()\n')
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        msg = ''.join('!! ' + line for line in lines)
        print "Unexpected error in copyFilesWorker(): ", msg
        logfile.write(msg)
    finally:
        logfile.write("finally statement copyFilesWorker() reached.")
        logfile.close()

def setPixelNeighborhood(img, x, y, neighborPixel_x, neighborPixel_y):
    width, height = img.size
    pixels = img.load() # create the pixel map
    
    for i in range(x, x+neighborPixel_x):
        for j in range(y, y+neighborPixel_y):
            if (i < width) and (j < height):
                pixels[i,j] = (255, 255, 255) # set the colour white

def maskBackground(img, x, y, neighborPixel_x, neighborPixel_y):
    width, height = img.size
    pixels = img.load() # create the pixel map
    
    for i in range(width):
        for j in range(height):
            if ( (i > x) and (i < (x+neighborPixel_x)) and (j > y) and (j < (y+neighborPixel_y)) ):
                pass
            else:
                pixels[i,j] = (255, 255, 255) # set the colour white


    
