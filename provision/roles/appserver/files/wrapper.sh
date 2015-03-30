#!/bin/bash

. /home/vagrant/venv/bin/activate
shift 1
echo "Starting up server"
exec python /vagrant/runserver.py &
deactivate
