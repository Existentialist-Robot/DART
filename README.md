# DART
DART

Running on a RPi Zero W 2 - rgb led matrix and a 200+ string of Neopixels

## Flash mircoSD with a lite Raspbian - can do headless and SSH as well.
https://www.raspberrypi.com/software/operating-systems/

### Headless setup *optional
##### https://learn.adafruit.com/raspberry-pi-zero-creation/text-file-editing

### If SSH-ing from Windows
##### https://medium.com/@jrcharney/connect-your-raspberry-pi-to-your-computer-via-ethernet-4564e1e68922

### Install GitHub
wget -qO- https://raw.githubusercontent.com/Botspot/pi-apps/master/install | bash

```
git config --global.name = ""
git config --global.email = ""
gh auth config
```
Use https & and the following limited-scope token

`
<>11ALFCAXQ0RuWdU6unUC3N_RDFx2uWHSsmvylIN3kAAQQuSKDZmCmpNdlmgCUlgfj1WF6XLZ6CAXBBvjnX`
      
### Install Matrix Driver
##### GUIDE: https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices
##### PACKAGE: https://github.com/hzeller/rpi-rgb-led-matrix/tree/master

```
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh >rgb-matrix.sh
sudo bash rgb-matrix.sh
```

Select 2. Convienience (since both the Matrix using the Quality compiled and the Neopixel with otherwise fight over the snd_bcm2835 kernel module)

### Install Strand Driver

#### Make a virtual env (including global access to system-wide packages)
```
sudo apt install python3-venv
python3 -m venv env --system-site-packages
```
Activate the environment
`
source env/bin/activate
`

Install Package

`
sudo pip install rpi_ws281x
`

#### Install 
##### https://github.com/rpi-ws281x/rpi-ws281x-python/tree/master

```
pip install rpi_ws281x
```

### Run script 
##### Must have the virtual environment activated (the one that Blinka was install into)
`
sudo --preserve-env=PATH,VIRTUAL_ENV python3 combined.py 
`

### Run with target image and with the intended dimensions





### Autorun script



