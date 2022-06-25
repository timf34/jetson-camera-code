wget https://nvidia.box.com/shared/static/p57jwntv436lfrd78inwl7iml6p13fzh.whl -O torch-1.8.0-cp36-cp36m-linux_aarch64.whl

# This, even though its straight from nvidia, doesn't seem to work!
# sudo apt-get install python3-pip libopenblas-base libopenmpi-dev libomp5 libomp-dev 
csudo apt-get install libopenblas-base libopenmpi-dev 
python3 -m pip install Cython
python3 -m pip install numpy torch-1.8.0-cp36-cp36m-linux_aarch64.whl


# Source: https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-11-now-available/72048


