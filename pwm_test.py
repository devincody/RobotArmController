sudo ./servod
echo 1=34% > /dev/servoblaster
echo 6=20% > /dev/servoblaster

echo 5=45% > /dev/servoblaster
echo 3=00% > /dev/servoblaster
echo 5=70% > /dev/servoblaster





#http://cihatkeser.com/servo-control-with-raspberry-pi-in-5-minutes-or-less/

import os
import time

os.chdir("PiBits")
os.chdir("ServoBlaster")
os.chdir("user")
os.system('sudo ./servod')


os.system("echo 1=100 > /dev/servoblaster")
time.sleep(2)
os.system("echo 1=60 > /dev/servoblaster")
time.sleep(2)


os.system("echo 1=100 > /dev/servoblaster")
time.sleep(2)


    # Using P1 pins:               7,11,12,13,15,16,18,22
    # Using P5 pins:

    # Servo mapping:
    #      0 on P1-7           GPIO-4
    #      1 on P1-11          GPIO-17
    #      2 on P1-12          GPIO-18
    #      3 on P1-13          GPIO-27
    #      4 on P1-15          GPIO-22
    #      5 on P1-16          GPIO-23
    #      6 on P1-18          GPIO-24
    #      7 on P1-22          GPIO-25