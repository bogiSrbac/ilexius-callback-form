from .models import Customer, Archive
from celery import shared_task
from ilexius import settings
import datetime
from datetime import date, datetime
from django.utils import timezone


@shared_task(bind=True)
def makeCallbacksRealizedCelery(self):
    getData = Customer.objects.all()

    dateTimeNow = timezone.now()
    for data in getData:
        if data.date_and_time_for_callback < dateTimeNow:
            data.realized = True
            data.administrator = 'By sistem'
            data.comment = 'This callback was not realized.'
            data.save()
            archive = Archive.objects.create(realizedCallbacks_id=data.pk)
            archive.save()

    return 'Done'