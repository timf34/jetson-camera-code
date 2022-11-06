#!/bin/bash

dt=$(date '+%d_%m_%Y');
mkdir -p ./logs
python3 record_and_detect_main_loop.py 2>&1 | tee logs/"$dt".txt
