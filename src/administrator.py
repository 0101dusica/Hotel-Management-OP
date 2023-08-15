import json
from datetime import datetime, timedelta, date
from tabulate import tabulate
from check import *
from prints import *

def pretraga_rezervacija(): #administrator ima mogucnost da pretrajuze rezervacije
	print("Da li zelite da pretrazujete rezervacije po: ")
	print("1. Statusu")
	print("2. Adresi")
	print("3. Korisnickom imenu domacina")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

	a = provera_broja(False, 0, 4) #pretrazivanje rezervacija je moguce na 3 nacina
		

	ispis = []
	if(a == 1): #po statusu
		print("Da li zelite da vidite: ")
		print("1. Potvrdjene rezervacije ")
		print("2. Odbijene rezervacije ")
		print("3. Zavrsene rezervacije ")
		b = provera_broja(False, 0, 4) #pretraga potvrdjenih ili odbijenih rezervacija

		count = 0
		with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
			rezervacije = json.load(f)
			for rezervacija in rezervacije:
				if(b == 1):
					if(rezervacija["status"].lower() == "prihvacena"): #ispis rezervacija koje su prihvacene
						count = count + 1
						ispis.append(ispis_rezervacija(rezervacija))
				elif(b == 2):
					if(rezervacija["status"].lower() == "odbijena"): #ispis rezervacija koje su odbijene
						count = count + 1
						ispis.append(ispis_rezervacija(rezervacija))
				else:
					if(rezervacija["status"].lower() == "zavrsena"): #ispis rezervacija koje su zavrsene
						count = count + 1
						ispis.append(ispis_rezervacija(rezervacija))

		if(count == 0): #ukoliko ne postoje rezervacije ispisuje se obavestenje na ekran
			if(b == 1):
				print("Trenutno nema potvrdjenih rezervacija! ")
			elif(b == 2):
				print("Trenutno nema odbijenih rezervacija! ")
			else:
				print("Treutno nema završenih rezervacija!")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		else:
			header = ["Sifra", "Adresa", "Datum Rezervacije", "Broj nocenja", "Cena","Osobe prijavljene za boravak u apartmanu", "Status" ]
			print(tabulate(ispis, header, tablefmt="psql"))
	elif(a == 2): #po mestu
		mesto = input("Unesite adresu apartmana za koji zelite da proverite rezervacije: ")
		mesto = mesto.lower()
		count = 0
		with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
			rezervacije = json.load(f)
			for rezervacija in rezervacije:
				if(rezervacija["status"]!= "odustanak" and rezervacija["status"] != "kreirana"):
					adresa = rezervacija["apartman"]["lokacija"]["adresa"]["ulica_broj"].lower() +" "+ rezervacija["apartman"]["lokacija"]["adresa"]["grad"].lower() +" "+rezervacija["apartman"]["lokacija"]["adresa"]["postanski_broj"].lower()
					if mesto in adresa: #ako je deo mesta koji je administrator uneo poklapajuci sa adresom u rezervaciji, ispisuje se ta rezervacija
						count = count + 1
						ispis.append(ispis_rezervacija(rezervacija))
		if(count == 0):
			print("Trenutno nema rezervacija za apartman na ovoj adresi! ")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		else:
			header = ["Sifra", "Adresa", "Datum Rezervacije", "Broj nocenja", "Cena","Osobe prijavljene za boravak u apartmanu", "Status" ]
			print(tabulate(ispis, header, tablefmt="psql"))
	else: #po korisnickom imenu domacina
		korisnicko_ime = input("Unesite korisnicko ime domacina za kog zelite da proverite rezervacije: ")
		brojac = 0 
		with open("../data/korisnici.json", "r", encoding="utf-8") as f:
			korisnici = json.load(f)
			for korisnik in korisnici:
				if( korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower()): #ako se korisnicka imena poklapaju iz fajla se izvlaci ime i prezime domacina
					domacin = korisnik["ime"] + " " + korisnik["prezime"]
					brojac = brojac + 1

		if(brojac == 0):
			print("Ne postoji domacin sa ovim korisnickim imenom!")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		else:
			count = 0
			with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
				rezervacije = json.load(f)
				for rezervacija in rezervacije:
					if(rezervacija["status"]!= "odustanak" and rezervacija["status"] != "kreirana"):
						if domacin.lower() in rezervacija["apartman"]["domacin"].lower(): #ako se domacin kojeg je administrator uneo i domacin u rezervaciji poklapaju, rezervacija se ispisuje
							count = count + 1
							ispis.append(ispis_rezervacija(rezervacija))
			if(count == 0):
				print("Trenutno nema rezervacija za apartmane domacina: ", domacin ,"! ")
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			else:
				header = ["Sifra", "Adresa", "Datum Rezervacije", "Broj nocenja", "Cena","Osobe prijavljene za boravak u apartmanu", "Status" ]
				print(tabulate(ispis, header, tablefmt="psql"))

def registracija_domacina(username): #administrator jedini ima pravo da napravi nalog novom domacinu
	print("Registrujte novog domacina! ")

	
	n = False
	while(n == False):
		count = 0
		korisnicko_ime = input("Unesite korisnicko ime: ")
		with open("../data/korisnici.json", "r", encoding="utf-8") as f: #proverava se da li korisnicko ime koje je korisnik uneo vec postoji
			korisnici = json.load(f)
			for korisnik in korisnici:
				if(korisnicko_ime.lower() == korisnik["korisnicko_ime"].lower() ):
					count = count + 1
					print("Greska! Nalog sa ovim korisnickim imenom vec postoji!")
					print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

					print("Da li zelite ponovo da pokusate da registrujete domacina ? ", end="")
					odgovor = provera_odgovora(False)
					if(odgovor.lower() == "ne"):
						n = True
		if(count == 0):
			n = True

	if(count == 0):
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
			
		upis = {"korisnicko_ime": korisnicko_ime, "lozinka": lozinka ,"ime": ime, "prezime": prezime, "pol" : pol, "kontakt_telefon" : telefon, "email": email, "uloga" : "domacin", "status": "aktivan"}
		korisnici.append(upis)
		with open("../data/korisnici.json", "w", encoding="utf-8") as f:
			json.dump(korisnici, f, indent= 4)

		print("Nalog je uspesno napravljen!")

def kreiranje_dodatne_opreme(): #administrator kreira novu dodatnu opremu, kojom domacini opisuju svoje apartmane
	provera = False
	while(provera == False):
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		naziv = input("Unesite naziv dodatne opreme koju zelite da unesete kao novu: ") #upisuje naziv

		count = 0
		with open("../data/dodatna_oprema.json", "r", encoding="utf-8") as f: #proverava se da li dodatna oprema sa tim nazivom vec postoji
			dodatna_oprema = json.load(f)
			for stavka in dodatna_oprema:
				if (naziv.lower() in stavka["naziv"]):
					print("Dodatna oprema pod ovim nazivom vec postoji! ")
					count = count + 1
					print("Da li zelite da pokusate ponovo sa unosom ? ", end="")
					odgovor = provera_odgovora(False)
					if(odgovor.lower() == "ne"):
						provera = True
		
		if(count == 0):
			provera = True #u slucaju da ne postoji, dodatna oprema se unosi u json
			print("Uspesno ste uneli novu dodatnu opremu, pod sifrom: ", dodatna_oprema[-1]["sifra"]+1, " i nazivom: ", naziv.lower())

			recnik = {"sifra": dodatna_oprema[-1]["sifra"]+1, "naziv": naziv.lower()} #sifra je za jedan veca od predhodne, naziv je uneo administrator
			dodatna_oprema.append(recnik)
			dodatna_oprema.sort(key=lambda x: x.get('sifra')) #sortiranje po siframa pre upis au datoteku
			with open("../data/dodatna_oprema.json", "w", encoding="utf-8") as f:
				json.dump(dodatna_oprema, f, indent= 4)
	
def brisanje_dodatne_opreme(): #administrator ima mogucnost da brise dodatnu opremu ako ona nije dodeljena ni jednom apartmanu
	
	with open("../data/dodatna_oprema.json", "r", encoding="utf-8") as f: #ispis dodatne opreme
		dodatna_oprema = json.load(f)
		for stavka in dodatna_oprema:
			print("Sifra: ", stavka["sifra"])
			print("Naziv: ", stavka["naziv"])
			print("~~~~~~~~~~~~~~~~~")
	
	provera = False
	while(provera == False):
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print("Unesite sifru opreme koju zelite da obrisete: ", end="") #unosi se sifra dodatne opreme koja se brise
		sifra = int_provera(False)

		count = 0
		with open("../data/apartmani.json", "r", encoding="utf-8") as f:
			apartmani = json.load(f)
			for apartman in apartmani:
				for i in apartman["sadrzaj_apartmana"]:
					if(sifra == i["sifra"]): #u slucaju da pronadje u apartmanima da neko koristi dodatnu opremu koja pokusava da se obrise, izbacuje se greska
						count = count + 1
		
		upis = []
		if(count == 0):
			with open("../data/dodatna_oprema.json", "r", encoding="utf-8") as f:
				dodatna_oprema = json.load(f)
				for stavka in dodatna_oprema:
					if(stavka["sifra"] != sifra): #u novu listu se upisuje svaka stavka koja se ne poklapa sa sifrom dodatne opreme koja se brise
						upis.append(stavka)

			with open("../data/dodatna_oprema.json", "w", encoding="utf-8") as f: #json se updatuje
				json.dump(upis, f, indent= 4)

			print("Dodatna oprema pod sifrom: ", sifra, " je uspesno obrisana!")
				 
		else: #ako se dodatna oprema koristi u nekom od apartmana, nije je moguce obrisati
			print("Nije moguce izvrsiti brisanje ove dodatne opreme! U ovom momentu se koristi za opis jednog apartmana! ")

		print("Da li zelite da obrisete jos dodatne opreme ? ", end="")
		ispis = provera_odgovora(False) 
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		if(ispis.lower() == "ne"):
			provera = True
				  
def blokiranje(): #administrator ima mogucnost da blokira ili odblokira korisnike koji imaju status gosta ili domacina
	print("Da li zelite da: ")
	print("1. Blokirate korisnika")
	print("2. Odblokirate korisnika")

	a = provera_broja(False, 0, 3)

	#lista korisnika 
	brojac_blokirani = 0
	brojac_aktivni = 0
	with open("../data/korisnici.json", "r", encoding="utf-8") as f: #u fajlu se pretrazuju korisnici koji su blokirani i oni koji nisu
		korisnici = json.load(f)
		count = 1
		for korisnik in korisnici:
			if(korisnik["uloga"] != "administrator"):
				if( a == 1): #ako administrator zeli da blokira korisnika, korisnik prethodno mora da ima aktivan nalog
					if(korisnik["status"] == "aktivan"):
						print(count, ". korisnicko ime: ", korisnik["korisnicko_ime"], ", uloga: " , korisnik["uloga"])
						count = count+1
						brojac_aktivni = brojac_aktivni + 1
				elif( a == 2): #slicno funkcionise i suprotno, ako zeli da odblokira korisnika, on prethodno mora da bude blokiran
					if(korisnik["status"] == "blokiran"):
						print(count, ". korisnicko ime: ", korisnik["korisnicko_ime"], ", uloga: " , korisnik["uloga"])
						count = count+1
						brojac_blokirani = brojac_blokirani + 1
				

				
	ponovo = False
	if((a == 1 and brojac_aktivni > 0) or (a == 2 and brojac_blokirani > 0)): # u slucaju da postoje aktivni korisnici i da admin zeli da blokira nekoga nastavlja se dalje, slicno funkcionise i suprotno
		while(ponovo == False): 
			#administrator unosi korisnicko ime osobe koju zeli da blokira ili odblokira
			if( a == 1 and brojac_aktivni > 0):
				ime = input("Unesite korisnicko ime osobe koju zelite da blokirate: ")
			elif( a == 2 and brojac_blokirani > 0):
				ime = input("Unesite korisnicko ime osobe koju zelite da odblokirate: ")
			
			promena = []
			count = 0
			with open("../data/korisnici.json", "r", encoding="utf-8") as f: #u fajlu se pretrazuje osoba sa korisnickim imenom koje je administrator uneo
				korisnici = json.load(f)
				for korisnik in korisnici:
					if(korisnik["uloga"] != "administrator"): #korisnik kog administrator zeli da blokira/odblokira ne moze da bude administrator
						if(korisnik["korisnicko_ime"].lower() == ime.lower()):
							if( a == 1 and korisnik["status"] == "aktivan"): #ako zeli da blokira osobu, ona mora biti aktivna
								recnik = {"korisnicko_ime": korisnik["korisnicko_ime"], "lozinka": korisnik["lozinka"], "ime": korisnik["ime"], "prezime": korisnik["prezime"],"pol": korisnik["pol"], "kontakt_telefon": korisnik["kontakt_telefon"], "email": korisnik["email"], "uloga":korisnik["uloga"], "status": "blokiran"}
								count = count+1
								ime_prezime = korisnik["ime"] + " " + korisnik["prezime"]
								uloga = korisnik["uloga"]
								promena.append(recnik)
							elif( a == 2 and korisnik["status"] == "blokiran"): #ako zeli da odblokira osobu, ona mora biti blokirana
								recnik = {"korisnicko_ime": korisnik["korisnicko_ime"], "lozinka": korisnik["lozinka"], "ime": korisnik["ime"], "prezime": korisnik["prezime"],"pol": korisnik["pol"], "kontakt_telefon": korisnik["kontakt_telefon"], "email": korisnik["email"], "uloga":korisnik["uloga"], "status": "aktivan"}
								#pravi se recnik u kom korisniku menja svoj status u aktivan
								count = count+1
								promena.append(recnik)
							elif(korisnik["status"] == "blokiran"):
								print("Ne mozete da blokirate korisnika koji je vec blokiran!")
							elif(korisnik["status"] == "aktivan"):
								print("Ne mozete da odblokirate korisnika koji je aktivan!")
						else:
							promena.append(korisnik)
					else:
						promena.append(korisnik)

			if(count != 0):  #u slucaju da su korisnici pronadjeni, izvrsava se novih podataka u json dokument
				with open("../data/korisnici.json", "w", encoding="utf-8") as f:
					json.dump(promena, f, indent= 4)

				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
				if( a == 1 ): #korisniku se ispisuje poruka da je uspesno izvrsio radnju (blokiranje ili odblokiranje)
					print("Uspesno ste blokirali korisnika sa korisnickim imenom: ", ime)
					if(uloga == "domacin"): #ako je korisnik kog je administrator blokirao domacin, svi njegovi apartmani i rezrvacije se brisu
						upis_apartmana = []
						upis_rezervacija = []
						sifre = []
						with open("../data/apartmani.json", "r", encoding="utf-8") as f:
							apartmani = json.load(f)
							for apartman in apartmani:
								if(apartman["domacin"].lower() == ime_prezime.lower()): #pronalazi se odgovarajuce ime domacina
									sifre.append(apartman["sifra"]) #cuvaju se sifre njegovih apartmana kako bi se mogle obrisati rezervacije vezane za te sifre
								else:
									upis_apartmana.append(apartman) #svi preostali apartmani se ponovo upisuju u datoteku apartmana

						with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
							rezervacije = json.load(f)
							for rezervacija in rezervacije:
								c = 0
								for i in range(len(sifre)): #za sve sifre koje u dodate u listu, pretrazuje se ima li poklapanja za tu rezervaciju, ako ima ona ce biti obrisana
									if(rezervacija["apartman"]["sifra"] == sifre[i]):
										c = c + 1
								if(c == 0):
									upis_rezervacija.append(rezervacija)
										
						with open("../data/rezervacije.json", "w", encoding="utf-8") as f: 
							json.dump(upis_rezervacija, f, indent= 4)

						with open("../data/apartmani.json", "w", encoding="utf-8") as f:
							json.dump(upis_apartmana, f, indent= 4)

						print("Svi apartmani koje je ovaj korisnik posedovao obrisani su iz baze podataka!")

					elif(uloga == "gost"): #u slucaju da je korisnik koji je blokiran gost, brisu se sve rezervacije koje su na njegovo ime i datumi se vracaju 
						novi_upis = []
						rezervacija_recnik = []
						with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
							rezervacije = json.load(f)
							for rezervacija in rezervacije:
								if(rezervacija["gosti"][0].lower() != ime_prezime.lower()):
									novi_upis.append(rezervacija)
								else:
									if(rezervacija["status"] == "kreirana" or rezervacija["status"] == "prihvacena"):
										rezervacija_recnik.append(rezervacija)

						for i in range(len(rezervacija_recnik)):
							upis_apartmana = []
							with open("../data/apartmani.json", "r", encoding="utf-8") as f:
								apartmani = json.load(f)
								for apartman in apartmani:
									if(apartman["sifra"] == rezervacija_recnik[i]["apartman"]["sifra"]):
										promena = apartman
									else:
										upis_apartmana.append(apartman)

							s = 0
							dostupnost = []
							for i in range(len(rezervacija_recnik)):
								d = rezervacija_recnik[i]["pocetni_datum_rezervacije"].split(".")
								datum = date(int(d[0]), int(d[1]), int(d[2]))

								poslednji_datum = datum + timedelta(days= rezervacija_recnik[i]["broj_nocenja"])
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
											r = {"od": rezervacija_recnik[i]["pocetni_datum_rezervacije"], "do": poslednji, "indeks" : i, "duzina": len(promena["dostupnost"])+1}
											s = s + 1
										elif(poslednji_datum == dostu1):
											r = {"od": rezervacija_recnik[i]["pocetni_datum_rezervacije"], "do": promena["dostupnost"][i]["do"], "indeks" : i, "duzina": len(promena["dostupnost"])}
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

							promena["dostupnost"] = dostupnost
							upis_apartmana.append(promena)
							upis_apartmana.sort(key=lambda y: y.get('sifra'))
							with open("../data/apartmani.json", "w", encoding="utf-8") as f:
								json.dump(upis_apartmana, f, indent= 4)

						with open("../data/rezervacije.json", "w", encoding="utf-8") as f:
							json.dump(novi_upis, f, indent= 4)

						print("Sve rezervacije koje su postojale pod ovim imenom su obrisane! ")
						brojac_aktivni = brojac_aktivni - 1
						

				elif( a == 2): #u slucaju da je osoba odblokirana, menja joj se status i iam prava da se ponovo uloguje na aplikaciju
					print("Uspesno ste odblokirali korisnika sa korisnickim imenom: ", ime)
					brojac_blokirani = brojac_blokirani - 1
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			else:
				print("Nalog sa ovim korisnickim imenom ne postoji!")
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

			
			if((a == 1 and brojac_aktivni > 0) or (a == 2 and brojac_blokirani > 0)): #u slucaju da jos uvek postoje neki korisnici koji mogu da se blokiraju ili odblokiraju, adminu se nudi opcija da ponovi ovu radnju
				if(a == 1):
					print("Da li zelite da blokirate jos osoba ? ", end="")
				else:
					print("Da li zelite da odblokirate jos osoba ? ", end="")
				o = provera_odgovora(False)
				if(o.lower() == "ne"):
					ponovo = True
			else:
				ponovo = True
	else:
		if(a == 1):
			print("Greska! Ne postoje korisnici koje mozete da blokirate ovog momenta!")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		else:   
			print("Greska! Ne postoje korisnici koje mozete da odblokirate ovog momenta!")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def izvestavanje(): #administrator ima mogucnost da izabere vise izvestaja koje zeli da pregleda
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("1. Lista potvrdjenih apartmana za izabran datum")
	print("2. Lista potvrdjenih apartmana po imenu domacina")
	print("3. Godisnji pregled angazovanja po domacinu")
	print("4. Mesecni pregled angazovanja po domacinu")
	print("5. Ukupan broj i cena rezervacija po datumu")
	print("6. Pregled zastupljenosti gradova")
	
	a = provera_broja(False, 0, 7)

	ispis = []
	if( a == 1 ): #lista svih potvrdjenih rezervacija za odredjeni datum
		print("Unesite datum za koji zelite da vidite izvestaj!")
		unesen_datum = unos_datuma()

		sifre_apartmana = []
		with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
			rezervacije = json.load(f)
			for rezervacija in rezervacije:
				if(rezervacija["status"] == "zavrsena" or rezervacija["status"] == "prihvacena"):
					#ovde ide deo sa proverama datuma
					lista_datuma = []
					for i in range(rezervacija["broj_nocenja"]):
						datum_lista = rezervacija["pocetni_datum_rezervacije"].split(".")
						datum = date(int(datum_lista[0]), int(datum_lista[1]), int(datum_lista[2])) + timedelta(days=i)
						lista_datuma.append(datum)

					for i in range(len(lista_datuma)):
						if(lista_datuma[i] == unesen_datum):
							sifre_apartmana.append(rezervacija["apartman"]["sifra"])

		if(len(sifre_apartmana) == 0):
			print("Datum koji proveravate nema rezervisanih apartmana! ")
		else:
			sifre_apartmana = list(set(sifre_apartmana))
			with open("../data/apartmani.json", "r", encoding="utf-8") as f:
				apartmani = json.load(f)
				for apartman in apartmani:
					for i in range(len(sifre_apartmana)):
						if(apartman["sifra"] == sifre_apartmana[i]):
							ispis.append(ispis_apartmana(apartman))

			header = ["Sifra", "Domacin", "Tip", "Sobe", "Gosti", "Adresa", "Cena", "Sadrzaj Apartmana"]
			print(tabulate(ispis, header, tablefmt="psql"))

	elif(a == 2): #lista potvrdjenih rezervacija za odredjenog domacina
		domacin = input("Unesite ime domacina da biste videli izvestaj za njegove apartmane: ") #pretraga se obavlja po imenu i prezimenu domacina
		brojac = 0 
		with open("../data/korisnici.json", "r", encoding="utf-8") as f:
			korisnici = json.load(f)
			for korisnik in korisnici:
				if(korisnik["uloga"] == "domacin"):
					if( (korisnik["ime"].lower()+ " "+ korisnik["prezime"].lower()) == domacin.lower()):
						brojac = brojac + 1

		if(brojac == 0):
			print("Ne postoji domacin sa ovim imenom!")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		else:
			sifre_apartmana = []
			with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
				rezervacije = json.load(f)
				for rezervacija in rezervacije:
					if domacin.lower() == rezervacija["apartman"]["domacin"].lower():
						if(rezervacija["status"] == "zavrsena" or rezervacija["status"] == "prihvacena"):
							sifre_apartmana.append(rezervacija["apartman"]["sifra"])
			if(len(sifre_apartmana) == 0):
				print("Trenutno nema rezervacija za apartmane domacina: ", domacin ,"! ")
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			else:
				sifre_apartmana = list(set(sifre_apartmana))
				print("Pretraga rezervisanih apartmana za domacina ", domacin)
				with open("../data/apartmani.json", "r", encoding="utf-8") as f:
					apartmani = json.load(f)
					for apartman in apartmani:
						for i in range(len(sifre_apartmana)):
							if(apartman["sifra"] == sifre_apartmana[i]):
								ispis.append(ispis_apartmana(apartman))

				header = ["Sifra", "Domacin", "Tip", "Sobe", "Gosti", "Adresa", "Cena", "Sadrzaj Apartmana"]
				print(tabulate(ispis, header, tablefmt="psql"))

	elif(a == 3 or a == 4): #godisnjji ili mesecni pregled rezervacija za svakoga domacina
		lista = []
		with open("../data/korisnici.json", "r", encoding="utf-8") as f:
			korisnici = json.load(f)
			for korisnik in korisnici:
				if(korisnik["uloga"] == "domacin"):
					recnik = {"domacin": (korisnik["ime"].lower()+" "+ korisnik["prezime"].lower()), "broj_rezervacija": 0, "ukupna_zarada": 0}
					lista.append(recnik)

		sifre_apartmana = []
		
		with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
			rezervacije = json.load(f)
			for rezervacija in rezervacije:
				if(rezervacija["status"].lower() == "zavrsena"):
					datum_lista = rezervacija["pocetni_datum_rezervacije"].split(".")
					datum = date(int(datum_lista[0]), int(datum_lista[1]), int(datum_lista[2]))
					if( a == 3 ):
						datum_godina = date(date.today().year-1, date.today().month, date.today().day) 
					else:
						if( (date.today().month-1) == 0 ):
							datum_godina = date(date.today().year-1, 12, date.today().day)  
						else:
							datum_godina = date(date.today().year, (date.today().month)-1, date.today().day)
					if(datum >= datum_godina and datum < date.today()):
						for i in range(len(lista)):
							if (lista[i]["domacin"].lower() == rezervacija["apartman"]["domacin"].lower() ):
								lista[i]["broj_rezervacija"] = lista[i]["broj_rezervacija"] + 1
								lista[i]["ukupna_zarada"] = lista[i]["ukupna_zarada"] + rezervacija["ukupna_cena"]
								sifre_apartmana.append(rezervacija["apartman"]["sifra"])

		if(len(sifre_apartmana) == 0):
			if(a == 3):
				print("Ne postoje rezervacije u poslednjih godinu dana! ")
			else:
				print("Ne postoje rezervacije u poslednjih mesec dana! ")
		else:
			for i in range(len(lista)):
				nesto = []
				nesto.append(lista[i]["domacin"].title())
				if(lista[i]["broj_rezervacija"] == 0):
					if(a == 3):
						nesto.append("Nema podataka o rezervacijama u proteklih godinu dana!")
					else:
						nesto.append("Nema podataka o rezervacijama u proteklih mesec dana!")

					nesto.append("0")
				else:
					nesto.append(lista[i]["broj_rezervacija"])
					nesto.append(lista[i]["ukupna_zarada"])

				ispis.append(nesto)

			header = ["Domacin", "Broj rezervacija", "Zarada"]
			print(tabulate(ispis, header, tablefmt="psql"))

	elif(a == 5): #ukupan broj i cena rezervacija za odredjeni datum
		domacin = input("Unesite ime domacina da biste videli izvestaj za njegove apartmane: ")
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		brojac = 0 
		with open("../data/korisnici.json", "r", encoding="utf-8") as f:
			korisnici = json.load(f)
			for korisnik in korisnici:
				if(korisnik["uloga"] == "domacin"):
					if( (korisnik["ime"].lower()+" "+ korisnik["prezime"].lower()) == domacin.lower()):
						brojac = brojac + 1

		if(brojac == 0):
			print("Ne postoji domacin sa ovim korisnickim imenom!")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		else:
			print("Unesite datum za koji zelite da vidite izvestaj!")
			unesen_datum = unos_datuma()

			sifre_apartmana = []
			lista_datuma = []
			ukupna_cena = 0
			broj_rezervacija = 0
			with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
				rezervacije = json.load(f)
				for rezervacija in rezervacije:
					if(rezervacija["status"] == "zavrsena" or rezervacija["status"] == "prihvacena"):
						if (domacin.lower() == rezervacija["apartman"]["domacin"].lower() ):
							for i in range(rezervacija["broj_nocenja"]):
								datum_lista = rezervacija["pocetni_datum_rezervacije"].split(".")
								datum = date(int(datum_lista[0]), int(datum_lista[1]), int(datum_lista[2])) + timedelta(days = i)
								if(datum == unesen_datum):
									cena = (rezervacija["apartman"]["cena_po_noci"])
									if(rezervacija["popust"] == "da"):
										cena = cena * 0.95 #ako je korisnik prilikom rezervacije imao pravo na popust cena po noci mu se smanjila za 5 posto
									
									with open("../data/praznici.json", "r", encoding="utf-8") as f: #proverava se da li se dan poklapa sa nekim praznicnim datumom
										praznici = json.load(f)
										for dan in praznici:
											dlista = dan["datum"].split(".")
											d = date(int(dlista[0]), int(dlista[1]), int(dlista[2]))
											if(d == date.today()):
												cena = cena * 1.05 #cena za taj dan se uvecava za 5 posto
												
									if(date.today().weekday() > 4): #ako je dan koji se proverava vikend to se belezi u listu, koja kasnije sluzi da se izracuna ukupna cena rezervacije
										cena = cena * 0.9 #cena za taj dan se smanjuje za 10 posto
										
									
									ukupna_cena = ukupna_cena + cena
									broj_rezervacija = broj_rezervacija + 1
									sifre_apartmana.append(rezervacija["apartman"]["sifra"])

			if(len(sifre_apartmana) == 0):
				print("Datum koji proveravate nema rezervisanih apartmana! ")
			else:
				sifre_apartmana = list(set(sifre_apartmana))
				header = ["Datum", "Domacin", "Ukupan broj potvrdjenih rezervacija", "Ukupna cena svih rezervacija"]
				i = []
				i.append(unesen_datum)
				i.append(domacin.title())
				i.append(broj_rezervacija)
				i.append(ukupna_cena)
				ispis.append(i)

				print(tabulate(ispis, header, tablefmt="psql"))

	elif(a == 6): #pregled zastupljenosti gradova
		brojac = 0
		lista = []
		with open("../data/rezervacije.json", "r", encoding="utf-8") as f:
			rezervacije = json.load(f)
			for rezervacija in rezervacije:
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
						
		if(brojac == 0):
			print("Ne postoje nikakve informacije u bazi podataka!")
		else:
			lista.sort(key=lambda x: x.get('ponavljanje'), reverse= True)
			
			for i in range(len(lista)):
				nesto = []
				nesto.append(str(i+1)+".")
				nesto.append(lista[i]["grad"])
				nesto.append(str(lista[i]["ponavljanje"])+ " / " + str(brojac))
				nesto.append(str(round(lista[i]["ponavljanje"]/brojac*100, 2)) + "%")

				ispis.append(nesto)

			header = ["Redni Broj", "Grad", "Ponavljanje", "Procenat Zastupljenosti"]
			print(tabulate(ispis, header, tablefmt="psql"))

def praznicni_dani(): #administrator ima pravo da unese praznicne dane, po kojima se kasnije racunaju cene apartmana
	print("Unesite praznicne datume: ")
	praznici = []

	with open("../data/praznici.json", "r", encoding="utf-8") as f: #proverava se da li su predhodno vec unoseni datumi
		datumi = json.load(f)
		for dan in datumi:
			praznici.append(dan) #ako postoje datumi od ranije, kopiraju se u listu koja ce naknadno da bude unesena

	p = False
	while(p == False): #aministrator unosi datume sve dok ne unese sve sto zeli

		datum = unos_datuma()
		count = 0
		for i in range(len(praznici)):
			n = praznici[i]["datum"].split(".")
			provera = date(int(n[0]),int(n[1]),int(n[2]))
			if(provera == datum):
				count = count + 1
				print("Greska. Ovaj datum ste vec uneli. Da li zelite da pokusate ponovo ? ", end="")
				odg = provera_odgovora(False)
				if(odg.lower() == "ne"):
					p = True
		
		if(count == 0):
			datum_str = str(datum.year) + "." + str(datum.month) + "." + str(datum.day) + "."
			recnik = {"datum": datum_str}
			praznici.append(recnik)

			print("Uspesno ste uneli praznicni datum! Da li zelite da unesete jos datuma ? ", end="")

			odgovor = provera_odgovora(False)
			if(odgovor.lower() == "ne"):
				p = True


	with open("../data/praznici.json", "w", encoding="utf-8") as f:
		json.dump(praznici, f, indent= 4) #na kraju se unosi cela lista u json datoteku

def aktivacija_apartmana():
	lista_sifri = []
	ispis = []
	with open("../data/apartmani.json", "r", encoding="utf-8") as f:
			apartmani = json.load(f)
			for apartman in apartmani:
				if(apartman["status"].lower() == "neaktivno"): #kada se proveri da li je apartman aktivan, ispisuju se podaci o njemu
					ispis.append(ispis_apartmana(apartman))
					lista_sifri.append(apartman["sifra"])
	
	if(len(lista_sifri) == 0): #ako nije pronadjen ni jedan aktivan apartman u datoteci, ispisuje se "greska"
		print("Trenutno ne postoje neaktivni apartmani u bazi podataka!")
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	else:

		header = ["Sifra", "Domacin", "Tip", "Sobe", "Gosti", "Adresa", "Cena", "Sadrzaj Apartmana"]
		print(tabulate(ispis, header, tablefmt="psql"))

		p = False
		while(p == False):
			print("Izaberite sifru apartmana koji zelite da aktivirate: ", end="")
			sifra = int_provera(False)

			novi_apartmani = []
			if(sifra in lista_sifri):
				with open("../data/apartmani.json", "r", encoding="utf-8") as f:
					apartmani = json.load(f)
					for apartman in apartmani:
						if(apartman["sifra"] == sifra):
							apartman["status"] = "aktivno"

						novi_apartmani.append(apartman)

			if(len(novi_apartmani) != 0):
				novi_apartmani.sort(key=lambda x: x.get('sifra')) #apartmani se sortiraju pre upisa
				with open("../data/apartmani.json", "w", encoding="utf-8") as f:
					json.dump(novi_apartmani, f, indent= 4)

				lista_sifri.remove(sifra)

				print("Uspesno ste aktivirali apartman pod sifrom ", sifra)
				print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

				if(len(lista_sifri) > 0):
					print("Da li zelite da nastavite ? ", end="")
					odgovor = provera_odgovora(False)
					if(odgovor.lower() == "ne"):
						p = True
				else:
					print("Ne postoji vise apartmana koje je potrebno aktivirati!")
					print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
					p = True
			else:
				print("Apartman sa ovom sifrom nije moguće aktivirati!")
				p = True
