#!/bin/bash

dt=$(date '+%d_%m_%Y');
mkdir -p ./logs
python3 test_file.py 2>&1 | tee logs/"$dt".txt

