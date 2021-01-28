#!/bin/bash

python3 app.py > /var/log/app.log
tail -f /var/log/app.log
