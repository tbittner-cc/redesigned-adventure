#!/bin/bash
redis-server &
celery -A description worker --loglevel=info &
python description.py

wait

# Stop the Celery worker and Beanstalkd server
pkill -f celery
pkill -f redis-server
