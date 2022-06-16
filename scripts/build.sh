#!/usr/bin/env bash


set -e

echo "preparing deps..."
sudo bash scripts/deps.sh

echo "cloning submodule..."
mkdir -p themes
sed -i 's/themes//g' .gitignore
git submodule add https://github.com/CaiJimmy/hugo-theme-stack themes/stack

echo "preparing media for posts..."
python3 scripts/media.py

echo "moving posts..."
mkdir -p content
cp -a posts content/

echo "adding layouts for search..."
mkdir -p layouts
cp -a themes/stack/layouts/page layouts/pages
