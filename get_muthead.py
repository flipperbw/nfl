#!/usr/bin/env python2
# coding: utf8

from bs4 import BeautifulSoup
import requests
from time import sleep
from termcolor import colored

players = [
        '1018001323-adam-vinatieri',
        '3-adam-vinatieri',
        '1018011695-johnny-hekker',
]

print '------------------'

for idx, p in enumerate(players):
    print 'Player: {}'.format(p)

    base_url = 'http://www.muthead.com/18/players/prices/{}/playstation-4'.format(p)

    print base_url

    cookies = {
        'Preferences.TimeZoneID': '81'
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': base_url,
        'Upgrade-Insecure-Requests': '1'
    }

    #requests.get('{}/refresh'.format(base_url), cookies=cookies, headers=headers)
    #sleep(1)
    
    q = requests.get('{}/refresh'.format(base_url), cookies=cookies, headers=headers).text
    #q = requests.get(base_url).text
    soup = BeautifulSoup(q, 'lxml')

    last_upd = soup.select('.player-prices-last-updated')[0].find('abbr')['title']
    print 'Updated: {}'.format(last_upd)
    
    a = soup.select('.player-prices-advanced-statistics')[0].find('td', text="Median (Q2)")
    med = a.find_next_sibling().text
    print 'Median: {}'.format(med)

    w = soup.select('.player-prices-live-auctions')[0]
    l = w.find_all('tr')[1:]
    for i in l:
        v = i.find_all('td')[-1].text
        try:
            vf = float(v.replace(',', ''))
        except ValueError as e:
            pass
        else:
            if vf < float(med.replace(',', '')):
                v = '{} **'.format(colored(v, 'green'))
        print v

    print '------------------'

    if idx != len(players) - 1:
        sleep(1)
