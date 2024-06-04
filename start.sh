#!/bin/bash
redis-server &
celery -A tasks worker --loglevel=info &
python tasks.py

wait

# Stop the Celery worker and Beanstalkd server
pkill -f celery
pkill -f redis-server
