# Overview

In this document I will go over how to install everything needed to run vision code on the Pi, using an API known as RobotPy-CScore. RobotPy-CScore is WPIlibC's cscore library adapted for python. You may think that the most difficult part is the code. NOPE! Installation is by far the most annoying part.

## Setting up the Pi

 1. Take the Micro-SD card out of the Pi. Put it into your computer. Format the card. "Formatting" means wiping the card.
 2. Download NOOBS-Lite [here](https://downloads.raspberrypi.org/NOOBS_lite_latest). Extract it, then drag all of the contents of the folder (but not the folder!) onto the SD card.
 3. Eject the SD card, then plug it into the Pi.
 4. Plug a monitor with an HDMI cable, a USB keyboard, and a USB mouse. NOOBS-Lite should boot up.
 5. Install Raspbian-Lite. After a while it will prompt you to log in. The credentials should be as follows:
 
        User: pi
        Pass: raspberry
 Your Pi is now ready to go!
 
## Installation of dependencies
Below are the instructions to install all necessary libraries to use the RobotPy-CScore API on the Pi

## OpenCV
 Sorry for the block of commands. Copy and paste each line. Google any errors you have that I don't cover at the end.
 
    sudo apt-get update
    sudo apt-get upgrade
    sudo rpi-update
    sudo reboot
    sudo apt-get install build-essential git cmake pkg-config
    sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
    sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
    sudo apt-get install libxvidcore-dev libx264-dev
    sudo apt-get install libgtk2.0-dev
    sudo apt-get install libatlas-base-dev gfortran
    cd ~
    git clone https://github.com/Itseez/opencv.git
    cd opencv
    git checkout 3.1.0
    cd ~
    git clone https://github.com/Itseez/opencv_contrib.git
    cd opencv_contrib
    git checkout 3.1.0
    sudo apt-get install python3-dev
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    pip install numpy
    cd ~/opencv
    mkdir build
    cd build
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=ON \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
        -D BUILD_EXAMPLES=ON ..
     make -j4
     sudo make install
     sudo ldconfig

### Errors you may get

     #include_next<stdlib.h>
     could not find stdlib.h
     
If a header file cannot be located (for example stdlib.h), then a work around is replacing the #include_next with #include . This can be done using the instructions below:

 1. Use "cd" to navigate to /usr/include/c++/6/
 2. Give yourself permission to edit the erroneous file (don't include the asterisks!):
 
        sudo chattr -i *insert file name here*
        lsattr *file name*
        sudo chown pi:pi *file name*
    
 3. Begin editing file:
 
        vi *file name*
        
 4. Use arrow keys to move cursor, type "x" to delete "_next"
 5. Save by typing ":w" and quit with ":q"
 6. Run "make -jv4" again, and that error will disappear.
 
 ## PyBind
 I don't know what this is but it is necessary for cscore to run. I think it allows for python/c++ integration.
 
      sudo pip3 install "pybind>=2.2"

## Finally, RobotPy-CSCore!

     sudo pip3 install robotpy-cscore
