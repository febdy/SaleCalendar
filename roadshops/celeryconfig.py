from celery.schedules import crontab
from datetime import timedelta

BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'rpc://'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

CELERYBEAT_SCHEDULE = {
    'add-every-midnight': {
        'task': 'tasks.readroadshops',
        'schedule': timedelta(seconds=10),
        # 'schedule': crontab(minute=0, hour=15), # 매일 자정마다 실행됨
    },
}
