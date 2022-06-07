#!/usr/bin/env bash


set -e

echo "clone submodule..."
mkdir -p themes
sed -i 's/themes//g' .gitignore
git submodule add https://github.com/CaiJimmy/hugo-theme-stack themes/stack

echo "moving posts..."
mkdir -p content
cp -a posts content/

echo "add layouts for search..."
mkdir -p layouts
cp -a themes/stack/layouts/page layouts/pages
