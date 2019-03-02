#!/bin/bash

# Python 2.7
for req in $(cat requirements.txt); do sudo pip2.7 install $req; done

# Python 3
#for req in $(cat requirements.txt); do pip install $req; done
