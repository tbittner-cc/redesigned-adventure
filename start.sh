#!/bin/bash
nohup beanstalkd &
sleep 1
python -u main.py
