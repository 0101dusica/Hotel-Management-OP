import json
from datetime import datetime, timedelta, date
from check import *
from prints import *
from tabulate import tabulate

def rezervacija_apartmana(korisnicko_ime):
    with open("../data/korisnici.json", "r", encoding="utf-8") as f: #preko korisnickog imena se trazi puno ime korisnika
        korisnici = json.load(f)
        for korisnik in korisnici:
            if( korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower()):
                gost = korisnik["ime"] + " " + korisnik["prezime"]

    popust = "ne"
    m = False
    while (m == False):
        print("Da li zelite da vidite listu apartmana koja je dostupna za rezevaciju ? ", end="")
        odgovor = provera_odgovora(False)

        apartman_ispis = []
        if(odgovor.lower() == "da"): #ispis liste aktivnih apartmana
            with open("../data/apartmani.json", "r", encoding="utf-8") as f:
                apartmani = json.load(f)
                for apartman in apartmani:
                    if(apartman["status"].lower() == "aktivno"):
                        apartman_ispis.append(ispis_apartmana(apartman))
                        
            header = ["Sifra", "Domacin", "Tip", "Sobe", "Gosti", "Adresa", "Cena", "Sadrzaj Apartmana"]
            print(tabulate(apartman_ispis, header, tablefmt="psql"))
        
        print("Unesite sifru apartmana koji zelite da rezervisete: ", end="")
        sifra = int_provera(False)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        upis = []
        sifra_rezervacije = 1 #u slucaju da je ovo prva rezervacija u file-u sifra ce biti 1
        with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
            rezervacije = json.load(f)
            for rez in rezervacije:
                upis.append(rez) #u listu se upisuju sve postojece rezervacije
                sifra_rezervacije = rez["sifra_rezervacije"] + 1 #uzima se sifra poslednje rezervacije i dodaje na nju broj 1
        
        novi_apartman = []
        
        max_osobe = 0
        dostupnost = []
        count = 0
        with open("../data/apartmani.json", "r", encoding="utf-8") as f:
            apartmani = json.load(f)
            for apartman in apartmani:
                if(sifra == apartman["sifra"]):
                    count = count + 1
                    if(apartman["status"].lower() =="neaktivan" ):
                        print("Ovaj apartman nije aktivan! Ne mozete izvrsiti rezervaciju!")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        m = True
                    else:
                        novi_apartman.append(apartman)
                        rezervacija = {"sifra" : apartman["sifra"], "lokacija": {"geografska_sirina": apartman["lokacija"]["geografska_sirina"],"geografska_duzina": apartman["lokacija"]["geografska_duzina"], "adresa": {"ulica_broj": apartman["lokacija"]["adresa"]["ulica_broj"], "grad": apartman["lokacija"]["adresa"]["grad"], "postanski_broj": apartman["lokacija"]["adresa"]["postanski_broj"]}}, "domacin": apartman["domacin"], "cena_po_noci": apartman["cena_po_noci"]}
                        max_osobe = apartman["broj_gostiju"]
                        for i in range(len(apartman["dostupnost"])):
                            dostupnost.append(apartman["dostupnost"][i])

        if(count == 0): #u slucaju da je korisnik uneo sifru apartmana koja ne postoji ispisuje mu se greska na ekran!
            print("Apartman sa ovom sifrom ne postoji!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        else:
            print("Dostupni termini u izabranom apartmanu su: ") #ispis dostupnih termina za apartman u narednih godinu dana
            datum_za_godinu = date(date.today().year+1, date.today().month, date.today().day)
            for i in range(len(dostupnost)):
                od_lista = dostupnost[i]["od"].split(".")
                od = date(int(od_lista[0]), int(od_lista[1]), int(od_lista[2]))
                do_lista = dostupnost[i]["do"].split(".")
                do = date(int(do_lista[0]), int(do_lista[1]), int(do_lista[2]))
                if(od < datum_za_godinu):
                    if(od <= date.today()):
                        if(do > date.today()):
                            if(do <= datum_za_godinu):
                                print("Od: ", date.today(), " Do: ", do)
                            else:
                                print("Od: ", date.today(), " Do: ", datum_za_godinu)
                    else:
                        if(do < datum_za_godinu):
                            print("Od: ", od, " Do: ",do)
                        else:
                            print("Od: ", od, " Do: ", datum_za_godinu)

            print("Unesite datum od kog zelite da rezervisete apartman!")
            datum = unos_datuma()

            if((datum < date.today())):# u slucaju da korisnik unese datum u proslosti na ekran mu se ispisuje greska
                print("Ne mozete da rezervisete datum u proslosti!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                m = True
            else:
                
                count = 0
                for i in range(len(dostupnost)): #proverava se da li je apartman dostupan od pocetnog datuma koji je korisnik uneo
                    od_lista = dostupnost[i]["od"].split(".")
                    od = date(int(od_lista[0]), int(od_lista[1]), int(od_lista[2]))
                    do_lista = dostupnost[i]["do"].split(".")
                    do = date(int(do_lista[0]), int(do_lista[1]), int(do_lista[2]))
                    if(datum >= od and datum < do):
                        count = count + 1
                
                
                if(count == 0 ): #ako apartman nije dostupan, ispisuje se greska
                    print("Apartman nije dostupan u terminu koji vi pretrazujete!")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    m = True
                else:
                    print("Unesite broj nocenja za koji rezervisete apartman: ", end="")
                    broj_nocenja = int_provera(False)
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    brojac = 0
                    dani_popusti = []
                    ukupna_cena = 0
                    poslenji_dan = datum + timedelta(days = broj_nocenja)
                    for k in range(broj_nocenja):
                        provera = datum + timedelta(days = k)
                        cena = rezervacija["cena_po_noci"]
                        c = 0 
                        with open("../data/praznici.json", "r", encoding="utf-8") as f: #proverava se da li se dan poklapa sa nekim praznicnim datumom
                            praznici = json.load(f)
                            for dan in praznici:
                                dlista = dan["datum"].split(".")
                                d = date(int(dlista[0]), int(dlista[1]), int(dlista[2]))
                                if(d == provera):
                                    cena = cena * 1.05 #cena za taj dan se uvecava za 5 posto

                        if(provera.weekday() > 3): #ako je dan koji se proverava vikend to se belezi u listu, koja kasnije sluzi da se izracuna ukupna cena rezervacije
                            cena = cena * 0.9 #cena za taj dan se smanjuje za 10 posto
                        
                        ukupna_cena = ukupna_cena + cena

                        for i in range(len(dostupnost)):
                            od_lista = dostupnost[i]["od"].split(".")
                            od = date(int(od_lista[0]), int(od_lista[1]), int(od_lista[2]))
                            do_lista = dostupnost[i]["do"].split(".")
                            do = date(int(do_lista[0]), int(do_lista[1]), int(do_lista[2]))
                            if(provera >= od and provera < do):
                                brojac = brojac + 1

                    
                    if(brojac != broj_nocenja):
                        print("Period koji zelite da rezervisete, nije dostupan!")
                        m = True
                    else:
                        print("Da li ste vi jedina osoba koja ce da gostuje u apartmanu ? ", end = "")
                        odg = provera_odgovora(False)
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                            
                        osoba = []
                        if(odg.lower() == "ne"): #unose se podaci o osobama koje ce da borave u apartmanu
                            n = False
                            while (n == False):
                                print("Koliko osoba ce biti u apartmanu ? ", end = "")
                                broj_osoba = int_provera(False)
                                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                if(broj_osoba > max_osobe):
                                    print("U apartmanu ne moze da boravi preko ", max_osobe, "osoba. Pokusajte ponovo sa unosom.")
                                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                else:
                                    n = True
                            for i in range(broj_osoba):
                                if( i == 0 ):
                                    print("Rezervaciju apartmana obavlja: ", gost)
                                    osoba.append(gost)
                                else:
                                    print("Unesite ime i prezime ", i+1, ". osobe: ", end="")
                                    o = input()
                                    osoba.append(o.title())
                        else:
                            osoba.append(gost)

            
                        if(popust == "da"): #ukoliko je korisnik ranije imao rezervacije, obracunava se popust od 5% na ukupnu cenu
                            print("Imate prava na popust ! Ukupna cena ove rezervacije bice umanjena za 5%")
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                            ukupna_cena = ukupna_cena*((100-5)/100)
                        
                        ukupna_cena = int(ukupna_cena)
                        datum_rezervacije = str(datum.year)+"."+str(datum.month)+"."+str(datum.day)+"." #datumi se u json datoteku upisuju kao string
                        ispis = []
                        done = []
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print("Potvrda Rezervacije!")
                        ispis.append(str(sifra_rezervacije))
                        adr = rezervacija["lokacija"]["adresa"]["ulica_broj"]+ ", "+ rezervacija["lokacija"]["adresa"]["grad"]+ ", "+  rezervacija["lokacija"]["adresa"]["postanski_broj"]
                        ispis.append(adr)
                        ispis.append(datum_rezervacije)
                        ispis.append(str(broj_nocenja))
                        ispis.append(str(ukupna_cena))
                        ispis_osoba = ""
                        for i in range(len(osoba)):
                            if(ispis_osoba == ""):
                                ispis_osoba = osoba[i]
                            else:
                                ispis_osoba = ispis_osoba + ", " + osoba[i]
                        ispis.append(ispis_osoba)

                        done.append(ispis)
                        header = ["Sifra", "Adresa", "Datum Rezervacije", "Broj nocenja", "Cena","Osobe prijavljene za boravak u apartmanu"]
                        print(tabulate(done, header, tablefmt="psql"))
                        

                        print("Da li zelite da potvrdite rezervaciju ? ", end="")
                        potvrda = provera_odgovora(False)
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                            

                        if(potvrda.lower() == "da"):
                            
                            recnik = {"sifra_rezervacije": sifra_rezervacije, "apartman": rezervacija, "pocetni_datum_rezervacije": datum_rezervacije, "broj_nocenja": broj_nocenja, "ukupna_cena": ukupna_cena, "gosti": osoba, "popust": popust,  "status": "kreirana"}
                            upis.append(recnik)

                            with open("../data/rezervacije.json", "w", encoding="utf-8") as f:
                                json.dump(upis, f, indent= 4)

                            print("Uspesno ste izvrsili rezervaciju apartmana!")
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                            nova_dostupnost = []
                            for i in range(len(dostupnost)):
                                od_lista = dostupnost[i]["od"].split(".")
                                od = date(int(od_lista[0]), int(od_lista[1]), int(od_lista[2]))
                                do_lista = dostupnost[i]["do"].split(".")
                                do = date(int(do_lista[0]), int(do_lista[1]), int(do_lista[2]))

                                if(datum >= od and poslenji_dan <= do):#u slucaju da su pocetni datum rezervacije i poslednji datum rezervacije izmedju odredjenog termina koji je slobodan u apartmanu, pravi se izmena u dostupnosti
                                    poslednji_datum = str(poslenji_dan.year)+"."+str(poslenji_dan.month)+"."+str(poslenji_dan.day)+"."
                                    if(datum == od and poslenji_dan == do):
                                        recnik_dostupnost = {"od": poslednji_datum, "do": dostupnost[i]["do"]}
                                    else:
                                        if(datum == od ):
                                            recnik_dostupnost = {"od": poslednji_datum, "do": dostupnost[i]["do"]}
                                            nova_dostupnost.append(recnik_dostupnost)
                                        elif(poslenji_dan == do):
                                            recnik_dostupnost = {"od": dostupnost[i]["od"], "do": datum_rezervacije}
                                            nova_dostupnost.append(recnik_dostupnost)
                                        else:
                                            recnik_dostupnost = {"od": dostupnost[i]["od"], "do": datum_rezervacije}
                                            recnik_dostupnost1 = {"od": poslednji_datum, "do": dostupnost[i]["do"]}
                                            nova_dostupnost.append(recnik_dostupnost)
                                            nova_dostupnost.append(recnik_dostupnost1)
                                else: 
                                    nova_dostupnost.append(dostupnost[i])
                            
                            novi_apartman[0]["dostupnost"] = nova_dostupnost #updatovana dostupnost u apartmanima

                            upis_apartmana = []
                            with open("../data/apartmani.json", "r", encoding="utf-8") as f:
                                apartmani = json.load(f)
                                for apartman in apartmani:
                                    if(sifra == apartman["sifra"]):
                                        upis_apartmana.append(novi_apartman[0])
                                    else:
                                        upis_apartmana.append(apartman)

                            upis_apartmana.sort(key=lambda y: y.get('sifra')) #apartmani se pre ponovnog upisa sortiraju po siframa

                            with open("../data/apartmani.json", "w", encoding="utf-8") as f:
                                    json.dump(upis_apartmana, f, indent= 4) #apartmani se upisuju u datoteku nakon updatovanja o novoj dostupnosti
                        
                            print("Ukoliko nastavite sa rezervacijama dobijate dodatnih 5% popusta na ukupnu cenu. ")
                            print("Da li zelite da nastavite sa rezervacijama ? ", end="")
                            o = provera_odgovora(False)
                            if(o.lower() == "ne"):
                                m = True
                            else:
                                popust = "da"
                        else:
                            m = True

def pregled_rezervacija(korisnicko_ime):#ispis svih trenutnih rezervacija koje postoje na korisnickom nalogu koji je prijavljen
    with open("../data/korisnici.json", "r", encoding="utf-8") as f:
        korisnici = json.load(f)
        for korisnik in korisnici:
            if( korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower()):
                gost = korisnik["ime"] + " " + korisnik["prezime"]

    brojac = 0
    ispis = []
    with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
        rezervacije = json.load(f)
        for rezervacija in rezervacije:
            if(rezervacija["gosti"][0].lower() == gost.lower()):
                if(rezervacija["status"].lower() != "odustanak"):
                    brojac = brojac + 1
                    ispis.append(ispis_rezervacija(rezervacija))

    if(brojac == 0):#greska koja se ispisuje u slucaju da ne postoje rezervacije na nalogu koji je trenutno prijavljen
        print("Trenutno nemate nikakve rezervacije!")
    else:
        header = ["Sifra", "Adresa", "Datum Rezervacije", "Broj nocenja", "Cena","Osobe prijavljene za boravak u apartmanu", "Status" ]
        print(tabulate(ispis, header, tablefmt="psql"))
    
def ponistavanje_rezervacija(korisnicko_ime): #u slucaju da korisnik odustane od rezervacije, njen status se menja i brisu se prethodno zauzeti datumi
    with open("../data/korisnici.json", "r", encoding="utf-8") as f:
        korisnici = json.load(f)
        for korisnik in korisnici:
            if( korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower()):
                gost = korisnik["ime"] + " " + korisnik["prezime"]

    print("Da li zelite da vidite listu vasih rezervacija ? ", end="")
    odg = provera_odgovora(False)

    ispis = []
    c = 0
    if(odg.lower() == "da"): #ispis liste svih rezervacija koje korisnik trenutno ima i moze da ih ponisti
        with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
            rezervacije = json.load(f)
            for rezervacija in rezervacije:
                if(rezervacija["gosti"][0].lower() == gost.lower()):
                    if(rezervacija["status"] == "prihvacena" or rezervacija["status"] == "kreirana"):
                        ispis.append(ispis_rezervacija(rezervacija))
                        c = c + 1
        if(c == 0):
            print("Trenutno nemate rezervacije koje mozete da ponistite!")
        else:
            header = ["Sifra", "Adresa", "Datum Rezervacije", "Broj nocenja", "Cena","Osobe prijavljene za boravak u apartmanu", "Status" ]
            print(tabulate(ispis, header, tablefmt="psql"))
        
    print("Unesite sifru rezervacije koju zelite da ponistite: ", end="")
    sifra = int_provera(False)
    
    upis = []
    neka_sifra = 0 #sifra koja je vezana uz apartman koji je osoba rezervisala i sada ponistava
    count = 0
    with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
        rezervacije = json.load(f)
        for rezervacija in rezervacije:
            if(rezervacija["status"] == "prihvacena" or rezervacija["status"] == "kreirana"): #gost ima mogucnost da otkaze rezervaciju ukoliko je ona prihvacena ili kreirana
                if(rezervacija["gosti"][0].lower() == gost.lower()): #na prvom mestu u gostima koji su upisani u rezervaciji se uvek nalazi osoba koja je rezervisala apartman
                    if(rezervacija["sifra_rezervacije"] != sifra):
                        upis.append(rezervacija)
                    else: #kada se pronadje rezervacija u datoteci, status joj se menja na odustanak
                        count = count+1
                        recnik = {"sifra_rezervacije": rezervacija["sifra_rezervacije"], "apartman": rezervacija["apartman"], "pocetni_datum_rezervacije": rezervacija["pocetni_datum_rezervacije"], "broj_nocenja": rezervacija["broj_nocenja"], "ukupna_cena": rezervacija["ukupna_cena"], "gosti": rezervacija["gosti"], "popust": rezervacija["popust"], "status": "odustanak"}
                        neka_sifra = rezervacija["apartman"]["sifra"]
                        broj_noci = rezervacija["broj_nocenja"]
                        upis.append(recnik)
                else:
                    upis.append(rezervacija)
            else:
                upis.append(rezervacija)

    if(count != 0):
        upis_apartmana = [] #upisuje se apartman koji ima istu sifru koja je stajala kod apartmana kod rezervacije koja se otkazuje
        with open("../data/apartmani.json", "r", encoding="utf-8") as f:
            apartmani = json.load(f)
            for apartman in apartmani:
                if(apartman["sifra"] == neka_sifra):
                    promena = apartman
                else:
                    upis_apartmana.append(apartman)

        dostupnost = []
        s = 0
        for i in range(len(promena["dostupnost"])):
            d = recnik["pocetni_datum_rezervacije"].split(".")
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
                    if(poslednji_datum < dostu1):
                        r = {"od": recnik["pocetni_datum_rezervacije"], "do": poslednji, "indeks" : i, "duzina": len(promena["dostupnost"])+1}
                        s = s + 1
                    elif(poslednji_datum == dostu1):
                        r = {"od": recnik["pocetni_datum_rezervacije"], "do": promena["dostupnost"][i]["do"], "indeks" : i, "duzina": len(promena["dostupnost"])}
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

        promena["dostupnost"] = dostupnost #dostupnost apartmana se updatuje
        upis_apartmana.append(promena)
        upis_apartmana.sort(key=lambda y: y.get('sifra')) #apartmani se sortiraju po sifri
        with open("../data/apartmani.json", "w", encoding="utf-8") as f:
            json.dump(upis_apartmana, f, indent= 4)


        upis.sort(key=lambda x: x.get('sifra_rezervacije'))#rezervacije se sortiraju po siframa
        with open("../data/rezervacije.json", "w", encoding="utf-8") as f:
            json.dump(upis, f, indent= 4)
        print("Uspesno ste otkazali rezervaciju pod sifrom ", sifra, "!")
    else: #u slucaju da ne postoji rezervacija sa sifrom koju je korisnik uneo, ispisuje se odgovarajuca greska
        print("Rezervacija sa ovom sifrom ne postoji!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
