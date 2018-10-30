cd /
cd /var/www
sudo python setConfigToActive.py
echo "setConfigToActive DONE"
sleep 10
echo "sleep DONE. Now start the Application."
python image_observation_threading_and_stream.py
cd /