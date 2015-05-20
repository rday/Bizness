#!/bin/bash

command -v virtualenv > /dev/null 2>&1 || { echo "Please install virtualenv on your system"; exit 1; }
virtualenv .venv
. .venv/bin/activate

command -v vagrant > /dev/null 2>&1 || { echo "Please install vagrant on your system"; exit 1; }

echo "Installing Ansible"
pip install ansible
vagrant up
mkdir user_tools
cp config-template config.py
echo "Please `vagrant ssh` and start the Flask server:"
echo "   PYTHONPATH=/vagrant python /vagrant/runserver.py"
