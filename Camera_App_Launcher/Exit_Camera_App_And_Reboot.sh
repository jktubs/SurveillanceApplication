#!/bin/bash
cd /
cd /var/www
sudo python setConfigToExit.py
echo "setConfigToExit DONE"
sleep 20

IN_DIRECTORY="/var/www/images/$(date +\%Y-\%m-\%d)"
BOX_DIRECTORY="/media/JENS_KRAMER/box"
OUT_DIRECTORY="/media/JENS_KRAMER/box/Surveillance_Images/$(date +\%Y-\%m-\%d)"
IN_CHRONLOGS_DIRECTORY="/home/pi/Desktop/Camera_App_Launcher/Logs"
OUT_CHRONLOGS_DIRECTORY="/media/JENS_KRAMER/box/Surveillance_Images/CronLogs"

count=120                            # Maximum number to try.
while [ $count -gt 0 ]
do
    echo 'Pinging'
    ping -c 1 dav.box.com                      # Try once.
    rc=$?
    #echo $rc    
    if [ $rc -eq 0 ]
    then
    sudo mount $BOX_DIRECTORY
    sudo mkdir $OUT_DIRECTORY
    sudo python copyFilesToBox.py $IN_DIRECTORY $OUT_DIRECTORY
    sudo mkdir $OUT_CHRONLOGS_DIRECTORY
    sudo python copyFilesToBox.py $IN_CHRONLOGS_DIRECTORY $OUT_CHRONLOGS_DIRECTORY
    count=1                    # If okay, flag to exit loop.
    echo 'Host reachable.'
    fi
    count=$((count-1))
    #let count--
    sleep 30
done
sleep 90m
sudo umount $BOX_DIRECTORY
echo "sleep DONE. Now reboot the PI."
sudo python restart.py
cd /