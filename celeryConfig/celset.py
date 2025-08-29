from celery import Celery
import time

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "default"},
}

@celery_app.task
def add(x, y):
    time.sleep(150)
    return x + y