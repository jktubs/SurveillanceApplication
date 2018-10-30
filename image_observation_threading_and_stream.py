#!/usr/bin python

from imports_and_helper import *

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
global counter
counter = 0
global logfile
global PHP_SCRIPT
global path_in

path_in = '/var/www/images/default'
global path_out
path_out = '/var/www/images/default'
global e
e = threading.Event()
                
def wait(image1, filename_current, image0, filename_last):
    print"\n%s\n" %(time.ctime())
    diffable = True

    if(diffable):
        #print "Start calculate diff"
        start = time.clock()
        #diff = numpy.absolute(image1 - image0)
        #image1_cropped = image1.crop((560, 210, 1020, 560)) #1280x960
        #image0_cropped = image0.crop((560, 210, 1020, 560)) #1280x960
        #image1_cropped = image1.crop((540, 30, 2230, 1460)) #2592x1944
        #image0_cropped = image0.crop((540, 30, 2230, 1460)) #2592x1944
        width, height = image1.size
        print "width = %d, height = %d" %(width, height)
        image1_cropped = image1.crop((395, 5, 1640, 1080)) #1920x1440
        image0_cropped = image0.crop((395, 5, 1640, 1080)) #1920x1440
        width, height = image1_cropped.size
        print "width_cropped = %d, height_cropped = %d" %(width, height)
        diff = numpy.array(ImageMath.eval('abs(int(a) - int(b))', a=image1_cropped, b=image0_cropped))
        #diff = numpy.array(ImageMath.eval('abs(int(a) - int(b))', a=image1, b=image0))
        end = time.clock()
        #print "End calculate diff: %.3f s" %(end-start)
        log = "End calculate diff: %.3f s\n" %(end-start)
        logfile.write(log)
        #selem = disk(3)
        
        threshold = 100  
        start = time.clock()
        low_values_indices = diff < threshold
        diff[low_values_indices] = 0
        end = time.clock()
        log = "Thresholding took: %.3f s\n" %(end-start)
        logfile.write(log)
        
        sum = numpy.sum(diff)
        start = time.clock()
        max = numpy.amax(diff)
        end = time.clock()
        log = "Max = %d , calc took: %.3f s\n" %(max, end-start)
        logfile.write(log)
        
        log = "sum = %d\n" %sum
        logfile.write(log)
        global thereWasADiff
        if( sum > 300000 and max > 110):#45000
            start = time.clock()
            image1_cropped.save(filename_current)
            end = time.clock()
            log = "End saving %s:  %.3f s\n" %(filename_current,end-start)
            logfile.write(log)
            start = time.clock()
            image0_cropped.save(filename_last)
            end = time.clock()
            log = "End saving %s:  %.3f s\n" %(filename_last,end-start)
            logfile.write(log)
            thereWasADiff = True

                

class Config:
    runMode = ''
    active_time_start_h = ''
    active_time_start_m = ''
    active_time_stop_h = ''
    active_time_stop_m = ''
    php_script = ''
    image_folder_root = ''

def readConfigFile():
    CONFIG_FILE = '/var/www/surveillance_config.txt'
    config = Config()
    linestring = open(CONFIG_FILE, 'r').read()
    begPos = linestring.find('RUN_MODE')
    begPos = linestring.find('#', begPos) + 1
    endPos = linestring.find('#', begPos)
    config.runMode = linestring[begPos:endPos]
    begPos = linestring.find('ACTIVE_TIME_START_HOUR')
    begPos = linestring.find('#', begPos) + 1
    endPos = linestring.find('#', begPos)
    config.active_time_start_h = linestring[begPos:endPos]
    begPos = linestring.find('ACTIVE_TIME_START_MINUTES')
    begPos = linestring.find('#', begPos) + 1
    endPos = linestring.find('#', begPos)
    config.active_time_start_m = linestring[begPos:endPos]
    begPos = linestring.find('ACTIVE_TIME_STOP_HOUR')
    begPos = linestring.find('#', begPos) + 1
    endPos = linestring.find('#', begPos)
    config.active_time_stop_h = linestring[begPos:endPos]
    begPos = linestring.find('ACTIVE_TIME_STOP_MINUTES')
    begPos = linestring.find('#', begPos) + 1
    endPos = linestring.find('#', begPos)
    config.active_time_stop_m = linestring[begPos:endPos]
    begPos = linestring.find('PHP_SCRIPT')
    begPos = linestring.find('#', begPos) + 1
    endPos = linestring.find('#', begPos)
    config.php_script = linestring[begPos:endPos]
    begPos = linestring.find('IMAGE_FOLDER_ROOT')
    begPos = linestring.find('#', begPos) + 1
    endPos = linestring.find('#', begPos)
    config.image_folder_root= linestring[begPos:endPos]
    print "runMode = %s" %config.runMode
    print "active_time_start_h = %s" %config.active_time_start_h
    print "active_time_start_m = %s" %config.active_time_start_m
    print "active_time_stop_h = %s" %config.active_time_stop_h
    print "active_time_stop_m = %s" %config.active_time_stop_m
    print "php_script = %s" %config.php_script
    print "image_folder_root = %s" %config.image_folder_root
    return config
    
def ensure_dir(directory):
    if not os.path.exists(directory):
    	print 'create directory: ' + directory
        os.makedirs(directory)
        updatePhpScript()
        global PHP_SCRIPT
        #shutil.copy(PHP_SCRIPT, os.path.join(directory,"__showAllImages.php"))
        shutil.copyfile(PHP_SCRIPT, os.path.join(directory,"__showAllImages.php"))
        return False
    else:
        return True

def getFolderSize(folder, idle):
    if(idle == True):
        total_size = os.path.getsize(folder)
        for item in os.listdir(folder):
            itempath = os.path.join(folder, item)
            if os.path.isfile(itempath):
                total_size += os.path.getsize(itempath)
            elif os.path.isdir(itempath):
                total_size += getFolderSize(itempath,idle)
        return total_size
    else:
        time.sleep(0.5)
        return 0

#use this method because it does not change permission
def replace(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

        
def updatePhpScript():
    global today
    linestring = open(PHP_SCRIPT, 'r').read()
    start = linestring.find('"') + 1
    end = linestring.find('"', start)
    yesterday = linestring[start:end] #letzter eingetragener Ordner
    today = datetime.date.today()
    print "replace %s in showAllImages_php by %s" %(str(yesterday), str(today))
    global PHP_SCRIPT
    replace(PHP_SCRIPT,str(yesterday),str(today))

try:
    # Create a pool of image processors
    done = False
    lock = threading.Lock()
    pool = []
    #IMAGE_FOLDER_ROOT = '/home/pi/background_substraction/1280_960/with_threshold/'
    config = readConfigFile()
    IMAGE_FOLDER_ROOT = config.image_folder_root
    ensure_dir(IMAGE_FOLDER_ROOT)
    LOGFILE = IMAGE_FOLDER_ROOT + 'logfile.txt'
    #LOGFILE = '/home/pi/background_substraction/logfile.txt'
    
    class ImageProcessor(threading.Thread):
        def __init__(self, id):
            #print "\nImageProcessor(): __init__()"
            super(ImageProcessor, self).__init__()
            self.stream = io.BytesIO()
            self.event = threading.Event()
            self.terminated = False
            print "\nImageProcessor(id=%s): " %id
            self.id = id;
            #print "\nImageProcessor(): self.start()"
            self.start()
    
        def run(self):
            print "\nImageProcessor(): run()"
            # This method runs in a separate thread
            global done
            firstImage = True
            idle = False
            #print "\nImageProcessor(): run() self.terminated " + str(self.terminated)
            while not self.terminated:
                # Wait for an image to be written to the stream
                if self.event.wait(2):
                    try:
                        #print "\nImageProcessor(): run() self.stream.seek(0)"
                        self.stream.seek(0)
                        #print "\nImageProcessor(): run() self.stream.seek(0) DONE"
                        #content = self.stream.read()
                        print "\nid = " + str(self.id)# + ": "  + content
                        
                        measurement_begin = time.clock()
                        im = Image.open(self.stream)
                        measurement_end = time.clock()
                        log = "Image.open() took: %.3f s\n" %(measurement_end-measurement_begin)
                        logfile.write(log)
                        #setPixelNeighborhood(im, 600,   200, 10, 10)
                        #setPixelNeighborhood(im, 2300,  400, 10, 10)
                        #setPixelNeighborhood(im, 900, 900, 10, 10)
                        #setPixelNeighborhood(im, 1900, 1200, 10, 10)
                        #maskBackground(im, 340, 5, 660, 695)
                        if(firstImage==True):
                            im_old = im
                            firstImage = False
                            start_total = 0
                        #a = skimageio.Image(im)
                        #skimageio.imsave(current_image, a)
                        #im.save(current_image)

                        # Read the image and do some processing on it
                        #Image.open(self.stream)
                        #...
                        #...
                        # Set done to True if you want the script to terminate
                        # at some point
                        #done=True                        
                        config = readConfigFile()
                        RUN_MODE = config.runMode
                        global PHP_SCRIPT
                        PHP_SCRIPT = config.php_script
                        IMAGE_FOLDER_ROOT = config.image_folder_root
                        measurement_begin = time.clock()                        
                        folderSize = getFolderSize(IMAGE_FOLDER_ROOT, idle)
                        measurement_end = time.clock()
                        log = "getFolderSize() took: %.3f s\n" %(measurement_end-measurement_begin)
                        print "folderSize = %d Bytes" %(folderSize)
                        if(folderSize > 5000*1000000): #5000 MB
                            log = "Exit due to too large directory (%d Bytes)\n" %folderSize
                            logfile.write(log)
                            print log
                            done=True
                        global counter
                        CURRENT_IMAGE_FOLDER_PATH = IMAGE_FOLDER_ROOT + '%s/' %(datetime.date.today())
                        ensure_dir(CURRENT_IMAGE_FOLDER_PATH)
                        global path_in
                        path_in = CURRENT_IMAGE_FOLDER_PATH
                        global path_out
                        path_out = '/media/usb/box/Surveillance_Images/' + '%s/' %(datetime.date.today())
                        #ensure_dir(path_out)
                        last_image = CURRENT_IMAGE_FOLDER_PATH + 'image%015d.jpg' %(counter)
                        counter += 1
                        current_image = CURRENT_IMAGE_FOLDER_PATH + 'image%015d.jpg' %(counter)
                        if(RUN_MODE == 'Exit'):
                            done=True
                        runTimeBegin_h = int(config.active_time_start_h)
                        runTimeBegin_m = int(config.active_time_start_m)
                        runTimeEnd_h   = int(config.active_time_stop_h)
                        runTimeEnd_m   = int(config.active_time_stop_m)
                        now = datetime.datetime.now()
                        begin_time = datetime.datetime(now.year,now.month,now.day,runTimeBegin_h,runTimeBegin_m)
                        end_time   = datetime.datetime(now.year,now.month,now.day,runTimeEnd_h,runTimeEnd_m)
                        logfile.write(log)
                        if( (now >= begin_time) and (now <= end_time) and (RUN_MODE == 'Active')):
                            idle = False
                            wait_begin = time.clock()
                            wait(im, current_image, im_old, last_image)
                            end_total = time.clock()
                            log = "1 cycle took: %.3f s (wait(): %.3f s)\n" %(end_total-start_total, end_total-wait_begin)
                            logfile.write(log)
                            start_total = time.clock()
                        else:
                            print now
                            print " in IDLE mode"
                            idle = True
                            time.sleep(2)

                        im_old = im
                    except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                        msg = ''.join('!! ' + line for line in lines)
                        print "Unexpected error in run(): ", msg
                        logfile.write(msg)
                        done=True
                    finally:
                        #print "\nImageProcessor(): run() self.stream.seek(0) FINALLY"
                        # Reset the stream and event
                        self.stream.seek(0)
                        #print "\nImageProcessor(): run() self.stream.seek(0) DONE FINALLY"
                        self.stream.truncate()
                        #print "\nImageProcessor(): run() self.stream.truncate() DONE FINALLY"
                        self.event.clear()
                        #print "\nImageProcessor(): run() self.event.clear() DONE FINALLY"
                        # Return ourselves to the pool
                        with lock:
                            #print "\nImageProcessor(): run() pool.append(self) FINALLY"
                            pool.append(self)
                            print "\nImageProcessor(): run(id=%s) pool.append(self) DONE FINALLY" %self.id
    
    def streams():
        print "\nstreams()"
        while not done:
            #print "\nstreams() with lock"
            with lock:
                #print "\nstream(): len(pool) = " + str(len(pool))
                if pool:
                    #print "\nstream(): processor = pool.pop()"
                    processor = pool.pop()
                else:
                    #print "\nstream(): processor = None"
                    processor = None
            if processor:
                #print "\nstream(): yield processor.stream"
                yield processor.stream
                #print "\nstream(): processor.event.set()"
                processor.event.set()
            else:
                # When the pool is starved, wait a while for it to refill
                time.sleep(0.1)
                #time.sleep(1)
    
    
    with picamera.PiCamera() as camera:
    	#logfile
    	print "check path" 
    	if os.path.isfile(LOGFILE):
    		print "exists"
    		backupFile = LOGFILE + '%s.txt' %(datetime.date.today())
    		print backupFile
    		os.rename(LOGFILE, backupFile) 
    	logfile = open(LOGFILE, 'a')
        logfile.write('Starting Surveillance Application:\n')
        pool = [ImageProcessor(i) for i in range(1)]
        camera.resolution = (1920, 1440)
        #camera.resolution = (2592, 1944)
        #camera.resolution = (1280, 960)
        #camera.resolution = (800, 600) #(640, 480)
        camera.framerate = 30 #30
        camera.start_preview()
        time.sleep(2)
        global e
        #t = threading.Thread(name='CopyFilesThread', target=copyFilesWorker, args=(e, 300)) #check every 5 mins for files to be uploaded
        #t.start()
        camera.capture_sequence(streams(), use_video_port=True)
except:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    msg = ''.join('!! ' + line for line in lines)
    print "Unexpected error: ", msg
    logfile.write("Unexpected error while saving:")
    logfile.write(msg)
    

finally:
    # Shut down the processors in an orderly fashion
    while pool:
        #print "\nwhile pool"
        with lock:
            #print "\nwhile pool: processor = pool.pop()"
            processor = pool.pop()
        print "\nwhile pool: processor.terminated = True"
        processor.terminated = True
        print "\nwhile pool: processor.join()"
        processor.join()
        print "\nwhile pool: processor.join() DONE"
    logfile.write("finally statement reached.")
    logfile.close()
    global e
    e.set()
    print "finally camera.close()"
    camera.close()
    
