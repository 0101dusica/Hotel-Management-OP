import json
from datetime import datetime, timedelta, date
import random
from tabulate import tabulate
from check import *
from prints import *

def promena_sifre(korisnicko_ime): #funkcija koja omogucava domacinu da promeni sifru nakon sto mu administrator napravi nalog
    stara_sifra = input("Unesite staru sifru: ")
    promena = []
    count = 0
    with open("../data/korisnici.json", "r", encoding="utf-8") as f:
        korisnici = json.load(f)
        for korisnik in korisnici:
            if( korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower()):
                if(korisnik["lozinka"] == stara_sifra):
                    nova_sifra = input("Unesite novu sifru: ")
                    recnik = {"korisnicko_ime": korisnik["korisnicko_ime"], "lozinka": nova_sifra, "ime": korisnik["ime"], "prezime": korisnik["prezime"],"pol": korisnik["pol"], "kontakt_telefon": korisnik["kontakt_telefon"], "email": korisnik["email"], "uloga":korisnik["uloga"], "status": korisnik["status"]}
                    count = count+1
            else:
                promena.append(korisnik)

    if(count != 0 ):
        promena.append(recnik)
        with open("../data/korisnici.json", "w", encoding="utf-8") as f:
            json.dump(promena, f, indent= 4)

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Uspesno ste promenili vasu sifru! ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    else:
        print("Niste uneli tacnu sifru! ")

def dodavanje_apartmana(korisnicko_ime): #domacin ima opciju da unese novi apartman, sa svim detaljima o istom
    with open("../data/korisnici.json", "r", encoding="utf-8") as f:
        korisnici = json.load(f)
        for korisnik in korisnici:
            if( korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower()):
                domacin = korisnik["ime"] + " " + korisnik["prezime"]

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Pazljivo unesite sve potrebne podatke da biste uspesno uneli novi apartman na nas listing!")
    provera = False
    while( provera == False): #petlja se izvrsava sve dok korisnik ne unese jednu od ponudjenih opcija
        tip = input("Da li je vas smestaj apartman ili soba? ")
        if (tip.lower() == "soba"): #ukoliko je tip soba, automatski se dodeljuje broj soba, tj 1
            broj_soba = 1
            provera = True
        elif(tip.lower() == "apartman"):
            provera_soba = False
            while(provera_soba == False):#korisnik unosi broj soba, koji ne moze da bude manji od 1
                print("Koliko soba ima vas apartman ? ", end="")
                broj_soba = int_provera(False)
                if(broj_soba <= 0):
                    print("Apartman ne moze da ima manje od 1 sobe! Pokusajte ponovo sa unosom!")
                else:
                    provera_soba = True        
            provera = True
        else:
            print("Mozete da unesete samo apartman ili sobu! Pokusajte ponovo! ")

    provera_osoba = False
    while(provera_osoba == False):
        print("Koliko osoba moze da boravi u vasem apartmanu? ", end="")
        broj_osoba = int_provera(False)
        if(broj_osoba <= 0):
            print("Apartman ne moze da prima manje od 1 osobe! Pokusajte ponovo sa unosom!")
        else:
            provera_osoba = True 

    #geografska duzina i sirina se random dodeljuju kao decimalni brojevi, a zatim se prebacuju u string kako bi bile upisane u json
    gs = float(random.randint(41,46)) + random.random()
    gs = str(round(gs, 2))
    gd = float(random.randint(18,22)) + random.random()
    gd = str(round(gd, 2))

    #broj mora biti unet u formatu int, postanski broj takodje, izvrsavaju se provere
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Unesite adresu na kojoj se nalazi vas apartman")
    ulica = input("Ulica: ")
    print("Broj: ", end="")
    broj = int_provera(False)
    ulica_i_broj = ulica + " " + str(broj)
    mesto = input("Mesto: ")
    print("Postanski Broj: ", end="")
    postanski_broj = int_provera(False)
    postanski_broj = str(postanski_broj)

    #cena se proverava da li je int i da li je manja od nule
    provera_cene = False
    while(provera_cene == False):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Unesite cenu boravka po jednoj noci za vas apartman: ", end="")
        cena = int_provera(False)
        if(cena <= 0):
            print("Apartman ne moze da ima cenu manju od 1 dinara!")
        else:
            provera_cene = True 


    #unosenje vec postojecih rezervacija od strane domacina
    lista_od = []
    lista_do = []
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Da li vec imate neke rezervacije za ovaj apartman ? ", end="")
    rez_odg = provera_odgovora(False)

    if(rez_odg.lower() == "da"): #u slucaju da domacin vec ima neke rezervacije za ovaj apartman unosi ih 
        print("Unesite sve datume za koje vec postoje rezervacije")
        neko = False
        while(neko == False):
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Unesite pocetni datum rezervacije: ")
            pocetni_datum = unos_datuma()
            pocetni = str(pocetni_datum.year) + "." + str(pocetni_datum.month) + "." + str(pocetni_datum.day) + "." 

            print("Unesite krajnji datum rezervacije: ")
            krajnji_datum = unos_datuma()
            krajnji = str(krajnji_datum.year) + "." + str(krajnji_datum.month) + "." + str(krajnji_datum.day)+ "." 
            
            if((pocetni_datum < date.today()) == True or (krajnji_datum < date.today()) == True ):# u slucaju da korisnik ne unese datume dobro na konzolu se ispisuje odgovarajuca greska
                print("Ne mozete da unosite rezervacije u proslosti! Pokusajte ponovo!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            elif((pocetni_datum > krajnji_datum) == True): 
                print("Krajnji datum ne moze biti pre pocetnog! Pokusajte ponovo!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            else:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("Da li imate jos rezervacija koje trebate da unesete ? ", end="")
                odgovor = provera_odgovora(False)
                if(odgovor.lower() == "ne"):
                    lista_od.append(pocetni)
                    lista_do.append(krajnji)
                    neko = True
                elif( odgovor.lower() == "da"):
                    lista_od.append(pocetni)
                    lista_do.append(krajnji)

        dostupnost = []
        danas = date.today()
        datum = str(danas.year) + "." + str(danas.month) + "." + str(danas.day) + "."
        datum_kraj = str(danas.year+100) + "." + str(danas.month) + "." + str(danas.day) + "."
        recnik = {"od": datum, "do": lista_od[0]}
        dostupnost.append(recnik)    
        for i in range(len(lista_od)):
            if(i+1 == len(lista_od)): #ako je poslednji recnik koji se unosi u listu, kao poslednji datum unosi se datum za 100 godina :)
                recnik = {"od": lista_do[i], "do": "2100.01.01."}
            else:
                recnik = {"od": lista_do[i], "do": lista_od[i+1]}

            dostupnost.append(recnik)     
    else:
        dostupnost = []
        danas = date.today()
        datum = str(danas.year) + "." + str(danas.month) + "." + str(danas.day) + "."
        do = str(danas.year+100) + "." + str(danas.month) + "." + str(danas.day) + "."
        recnik = {"od": datum, "do": do}

        dostupnost.append(recnik)
    #domacin ima mogucnost da unese dodatnu opremu koja predhodno postoji i kreirana je od strane administratora
    
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Unesite dodatnu opremu koju vas apartman poseduje!")
    print("Da li zelite da pretrazujete po: ")
    print("1. Sifri dodatne opreme")
    print("2. Pretragom naziva dodatne opreme")
    
    odabir = provera_broja(False, 0, 3) 
        
    
    oprema_sifre_lista = []
    nazivi_opreme_lista = []
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print("Lista dodatne opreme: ")
    with open("../data/dodatna_oprema.json", "r", encoding="utf-8") as f:
        dodatna_oprema = json.load(f)
        for stavka in dodatna_oprema:
            print("Sifra: ", stavka["sifra"])
            print("Naziv: ", stavka["naziv"])
            print("~~~~~~~~~~~~~~~~~~~~~~~~")
    provera_opreme = False
    while(provera_opreme == False):
        if(odabir == 1):
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Unesite sifru dodatne opreme koju zelite da unesete: ", end="")
            oprema_sifra = int_provera(False)

            if(oprema_sifra in oprema_sifre_lista):
                print("Vec ste uneli sifru za ovu dodatnu opremu !")
            else:
                oprema_sifre_lista.append(oprema_sifra)

            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Da li zelite da unesete jos dodatne opreme ? da ne -> ", end="")
            odgovor_nastavak = provera_odgovora(False)
            if(odgovor_nastavak.lower() == "ne"):
                provera_opreme = True
        else:
            print("Unesite naziv dodatne opreme koju zelite da unesete: ", end="")
            naziv_opreme = input()
            if(naziv_opreme in nazivi_opreme_lista):
                print("Vec ste uneli naziv za ovu dodatnu opremu !")
            else:
                nazivi_opreme_lista.append(naziv_opreme.lower())

            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Da li zelite da unesete jos dodatne opreme ?  ", end="")
            odgovor_nastavak = provera_odgovora(False)
            if(odgovor_nastavak.lower() == "ne"):
                provera_opreme = True

    dodatna_oprema_unos = []
    
    with open("../data/dodatna_oprema.json", "r", encoding="utf-8") as f: #u fajlu sa dodatnom opremom proverava se da li je korisnik uneo tacne informacije
        dodatna_oprema = json.load(f)
        for stavka in dodatna_oprema:
            if(odabir == 1):
                for i in range(len(oprema_sifre_lista)):
                    if(stavka["sifra"] == oprema_sifre_lista[i]):
                        dodatna_oprema_unos.append(stavka)
            else:
                for i in range(len(nazivi_opreme_lista)):
                    if(nazivi_opreme_lista[i].lower() in stavka["naziv"].lower() ):
                        dodatna_oprema_unos.append(stavka)

    lista_sifri = []
    with open("../data/apartmani.json", "r", encoding="utf-8") as f: #potrebno je pronaci poslednju sifru da bi sledeci apartman imao sifru +1
        apartmani = json.load(f)
        for apartman in apartmani:
            lista_sifri.append(apartman["sifra"])

    dodatna_oprema_unos.sort(key=lambda x: x.get('sifra')) #dodatna oprema se sortira prema sifri
    
    if(len(lista_sifri) > 0):
        lista_sifri.sort()
        sifra = lista_sifri[len(lista_sifri)-1]+1
    else:
        sifra = 1

    upis = {"sifra" : sifra, "tip": tip, "broj_soba": broj_soba, "broj_gostiju": broj_osoba, "lokacija": 
    {"geografska_sirina": gs, "geografska_duzina": gd, "adresa": {"ulica_broj": ulica_i_broj.title(), "grad": mesto.title(),"postanski_broj": postanski_broj}},
    "dostupnost": dostupnost, "domacin": domacin, "cena_po_noci": cena, "status": "neaktivno", "sadrzaj_apartmana": dodatna_oprema_unos}
    #recnik koji je sastavljen od podataka koje je uneo korisnik, se upisuje u json datoteku

    apartmani.append(upis)
    with open("../data/apartmani.json", "w", encoding="utf-8") as f:
        json.dump(apartmani, f, indent= 4)

    print("Vas apartman je uspesno dodat u nasu bazu podataka, potvrdom administratora apartman prelazi u aktivno stanje!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
def izmena_podataka_apartmana(korisnicko_ime): #domacin ima mogucnost da menja podatke o apartmanu koji je uneo ranije

    with open("../data/korisnici.json", "r", encoding="utf-8") as f:
        korisnici = json.load(f)
        for korisnik in korisnici:
            if( korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower()):
                domacin = korisnik["ime"] + " " + korisnik["prezime"]

    brojac = 0
    ispis = []
    with open("../data/apartmani.json", "r", encoding="utf-8") as f:#ispisuje se ista svih njegovih apartmana
        apartmani = json.load(f)
        for apartman in apartmani:
            if(apartman["domacin"].lower() == domacin.lower()):
                ispis.append(ispis_apartmana(apartman))
                brojac = brojac + 1

    if(brojac == 0):
        print("Trenutno nemate ni jedan apartman! Pokusajte prvo da unesete novi apartman!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    else:
        header = ["Sifra", "Domacin", "Tip", "Sobe", "Gosti", "Adresa", "Cena", "Sadrzaj Apartmana"]
        print(tabulate(ispis, header, tablefmt="psql"))
    
        print("Unesite sifru apartmana za koji zelite da menjate podatke: ", end="")
        sifra = int_provera(False) 

        upis = []
        promena = 0
        with open("../data/apartmani.json", "r", encoding="utf-8") as f: #trazi se apartman za koji domacin zeli da menja podatke
            apartmani = json.load(f)
            for apartman in apartmani:
                if(apartman["domacin"].lower() == domacin.lower()):
                    if(apartman["sifra"] != sifra):
                        upis.append(apartman)
                    else:
                        izmena = apartman
                        promena = promena + 1
                else:
                    upis.append(apartman)

        if(promena == 0): #u slucaju da apartman sa takvom sifrom ne postoji ispisuje se greska na ekran
            print("Ne postoji apartman sa sifrom koju ste vi uneli! ")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        else:
            provera = True 
            while(provera == True):
                print("1. Tip i Broj soba")
                print("2. Broj Gostiju")
                print("3. Lokacija")
                print("4. Promenite termine dostupnosti")
                print("5. Cena po Noci")
                print("6. Dodatna Oprema")
                pretraga = provera_broja(False, 0,7) #domacin bira sta od informacija zeli da menja

                if(pretraga == 1): #tip i broj soba
                    provera_tipa = False
                    while( provera_tipa == False): #petlja se izvrsava sve dok korisnik ne unese jednu od ponudjenih opcija
                        tip = input("Da li je vas smestaj apartman ili soba? ")
                        if (tip.lower() == "soba"):
                            broj_soba = 1
                            provera_tipa = True
                        elif(tip.lower() == "apartman"):
                            provera_soba = False
                            while(provera_soba == False):
                                print("Koliko soba ima vas apartman ? ", end="")
                                broj_soba = int_provera(False)
                                if(broj_soba <= 0):
                                    print("Apartman ne moze da ima manje od 1 sobe! Pokusajte ponovo sa unosom!")
                                else:
                                    provera_soba = True        
                            provera_tipa = True
                        else:
                            print("Mozete da unesete samo apartman ili sobu! Pokusajte ponovo! ")

                    izmena["tip"] = tip
                    izmena["broj_soba"] = broj_soba
                elif(pretraga == 2): #broj gostiju
                    provera_osoba = False
                    while(provera_osoba == False):
                        print("Koliko osoba moze da boravi u vasem apartmanu ? ", end="")
                        broj_osoba = int_provera(False) #ovde sam stala, nastaviti sa proverama
                        if(broj_osoba <= 0):
                            print("Apartman ne moze da prima manje od 1 osobe! Pokusajte ponovo sa unosom!")
                        else:
                            provera_osoba = True 
                    izmena["broj_gostiju"] = broj_osoba
                elif(pretraga == 3): #lokacija
                    #geografska duzina i sirina se random dodelju kao decimalni brojevi, a zatim se prebacuju u string kako bi bile upisane u jsonu
                    gs = float(random.randint(41,46)) + random.random()
                    gs = str(round(gs, 2))
                    gd = float(random.randint(18,22)) + random.random()
                    gd = str(round(gd, 2))

                    #broj mora biti unet u formatu int, postanski broj takodje, izvrsavaju se provere
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print("Unesite adresu na kojoj se nalazi vas apartman")
                    ulica = input("Ulica: ")
                    print("Broj: ", end="")
                    broj = int_provera(False)
                    ulica_i_broj = ulica + " " + str(broj)
                    mesto = input("Mesto: ")
                    print("Postanski Broj: ", end="")
                    postanski_broj = int_provera(False)
                    postanski_broj = str(postanski_broj)

                    izmena["lokacija"]["geografska_sirina"] = gs
                    izmena["lokacija"]["geografska_duzina"] = gd
                    izmena["lokacija"]["adresa"]["ulica_broj"] = ulica_i_broj.title()
                    izmena["lokacija"]["adresa"]["grad"] = mesto.title()
                    izmena["lokacija"]["adresa"]["postanski_broj"] = postanski_broj
                elif(pretraga == 4): #termini dostupnosti
                    dostupnost = izmena["dostupnost"]
                    print("Dostupni termini za ovaj apartmanu su: ") #ispis dostupnih termina za apartman u narednih godinu dana
                    datum_za_godinu = date(date.today().year+1, date.today().month, date.today().day)
                    for i in range(len(dostupnost)):
                        od_lista = dostupnost[i]["od"].split(".")
                        od = date(int(od_lista[0]), int(od_lista[1]), int(od_lista[2]))
                        do_lista = dostupnost[i]["do"].split(".")
                        do = date(int(do_lista[0]), int(do_lista[1]), int(do_lista[2]))
                        if(od < datum_za_godinu):
                            if(od < date.today()):
                                if(do > date.today()):
                                    if(do < datum_za_godinu):
                                        print("Od: ", date.today(), " Do: ",do)
                                    else:
                                        print("Od: ", date.today(), " Do: ", datum_za_godinu)
                            else:
                                if(do < datum_za_godinu):
                                    print("Od: ", od, " Do: ",do)
                                else:
                                    print("Od: ", od, " Do: ", datum_za_godinu)

                    neko = False
                    lista_od = []
                    lista_do = []
                    while(neko == False):
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print("Unesite pocetni datum rezervacije: ")
                        pocetni_datum = unos_datuma()
                        pocetni = str(pocetni_datum.year) + "." + str(pocetni_datum.month) + "." + str(pocetni_datum.day) + "." 

                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print("Unesite krajnji datum rezervacije: ")
                        krajnji_datum = unos_datuma()
                        krajnji = str(krajnji_datum.year) + "." + str(krajnji_datum.month) + "." + str(krajnji_datum.day)+ "." 
                        
                        if((pocetni_datum < date.today()) == True or (krajnji_datum < date.today()) == True ):# u slucaju da korisnik ne unese datume dobro na konzolu se ispisuje odgovarajuca greska
                            print("Ne mozete da unosite rezervacije u proslosti! Pokusajte ponovo!")
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        elif((pocetni_datum > krajnji_datum) == True): 
                            print("Krajnji datum ne moze biti pre pocetnog! Pokusajte ponovo!")
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        else:
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                            lista_od.append(pocetni)
                            lista_do.append(krajnji)
                            neko = True

                        
                    count = 0
                    for i in range(len(dostupnost)): #proverava se da li je apartman dostupan od pocetnog datuma koji je korisnik uneo
                        od_lista = dostupnost[i]["od"].split(".")
                        od = date(int(od_lista[0]), int(od_lista[1]), int(od_lista[2]))
                        do_lista = dostupnost[i]["do"].split(".")
                        do = date(int(do_lista[0]), int(do_lista[1]), int(do_lista[2]))
                        if(pocetni_datum >= od and pocetni_datum < do):
                            count = count + 1
                    
                    
                    if(count == 0 ): #ako apartman nije dostupan, ispisuje se greska
                        print("Apartman nije dostupan u terminu koji vi pretrazujete!")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        m = True
                    else:
                        b = str(krajnji_datum - pocetni_datum)
                        br = b.split(" ")
                        broj_nocenja = int(br[0])
                        brojac = 0
                        for k in range(broj_nocenja):
                            provera = pocetni_datum + timedelta(days = k)

                            for i in range(len(dostupnost)):
                                od_lista = dostupnost[i]["od"].split(".")
                                od = date(int(od_lista[0]), int(od_lista[1]), int(od_lista[2]))
                                do_lista = dostupnost[i]["do"].split(".")
                                do = date(int(do_lista[0]), int(do_lista[1]), int(do_lista[2]))
                                if(provera >= od and provera < do):
                                    brojac = brojac + 1

                        
                        if(brojac != broj_nocenja):
                            print("Period za koji pokusavate da unsete rezervaciju trenutno nije dostupan!")
                        else:
                            print("Uspseno ste izmenili dostupnost za ovaj apartman!")
                            nova_dostupnost = []
                            for i in range(len(dostupnost)):
                                od_lista = dostupnost[i]["od"].split(".")
                                od = date(int(od_lista[0]), int(od_lista[1]), int(od_lista[2]))
                                do_lista = dostupnost[i]["do"].split(".")
                                do = date(int(do_lista[0]), int(do_lista[1]), int(do_lista[2]))

                                if(pocetni_datum >= od and krajnji_datum <= do):#u slucaju da su pocetni datum rezervacije i poslednji datum rezervacije izmedju odredjenog termina koji je slobodan u apartmanu, pravi se izmena u dostupnosti
                                    prvi_dan = str(pocetni_datum.year)+"."+str(pocetni_datum.month)+"."+str(pocetni_datum.day)+"."
                                    recnik_dostupnost = {"od": dostupnost[i]["od"], "do": prvi_dan}
                                    poslednji_datum = str(krajnji_datum.year)+"."+str(krajnji_datum.month)+"."+str(krajnji_datum.day)+"."
                                    recnik_dostupnost1 = {"od": poslednji_datum, "do": dostupnost[i]["do"]}
                                    nova_dostupnost.append(recnik_dostupnost)
                                    nova_dostupnost.append(recnik_dostupnost1)
                                else: 
                                    nova_dostupnost.append(dostupnost[i]) #updatovana dostupnost u apartmanima
                                                                                
                            izmena["dostupnost"] = nova_dostupnost
                elif(pretraga == 5): #cena po noci
                    provera_cene = False
                    #cena se proverava da li je int i da li je manja od nule
                    provera_cene = False
                    while(provera_cene == False):
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print("Unesite cenu boravka po jednoj noci za vas apartman: ", end="")
                        cena = int_provera(False)
                        if(cena <= 0):
                            print("Apartman ne moze da ima cenu manju od 1 dinara!")
                        else:
                            provera_cene = True 
                    izmena["cena_po_noci"] = cena
                elif(pretraga == 6): #dodatna oprema
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print("Da li zelite da: ")
                    print("1. Dodate novu dodatnu opremu")
                    print("2. Obrisete dodatnu opremu")
                    odabir = provera_broja(False, 0, 3) #mogucnost da obrise postojecu ili doda novu
                        
                    oprema_sifre_lista = [] #ovde su smestene sifre dodatne oprema koja vec postoji u ovom apartmanu
                    for i in range(len(izmena["sadrzaj_apartmana"])):
                        oprema_sifre_lista.append(izmena["sadrzaj_apartmana"][i]["sifra"]) 
                    
                    provera_opreme = False
                    while(provera_opreme == False):
                        if(odabir == 1): #dodavanje nove opreme
                            
                            print("DODATNA OPREMA U VASEM APARTMANU: ") #ispisuje se sva dodatna oprema koja postoji u tom apatmanu
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                            for i in range(len(izmena["sadrzaj_apartmana"])):
                                print("Sifra: ", izmena["sadrzaj_apartmana"][i]["sifra"])
                                print("Naziv: ", izmena["sadrzaj_apartmana"][i]["naziv"])
                                print("~~~~~~~~~~~~~~~~~~~~~~~~")

                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                            print("Lista dodatne opreme: ") #ispisuje se lista dodatne opreme koju je administrator do sada kreirao
                            with open("../data/dodatna_oprema.json", "r", encoding="utf-8") as f:
                                dodatna_oprema = json.load(f)
                                for stavka in dodatna_oprema:
                                    print("Sifra: ", stavka["sifra"])
                                    print("Naziv: ", stavka["naziv"])

                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                            print("Unesite sifru dodatne opreme koju zelite da unesete: ", end="")
                            oprema_sifra = int_provera(False) 
                            
                            if(oprema_sifra in oprema_sifre_lista): #ako ne postoji dodatna oprema pod sifrom koju je domaicn uneo, ispisuje se greska na ekran
                                print("Ova dodatna oprema vec postoji kao opis vaseg apartmana !")
                            else:
                                oprema_sifre_lista.append(oprema_sifra)
                                with open("../data/dodatna_oprema.json", "r", encoding="utf-8") as f:
                                    dodatna_oprema = json.load(f)
                                    for stavka in dodatna_oprema:
                                        if(stavka["sifra"] == oprema_sifra):
                                            recnik = {"sifra": stavka["sifra"], "naziv": stavka["naziv"]}
                                            izmena["sadrzaj_apartmana"].append(recnik) #kada se pronadje dodatna oprema sa odg sifrom, ona se dodaje u apartman koji menjamo
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                            print("Da li zelite da unesete jos dodatne opreme ? ", end="")
                            odgovor_nastavak = provera_odgovora(False) #domacin ponavlja dodavanje sve dok on to zeli
                            
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                            if(odgovor_nastavak.lower() == "ne"):
                                provera_opreme = True

                        else: #brisanje opreme
                            if(len(oprema_sifre_lista) > 0): #provera da li postoji podataka koje korisnik moze da obrise 
                                #ispis trenutno postojece dodatne opreme u apartmanu
                                print("DODATNA OPREMA U VASEM APARTMANU: ")
                                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                for i in range(len(izmena["sadrzaj_apartmana"])):
                                    print("Sifra: ", izmena["sadrzaj_apartmana"][i]["sifra"])
                                    print("Naziv: ", izmena["sadrzaj_apartmana"][i]["naziv"])
                                    print("~~~~~~~~~~~~~~~~~~~~~~~~")

                                #unos sifre po kojoj ce se obrisati odredjena stavka iz dodatne opreme
                                print("Unesite sifru dodatne opreme koju zelite da obrisete: ", end="")
                                oprema_sifra = int_provera(False)
                                        
                                if(oprema_sifra in oprema_sifre_lista): #ako sifra koju je domacin uneo postoji u listi dodatne opreme koja je vec uneta, brisanje je moguce
                                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                                    sadrzaj_nova_lista = []
                                    for i in range(len(izmena["sadrzaj_apartmana"])):
                                        if(izmena["sadrzaj_apartmana"][i]["sifra"] != oprema_sifra): #ako se sifra trenutne dodatne opreme u apartmanu i sifra koju je domacin uneo ne poklapaju, ta dodatna oprema ce biti kopirana u novu listu
                                            sadrzaj_nova_lista.append(izmena["sadrzaj_apartmana"][i])
                                        else:
                                            oprema_sifre_lista.remove(oprema_sifra)
                                        
                                    sadrzaj_nova_lista.sort(key=lambda x: x.get('sifra')) #dodatna oprema se sortira po siframa
                                    izmena["sadrzaj_apartmana"] = sadrzaj_nova_lista
                                    
                                else:
                                    print("Ne postoji dodatna oprema sa ovom sifrom! ")

                                if(len(oprema_sifre_lista) > 0 ):
                                    print("Da li zelite da obrisete jos dodatne opreme ? ", end="")
                                    odgovor_nastavak = provera_odgovora(False)
                                    
                                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                    if(odgovor_nastavak.lower() == "ne"):
                                        provera_opreme = True
                                else:
                                    print("Ne postoji vise dodatne opreme koju mozete da obrisete! ")
                                    provera_opreme = True
                                    
                                
                print("Da li zelite da menjate jos podataka za ovaj apartman ? ", end="")
                ispis = provera_odgovora(False)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                if(ispis.lower() == "ne"):
                    provera = False

            izmena["sadrzaj_apartmana"].sort(key=lambda x: x.get('sifra')) #dodatna oprema se uvek sortira po siframa
            upis.append(izmena) 
            upis.sort(key=lambda x: x.get('sifra')) #apartmani se sortiraju pre upisa
            with open("../data/apartmani.json", "w", encoding="utf-8") as f:
                json.dump(upis, f, indent= 4)
            
def brisanje_apartmana(korisnicko_ime): #domacin ima opciju da obrise apartman koji je ranije uneo
    with open("../data/korisnici.json", "r", encoding="utf-8") as f:
        korisnici = json.load(f)
        for korisnik in korisnici:
            if( korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower()):
                domacin = korisnik["ime"] + " " + korisnik["prezime"]

    brojac = 0
    ispis = []
    with open("../data/apartmani.json", "r", encoding="utf-8") as f: #ispis liste svih njegovih apartmana
        apartmani = json.load(f)
        for apartman in apartmani:
            if(apartman["domacin"].lower() == domacin.lower()):
                ispis.append(ispis_apartmana(apartman))
                brojac = brojac + 1

    if(brojac == 0):
        print("Trenutno nemate ni jedan apartman! Pokusajte prvo da unesete novi apartman!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    else:
        header = ["Sifra", "Domacin", "Tip", "Sobe", "Gosti", "Adresa", "Cena", "Sadrzaj Apartmana"]
        print(tabulate(ispis, header, tablefmt="psql"))
    
        print("Unesite sifru apartmana koji zelite da obrisete: ", end="")
        sifra = int_provera(False) #unosi se sifra apartmana

        brisanje = 0
        upis = []
        with open("../data/apartmani.json", "r", encoding="utf-8") as f:
            apartmani = json.load(f)
            for apartman in apartmani:
                if(apartman["domacin"].lower() == domacin.lower()):
                    if(apartman["sifra"] != sifra):
                        upis.append(apartman)
                    else:
                        brisanje = brisanje + 1
                else:
                    upis.append(apartman)

        if(brisanje == 0):
            print("Ne mozete da obrisete apartman sa ovom sifrom!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        else:
            novi_upis = []
            with open("../data/rezervacije.json", "r", encoding="utf-8") as f: #brisu se sve rezervacije koje su postojale za ovaj apartman
                rezervacije = json.load(f)
                for rezervacija in rezervacije:
                    if(rezervacija["apartman"]["sifra"] != sifra):
                        novi_upis.append(rezervacija)
            
            print("Uspesno ste obrisali ovaj apartman!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            with open("../data/rezervacije.json", "w", encoding="utf-8") as f:
                json.dump(novi_upis, f, indent= 4)
            with open("../data/apartmani.json", "w", encoding="utf-8") as f:
                json.dump(upis, f, indent= 4)

def pregled_rezervacije(korisnicko_ime): #domacin ima mogucnost da vidi sve nepotvrdjene rezervacije koje su vezane za njegove apartmane
    with open("../data/korisnici.json", "r", encoding="utf-8") as f:
        korisnici = json.load(f)
        for korisnik in korisnici:
            if( korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower()):
                domacin = korisnik["ime"] + " " + korisnik["prezime"]

    count = 0
    ispis = []
    with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
        rezervacije = json.load(f)
        for rezervacija in rezervacije:
            if(rezervacija["apartman"]["domacin"].lower() == domacin.lower()):
                if(rezervacija["status"].lower() == "kreirana"):
                    count = count + 1
                    ispis.append(ispis_rezervacija(rezervacija))

    if(count == 0):
        print("Trenutno nema rezervacija za vase apartmane! ")
    else:
        header = ["Sifra", "Adresa", "Datum Rezervacije", "Broj nocenja", "Cena","Osobe prijavljene za boravak u apartmanu", "Status" ]
        print(tabulate(ispis, header, tablefmt="psql"))

def potvrda_odbijanje_rezervacije(korisnicko_ime): #domacin odbija ili potvrdjuje svaku rezervaciju koja mu stigne
    with open("../data/korisnici.json", "r", encoding="utf-8") as f:
        korisnici = json.load(f)
        for korisnik in korisnici:
            if( korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower()):
                domacin = korisnik["ime"] + " " + korisnik["prezime"]

    c = 0
    ispis = []
    with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
        rezervacije = json.load(f)
        for rezervacija in rezervacije:
            if(rezervacija["apartman"]["domacin"].lower() == domacin.lower()):
                if(rezervacija["status"].lower() == "kreirana"):
                    c = c + 1
                    ispis.append(ispis_rezervacija(rezervacija))

    if(c == 0):
        print("Trenutno nema rezervacija za vase apartmane! ")
    else:
        header = ["Sifra", "Adresa", "Datum Rezervacije", "Broj nocenja", "Cena","Osobe prijavljene za boravak u apartmanu", "Status" ]
        print(tabulate(ispis, header, tablefmt="psql"))

        print("Unesite sifru rezervacije koju zelite da potvrdite ili odbijete: ", end="")
        sifra = int_provera(False) #prvo bira koju rezervaciju ce da potvrdi ili odbije
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        count = 0
        rezervacija_upis = []
        with open("../data/rezervacije.json", "r", encoding="utf-8") as f: #proverava se da li ta rezervacija postoji
            rezervacije = json.load(f)
            for rezervacija in rezervacije:
                if(rezervacija["apartman"]["domacin"].lower() == domacin.lower()):
                    if(rezervacija["status"].lower() == "kreirana"):
                        if(rezervacija["sifra_rezervacije"] == sifra):
                            count = count + 1
                            rezervacija_recnik = rezervacija
                            broj_noci = rezervacija["broj_nocenja"]
                        else:
                            rezervacija_upis.append(rezervacija)
                    else:
                        rezervacija_upis.append(rezervacija)
                else:
                    rezervacija_upis.append(rezervacija)

        if(count == 0 ): #ako rezervacija sa tom sifrom ne postoji, ispisuje se greska na ekran
            print("Rezervacija sa sifrom koju ste vi uneli ne postoji!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        else:
            print("Da li zelite da: ")
            print("1. Odbijete Rezervaciju ")
            print("2. Potvrdite Rezervaciju ")

            odgovor = provera_broja(False, 0, 3) #domacin bira zeli li da obrije ili potrvdi rezervaciju
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
            if(odgovor == 1): #domacin odbija rezervaciju
                upis_apartmana = []
                with open("../data/apartmani.json", "r", encoding="utf-8") as f: #pretrazuje se apartman koji je povezan uz ovu rezervaciju
                    apartmani = json.load(f)
                    for apartman in apartmani:
                        if(apartman["sifra"] == rezervacija_recnik["apartman"]["sifra"]):
                            promena = apartman
                        else:
                            upis_apartmana.append(apartman)

                dostupnost = [] 
                s = 0
                for i in range(len(promena["dostupnost"])):
                    d = rezervacija_recnik["pocetni_datum_rezervacije"].split(".")
                    datum = date(int(d[0]), int(d[1]), int(d[2]))

                    poslednji_datum = datum + timedelta(days= broj_noci)
                    poslednji = str(poslednji_datum.year) + "."+ str(poslednji_datum.month) + "."+ str(poslednji_datum.day) + "."

                    k = promena["dostupnost"][i]["do"].split(".")
                    datum_u_dostupnosti = date(int(k[0]),int(k[1]), int(k[2]))

                    if(i+1 < len(promena["dostupnost"])):
                        f = promena["dostupnost"][i+1]["od"].split(".")
                        dostu = date(int(f[0]),int(f[1]), int(f[2]))
                    if(s == 0):

                        if(datum < datum_u_dostupnosti):
                            w = promena["dostupnost"][i]["od"].split(".")
                            dostu1 = date(int(w[0]),int(w[1]), int(w[2]))
                            print("dostu je ", dostu1)
                            if(poslednji_datum < dostu1):
                                r = {"od": rezervacija_recnik["pocetni_datum_rezervacije"], "do": poslednji, "indeks" : i, "duzina": len(promena["dostupnost"])+1}
                                s = s + 1
                            elif(poslednji_datum == dostu1):
                                r = {"od": rezervacija_recnik["pocetni_datum_rezervacije"], "do": promena["dostupnost"][i]["do"], "indeks" : i, "duzina": len(promena["dostupnost"])}
                                s = s + 1

                        if(datum == datum_u_dostupnosti): 
                            if(poslednji_datum == dostu):
                                r = {"od": promena["dostupnost"][i]["od"], "do": promena["dostupnost"][i+1]["do"], "indeks" : i, "duzina": len(promena["dostupnost"])-1}
                                s = s + 1
                            elif(poslednji_datum < dostu):
                                r = {"od": promena["dostupnost"][i]["od"], "do": poslednji, "indeks" : i, "duzina": len(promena["dostupnost"])}
                                s = s + 1
                x = 0
                for i in range(r["duzina"]):
                    if(r["indeks"] == i):
                        nesto = {"od" : r["od"], "do": r["do"]}
                        dostupnost.append(nesto)
                        x = x+1
                    else:
                        if(r["duzina"] == len(promena["dostupnost"])):
                            dostupnost.append(promena["dostupnost"][i])
                        elif(r["duzina"] > len(promena["dostupnost"])):
                            if(x == 0):
                                dostupnost.append(promena["dostupnost"][i])
                            else:
                                dostupnost.append(promena["dostupnost"][i-1])
                        else:
                            if(x == 0):
                                dostupnost.append(promena["dostupnost"][i])
                            else:
                                dostupnost.append(promena["dostupnost"][i+1])

                promena["dostupnost"] = dostupnost #dostupnost se updatuje u apartmanu
                upis_apartmana.append(promena) #upisuje se apartman u listu svih ostalih
                upis_apartmana.sort(key=lambda y: y.get('sifra')) #apartmani se sortiraju po siframa
                with open("../data/apartmani.json", "w", encoding="utf-8") as f:
                    json.dump(upis_apartmana, f, indent= 4)

                
                rezervacija_recnik["status"] = "odbijena" #status rezervacije prelazi u odbijena
                rezervacija_upis.append(rezervacija_recnik)
                rezervacija_upis.sort(key=lambda x: x.get('sifra_rezervacije')) #rezervacije se sortiraju prema siframa
                with open("../data/rezervacije.json", "w", encoding="utf-8") as f:
                    json.dump(rezervacija_upis, f, indent= 4)
            else:
                rezervacija_recnik["status"] = "prihvacena" #status rezervacije se menja u prihvacena
                rezervacija_upis.append(rezervacija_recnik) 
                rezervacija_upis.sort(key=lambda x: x.get('sifra_rezervacije')) #rezervacije se sortiraju prema siframa

                with open("../data/rezervacije.json", "w", encoding="utf-8") as f:
                    json.dump(rezervacija_upis, f, indent= 4)