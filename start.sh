#!/bin/bash
redis-server &
sleep 2
celery -A tasks worker --loglevel=info &
sleep 2
python tasks.py

# Stop the Celery worker and Beanstalkd server
pkill -f celery
pkill -f redis-server
