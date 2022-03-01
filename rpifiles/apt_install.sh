#!/bin/sh


sudo apt update && sudo apt full-upgrade

sudo apt install python3-pip python3-opencv libx264-dev libjpeg-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-gl gstreamer1.0-gtk3 build-essential libzbar-dev

pip3 install python-dotenv pyzbar firebase_admin