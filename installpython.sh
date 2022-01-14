#!/bin/bash

#set parameters
#for python
pver=3.10.1
pyver=${pver%.*}

#install necessary packages
apt update && apt upgrade
apt install wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

#install python
cd ~
#make sure empty files
rm -rf Python*
wget --no-check-certificate https://www.python.org/ftp/python/$pver/Python-$pver.tar.xz
tar -xvJf Python-$pver.tar.xz
cd Python-$pver

#continue configure
./configure --enable-optimizations
make -j 2

# install
make altinstall

# create links
realpython3=$(which python3)
rm -rf $realpython3
ln -s /usr/local/bin/python$pyver $realpython3
# realpip3=$(which pip3)
# rm -rf $realpip3
# ln -s /bin/pip3 /usr/local/bin/pip3
