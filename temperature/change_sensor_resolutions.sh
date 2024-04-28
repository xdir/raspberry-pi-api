#!/bin/bash

# Setting the resolution of DS18B20 sensors to 10 bits

echo 9 > /sys/bus/w1/devices/28-031654c65fff/w1_slave
echo 9 > /sys/bus/w1/devices/28-0214630b7cff/w1_slave
echo 9 > /sys/bus/w1/devices/28-00000f9c3848/w1_slave
