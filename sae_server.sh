#!/usr/bin/env bash

# set -a makes automatically exports all subsequent variables
set -a

# reset the -a option
set +a

# launch the python server
venv/bin/python3 ./web_server.py