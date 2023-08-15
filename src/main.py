import json
from datetime import datetime, timedelta, date
from operator import itemgetter
from tabulate import tabulate
from check import *
from prints import *
from gost import *
from domacin import *
from administrator import *


#glavni meni koji se otvara prilikom pokretanja aplikacije
def meni(): #ispisuje se njen sadrzaj i u odnosu na to koji korisnik pristupa aplikaciji, odredjuje se prikaz

    zavrsene_rezervacije()

    print("HighFive Aparments")
    print("1. Top 10 gradova")
    print("2. Pregled aktivnih apartmana")
    print("3. Pretraga apartmana")
    print("4. Visekriterijumska pretraga apartmana")
    print("5. Prijavite se")
    print("6. Registrujte se")
    print("7. Izlazak iz aplikacije")

    a = provera_broja(False, 0, 8) #poziva se funkcija koja od korisnika zahteva da unese broj, i poziva se sve dok unos ne bude pravilan (u zadatom opsegu i int)

    if(a == 1):
        top_10()
        meni()
    if(a == 2):
        pregled_aktivnih()
        meni()
    if(a == 3):
        pretraga_apartmana("svi", "")
        meni()
    if(a == 4):
        visekriterijumska_pretraga("svi", "")
        meni()
    if(a == 5):
        prijava()
    if(a == 6):
        registracija()
    if(a == 7):
        exit()

def zavrsene_rezervacije(): #funkcija koja se pokrece prilikom svakog pokretanja i proverava da li su rezervacije iz datoteke u proslosti, ako jesu, menja im status
    count = 0
    rezervacija_upis = []
    rezervacija_recnici = []
    with open("../data/rezervacije.json", "r", encoding="utf-8") as f: #proverava se da li ta rezervacija postoji
        rezervacije = json.load(f)
        for rezervacija in rezervacije:
            if(rezervacija["status"].lower() == "prihvacena"):
                count = count + 1
                rezervacija_recnici.append(rezervacija)
            else:
                rezervacija_upis.append(rezervacija)

    if(count != 0):
        for i in range((len(rezervacija_recnici))):
            od = rezervacija_recnici[i]["pocetni_datum_rezervacije"].split(".")
            pocetni_datum = date(int(od[0]), int(od[1]), int(od[2]))
            datum = pocetni_datum + timedelta(days = rezervacija_recnici[i]["broj_nocenja"])
            if(datum < date.today()):
                rezervacija_recnici[i]["status"] = "zavrsena"

            rezervacija_upis.append(rezervacija_recnici[i]) 
        
        rezervacija_upis = sorted(rezervacija_upis, key=itemgetter('sifra_rezervacije')) 
    
        with open("../data/rezervacije.json", "w", encoding="utf-8") as f:
            json.dump(rezervacija_upis, f, indent= 4)

#prijava na aplikaciju
def prijava():#korisnici koji vec imaju nalog prolaze samo kroz proces prijave
    
    korisnicko_ime = input("Unesite korisnicko ime: ") #korisnik unosi svoje korisnicko ime, koje se zatim pretrazuje u json-u "korisnici"
    lozinka_provera = " "
    uloga = " "
    status = " "
    with open("../data/korisnici.json", "r", encoding="utf-8") as f:
            korisnici = json.load(f)
            for korisnik in korisnici:
                if(korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower()): #u slucaju da se korisnicko ime pronadje, u proveru se stavlja njegova lozinka
                    lozinka_provera = korisnik["lozinka"]
                    uloga = korisnik["uloga"] #pamti se takodje i njegova uloga, kako bi kasnije mogao da se otvori odgovarajuci meni
                    status = korisnik["status"]
    
    if(status.lower() == " "): #u slucaju da se status nije promenio prilikom ucitavanja korisnika iz json-a, to znaci da nema odgovarajuceg korisnickog imena
        print("Registracija nije uspela. Korisnicko ime ne postoji u Bazi podataka! Da li zelite da pokusate ponovo ? ", end="")
        odgovor = provera_odgovora(False)
        if(odgovor.lower() == "da"):
            prijava()
        else:
            meni()
    elif(status.lower() == "blokiran"): # ako je korisnik blokiran, nema pravo na prijavu
        print("Greska! Ovaj nalog je blokiran od strane administratora! Nemate prava da koristite aplikaciju! ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        meni()
    elif(status.lower() == "aktivan"): 
        loznka = input("Unesite lozinku: ")
        if(lozinka_provera.lower() == loznka.lower()): #ako su lozinke iste, u zavisnosti od uloge, otvara se meni
            print("Uspesno ste se prijavili na nalog ", korisnicko_ime)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            if(uloga == "gost"):
                gost(korisnicko_ime)
            elif (uloga == "domacin"):
                domacin(korisnicko_ime)
            else:
                administrator(korisnicko_ime)
        else: #ako lozinke nisu iste, korisnik nije uneo dobru lozinku, izlazi greska
            print("Registracija nije uspela. Uneli ste pogresnu lozinku! Da li zelite da pokusate ponovo ? ", end="")
            odgovor = provera_odgovora(False)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            if(odgovor.lower() == "da"):
                prijava()
            else:
                meni()

def registracija(): #ukoliko je neko novi korisnik i zeli da otvori nalog, ova funkcija prikuplja sve podatke koji su potrebni za kreiranje novog korisnika u bazi podataka
    print("Registrujte se kao novi korisnik! ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    korisnicko_ime = input("Unesite korisnicko ime: ")
    with open("../data/korisnici.json", "r", encoding="utf-8") as f: #proverava se da li korisnicko ime koje je korisnik uneo vec postoji
        korisnici = json.load(f)
        for korisnik in korisnici:
            if(korisnicko_ime.lower() == korisnik["korisnicko_ime"].lower() ):
                print("Greska! Nalog sa ovim korisnickim imenom vec postoji! Da li zelite da pokusate ponovo ? ", end="")
                odgovor = provera_odgovora(False)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                if(odgovor.lower() == "da"):
                    registracija()
                else:
                    meni()

    lozinka = input("Unesite lozinku: ")

    provera = False
    while(provera == False):
        print("Unesite broj telefona: +381 ", end = "")
        telefon = int_provera(False) #izvrsava se provera da li je ceo unet telefon u formatu int
        if(telefon < 699999999 and telefon > 60000000):
            provera = True
        else:
            print("Ovo je nepostojeci broj telefona, pokusajte ponovo!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    telefon = "+381 " + str(telefon)

    email = input("Unesite email: ")
    
    index_monkey = email.lower().find("@")
    index_tacka = email.lower().find(".", index_monkey, 30)
    while (index_monkey > index_tacka or index_tacka < 0 or index_monkey < 0): # dok korisnik ne unese email u dobrom formatu, vrti se ova petlja
            
        print("Email nije unet u pravom formatu! primer@domen.com ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        email = input("Pokusajte pomovo da unesete email: ")

        index_monkey = email.lower().find("@")
        index_tacka = email.lower().find(".")

    ime = input("Unesite ime: ")
    prezime = input("Unesite prezime: ")
    print("Izaberite pol: ") #korisik bira pol, koji se zatim cuva u promenljivoj
    print("1. Musko")
    print("2. Zensko")
    print("3. Radije ne bih dao ovu informaciju")
    o= provera_broja(False, 0, 4)

    if(o == 1):
        pol = "muski"
    elif(o == 2):
        pol = "zensko"
    else:
        pol = "neutralan"

    upis = {"korisnicko_ime": korisnicko_ime, "lozinka": lozinka ,"ime": ime, "prezime": prezime, "pol" : pol, "kontakt_telefon" : telefon, "email": email, "uloga" : "gost", "status": "aktivan"}
    korisnici.append(upis) # na listu svih trenutno postojecih korisnika dodaje se jos jedan recnik sa podacima o novom korisniku 

    with open("../data/korisnici.json", "w", encoding="utf-8") as f:
        json.dump(korisnici, f, indent= 4) #u json se dodaje nova, updatovana lista  

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Nalog je uspesno napravljen, prijavite se!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    prijava()


#funkcionalnosti koje su zajednicke za sve korisnike
def pregled_aktivnih(): #funkcija sluzi za ispis svih aktivnih apartmana koji se trenutno nalaze u datoteci    
    count = 0
    ispis = []
    with open("../data/apartmani.json", "r", encoding="utf-8") as f:
            apartmani = json.load(f)
            for apartman in apartmani:
                if(apartman["status"].lower() == "aktivno"): #kada se proveri da li je apartman aktivan, ispisuju se podaci o njemu
                    count = count + 1
                    ispis.append(ispis_apartmana(apartman))
    
    if(count == 0): #ako nije pronadjen ni jedan aktivan apartman u datoteci, ispisuje se "greska"
        print("Trenutno ne postoje aktivni apartmani u bazi podataka!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    else:
        header = ["Sifra", "Domacin", "Tip", "Sobe", "Gosti", "Adresa", "Cena", "Sadrzaj Apartmana"]
        print(tabulate(ispis, header, tablefmt="psql"))

def pretraga_apartmana(status, korisnicko_ime): #funkcija koja omogucava pretragu apartmana po razlicitim kriterijumima 
    print("1. Pretraga po mestu")
    print("2. Pretraga po vremenu dostupnosti")
    print("3. Pretraga po broju soba")
    print("4. Pretraga po broju osoba")
    print("5. Pretraga po ceni apartmana")
    pretraga = provera_broja(False, 0, 6)

    ispis = []
    if(pretraga == 1): #mesto
        count = 0
        mesto = input("Pretraga po mestu: ")
        mesto = mesto.lower() #korisnik unosi grad po za koji pretrazuje apartmane

        with open("../data/apartmani.json", "r", encoding="utf-8") as f:
            apartmani = json.load(f)
            for apartman in apartmani:
                if(apartman["status"].lower() == "aktivno"):
                    if mesto in apartman["lokacija"]["adresa"]["grad"].lower(): #ako su grad iz datoteke i koji je korisnik uneo isti, ispisuju se informacije o apartmanu
                        ispis.append(ispis_apartmana(apartman))

                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        count = count + 1

        if (count == 0): #ako nije pronadjen ni jedan apartman u gradu koji korisnik pretrazuje ispisuje se "greska"
            print("Trenutno nemamo apartmane koji odgovaraju vasoj pretrazi!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        else:
            header = ["Sifra", "Domacin", "Tip", "Sobe", "Gosti", "Adresa", "Cena", "Sadrzaj Apartmana"]
            print(tabulate(ispis, header, tablefmt="psql"))
    elif(pretraga == 2): #dostupnost
        count = 0

        print("Unesite pocetni datum od kog pretrazujete apartman: ")
        pocetni_datum = unos_datuma() #godina/mesec/dan 

        print("Unesite krajnji datum do kog pretrazujete apartman: ")
        krajnji_datum = unos_datuma() #godina/mesec/dan

        if((pocetni_datum < date.today()) == True or (krajnji_datum < date.today()) == True ):# u slucaju da korisnik ne unese datume dobro na konolu se ispisuje odgovarajuca greska
            print("Ne mozete da pretrazujete za datume u proslosti! Da li zelite da pokusate ponovo ? ", end="")
            odgovor = provera_odgovora(False)
            if (odgovor.lower() == "da"):
                pretraga_apartmana(status, korisnicko_ime)
            else:
                if(status == "svi"):
                    meni()
                elif(status == "gost"):
                    gost(korisnicko_ime)
                elif(status == "domacin"):
                    domacin(korisnicko_ime)
                elif(status == "administrator"):
                    administrator(korisnicko_ime)
        elif((pocetni_datum > krajnji_datum) == True): #provera da li je krajnji datum pre pocetnog, ako jeste korisniku se ispisuje greska
            print("Krajnji datum ne moze biti pre pocetnog! Da li zelite da pokusate ponovo ? ", end="")
            odgovor = provera_odgovora(False)
            if (odgovor.lower() == "da"):
                pretraga_apartmana(status, korisnicko_ime)
            else:
                if(status == "svi"):
                    meni()
                elif(status == "gost"):
                    gost(korisnicko_ime)
                elif(status == "domacin"):
                    domacin(korisnicko_ime)
                elif(status == "administrator"):
                    administrator(korisnicko_ime)
        else: # ako su datumi uneti pravilno, izvrsava se pretraga apartmana
            with open("../data/apartmani.json", "r", encoding="utf-8") as f:
                apartmani = json.load(f)
                for apartman in apartmani:
                    if(apartman["status"].lower() == "aktivno"):
                        provera = 0  
                        for i in range(len(apartman["dostupnost"])): #u apartmanu postoje podaci o dostupnosti istog

                            od_lista = apartman["dostupnost"][i]["od"].split(".") #uzimaju se podaci od kada je apartman dostupan
                            od = date(int(od_lista[0]), int(od_lista[1]), int(od_lista[2]))

                            do_lista = apartman["dostupnost"][i]["do"].split(".") #podaci do kada je apartman dostupan
                            do = date(int(do_lista[0]), int(do_lista[1]), int(do_lista[2]))

                            if((od <= pocetni_datum) == True and (krajnji_datum <= do) == True): #ako je pocetni datum koji je korisnik uneo veci ili jednak datumu od kada je apartman dostupan i u isto vreme je krajnji datum manji ili jednak datumu do kada je dostupan, to znaci da se taj apartman ispisuje na konzolu
                                provera = provera + 1

                        if(provera != 0): #ispis apartmana
                            ispis.append(ispis_apartmana(apartman))
                            count = count + 1

            if (count == 0): #u slucaju da ne postoji ni jedan dostupan apartman ispisuje se "greska"
                print("Trenutno nemamo apartmane koji odgovaraju vasoj pretrazi!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            else:
                header = ["Sifra", "Domacin", "Tip", "Sobe", "Gosti", "Adresa", "Cena", "Sadrzaj Apartmana"]
                print(tabulate(ispis, header, tablefmt="psql"))
    elif (pretraga == 3 or pretraga == 4 or pretraga == 5):
        count = 0
        if(pretraga == 3):
            print("Koji je najmanji broj soba koji pretrazujete ? ", end="")
            broj_soba_min = int_provera(False)
            print("Koji je najveci broj soba koji pretrazujete ? ", end="")
            broj_soba_max = int_provera(False)
            if(broj_soba_max<broj_soba_min):
                print("Greska! Najveci broj soba koji pretrazujete mora da bude veci od najmanjeg!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                count = count + 1
        elif(pretraga == 4):
            print("Koji je najmanji broj osoba za koji pretrazujete apartman? ", end="")
            broj_osoba_min = int_provera(False)
            print("Koji je najveci broj osoba za koji pretrazujete apartman? ", end="")
            broj_osoba_max = int_provera(False)
            if(broj_osoba_max< broj_osoba_min):
                print("Greska! Najveci broj osoba za koje pretrazujete mora da bude veci od najmanjeg!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                count = count + 1
        else:
            print("Koja je minimalna cena za jednu noc u apartmanu ? ", end="")
            cena_min = int_provera(False)
            print("Koja je maksimalna cena za jednu noc u apartmanu ? ", end="")
            cena_max = int_provera(False)
            if(cena_max < cena_min):
                print("Greska! Maksimalna cena mora da bude od minimalne!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                count = count + 1

        with open("../data/apartmani.json", "r", encoding="utf-8") as f:
            apartmani = json.load(f)
            for apartman in apartmani:
                if(apartman["status"].lower() == "aktivno"): #ako su apartmani aktivni
                    point = 0
                    if(pretraga == 3): #korisnik zeli da pretrazuje po broju soba
                        if( apartman["broj_soba"] >= broj_soba_min and apartman["broj_soba"] <= broj_soba_max ):
                            point = point + 1
                    elif(pretraga == 4): #pretraga po broju gostiju
                        if(apartman["broj_gostiju"] >= broj_osoba_min and apartman["broj_gostiju"] <= broj_osoba_max):
                            point = point + 1
                    else: #pretraga po ceni
                        if(apartman["cena_po_noci"] >= cena_min and apartman["cena_po_noci"] <= cena_max):
                            point = point + 1
                    if(point != 0): #ispis apartmana
                        ispis.append(ispis_apartmana(apartman))
                        count = count + 1

        if (count == 0):#slucaj kada ne postoji apartmana koji se ispisuju na konzolu
            print("Trenutno nemamo apartmane koji odgovaraju vasoj pretrazi!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        else:
            header = ["Sifra", "Domacin", "Tip", "Sobe", "Gosti", "Adresa", "Cena", "Sadrzaj Apartmana"]
            print(tabulate(ispis, header, tablefmt="psql"))

def visekriterijumska_pretraga(status, korisnicko_ime): #prvi parametar odredjue koji se meni otvara prilikom greske u kucanju, drugi sluzi kao parametar za funcije gost, domacin i administrator
    provera = True
    lista_pretraga = []

    while(provera == True):#petlja se izvrsava sve dok korisnik ne odluci da je uneo sve kriterijume po kojima zeli da vrsi pretragu ili dok ne unese sve kriterijume koji su ponudjeni
        print("1. Pretraga po mestu")
        print("2. Pretraga po vremenu dostupnosti")
        print("3. Pretraga po broju soba")
        print("4. Pretraga po broju osoba")
        print("5. Pretraga po ceni apartmana")
        print("Na koji nacin zelite da izvrsite pretragu? ", end="")
        pretraga = provera_broja(False, 0, 6)
        if(pretraga in lista_pretraga):
            print("Vec ste izabrali pretragu na ovaj nacin. Da li zelite da pokusate ponovo ? ", end="")
            odgovor = provera_odgovora(False)
            if(odgovor.lower() == "ne"):
                provera = False
        else:
            lista_pretraga.append(pretraga)

        if(len(lista_pretraga) == 5):
            print("Izabrali ste sve nacine pretrage.")
            provera = False
        else:
            print("Da li zelite da pretrazujete na jos neki nacin ? ", end="")
            ispis = provera_odgovora(False)
            if(ispis.lower() == "ne"):
                provera = False

    count = 0 
    ispis = []
    for i in lista_pretraga:
        if(i == 1): #pretraga je po gradu
            mesto = input("Pretraga po mestu: ")
            mesto = mesto.lower()
        elif ( i == 2):
            print("Unesite pocetni datum od kog pretrazujete apartman: ")
            pocetni_datum = unos_datuma() #godina/mesec/dan 

            print("Unesite krajnji datum do kog pretrazujete apartman: ")
            krajnji_datum = unos_datuma() #godina/mesec/dan

            
            if((pocetni_datum < date.today()) == True or (krajnji_datum < date.today()) == True ):# u slucaju da korisnik ne unese datume dobro na konolu se ispisuje odgovarajuca greska
                print("Ne mozete da pretrazujete za datume u proslosti! Da li zelite da pokusate ponovo ? ", end="")
                odgovor = provera_odgovora(False)
                if (odgovor.lower() == "da"):
                    pretraga_apartmana()
                else:
                    if(status == "svi"):
                        meni()
                    elif(status == "gost"):
                        gost(korisnicko_ime)
                    elif(status == "domacin"):
                        domacin(korisnicko_ime)
                    elif(status == "administrator"):
                        administrator(korisnicko_ime)
            elif((pocetni_datum > krajnji_datum) == True): 
                print("Krajnji datum ne moze biti pre pocetnog! Da li zelite da pokusate ponovo ? ", end="")
                odgovor = provera_odgovora(False)
                if (odgovor.lower() == "da"):
                    pretraga_apartmana()
                else:
                    if(status == "svi"):
                        meni()
                    elif(status == "gost"):
                        gost(korisnicko_ime)
                    elif(status == "domacin"):
                        domacin(korisnicko_ime)
                    elif(status == "administrator"):
                        administrator(korisnicko_ime)
        elif(i == 3):
            print("Koji je najmanji broj soba koji pretrazujete ? ", end="")
            broj_soba_min = int_provera(False)
            print("Koji je najveci broj soba koji pretrazujete ? ", end="")
            broj_soba_max = int_provera(False)
            if(broj_soba_max<broj_soba_min):
                print("Greska! Najveci broj soba koji pretrazujete mora da bude veci od najmanjeg!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                count = count + 1
        elif( i ==4):
            print("Koji je najmanji broj osoba za koji pretrazujete apartman? ", end="")
            broj_osoba_min = int_provera(False)
            print("Koji je najveci broj osoba za koji pretrazujete apartman? ", end="")
            broj_osoba_max = int_provera(False)
            if(broj_osoba_max< broj_osoba_min):
                print("Greska! Najveci broj osoba za koje pretrazujete mora da bude veci od najmanjeg!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                count = count + 1
        else:
            print("Koja je minimalna cena za jednu noc u apartmanu ? ", end="")
            cena_min = int_provera(False)
            print("Koja je maksimalna cena za jednu noc u apartmanu ? ", end="")
            cena_max = int_provera(False)
            if(cena_max < cena_min):
                print("Greska! Maksimalna cena mora da bude od minimalne!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                count = count + 1

    with open("../data/apartmani.json", "r", encoding="utf-8") as f:
        apartmani = json.load(f)
        for apartman in apartmani:
            if(apartman["status"].lower() == "aktivno"):
                tacna_pretraga = 0 
                for i in lista_pretraga: #prolazimo kroz listu u kojoj se nalaze nacini na koje korisnik izvrsava pretragu i prebrojavamo apartmane koji se slazu sa odredjenom pretragom
                    if(i == 1):
                        if mesto in apartman["lokacija"]["adresa"]["grad"].lower():
                            tacna_pretraga = tacna_pretraga + 1
                    elif(i == 2):
                        provera = 0  
                        for i in range(len(apartman["dostupnost"])):
                            od_lista = apartman["dostupnost"][i]["od"].split(".")
                            od = date(int(od_lista[0]), int(od_lista[1]), int(od_lista[2]))
                            do_lista = apartman["dostupnost"][i]["do"].split(".")
                            do = date(int(do_lista[0]), int(do_lista[1]), int(do_lista[2]))

                            if((od <= pocetni_datum) == True and (krajnji_datum <= do) == True):
                                provera = provera + 1
                        if(provera != 0):
                            tacna_pretraga = tacna_pretraga + 1
                    elif(i == 3):
                        if( apartman["broj_soba"] >= broj_soba_min and apartman["broj_soba"] <= broj_soba_max ):
                            tacna_pretraga = tacna_pretraga + 1
                    elif(i == 4):
                        if(apartman["broj_gostiju"] >= broj_osoba_min and apartman["broj_gostiju"] <= broj_osoba_max):
                            tacna_pretraga = tacna_pretraga + 1
                    elif(i == 5):
                        if(apartman["cena_po_noci"] >= cena_min and apartman["cena_po_noci"] <= cena_max):
                            tacna_pretraga = tacna_pretraga + 1
                
                if(tacna_pretraga == len(lista_pretraga)): #ako je pretraga za jedan apartman potvrdjena isto puta koliko je i lista dugacka, to znaci da su pretrage na svaki nacin tacne, i da se apartman ispisuje na konzolu
                    ispis.append(ispis_apartmana(apartman))

                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    count = count + 1

    if (count == 0):
        print("Trenutno nemamo apartmane koji odgovaraju vasoj pretrazi!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    else:
        header = ["Sifra", "Domacin", "Tip", "Sobe", "Gosti", "Adresa", "Cena", "Sadrzaj Apartmana"]
        print(tabulate(ispis, header, tablefmt="psql"))

def top_10(): #funkcija ispisuje 10 trenutno najpopularnijih gradova u poslednjih godinu dana
    brojac = 0
    lista = []
    with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
        rezervacije = json.load(f)
        for rezervacija in rezervacije:
            datum_lista = rezervacija["pocetni_datum_rezervacije"].split(".")
            datum = date(int(datum_lista[0]), int(datum_lista[1]), int(datum_lista[2])) #pocetni datum rezervacije koja se proverava
            datum_godina = date(date.today().year-1, date.today().month, date.today().day) #datum pre godinu dana
            if(datum >= datum_godina and datum <= date.today()):
                if(rezervacija["status"].lower() == "prihvacena" or rezervacija["status"].lower() == "zavrsena"):
                    brojac = brojac + 1
                    if (len(lista) == 0): #ako je lista prazna dodaje se novi recnik koji sadrzi naziv grada i dodaje se jedno ponavljanje
                        recnik = {"grad": rezervacija["apartman"]["lokacija"]["adresa"]["grad"].lower(), "ponavljanje": 1}
                        lista.append(recnik) #recnik se dodaje u listu
                    else: #ako u listi vec postoji neki recnik pretrazuje se da se vidi da li je grad iz rezervacije isti kao i prethodno upisan 
                        pronadjen = 0
                        for i in range(len(lista)): #pretraga u listi
                            if(rezervacija["apartman"]["lokacija"]["adresa"]["grad"].lower() == lista[i]["grad"]): #ako grad vec postoji samo se povecava broi ponavljanja
                                pronadjen = pronadjen + 1
                                indeks = i
                                
                        if(pronadjen != 0): # u slucaju da recnik sa nazivom grada vec postoji u listi, samo se povecava broj ponavljanja za 1
                            lista[indeks]["ponavljanje"] = lista[indeks]["ponavljanje"] + 1
                        else: #ako ne postoji, pravi se novi recnik sa novim gradom i inicijalnim jednim ponavljanjem 
                            recnik = {"grad": rezervacija["apartman"]["lokacija"]["adresa"]["grad"].lower(), "ponavljanje": 1}
                            lista.append(recnik) 
                    
    if(brojac == 0): #u slucaju da ne postoje prihvacene rezervacije u bazi, ispisuje se "greska"
        print("Ne postoje informacije o najpopularnijim gradovima!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    else:
        lista.sort(key=lambda x: x.get('ponavljanje'), reverse= True) #lista se sortira po broju ponavljanja, od najveceg do najmanjeg

        ispis = []
        if(len(lista) > 10): #u slucaju da lista sadrzi vise od 10 gradova, ispisuje se samo prvih 10
            print("Top 10 gradova:")
            for i in range(10):
                gradovi = []
                gradovi.append(str(i+1) + ". ")
                gradovi.append(lista[i]["grad"])
                ispis.append(gradovi)
        else: #ako lista ima manje od 10 gradova, ispisujus se svi
            print("Trenutno ne postoji 10 gradova u bazi podataka. Ovo je nasih top ", len(lista), ":")
            for i in range(len(lista)):
                gradovi = []
                gradovi.append(str(i+1) + ". ")
                gradovi.append(lista[i]["grad"])
                gradovi.append(lista[i]["ponavljanje"]) 
                ispis.append(gradovi)

        header = ["Redni Broj", "Grad", "ponavljanja"]
        print(tabulate(ispis, header, tablefmt="psql")) 

#tri menija koja se otvaraju u zavisnosti od uloge korisnika
def gost(korisnicko_ime): #meni koji se otvara prilikom prijavljivanja na nalog koji ima status gosta

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("1. Top 10 gradova")
    print("2. Pregled aktivnih apartmana")
    print("3. Pretraga apartmana")
    print("4. Visekriterijumska pretraga apartmana")
    print("5. Rezervacija apartmana")
    print("6. Pregled rezervacija")
    print("7. Ponistavanje rezervacija")
    print("8. Odjavite se")

    a = provera_broja(False, 0, 9)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if(a == 1):
        top_10()
        gost(korisnicko_ime)
    if(a == 2):
        pregled_aktivnih()
        gost(korisnicko_ime)
    if(a == 3):
        pretraga_apartmana("gost", korisnicko_ime)
        gost(korisnicko_ime)
    if(a == 4):
        visekriterijumska_pretraga("gost", korisnicko_ime)
        gost(korisnicko_ime)
    if(a == 5):
        rezervacija_apartmana(korisnicko_ime)
        gost(korisnicko_ime)
    if(a == 6):
        pregled_rezervacija(korisnicko_ime)
        gost(korisnicko_ime)
    if(a == 7):
        ponistavanje_rezervacija(korisnicko_ime)
        gost(korisnicko_ime)
    if(a == 8):
        meni()    

def domacin(korisnicko_ime): #meni koji se ispisuje korisniku nakon prijave, ukoliko se utvrdi da je njegova uloga domacin

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("1. Top 10 gradova")
    print("2. Pregled aktivnih apartmana")
    print("3. Pretraga apartmana")
    print("4. Visekriterijumska pretraga apartmana")
    print("5. Dodavanje apartmana")
    print("6. Izmena podataka o apartmanu")
    print("7. Brisanje aparmana")
    print("8. Pregled nepotvrdjenih rezervacija")
    print("9. Potvrda ili odbijanje rezervacije")
    print("10. Promenite sifru za vas nalog")
    print("11. Odjavite se")

    a = provera_broja(False, 0, 12)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if(a == 1):
        top_10()
        domacin(korisnicko_ime)
    if(a == 2):
        pregled_aktivnih()
        domacin(korisnicko_ime)
    if(a == 3):
        pretraga_apartmana("domacin", korisnicko_ime)
        domacin(korisnicko_ime)
    if(a == 4):
        visekriterijumska_pretraga("domacin", korisnicko_ime)
        domacin(korisnicko_ime)
    if(a == 5):
        dodavanje_apartmana(korisnicko_ime)
        domacin(korisnicko_ime)
    if(a == 6):
        izmena_podataka_apartmana(korisnicko_ime)
        domacin(korisnicko_ime)
    if(a == 7):
        brisanje_apartmana(korisnicko_ime)
        domacin(korisnicko_ime)
    if(a == 8):
        pregled_rezervacije(korisnicko_ime)
        domacin(korisnicko_ime)
    if(a == 9):
        potvrda_odbijanje_rezervacije(korisnicko_ime)
        domacin(korisnicko_ime)
    if(a == 10):
        promena_sifre(korisnicko_ime)
        domacin(korisnicko_ime)
    if(a == 11):
        meni()

def administrator(korisnicko_ime): #meni koji se otvara kada se korisnik prijavi kao administrator 
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("1. Top 10 gradova")
    print("2. Pregled aktivnih apartmana")
    print("3. Pretraga apartmana")
    print("4. Visekriterijumska pretraga apartmana")
    print("5. Pretraga rezervacija")
    print("6. Registracija novih domacina")
    print("7. Kreiranje dodatne opreme")
    print("8. Brisanje dodatne opreme")
    print("9. Blokiranje korisnika")
    print("10. Izvestavanje")
    print("11. Dodavanje praznicnih datuma")
    print("12. Aktivacija novih apartmana")
    print("13. Odjavite se")

    a = provera_broja(False, 0, 14)

    if(a == 1):
        top_10()
        administrator(korisnicko_ime)
    if(a == 2):
        pregled_aktivnih()
        administrator(korisnicko_ime)
    if(a == 3):
        pretraga_apartmana("administrator", korisnicko_ime)
        administrator(korisnicko_ime)
    if(a == 4):
        visekriterijumska_pretraga("administrator", korisnicko_ime)
        administrator(korisnicko_ime)
    if(a == 5):
        pretraga_rezervacija()
        administrator(korisnicko_ime)
    if(a == 6):
        registracija_domacina(korisnicko_ime)
        administrator(korisnicko_ime)
    if(a == 7):
        kreiranje_dodatne_opreme()
        administrator(korisnicko_ime)
    if(a == 8):
        brisanje_dodatne_opreme()
        administrator(korisnicko_ime)
    if(a == 9):
        blokiranje()
        administrator(korisnicko_ime)
    if(a == 10):
        izvestavanje()
        administrator(korisnicko_ime)
    if(a == 11):
        praznicni_dani()
        administrator(korisnicko_ime)
    if(a == 12):
        aktivacija_apartmana()
        administrator(korisnicko_ime)
    if(a == 13):
        meni()

#pokretanje aplikacije
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
meni() 