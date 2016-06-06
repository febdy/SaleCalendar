from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from roadshops.models import Roadshops
from datetime import datetime, timedelta, timezone


class Home(TemplateView):
    template_name = 'main.html'


def home(request, num=None, num2=None):
    context = print_shops()

    return render_to_response('main.html', context)


def temp(request):
    context = print_shops()

    return render_to_response('temp.html', context)


def check_event_active():
    db_eventlist = Roadshops.objects.all().filter(is_active='Y')

    for db_event in db_eventlist:
        now = datetime.now(timezone.utc)
        last_updated = db_event.updated_at

        if now - last_updated > timedelta(hours=24):
            db_event.is_active = 'N'
            db_event.save()


def print_shops():
    check_event_active()
    shops = Roadshops.objects.all().filter(is_active='Y')
    context = {'shops': shops}
    return context
