import time
from celery import Celery
celery_app = Celery('test', broker='amqp://guest:guest@localhost:5672//')


@celery_app.task
def send_email(name):
    print("向%s发送邮件..."%name)
    time.sleep(5)
    print("向%s发送邮件完成"%name)
    return "ok"


result = send_email.delay("yuan")
print(result.id)
result2 = send_email.delay("alex")
print(result2.id)