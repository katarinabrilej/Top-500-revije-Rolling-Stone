import csv
import json
import os
import re
import sys

import requests


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


def zapisi_json(objekt, ime_datoteke):
    '''Iz danega objekta ustvari JSON datoteko.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)


vzorec = re.compile(
    r'data-list-item="(?P<mesto>\d+)".*?'
    r'data-list-title="(?P<avtor>.*?), (I)?&(#8216;)?(#8217;)?(?P<naslov>.*?)(&#8217;)?".*?data-list-permalink="https://www.rollingstone..*?'
    r'Producer(s)?(:)?(&#xA0;)?(</strong>)?( </strong>)?(:)?(?P<producent>.*?)(<.*?)?( )?Released:.*?'
    r'(&apos;)?(&#8217;)?(&#x2019;)?(?P<leto>\d{2,4})(,)?(?P<zalozba>.*?)</p>.*?'
    #<br />.*?(?P<tedni>\d{1,2}).*?
    r'Appears on:.*?<em>(<a  href=)?.*?>(?P<album>.*?)(</a>)?</em>.*?',

    


    
    #r'href="/title/tt(?P<id>\d+)/\?ref_=adv_li_tt"[^>]*?'
    #r'>(?P<naslov>.+?)</a>.*?'
    #r'lister-item-year text-muted unbold">.*?\((?P<leto>\d{4})\)</span>.*?'
    #r'runtime">(?P<dolzina>\d+?) min</.*?'
    #r'<strong>(?P<ocena>.+?)</strong>.*?'
    #r'<p class="text-muted">(?P<opis>.+?)<.*?',
    re.DOTALL
)


def izloci_podatke_skladbe(ujemanje_skladbe):
    podatki_skladbe = ujemanje_skladbe.groupdict()
    podatki_skladbe['mesto'] = int(podatki_skladbe['mesto'])
    podatki_skladbe['avtor'] = podatki_skladbe['avtor'].replace('&#8217;',"'")
    podatki_skladbe['naslov'] = podatki_skladbe['naslov'].replace('&#8217;',"'")
    podatki_skladbe['naslov'] = podatki_skladbe['naslov'].replace('&#8216;',"'")
    podatki_skladbe['naslov'] = podatki_skladbe['naslov'].replace('&#8221;',"'")
    podatki_skladbe['naslov'] = podatki_skladbe['naslov'].replace('&#8211;',"-")
    podatki_skladbe['naslov'] = podatki_skladbe['naslov'].replace('&amp;',"&")
    podatki_skladbe['producent'] = podatki_skladbe['producent'].replace('&#xA0;',"").strip()
    podatki_skladbe['producent'] = podatki_skladbe['producent'].replace('&quot;','"')
    podatki_skladbe['producent'] = podatki_skladbe['producent'].replace('&#xE9;','é')
    podatki_skladbe['producent'] = podatki_skladbe['producent'].replace('&apos;',"'")
    podatki_skladbe['zalozba'] = podatki_skladbe['zalozba'].replace('&amp;',"&")
    podatki_skladbe['zalozba'] = podatki_skladbe['zalozba'].replace('&#xA0;',"").strip()


    #podatki_skladbe['leto'] = int(podatki_skladbe['leto'])
    #podatki_skladbe['opis'] = podatki_skladbe['opis'].strip()
    #podatki_skladbe['dolzina'] = int(podatki_skladbe['dolzina'])
    #podatki_skladbe['ocena'] = float(podatki_skladbe['ocena'].replace(',', '.'))
    return podatki_skladbe


#for i in range(1, 11):
#    url = (
#        'https://www.rollingstone.com/music/music-lists/'
#        '500-greatest-songs-of-all-time-151127/'
#        '?list_page={}'     
#    ).format(i)
#    shrani_spletno_stran(url, 'zajeti-podatki/top-skladbe-{}.html'.format(i))


podatki_skladb = []
for i in range(1, 11):
    vsebina = vsebina_datoteke(
        'zajeti-podatki/top-skladbe-{}.html'.format(i))
    for ujemanje_skladbe in vzorec.finditer(vsebina):
        #print(podatki_skladb)
        podatki_skladb.append(izloci_podatke_skladbe(ujemanje_skladbe))
zapisi_json(podatki_skladb, 'obdelani-podatki/vse-skladbe.json')
zapisi_csv(podatki_skladb, ["mesto","avtor","naslov","producent","leto","zalozba","album"], 'obdelani-podatki/vse-skladbe.csv')

print(len(podatki_skladb))

