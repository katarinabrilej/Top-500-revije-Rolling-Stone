import re
import orodja
import uredi_imena


vzorec_bloka = re.compile(
    r'id="list-item.*?'
    r'</article><!-- .c-list__item -->',
    flags=re.DOTALL
)

vzorec_skladbe = re.compile(
    r'data-list-item="(?P<id>\d+)".*?'
    r'data-list-title="(?P<izvajalec>.*?), (I)?&(#8216;)?(#8217;)?.*?'
    r'(?P<naslov>.*?)(&#8217;)?".*?data-list-permalink="https://www.rollingstone..*?'
    r'Writer(s)?:( )?(</strong>)?(&#xA0;</strong>)?(</a>)?(?P<avtor>.*?)(<strong>)?(<span>&#xA0;</span>)?<br.*?'
    r'Producer(s)?(:)?(&#xA0;)?(</strong>)?( </strong>)?(:)?(?P<producent>.*?)(<strong>)?(<b.*?)?( )?Released.*?'
    r'(&apos;)?(&#8217;)?(&#x2019;)?(?P<leto>\d{2,4})(,)?(?P<zalozba>.*?)</p>.*?',
    flags = re.DOTALL
)

vzorec_avtor2 = re.compile(
    r'.*?>(?P<avtor2>.*?)</a>.*?',
    flags = re.DOTALL
)

vzorec_producent2 = re.compile(
    r'</strong>(?P<producent2>.*)',
    flags = re.DOTALL
)

vzorec_zalozba_billboard = re.compile(
    r'(?P<zalozba2>.*?)(<strong>)?<br />(</strong>)?(?P<billboard>.*)',
    flags = re.DOTALL
)

vzorec_billboard_p = re.compile(
    r'Released:.*?</p>.*?<p>(?P<tedni_p>\d{1,2}).*?week(s)?.*?No..*?(?P<mesto_p>\d{1,2})</p>',
    flags = re.DOTALL
)

vzorec_tedni_dnevi = re.compile(
    r'.*?(?P<tedni>\d{1,2}).*?(?P<mesto>\d{1,2}).*?',
    flags = re.DOTALL
)


vzorec_album = re.compile(
    r'Appears on(:)?.*?(</strong>)?.*?( <em>)?(?P<album>.*?)(\()?(</em>|</a>).*?',
    flags = re.DOTALL
)

vzorec_album2 = re.compile(
    r'.*? >(?P<album2>.*)',
    flags = re.DOTALL
)

vzorec_album3 = re.compile(
    r'.*?(</strong>)?<em>(?P<album3>.*)(</strong>)?',
    flags = re.DOTALL
)

vzorec_album_EP = re.compile(
    r'(<strong>)?(<em>)?(?P<album_EP>.*)(|</strong>)',
    flags = re.DOTALL
)

vzorec_blondie = re.compile(
    r'The 500 Greatest Albums of All Time.*?<em>(?P<album_blondie>.*)</em></a></p>.*?',
    flags = re.DOTALL
)



def uredi_kodiranje(slovar):
    for key, value in slovar.items():
        slovar[key] = slovar[key].strip()
        slovar[key] = slovar[key].replace('&#8217;',"'")
        slovar[key] = slovar[key].replace('&#8216;',"'")
        slovar[key] = slovar[key].replace('&#8221;',"'")
        slovar[key] = slovar[key].replace('&#8211;',"-")
        slovar[key] = slovar[key].replace('&#xA0;'," ")
        slovar[key] = slovar[key].replace('&quot;','"')
        slovar[key] = slovar[key].replace('&apos;',"'")
        slovar[key] = slovar[key].replace('&#x2019;',"'")
        slovar[key] = slovar[key].replace('&#xE9;','é')
        slovar[key] = slovar[key].replace('&#xF6;','ö')
        slovar[key] = slovar[key].replace('&amp;',"&")
        slovar[key] = slovar[key].replace('&#x2026;',"…")
        slovar[key] = slovar[key].replace('</strong>',"")
    return slovar
    

def izloci_podatke_skladbe(blok):
    skladba = vzorec_skladbe.search(blok).groupdict()
    uredi_kodiranje(skladba)
    skladba['id'] = int(skladba['id'])

    avtor2 = vzorec_avtor2.search(skladba['avtor'])
    if avtor2:
        skladba['avtor'] = avtor2['avtor2']
    skladba['avtor']  = skladba['avtor'].split(', ')


    producent2 = vzorec_producent2.search(skladba['producent'])
    if producent2:
        skladba['producent'] = producent2['producent2']
    producent3 = vzorec_avtor2.search(skladba['producent'])
    if producent3:
        skladba['producent'] = producent3['avtor2']
    skladba['producent']  = skladba['producent'].split(', ')

    skladba['leto'] = int(skladba['leto'])
    if skladba['leto'] < 10:
        skladba['leto'] = skladba['leto'] + 2000
    if skladba['leto'] < 100:
        skladba['leto'] = skladba['leto'] + 1900
            

    zalozba_billboard = vzorec_zalozba_billboard.search(skladba['zalozba'])
    billboard_p = vzorec_billboard_p.search(blok)
    if zalozba_billboard:
        skladba['zalozba'] = zalozba_billboard['zalozba2']
        if skladba['zalozba'] == "":
            skladba['zalozba'] = None
        tedni_dnevi = vzorec_tedni_dnevi.search(zalozba_billboard['billboard'])
        if tedni_dnevi:
            skladba['tedni'] = tedni_dnevi['tedni']
            skladba['mesto'] = tedni_dnevi['mesto']
        else:
            skladba['tedni'] = zalozba_billboard['billboard']
            skladba['mesto'] = zalozba_billboard['billboard']
    else:
        skladba['tedni'] = None
        skladba['mesto'] = None
        if billboard_p:
            skladba['tedni']  = billboard_p['tedni_p']
            skladba['mesto']  = billboard_p['mesto_p']
        else:
            skladba['tedni'] = None
            skladba['mesto'] = None
    
    album = vzorec_album.search(blok).groupdict()
    uredi_kodiranje(album)
    skladba['album'] = album['album']
    album2 = vzorec_album2.search(skladba['album'])
    album3 = vzorec_album3.search(skladba['album'])
    if album2:
        skladba['album'] = album2['album2'].strip()
        album_EP = vzorec_album_EP.search(album2['album2'])
        if album_EP:
            skladba['album'] = album_EP['album_EP'].strip()

    else:
        if album3:
            skladba['album'] = album3['album3'].strip()
    if skladba['album'] == "<em>":
        album_blondie = vzorec_blondie.search(blok)
        if album_blondie:
            skladba['album'] = album_blondie['album_blondie']
        

    return skladba

def skladbe_na_strani(st_strani):
    url = (
        'https://www.rollingstone.com/music/music-lists/'
        '500-greatest-songs-of-all-time-151127/'
        '?list_page={}'     
    ).format(st_strani)
    ime_datoteke = 'zajeti-podatki/top-skladbe-{}.html'.format(
        st_strani)
    #orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka.finditer(vsebina):
        yield izloci_podatke_skladbe(blok.group(0))

def izloci_gnezdene_podatke(skladbe):
    avtorji, producenti = [], []

    for skladba in skladbe:
        for producent in skladba.pop('producent'):
            if producent in skladba['izvajalec']:
                if producent in uredi_imena.slovar.keys():
                    producent = producent.replace(producent, uredi_imena.slovar[producent])
            for a in skladba['avtor']:
                if producent in a:
                    if producent in uredi_imena.slovar2.keys():
                        producent = producent.replace(producent, uredi_imena.slovar2[producent])
            producenti.append(
                    {'skladba': skladba['id'], 'producent': producent})

        for avtor in skladba.pop('avtor'):
            if avtor in skladba['izvajalec']:
                if avtor in uredi_imena.slovar.keys():
                    avtor = avtor.replace(avtor, uredi_imena.slovar[avtor])
            avtorji.append({'skladba': skladba['id'], 'avtor': avtor})
            
    return avtorji, producenti


skladbe = []
for st_strani in range(1, 11):
    for skladba in skladbe_na_strani(st_strani):
        skladbe.append(skladba)
orodja.zapisi_json(skladbe, 'obdelani-podatki/skladbe.json')
orodja.zapisi_csv(skladbe, ["id","izvajalec","naslov","avtor","producent","leto","zalozba","tedni","mesto","album"], 'obdelani-podatki/skladbe.csv')
avtorji, producenti = izloci_gnezdene_podatke(skladbe)
orodja.zapisi_csv(avtorji, ['skladba', 'avtor'], 'obdelani-podatki/avtorji.csv')
orodja.zapisi_csv(producenti, ['skladba', 'producent'], 'obdelani-podatki/producenti.csv')
print(len(skladbe))


