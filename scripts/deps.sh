#!/usr/bin/env bash


set -e

PKGS="git unzip wget"

echo "updating apt..."
sudo apt update

echo "installing dependencies..."
sudo apt install -y $PKGS

echo "updating pip"
python3 -m pip install --upgrade pip
