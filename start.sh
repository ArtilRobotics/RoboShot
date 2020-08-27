#!/usr/bin/env bash

echo"-----------------------------------------------------------------------"
echo" _   _  _____  _____  _____  _____ ______   _____  _____  _____  _____"
echo"| | | ||  ___|/  __ \|_   _||  _  || ___ \ |  _  ||  _  ||  _  ||  _  |"
echo"| |_| || |__  | /  \/  | |  | | | || |_/ / | |_| || |/' || |/' || |/' |"
echo"|  _  ||  __| | |      | |  | | | ||    /  \____ ||  /| ||  /| ||  /| |"
echo"| | | || |___ | \__/\  | |  \ \_/ /| |\ \  .___/ /\ |_/ /\ |_/ /\ |_/ /"
echo"\_| |_/\____/  \____/  \_/   \___/ \_| \_| \____/  \___/  \___/  \___/"
echo"-----------------------------------------------------------------------"

nohup python3 src/Hector/HectorServer.py > Server.out 2>&1 &
nohup python3 src/Hector/HectorController.py > Controller.out 2>&1 &
nohup sudo python3 src/Hector/LEDStripServer.py > /dev/null 2>&1 &
#mosquitto_sub -v -t "Hector9000/#"