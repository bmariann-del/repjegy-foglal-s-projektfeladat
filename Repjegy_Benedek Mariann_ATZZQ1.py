import datetime

class Jarat:
    def __init__(self, jszam, cel, alap_ar):
        self.jszam = jszam
        self.cel = cel
        
        # csak pozitív lehet az ár, ha mínuszt adnak meg, lenullázzuk
        if alap_ar < 0:
            self.alap_ar = 0 
        else:
            self.alap_ar = alap_ar

    def vegleges_ar(self):
        # ősosztályban ez üres, majd a leszármazottban megírjuk a szabályokat
        pass

    def __str__(self):
        return f"Járat: {self.jszam} - {self.cel} (Ár: {self.vegleges_ar()} Ft)"


class BelfoldiJarat(Jarat):
    def vegleges_ar(self):
        # 20% kedvezmény a belföldiekre
        return int(self.alap_ar * 0.8)

    def __str__(self):
        return "[Belföldi] " + super().__str__()


class NemzetkoziJarat(Jarat):
    def vegleges_ar(self):
        # 50% felár a külföldiekre
        return int(self.alap_ar * 1.5)

    def __str__(self):
        return "[Nemzetközi] " + super().__str__()


class LegitCeg:
    def __init__(self, nev):
        self.nev = nev
        self.jarat_lista = []

    def uj_jarat_hozzaadasa(self, uj_jarat):
        self.jarat_lista.append(uj_jarat)

    def jarat_keresese(self, jszam):
        for j in self.jarat_lista:
            if j.jszam == jszam:
                return j
        return None


class Jegy:
    def __init__(self, utas, jarat, datum):
        self.utas_neve = utas
        self.jarat = jarat
        self.indulas_datum = datum
        self.fizetendo = jarat.vegleges_ar()

    def __str__(self):
        return f"Utas: {self.utas_neve} | {self.jarat.jszam} ({self.jarat.cel}) | Dátum: {self.indulas_datum} | Ár: {self.fizetendo}"


class FoglalasRendszer:
    def __init__(self, ceg):
        self.ceg = ceg
        self.foglalasok = []

    def uj_foglalas(self, utas, jszam, datum_str):
        if utas == "":
            print("Nem adtál meg nevet!")
            return None

        try:
            # átalakítjuk a stringet dátummá
            d = datetime.datetime.strptime(datum_str, "%Y-%m-%d")
        except:
            print("Rossz a dátum formátuma. Kérlek így add meg: YYYY-MM-DD")
            return None

        if d < datetime.datetime.now():
            print("Múltbéli időpontra nem lehet foglalni.")
            return None

        j = self.ceg.jarat_keresese(jszam)
        if j == None:
            print("Nincs ilyen járatszám a rendszerben.")
            return None

        f = Jegy(utas, j, datum_str)
        self.foglalasok.append(f)
        return f.fizetendo

    def mentes_torlese(self, utas, jszam):
        talalat = False
        for f in self.foglalasok:
            if f.utas_neve == utas and f.jarat.jszam == jszam:
                self.foglalasok.remove(f)
                talalat = True
                break # elég egyet törölni
        
        if talalat == False:
            print("Nincs ilyen foglalás, amit törölni lehetne.")
        else:
            print("Sikeresen törölve!")

    def osszes_kiiratasa(self):
        if len(self.foglalasok) == 0:
            print("Jelenleg üres a lista.")
        else:
            print("\n--- Aktuális Foglalások ---")
            for f in self.foglalasok:
                print(f)
            print("---------------------------")


# Főprogram és tesztadatok

lt = LegitCeg("Egyetemi Légitársaság")

lt.uj_jarat_hozzaadasa(BelfoldiJarat("MA101", "Debrecen", 15000))
lt.uj_jarat_hozzaadasa(BelfoldiJarat("MA102", "Pécs", 12000))
lt.uj_jarat_hozzaadasa(NemzetkoziJarat("MA201", "London", 80000))

rendszer = FoglalasRendszer(lt)

# feltöltöm pár alap adattal
rendszer.uj_foglalas("Kiss Anna", "MA101", "2026-06-01")
rendszer.uj_foglalas("Nagy Péter", "MA101", "2026-06-02")
rendszer.uj_foglalas("Fekete Luca", "MA201", "2026-07-01")
rendszer.uj_foglalas("Szabó Éva", "MA102", "2026-06-05")
rendszer.uj_foglalas("Tóth Gábor", "MA102", "2026-06-10")
rendszer.uj_foglalas("Horváth Dóra", "MA201", "2026-07-15")

# Konzolos menü
while True:
    print("\n*** Menü ***")
    print("1. Járatok listája")
    print("2. Jegy foglalása")
    print("3. Foglalás lemondása")
    print("4. Foglalások megtekintése")
    print("0. Kilépés")
    
    valasztas = input("Mit szeretnél tenni? ")

    if valasztas == "1":
        print("\nElérhető járatok:")
        for j in lt.jarat_lista:
            print(j)
            
    elif valasztas == "2":
        nev = input("Add meg a neved: ")
        jarat = input("Járatszám (pl. MA101): ")
        datum = input("Dátum (pl. 2026-10-15): ")
        
        ar = rendszer.uj_foglalas(nev, jarat, datum)
        if ar != None:
            print(f"A foglalás sikeres! A fizetendő összeg: {ar} Ft.")
            
    elif valasztas == "3":
        nev = input("Név: ")
        jarat = input("Járatszám: ")
        rendszer.mentes_torlese(nev, jarat)
        
    elif valasztas == "4":
        rendszer.osszes_kiiratasa()
        
    elif valasztas == "0":
        print("Kilépés...")
        break
        
    else:
        print("Ilyen menüpont nincs, próbáld újra!")