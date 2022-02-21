#!/bin/bash
echo "hello there"
cat /sys/class/rtc/rtc0/wakealarm
sudo sh -c "echo 0 > /sys/class/rtc/rtc0/wakealarm"
sudo sh -c "echo `date '+%s' -d '+ 720 minutes'` > /sys/class/rtc/rtc0/wakealarm"
cat /sys/class/rtc/rtc0/wakealarm
sudo systemctl suspend
