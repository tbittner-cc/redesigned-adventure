# tasks.py

from celery import Celery
print("hello")

app = Celery('tasks', broker='beanstalk://localhost:11300')

@app.task
def add(x, y):
    return x + y