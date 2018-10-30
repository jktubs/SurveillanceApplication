#!/bin/bash
# check and log if a host is reachable by ping

count=10                            # Maximum number to try.
while [ $count -gt 0 ]
do
    echo 'Pinging'
    ping -c 1 www.google.rr                      # Try once.
    rc=$?
    #echo $rc    
    if [ $rc -eq 0 ]
    then
    count=1                    # If okay, flag to exit loop.
    echo 'Host reachable.'
    fi
    count=$((count-1))
    #let count--
    sleep 1
done


echo 'End reached'