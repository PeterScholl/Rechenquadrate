import GPT_Rechenquadrat as rq
import random
from types import MappingProxyType

RECHENZEICHEN = "+-x÷"

#Konstante Werte für die Maximalen Ergebnisse der Rechnungen
MAX_ERG = MappingProxyType({
    "++": 24, "+-": 16, "+x": 135, "+÷": 17,
    "-+": 16, "--": 6, "-x": 64, "-÷": 7,
    "x+": 79, "x-": 71, "xx": 504 , "x÷": 72,
    "÷+": 17, "÷-": 7, "÷x": 72, "÷÷": 4
})

#Konstante Werte für die minimale Häufigkeit, mit der ein Ergebnis vorkommen muss
MIN_HAEUFIG = MappingProxyType({
    "++": 6, "+-": 2, "+x": 2, "+÷": 2,
    "-+": 2, "--": 2, "-x": 1, "-÷": 1,
    "x+": 2, "x-": 2, "xx": 6 , "x÷": 2,
    "÷+": 2, "÷-": 1, "÷x": 1, "÷÷": 2
})


def bestimmeAlleErgebnisse(rechenzeichen1, rechenzeichen2):
    rq1 = rq.Rechenquadrat()
    results = {}
    for f1 in range(1,10):
        for f2 in range(1,10):
            for f3 in range(1,10):
                if (f1 != f2 and f1 != f3 and f2 != f3):
                    #Alle Verschieden
                    expression=str(f1)+rechenzeichen1+str(f2)+rechenzeichen2+str(f3)
                    erg = rq1.evaluate_expression(expression)
                    if (erg[1] and erg[2] and erg[3]):
                        #Berechnung immer positiv und immer ganzzahl
                        if erg[0] in results:
                            results[erg[0]].append(expression)
                        else:
                            results[erg[0]] = [expression]
    return results

def bestimmeAlleErgebnisseMitGegHaeufigkeit(rechenzeichen1,rechenzeichen2,haeufig):
    alle = bestimmeAlleErgebnisse(rechenzeichen1, rechenzeichen2)
    filtered= {k: v for k, v in alle.items() if len(v) == haeufig}
    return list(filtered.keys())

def generiereListeAllerRechnungen():
    result = {}
    for z1 in "+-x÷":
        for z2 in "+-x÷":
            dict = bestimmeAlleErgebnisse(z1,z2)
            inverted_dict = {item: len(vlist) for vlist in dict.values() for item in vlist}
            result.update(inverted_dict)
    return result


def anzGemeinsamerZiffern(rech1,rech2):
    a = set()
    a.add(int(rech1[0]))
    a.add(int(rech1[2]))
    a.add(int(rech1[4]))
    a.add(int(rech2[0]))
    a.add(int(rech2[2]))
    a.add(int(rech2[4]))
    return 6-len(a)


def generiereEinfachesRQ():
    rqNeu = rq.Rechenquadrat()
    listeAllerRechnungen = generiereListeAllerRechnungen()
    
    #Idee finde zwei nahezu eindeutige Rechnungen, die in höchstens einer Zahl übereinstimmen
    max_lsg = 2
    einfacheRechnungen = {k: v for k, v in listeAllerRechnungen.items() if v <= max_lsg} # nur ein oder zwei Lsg
    print("Es gibt",len(einfacheRechnungen),f"Rechnungen mit höchstens {max_lsg} Lsg")
    einfRechenausdruecke = list(list(einfacheRechnungen.keys()))
    loop = 0
    while True:
        loop +=1
        r1 = einfRechenausdruecke[random.randint(0,len(einfRechenausdruecke)-1)]
        r2 = einfRechenausdruecke[random.randint(0,len(einfRechenausdruecke)-1)]
        if anzGemeinsamerZiffern(r1,r2) < 2: 
            break
        elif loop > 100:
            print("Zu viele Versuche")
            exit(1)
    print("Gefundene Rechenausdrücke:",r1,r2)
    #Trage diese in das Rechenquadrat ein
    if anzGemeinsamerZiffern(r1,r2) == 0:
        #Keine Gemeinsame Ziffer
        print("Keine gem. Ziffern")
        zeilennr = [1,2,3]
        random.shuffle(zeilennr)
        #Zufällige Zeile auswählen - r1 eintragen
        rqNeu.set_expression_zeile(zeilennr[0],r1)
        #Zufällige nächste Zeile auswählen - r2 eintragen
        rqNeu.set_expression_zeile(zeilennr[1],r2)
        #Restlichen Zahlen in die fehlende Zeile eintragen
        ziffern = [*ziffernEinerExpression(r1),*ziffernEinerExpression(r2)]
        #print("Ziffern",ziffern)
        restziffern = list(set(range(1,10)) - set(ziffern))
        random.shuffle(restziffern)
        #print("Restziffern - zufällig", restziffern)
        rqNeu.set_expression_zeile(zeilennr[2],str(restziffern[0])+"+"+str(restziffern[1])+"+"+str(restziffern[2]))
        #Gültige Rechenzeichen durch ausprobieren ermitteln (alle - for Schleife mit zufälliger Reihenfolge
        for rz in charGeneratorLength("+-x÷",8):
            for pos in range(8):
                if (pos<2): #Die beiden Zeichen in der Zeile
                    rqNeu.set_rechenzeichen_zeile(zeilennr[2],pos+1,rz[pos])
                else: #Die Sechs Zeichen in der Zeile
                    spalte = (pos-2)//2 +1
                    sppos  = (pos-2)%2 + 1  
                    #print(f"spalte {spalte} - Position {sppos} - Rechenzeichen {rz[pos]}")
                    rqNeu.set_rechenzeichen_spalte(spalte,sppos,rz[pos])
            #Prüfen ob Valid
            evZeile = rqNeu.evaluate_zeile(zeilennr[2])
            valid = evZeile[1] and evZeile[2] and evZeile[3]
            rqNeu.set_ergebnis_zeile(zeilennr[2],evZeile[0])
            for i in range(1,4):
                evSpalte = rqNeu.evaluate_spalte(i)
                valid = valid and evSpalte[1] and evSpalte[2] and evSpalte[3]
                rqNeu.set_ergebnis_spalte(i,evSpalte[0])
            if (valid):
                break

        #Zufällig spiegeln (Zeile->Spalte)               

    else:
        print("Eine gemeinsame Ziffer")
        #Postionen der gemeinsamen Ziffer finden
        pos1 = 0
        pos2 = 0
        while True:
            if r1[pos1]==r2[pos2]:
                break
            else:
                pos2 += 2
                if pos2 > 4:
                    pos2 = 0
                    pos1 += 2
        #Entsprechend in Zeile und Spalte eintragen
        pos1//=2
        pos2//=2
        print(f"Rechenausdruck r1 {r1}, r2 {r2}, pos1 {pos1}, pos2 {pos2}")
        # r1 in Zeile pos2+1
        rqNeu.set_expression_zeile(pos2+1, r1)
        # r2 in Spalte pos1+1
        rqNeu.set_expression_spalte(pos1+1,r2)
        #Rest füllen
        #Restlichen Zahlen in die fehlende Zeile eintragen
        ziffern = [*ziffernEinerExpression(r1),*ziffernEinerExpression(r2)]
        print("Ziffern",ziffern)
        restziffern = list(set(range(1,10)) - set(ziffern))
        random.shuffle(restziffern)
        print("Restziffern - zufällig", restziffern)
        for ziffpos in range(9):
            if ziffpos//3 != pos2 and ziffpos%3 != pos1:
                rqNeu.set_ziffer(ziffpos,restziffern.pop())

        #Gültige Rechenzeichen durch ausprobieren ermitteln (alle - for Schleife mit zufälliger Reihenfolge
        for rz in charGeneratorLength("+-x÷",8):
            for pos in range(8):
                if (pos<4): #Die vier Zeichen in den Zeilen (pos2 enthält ausschlusszeile
                    zpos = pos + (2 if pos>=2*pos2 else 0)
                    #print(zpos)
                    rqNeu.set_rechenzeichen(zpos,rz[pos])
                else: #Die vier Zeichen in den Spalten (pos1 enthält ausschlusszeile)
                    spalte = (pos-4)//2
                    if (spalte>=pos1): spalte+=1
                    spalte += 1
                    sppos  = pos%2 + 1  
                    #print(f"spalte {spalte} - Position {sppos} - Rechenzeichen {rz[pos]}")
                    rqNeu.set_rechenzeichen_spalte(spalte,sppos,rz[pos])
            #Prüfen ob Valid
            valid = True
            for i in range(1,4):
                evZeile = rqNeu.evaluate_zeile(i)
                valid = valid and evZeile[1] and evZeile[2] and evZeile[3]
                rqNeu.set_ergebnis_zeile(i,evZeile[0])
                evSpalte = rqNeu.evaluate_spalte(i)
                valid = valid and evSpalte[1] and evSpalte[2] and evSpalte[3]
                rqNeu.set_ergebnis_spalte(i,evSpalte[0])
            if (valid):
                break

        #Zufällig spiegeln

    rqNeu.ausgabe()

    return rqNeu

def ziffernEinerExpression(expression):
    return list(map(int,[expression[0],expression[2],expression[4]]))

def charGenerator(string):
    shuffled = list(string)
    random.shuffle(shuffled)
    shuffled_s = "".join(shuffled)
    for i in range(len(shuffled_s)):  # Alle Zeichen
        yield shuffled_s[i]

def charGeneratorLength(s, length):
    """Generator, der eine Liste fester Länge erstellt und an zufälligen Positionen Zeichen ersetzt."""
    generators = [charGenerator(s) for _ in range(length)]
    positions = [next(g) for g in generators]  # Initiale Füllung mit den ersten Zeichen

    while True:
        yield positions.copy()  # Aktuelle Liste ausgeben

        for i in range(length - 1, -1, -1):  # Von rechts nach links durchlaufen
            try:
                positions[i] = next(generators[i])  # Nächstes Zeichen für diese Position
                break  # Nur eine Position ändern
            except StopIteration:
                if i == 0:
                    return  # Beenden, wenn alle Generatoren durch sind
                generators[i] = charGenerator(s)  # Neuen Generator starten
                positions[i] = next(generators[i])  # Neu befüllen

if __name__ == "__main__":
    for char in "+-x÷":
        print("÷",char,bestimmeAlleErgebnisse('÷',char))
    rq2 = rq.Rechenquadrat()
    print(rq2.evaluate_expression("9x8x7"))
    print(bestimmeAlleErgebnisseMitGegHaeufigkeit('+','÷',2))

    print("Anz gemeinsamer Ziffern von 9÷1x2 und 6+2+9:",anzGemeinsamerZiffern('9÷1x2','6+2+9'))

    listeAllerRechnungen = generiereListeAllerRechnungen()
    print(len(listeAllerRechnungen))

    print("Ziffern der Expression 1x2+9",ziffernEinerExpression('1x2+9'))

    
    for i in charGenerator("abcd"):
        print(i)

    print("Multi")

    pos = charGeneratorLength("+-x/",3)
    for i in range(8):
        print(next(pos))

    generiereEinfachesRQ()
