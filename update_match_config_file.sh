#!/bin/bash

# This file will git pull just the config.py and stream_port1234.sh file within jetson-camera-code folder.
# It will update these files once the jetson connects to the internet
# Here is the main resources:
# 1) https://askubuntu.com/questions/258580/how-to-run-a-script-depending-on-internet-connection
# 2) https://stackoverflow.com/questions/28375418/git-how-to-pull-a-single-file-from-a-server-repository-in-git

# I'm not entirely sure how to git fetch from another directory so I'm going to use two files for this, one which we
# will leave in the jetson-camera-code folder which runs the git commands, and the other which we'll move to the
# /etc/network/if-up.d/ directory and which will run this file.

git fetch --all
git checkout origin/main -- config.py stream_port1234.sh