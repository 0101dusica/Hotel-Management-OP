import datetime
from datetime import date

def provera_broja(p, donja_granica, gornja_granica):
    while (p == False):
        a = input("Unesite opciju koju zelite: " )
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        try:
            a = int(a)
            if( a < gornja_granica and a > donja_granica):
                p = True
                return a
            else:
                print("Niste uneli jednu od ponudjenih opcija. Pokusajte ponovo.")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        except ValueError:
            print("Morate da unesete broj. Pokusajte ponovo!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def int_provera(p):
    while (p == False):
        a = input()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        try:
            a = int(a)
            p = True
            return a
        except ValueError:
            print("Morate da unesete broj. Pokusajte ponovo!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def decimala_provera(p):
    while (p == False):
        a = input()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        try:
            a = float(a)
            p = True
            return a
        except ValueError:
            print("Morate da unesete broj. Pokusajte ponovo!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def provera_odgovora(p):
    while (p == False):
        odgovor = input("da ne -> ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        if(odgovor.lower() == "da" or odgovor.lower() == "ne"):
            p == True
            return odgovor
        else:
            print("Niste uneli jedan od ponudjenih odgovora. Pokusajte ponovo sa unosom ! ", end="")

def unos_datuma():
    provera = False
    while(provera == False):
        print("Unesite dan -> ", end="")
        dan = int_provera(False)
        print("Unesite mesec -> ", end="")
        mesec = int_provera(False)
        print("Unesite godinu -> ", end="")
        godina = int_provera(False)

        if((godina - (date.today().year + 5)) > 0):
            print("Ne mozete da uneste ovu godinu! Pokusajte ponovo sa unosom! ")
        else:
            if(mesec < 13 and mesec > 0):
                if(mesec == 1 or mesec == 3 or mesec == 5 or mesec == 7 or mesec == 8 or mesec == 10 or mesec == 12):
                    if(dan <= 31 and dan > 0):
                        provera = True
                    else:
                        print("U ", mesec,". mesecu nema ", dan, " dana. Pokusajte ponovo sa unosom!")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                elif(mesec == 2):
                    if( godina%4 == 0 ):
                        if(dan <= 29 and dan > 0):
                            provera = True
                        else:
                            print("U ", mesec,". mesecu nema ", dan, " dana. Pokusajte ponovo sa unosom!")
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    else:
                        if(dan <= 28 and dan > 0):
                            provera = True
                        else:
                            print("U ", mesec,". mesecu nema ", dan, " dana. Pokusajte ponovo sa unosom!")
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                else:
                    if(dan <= 30 and dan > 0):
                        provera = True
                    else:
                        print("U ", mesec,". mesecu nema ", dan, " dana. Pokusajte ponovo sa unosom!")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            else:
                print("Greska! Nema ", mesec, " meseci u godini! Pokusajte ponovo!")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
    datum = date(godina, mesec, dan)
    return datum