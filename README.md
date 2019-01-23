Top 500 revije Rolling Stone
=============================================

Analizirala bom top 500 skladb vseh časov po mnenju revije Rolling Stone,
seznam pa je dostopen na strani:
https://www.rollingstone.com/music/music-lists/500-greatest-songs-of-all-time-151127/

Za vsako skladbo bom pridobila naslednje podatke:
* izvajalec
* naslov skladbe
* avtor skladbe
* producent
* leto izida
* najvišje mesto na lestvici Bilboard Hot 100
* število tedno na lestvici Bilboard Hot 100
* opis
* album
* založba

(postopek je v datoteki podatki.py, shranjene strani v mapi zajeti-podatki,
tabele pa v mapi obdelani-podatki)

Delovne hipoteze:
* Ali sta najvišje mesto in število tednov na lestvici Billboard Hot 100 povezani?
* Ali so pesmi enakomerne porazdeljene po desetletjih?
* Katera založba/izvajalec/producent/avtor ima največ skladb uvrščenih na seznam?
* Ali obstaja povezava med mestom na naši lestvici in mestom ter tedni na lestvici Bllboard?
* Kakšen je delež prvih mest na lestvici Billboard?
* Katerih izvajalcem je uspelo v enem letu ustvariti največ pesmi na lestvici?

Podatki so shranjeni v mapi obdelani-podatki, kjer so tudi na kratko opisani v README datoteki.
Uvoz podatkov pa je shranjen v datoteki podatki.py (skupaj s pomožno datoteko orodja.py). Analiza.ipynb vsebuje analizo podatkov, kjer sem testirala delovne hipoteze. 

