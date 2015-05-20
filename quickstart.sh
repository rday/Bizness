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
echo "Installation complete. Please login to the Vagrant system"
echo "to populate the database and start the development server:"
echo
echo "  $ vagrant ssh"
echo "  $ DATABASE_URL=postgres://biz:ness@localhost/bizness PYTHONPATH=/vagrant python /vagrant/tools/populate_db.py"
echo "  $ DATABASE_URL=postgres://biz:ness@localhost/bizness PYTHONPATH=/vagrant python /vagrant/runserver.py"
