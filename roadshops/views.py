from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from roadshops.models import Roadshops


class Home(TemplateView):
    template_name = 'main.html'


def home(request, num=None, num2=None):
    context = print_shops()

    return render_to_response('main.html', context)


def temp(request):
    context = print_shops()

    return render_to_response('temp.html', context)


def print_shops():
    shops = Roadshops.objects.all()
    context = {'shops': shops}
    return context
