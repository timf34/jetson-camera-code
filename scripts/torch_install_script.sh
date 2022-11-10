# Source: https://qengineering.eu/install-pytorch-on-jetson-nano.html

# install the dependencies (if not already onboard)
sudo apt-get install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev
sudo -H pip3 install future
sudo pip3 install -U --user wheel mock pillow
sudo -H pip3 install testresources
# above 58.3.0 you get version issues
sudo -H pip3 install setuptools==58.3.0
sudo -H pip3 install Cython
# install gdown to download from Google drive
sudo -H pip3 install gdown
# download the wheel
gdown https://drive.google.com/uc?id=1-XmTOEN0z1_-VVCI3DPwmcdC-eLT_-n3
# install PyTorch 1.8.0
sudo -H pip3 install torch-1.8.0a0+37c1f4a-cp36-cp36m-linux_aarch64.whl
# clean up
rm torch-1.8.0a0+37c1f4a-cp36-cp36m-linux_aarch64.whl
