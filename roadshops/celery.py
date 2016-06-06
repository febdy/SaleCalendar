from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SaleCalendar.settings')

app = Celery('roadshops',
             broker='amqp://',
             backend='amqp://',
             include=['roadshops.tasks'])

# Optional configuration, see the application user guide.
app.config_from_object('roadshops.celeryconfig')

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
