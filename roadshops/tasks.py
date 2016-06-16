from __future__ import absolute_import
from roadshops.celery import app
from roadshops.models import Roadshops
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup

import urllib.request


@app.task(name='tasks.readroadshops')
def readroadshops():
    check_event_active()
    etude()
    skinfood()
    aritaum()
    innisfree()
    thefaceshop()
    thesaem()
    itsskin()
    naturerepublic()
    tonymoly()


@app.task
def etude():
    soup = read_url('http://www.etude.co.kr/event.do?method=list')

    templist = soup.find('div', 'evnetList')
    ul_tag = templist.contents[1]

    eventlist = []

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        event_info = Roadshops()

        period = event.find('em').get_text()
        start_date = period.split(' ~ ')[0]
        end_date = period.split(' ~ ')[1]

        event_info.event_name = event.find('span', 'tit').get_text()
        event_info.roadshop_name = Roadshops.ETUDE
        event_info.image_url = event.find('img').get('src')
        if event.find('a').get('href')[0] == '/':
            event_info.link_url = 'http://www.etude.co.kr'+event.find('a').get('href')
        elif event.find('a').get('href')[0] != '/':
            event_info.link_url = event.find('a').get('href')
        event_info.start_date = datetime.strptime(start_date, "%Y.%m.%d")
        event_info.end_date = datetime.strptime(end_date + " 23:59:59", "%Y.%m.%d %H:%M:%S")
        event_info.is_active = 'Y'

        check_db('ETUDE_HOUSE', event_info)


@app.task
def skinfood():
    soup = read_url('http://www.theskinfood.com/event/eventList.do')

    ul_tag = soup.find('ul', 'eventList passed')

    eventlist = []

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        event_info = Roadshops()

        # 혜택, 기간 나누기
        period = event.find('p').get_text()
        start_date = period.split(' ~ ')[0]
        end_date = period.split(' ~ ')[1]

        event_info.event_name = event.find('strong').get_text()
        event_info.roadshop_name = 'SKIN_FOOD'
        event_info.image_url = event.find('img').get('src')
        event_info.link_url = 'http://www.theskinfood.com'+event.find('a').get('href')
        event_info.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        event_info.end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        event_info.is_active = 'Y'

        check_db('SKIN_FOOD', event_info)


@app.task
def aritaum():
    soup = read_url('http://www.aritaum.com/event/ev/event_ev_event_list.do')

    templist = soup.find('div', 'event_lst')
    ul_tag = templist.contents[1]

    eventlist = []

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        event_info = Roadshops()

        period = event.find('span', 'date').get_text()
        start_date = period.split('~')[0]
        end_date = period.split('~')[1]

        event_info.event_name = event.find('span', 'desc').get_text()
        event_info.roadshop_name = Roadshops.ARITAUM
        get_image_url = event.find('a').get('style')
        image_url = get_image_url.split('(')[1]
        image_url = image_url.split(')')[0]
        event_info.image_url = image_url

        if event.find('a').get('href') == '#':
            event_info.link_url = 'http://www.aritaum.com/event/ev/event_ev_event_view.do?i_sEventcd=' + event.find('a').get('id')
        else:
            event_info.link_url = event.find('a').get('href')
        event_info.start_date = datetime.strptime(start_date, "%Y.%m.%d")
        event_info.end_date = datetime.strptime(end_date + " 23:59:59", "%Y.%m.%d %H:%M:%S")
        event_info.is_active = 'Y'

        check_db('ARITAUM', event_info)


@app.task
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


@app.task
def innisfree_save(soup):
    eventlist = []

    templist = soup.find('div', 'eventList')
    ul_tag = templist.contents[1]

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        event_info = Roadshops()

        period = event.find_all('dd')[1].get_text()
        start_date = period.split(' ~ ')[0]
        end_date = period.split(' ~ ')[1]

        event_info.event_name = event.find('strong').get_text()
        event_info.roadshop_name = Roadshops.INNISFREE
        event_info.describe = event.find('p').find('a').next_sibling
        event_info.image_url = event.find('img').get('src')

        if event.find('a').get('href')[0] == '/':
            event_info.link_url = 'http://www.innisfree.co.kr'+event.find('a').get('href')
        elif event.find('a').get('href')[0] != '/':
            event_info.link_url = event.find('a').get('href')

        event_info.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date[0] == '2' and end_date[1] == '0':
            try:
                event_info.end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
            except ValueError:
                event_info.end_date = None
        else:
            event_info.end_date = None # @TODO end_date 형식이 다를 경우 처리하기
        event_info.is_active = 'Y'

        check_db('INNISFREE', event_info)


@app.task
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


@app.task
def thefaceshop_save(soup):
    eventlist = []

    ul_tag = soup.find('ul', 'ComEventList')

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        event_info = Roadshops()

        if type(event.find('p')) == int:
            continue

        period = event.find('p').get_text()
        start_date = period.split(' ~ ')[0]
        end_date = period.split(' ~ ')[1]

        event_info.event_name = event.find('span', 's_tit7').contents[1].strip()
        event_info.roadshop_name = Roadshops.THE_FACE_SHOP
        event_info.image_url = event.find('img').get('src')

        if event.find('a').get('href')[0] == 'h':
            event_info.link_url = event.find('a').get('href')
        elif event.find('a').get('href')[0] != 'h':
            event_info.link_url = 'http://www.thefaceshop.com/mall/event/'+event.find('a').get('href')

        event_info.start_date = datetime.strptime(start_date, "%Y.%m.%d")
        if end_date[0] == '2' and end_date[1] == '0':
            event_info.end_date = datetime.strptime(end_date + " 23:59:59", "%Y.%m.%d  %H:%M:%S")
        event_info.is_active = 'Y'

        check_db('THE_FACE_SHOP', event_info)


@app.task
def thesaem():
    # Roadshops.objects.all().delete()
    soup = read_url('http://www.thesaemcosmetic.com/event/now_event_list')

    eventlist = []

    templist = soup.find('div', 'event-list')
    ul_tag = templist.contents[1]

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        event_info = Roadshops()

        if type(event.find('span')) == int:
            continue

        period = event.find('span').get_text()
        start_date = period.split(' ~ ')[0]
        end_date = period.split(' ~ ')[1]

        event_info.event_name = event.find('h5').get_text()
        event_info.roadshop_name = Roadshops.THE_SAEM
        event_info.image_url = 'http://www.thesaemcosmetic.com'+event.find('img').get('src')

        if event.find('a').get('href')[0] == '/':
            event_info.link_url = 'http://www.thesaemcosmetic.com'+event.find('a').get('href')
        elif event.find('a').get('href')[0] != '/':
            event_info.link_url = event.find('a').get('href')

        event_info.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date[0] == '2' and end_date[1] == '0':
            event_info.end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        event_info.is_active = 'Y'

        check_db('THE_SAEM', event_info)


@app.task
def itsskin():
    soup = read_url('http://www.itsskin.com/event/wip_list.asp')

    eventlist = []

    templist = soup.find('div', 'event_list')
    ul_tag = templist.contents[1]

    for event in ul_tag.contents:
        if event != '\n':
            eventlist.append(event)

    for event in eventlist:
        event_info = Roadshops()

        if type(event.find('span')) == int:
            continue

        period = event.find('span', 'date').get_text()
        remove_text = period.split(' : ')[1]
        split_date = remove_text.split(' / ')[0]
        start_date = split_date.split(' ~ ')[0]
        end_date = split_date.split(' ~ ')[1]

        event_info.event_name = event.find('span').get_text()
        event_info.roadshop_name = Roadshops.ITS_SKIN
        event_info.image_url = 'http://www.itsskin.com'+event.find('img').get('src')
        event_info.link_url = 'http://www.itsskin.com/event/'+event.find('a').get('href')

        event_info.start_date = datetime.strptime(start_date, "%Y.%m.%d")
        if end_date[0] == '2' and end_date[1] == '0':
            event_info.end_date = datetime.strptime(end_date + " 23:59:59", "%Y.%m.%d %H:%M:%S")
        event_info.is_active = 'Y'

        check_db('ITS_SKIN', event_info)


@app.task
def naturerepublic():
    soup = read_url('http://m.naturerepublic.com/event/ing')

    eventlist = soup.find_all('div', 'event_wrap')

    for event in eventlist:
        event_info = Roadshops()

        event_info.event_name = event.find('div', 'event_tit').get_text()
        event_info.roadshop_name = Roadshops.NATURE_REPUBLIC
        event_info.image_url = event.find('img').get('src')
        event_info.link_url = 'http://m.naturerepublic.com'+event.find('a').get('href')

        now = datetime.utcnow()
        event_info.start_date = now
        event_info.is_active = 'Y'

        check_db('NATURE_REPUBLIC', event_info)


@app.task
def tonymoly():
    soup = read_url('http://www.etonymoly.com/html/event/event_list.asp?board=event&board_group=1')

    eventlist = soup.find_all('div', 'area')

    for event in eventlist:
        event_info = Roadshops()

        period = event.find('li').get_text()
        remove_text = period.split('\r')[1]
        split_date = remove_text.split('\n\t\t\t\t\t\t\t\t\t\t\t')[1]
        start_date = split_date.split('~')[0]
        end_date = split_date.split('~')[1]

        event_info.event_name = event.find('span').get_text().strip()
        event_info.roadshop_name = Roadshops.TONYMOLY
        event_info.image_url = 'http://www.etonymoly.com'+event.find('img').get('src')
        get_link=event.find('a').get('href')
        event_info.link_url = 'http://www.etonymoly.com/html/event/'+get_link.split('\'')[1]

        event_info.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date[0] == '2' and end_date[1] == '0':
            event_info.end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        event_info.is_active = 'Y'

        check_db('TONYMOLY', event_info)


@app.task
def read_url(url):
    f = urllib.request.urlopen(url)
    text = f.read().decode(f.info().get_param('charset'))
    soup = BeautifulSoup(text, "lxml")
    return soup


@app.task
def check_event_active():
    db_eventlist = Roadshops.objects.all().filter(is_active='Y')
    for db_event in db_eventlist:
        now = datetime.now(timezone.utc)
        last_updated = db_event.updated_at

        if now - last_updated > timedelta(hours=24):
            db_event.is_active = 'N'
            db_event.save()


@app.task
def check_db(shop_name, event_info):
    db_eventlist = Roadshops.objects.all().filter(roadshop_name=shop_name, is_active='Y')
    db_count = 0

    if db_eventlist.exists():
        for db_event in db_eventlist:
            check_exist = 0
            check_date = 0
            db_count += 1

            if event_info.event_name == db_event.event_name:
                check_exist += 1
            if event_info.link_url == db_event.link_url:
                check_exist += 1
            if event_info.image_url == db_event.image_url:
                check_exist += 1

            if datetime.date(event_info.start_date) == datetime.date(db_event.start_date):
                check_date += 1
            if event_info.end_date is not None and db_event.end_date is not None:
                if datetime.date(event_info.end_date) == datetime.date(db_event.end_date):
                    check_date += 1

            if check_exist == 3 and check_date == 2:
                db_event.save()
                break
            elif check_exist == 0 and db_count == len(db_eventlist):
                event_info.save()
                break
            elif (1 < check_exist < 3) or (1 < check_exist and check_date < 2):
                db_event.event_name = event_info.event_name
                db_event.start_date = event_info.start_date
                db_event.end_date = event_info.end_date
                db_event.describe = event_info.describe
                db_event.link_url = event_info.link_url
                db_event.image_url = event_info.image_url
                db_event.modified_at = datetime.now()
                db_event.save()
                break

    else:
        event_info.save()
