#!/usr/bin/env bash


set -e

PACKAGES="git unzip wget"
PIP_REQ_PATH="scripts/requirements.txt"

# echo "updating apt..."
# sudo apt update

# echo "installing dependencies..."
# sudo apt install -y $PACKAGES

echo "updating pip"
python3 -m pip install --upgrade pip

echo "installing python packages..."
python3 -m pip install -r $PIP_REQ_PATH
