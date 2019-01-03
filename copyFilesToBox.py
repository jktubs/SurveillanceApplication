import sys
import subprocess
import io
import os
import shutil
import time
import threading
import logging
import traceback

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


def copyFilesWorker(path_in, path_out):
    try:
        logging.debug('Check if files to be copied are available.')
        src_files = os.listdir(path_in)
        for file_name in src_files:
            full_file_name = os.path.join(path_in, file_name)
            if (os.path.isfile(full_file_name) and not os.path.exists(os.path.join(path_out, file_name))):
                logging.debug('copy %s', file_name)
                shutil.copyfile(full_file_name, os.path.join(path_out, os.path.basename(full_file_name)))
        logging.debug('Leaving copyFilesWorker()')
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        msg = ''.join('!! ' + line for line in lines)
        logging.debug('Unexpected error in copyFilesWorker(): %s', msg)
    finally:
        logging.debug('finally statement copyFilesWorker() reached.')
        
def copyFilesToDropbox(path_in, path_out):
    try:
        logging.debug('Check if files to be copied are available.')
        src_files = os.listdir(path_in)
        for file_name in src_files:
            full_file_name = os.path.join(path_in, file_name)
            if (os.path.isfile(full_file_name)):
                logging.debug('copy %s', file_name)
                cmd = 'rclone check \'' + full_file_name + '\' ' + path_out
                print cmd + '\n'
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                out, err = p.communicate()
                print out
                print err
                if(out.find('0 differences found') != -1):
                	print full_file_name + ' identical already in Dropbox\n'
                else:
                    print full_file_name + ' not identical in Dropbox yet. Uploading ... \n'
                    cmd = 'rclone copy \'' + full_file_name + '\' ' + path_out
                    print cmd + '\n'
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                    out, err = p.communicate()
                    print out
                    print err

        logging.debug('Leaving copyFilesWorker()')
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        msg = ''.join('!! ' + line for line in lines)
        logging.debug('Unexpected error in copyFilesToDropbox(): %s', msg)
    finally:
        logging.debug('finally statement copyFilesToDropbox() reached.')
    
try:
    path_in = sys.argv[1]
    path_out = sys.argv[2]
    t = threading.Thread(name='CopyFilesThread', target=copyFilesToDropbox, args=(path_in, path_out))
    t.start()
except:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    msg = ''.join('!! ' + line for line in lines)
    logging.debug('Unexpected error: %s', msg)
    

finally:
    logging.debug('finally reached.')
    