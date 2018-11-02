# Obdelava podatkov

Podatke o 500 najboljših pesmih vseh časov  sem uvozila in jih shranila v tri csv datoteke. 

skladbe.csv je glavna datoteka v kateri so vsi podatki, vsebuje naslednje stolpce:
* id  ~  mesto skladbe na strani
* izvajalec ~ izvajalec skladbe
* naslov ~  naslov skladbe
* avtor ~  avtorji skladbe (kot seznam)
* producent ~  producenti skladbe (kot seznam)
* leto ~  leto izida skladbe
* zalozba ~  zalozba, pri kateri je skladba izsla
* tedni ~ število tednov, ko je bila skladba na lestvici Billboard
* mesto ~  najvišje mesto, ki ga je skladba dosegla na lestvici Billboard
(namesto tedna in mesta je lahko napisano tudi npr. Did Not Chart, 
če se skladba ni uvrstila na lestvico)
* album ~ album na katerem je skladba izšla

avtorji.csv vsebuje naslednje stolpce:
* id  ~  mesto skladbe na strani
* avtor ~  avtor skladbe
(avtorjev za posamezno pesem je lahko več, zato so te pesmi podane
tolikokrat kot je avtorjev)

producenti.csv vsebuje naslednje stolpce:
* id  ~  mesto skladbe na strani
* producent ~  producent skladbe
(prav tako je producentov za posamezno pesem lahko več, zato so te 
pesmi podane tolikokrat kot je producentov)
