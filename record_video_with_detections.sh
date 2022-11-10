#!/bin/bash

# Note: I was having issues running this file at Bohs on 6/11/22 (before I changed directory)

dt=$(date '+%d_%m_%Y');
mkdir -p ../logs
python3 ../record_and_detect_main_loop.py 2>&1 | tee ../logs/"$dt".txt
