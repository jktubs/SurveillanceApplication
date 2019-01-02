#!/bin/bash
cd /
cd /var/www
sudo python setConfigToExit.py
echo "setConfigToExit DONE"
sleep 20

/home/pi/Desktop/Camera_App_Launcher/Upload_to_Dropbox.sh

sleep 1m
echo "sleep DONE. Now reboot the PI."
sudo python restart.py
cd /