apt-get update

apt-get install pip

pip install -U Flask

pip install w1thermsensor

echo "dtoverlay=w1-gpio" >> /boot/firmware/config.txt
