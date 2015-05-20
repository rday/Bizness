#!/bin/bash

command -v virtualenv > /dev/null 2>&1 || { echo "Please install virtualenv on your system"; exit 1; }
virtualenv .venv
. .venv/bin/activate

command -v vagrant > /dev/null 2>&1 || { echo "Please install vagrant on your system"; exit 1; }

pip install -r requirements.txt
vagrant up
