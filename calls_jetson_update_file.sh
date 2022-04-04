#!/bin/bash

# Copy this file to /etc/NetworkManager/dispatcher.d 
# Most of this file is superfluous besidest the command to run the update_match_config_file.sh

# Make sure to chmod +x the update_config python file!

# Source: https://www.techytalk.info/start-script-on-network-manager-successful-connection/

IF=$1
STATUS=$2

if [ "$IF" == "wlan0" ]
then
    case "$2" in
        up)
        logger -s "NM Script up triggered"
	(cd /home/timf34/jetson-camera-code; ./update_match_config_file.sh)
	# source /home/timf34/jetson-camera-code; ./update_match_config_file.sh 
	# wouldn't work. It said something like fatal: no git repository in directory
        ;;
        down)
        logger -s "NM Script down triggered"
        ;;
        pre-up)
        logger -s "NM Script pre-up triggered"
        ;;
        post-down)
        logger -s "NM Script post-down triggered"
        ;;
        *)
        ;;
    esac
fi
