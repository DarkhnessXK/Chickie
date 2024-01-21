from src.scheduler import celerybeat_scheduler
from celery import Celery  # type: ignore

app = Celery(
    "myapp",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)


@app.task
def my_task(arg1, arg2):
    print(arg1)
    print(arg2)
    return "result"


celerybeat_scheduler.init_app(app)
