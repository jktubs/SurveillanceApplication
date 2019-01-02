#!/bin/bash
cd /
cd /var/www

IN_DIRECTORY="/var/www/images/$(date +\%Y-\%m-\%d)"
DROPBOX_DIRECTORY="dropbox:Surveillance/$(date +\%Y-\%m-\%d)"

IN_FTP_IMAGES_DIRECTORY="/home/pi/Desktop/Camera_FTP/$(date +\%Y\%m\%d)/images"
DROPBOX_FTP_IMAGES_DIRECTORY="dropbox:Surveillance/FTP/$(date +\%Y\%m\%d)/images"
IN_FTP_RECORD_DIRECTORY="/home/pi/Desktop/Camera_FTP/$(date +\%Y\%m\%d)/record"
DROPBOX_FTP_RECORD_DIRECTORY="dropbox:Surveillance/FTP/$(date +\%Y\%m\%d)/record"

count=120                            # Maximum number to try.
while [ $count -gt 0 ]
do
    echo 'Pinging'
    ping -c 1 dropbox.com                      # Try once.
    rc=$?
    #echo $rc    
    if [ $rc -eq 0 ]
    then
    
    sudo python copyFilesToBox.py $IN_DIRECTORY $DROPBOX_DIRECTORY
    sudo python copyFilesToBox.py $IN_FTP_IMAGES_DIRECTORY $DROPBOX_FTP_IMAGES_DIRECTORY
    sudo python copyFilesToBox.py $IN_FTP_RECORD_DIRECTORY $DROPBOX_FTP_RECORD_DIRECTORY
    
    count=1                    # If okay, flag to exit loop.
    echo 'Host reachable.'
    fi
    count=$((count-1))
    #let count--
    sleep 30
done
sleep 10
cd /