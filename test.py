import time
from celery import Celery
celery_app = Celery('main', broker='amqp://guest:guest@localhost:5672',
                    backend='redis://r-uf6vu210urvtz08emppd.redis.rds.aliyuncs.com:6379')


@celery_app.task
def send_email(name):
    print("向%s发送邮件..."%name)
    time.sleep(5)
    print("向%s发送邮件完成"%name)
    return "ok"

if __name__ == '__main__':
    result = send_email.delay("yuan")
    result2 = send_email.delay("alex")