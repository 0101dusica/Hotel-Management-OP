
def ispis_rezervacija(rezervacija):

	lista = []
	lista.append(rezervacija["sifra_rezervacije"])
	str = rezervacija["apartman"]["lokacija"]["adresa"]["ulica_broj"] + ", " + rezervacija["apartman"]["lokacija"]["adresa"]["grad"]+ ", " +  rezervacija["apartman"]["lokacija"]["adresa"]["postanski_broj"]
	lista.append(str)
	lista.append(rezervacija["pocetni_datum_rezervacije"])
	lista.append(rezervacija["broj_nocenja"])
	lista.append(rezervacija["ukupna_cena"])
	gosti = ""
	for i in range(len(rezervacija["gosti"])):
		if(gosti == ""):
			gosti = rezervacija["gosti"][i]
		else:
			gosti = gosti + ", " + rezervacija["gosti"][i]
	lista.append(gosti)
	lista.append(rezervacija["status"])

	return lista

def ispis_apartmana(apartman):

	lista = []

	lista.append(apartman["sifra"])
	lista.append(apartman["domacin"])
	lista.append(apartman["tip"].upper())
	lista.append(apartman["broj_soba"])

	lista.append(apartman["broj_gostiju"])
	str = apartman["lokacija"]["adresa"]["ulica_broj"] + ", " + apartman["lokacija"]["adresa"]["grad"]+ ", " +  apartman["lokacija"]["adresa"]["postanski_broj"]
	lista.append(str)
	lista.append(apartman["cena_po_noci"])
	
	sadrzaj = ""
	if(len(apartman["sadrzaj_apartmana"]) > 0):
		for i in range(len(apartman["sadrzaj_apartmana"])):
			if(i == 0):
				sadrzaj = apartman["sadrzaj_apartmana"][i]["naziv"]
			else:
				sadrzaj = sadrzaj + ", " + apartman["sadrzaj_apartmana"][i]["naziv"]
	else:
		sadrzaj = "Nije dostupan dodatan sadrzaj!"

	lista.append(sadrzaj)

	return lista