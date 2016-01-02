from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from roadshops.models import Roadshops
from datetime import datetime
from bs4 import BeautifulSoup

import urllib.request


class Home(TemplateView):
    template_name = 'main.html'


def home(request, num=None, num2=None):
    Roadshops.objects.all().delete()
    etude()
    skinfood()
    context = print_shops()
    return render_to_response('main.html', context)


def temp(request):
    Roadshops.objects.all().delete()
    etude()
    skinfood()
    context = print_shops()

    return render_to_response('temp.html', context)


def etude():
    url = 'http://www.etude.co.kr/event.do?method=list'
    f = urllib.request.urlopen(url)
    text = f.read().decode('utf-8')

    soup = BeautifulSoup(text)

    templist = soup.find('div', 'evnetList')
    ul_tag = templist.contents[1]

    eventlist = []

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        temp = Roadshops()

        period = event.find('em').get_text()
        start_date = period.split(' ~ ')[0]
        end_date = period.split(' ~ ')[1]

        temp.event_name = event.find('span', 'tit').get_text()
        temp.roadshop_name = Roadshops.ETUDE
        temp.image_url = event.find('img').get('src')
        if event.find('a').get('href')[0] == '/':
            temp.link_url = 'http://www.etude.co.kr'+event.find('a').get('href')
        elif event.find('a').get('href')[0] != '/':
            temp.link_url = event.find('a').get('href')
        temp.start_date = datetime.strptime(start_date, "%Y.%m.%d")
        temp.end_date = datetime.strptime(end_date + " 23:59:59", "%Y.%m.%d %H:%M:%S")
        temp.save()


def skinfood():
    url = 'http://www.theskinfood.com/event/eventList.do'
    f = urllib.request.urlopen(url)
    text = f.read().decode('utf-8')

    soup = BeautifulSoup(text)

    templist = soup.find('ul', 'eventList passed')

    eventlist = []

    for event in templist.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        temp = Roadshops()

        # 혜택, 기간 나누기
        period = event.find('p').get_text()
        start_date = period.split(' ~ ')[0]
        end_date = period.split(' ~ ')[1]

        temp.event_name = event.find('strong').get_text()
        temp.roadshop_name = 'SKIN_FOOD'
        temp.image_url = event.find('img').get('src')
        temp.link_url = 'http://www.theskinfood.com'+event.find('a').get('href')
        temp.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        temp.end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        temp.save()


def print_shops():
    shops = Roadshops.objects.all()
    context = {'shops': shops}
    return context
