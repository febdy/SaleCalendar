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
    aritaum()
    innisfree()
    thefaceshop()
    thesaem()
    itsskin()
    context = print_shops()

    return render_to_response('main.html', context)


def temp(request):
    Roadshops.objects.all().delete()
    etude()
    skinfood()
    aritaum()
    innisfree()
    thefaceshop()
    thesaem()
    itsskin()
    context = print_shops()

    return render_to_response('temp.html', context)


def etude():
    soup = read_url('http://www.etude.co.kr/event.do?method=list')

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
    soup = read_url('http://www.theskinfood.com/event/eventList.do')

    ul_tag = soup.find('ul', 'eventList passed')

    eventlist = []

    for event in ul_tag.contents:
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


def aritaum():
    soup = read_url('http://www.aritaum.com/event/ev/event_ev_event_list.do')

    templist = soup.find('div', 'event_lst')
    ul_tag = templist.contents[1]

    eventlist = []

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        temp = Roadshops()

        period = event.find('span', 'date').get_text()
        start_date = period.split('~')[0]
        end_date = period.split('~')[1]

        temp.event_name = event.find('span', 'desc').get_text()
        temp.roadshop_name = Roadshops.ARITAUM
        #  temp.image_url = event.find('img').get('src')
        """if event.find('a').get('href')[0] == '/':
            temp.link_url = 'http://www.etude.co.kr'+event.find('a').get('href')
        elif event.find('a').get('href')[0] != '/':
            temp.link_url = event.find('a').get('href')"""
        temp.start_date = datetime.strptime(start_date, "%Y.%m.%d")
        temp.end_date = datetime.strptime(end_date + " 23:59:59", "%Y.%m.%d %H:%M:%S")
        temp.save()


def innisfree():
    soup = read_url('http://www.innisfree.co.kr/Event.do')

    innisfree_save(soup)

    paging = soup.find('div', 'paging')

    pages = paging.find_all('a')

    for page in pages:
        if page.get('class') == ['first']:
            continue
        elif page.get('class') == ['last']:
            break
        page_url = 'http://www.innisfree.co.kr'+page.get('href')
        soup = read_url(page_url)
        innisfree_save(soup)


def innisfree_save(soup):
    eventlist = []

    templist = soup.find('div', 'eventList')
    ul_tag = templist.contents[1]

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        temp = Roadshops()

        period = event.find_all('dd')[1].get_text()
        start_date = period.split(' ~ ')[0]
        end_date = period.split(' ~ ')[1]

        temp.event_name = event.find('strong').get_text()
        temp.roadshop_name = Roadshops.INNISFREE
        temp.describe = event.find('p').find('a').next_sibling
        temp.image_url = event.find('img').get('src')

        if event.find('a').get('href')[0] == '/':
            temp.link_url = 'http://www.innisfree.co.kr'+event.find('a').get('href')
        elif event.find('a').get('href')[0] != '/':
            temp.link_url = event.find('a').get('href')

        temp.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date[0] == '2':
           temp.end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        temp.save()


def thefaceshop():
    soup = read_url('http://www.thefaceshop.com/mall/event/event.jsp')

    thefaceshop_save(soup)

    paging = soup.find('div', 'paging_type1')

    pages = paging.find_all('a')

    for page in pages:
        page_url = 'http://www.thefaceshop.com/mall/event/'+page.get('href')
        soup = read_url(page_url)
        thefaceshop_save(soup)

        if page.get('class') == ['cnt']:
            break


def thefaceshop_save(soup):
    eventlist = []

    ul_tag = soup.find('ul', 'ComEventList')

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        temp = Roadshops()

        if type(event.find('p')) == int:
            continue

        period = event.find('p').get_text()
        start_date = period.split(' ~ ')[0]
        end_date = period.split(' ~ ')[1]

        temp.event_name = event.find('span', 's_tit7').contents[1]
        temp.roadshop_name = Roadshops.THE_FACE_SHOP
        temp.image_url = event.find('img').get('src')

        if event.find('a').get('href')[0] == 'h':
            temp.link_url = event.find('a').get('href')
        elif event.find('a').get('href')[0] != 'h':
            temp.link_url = 'http://www.thefaceshop.com/mall/event/'+event.find('a').get('href')

        temp.start_date = datetime.strptime(start_date, "%Y.%m.%d")
        if end_date[0] == '2':
           temp.end_date = datetime.strptime(end_date + " 23:59:59", "%Y.%m.%d  %H:%M:%S")
        temp.save()


def thesaem():
    soup = read_url('http://www.thesaemcosmetic.com/event/now_event_list')

    eventlist = []

    templist = soup.find('div', 'event-list')
    ul_tag = templist.contents[1]

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        temp = Roadshops()

        if type(event.find('span')) == int:
            continue

        period = event.find('span').get_text()
        start_date = period.split(' ~ ')[0]
        end_date = period.split(' ~ ')[1]

        temp.event_name = event.find('h5').get_text()
        temp.roadshop_name = Roadshops.THE_SAEM
        temp.image_url = 'http://www.thesaemcosmetic.com'+event.find('img').get('src')

        if event.find('a').get('href')[0] == '/':
            temp.link_url = 'http://www.thesaemcosmetic.com'+event.find('a').get('href')
        elif event.find('a').get('href')[0] != '/':
            temp.link_url = event.find('a').get('href')

        temp.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date[0] == '2':
           temp.end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        temp.save()


def itsskin():
    soup = read_url('http://www.itsskin.com/event/wip_list.asp')

    eventlist = []

    templist = soup.find('div', 'event_list')
    ul_tag = templist.contents[1]

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        temp = Roadshops()

        if type(event.find('span')) == int:
            continue

        period = event.find('span', 'date').get_text()
        remove_text = period.split(' : ')[1]
        split_date = remove_text.split(' / ')[0]
        start_date = split_date.split(' ~ ')[0]
        end_date = split_date.split(' ~ ')[1]

        temp.event_name = event.find('span').get_text()
        temp.roadshop_name = Roadshops.ITS_SKIN
        temp.image_url = 'http://www.itsskin.com'+event.find('img').get('src')
        temp.link_url = 'http://www.itsskin.com/event/'+event.find('a').get('href')

        temp.start_date = datetime.strptime(start_date, "%Y.%m.%d")
        if end_date[0] == '2':
           temp.end_date = datetime.strptime(end_date + " 23:59:59", "%Y.%m.%d %H:%M:%S")
        temp.save()


def read_url(url):
    f = urllib.request.urlopen(url)
    text = f.read().decode(f.info().get_param('charset'))
    soup = BeautifulSoup(text)
    return soup


def print_shops():
    shops = Roadshops.objects.all()
    context = {'shops': shops}
    return context
