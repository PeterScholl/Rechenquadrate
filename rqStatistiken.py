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
    listeAllerRechnungen = generiereListeAllerRechnungen()
    
    #Idee finde zwei nahezu eindeutige Rechnungen, die in höchstens einer Zahl übereinstimmen
    max_lsg = 3
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
    #Fülle die fehlenden Rechenzeichen (8 Stück und Zahlen )
    return False

if __name__ == "__main__":
    for char in "+-x÷":
        print("÷",char,bestimmeAlleErgebnisse('÷',char))
    rq2 = rq.Rechenquadrat()
    print(rq2.evaluate_expression("9x8x7"))
    print(bestimmeAlleErgebnisseMitGegHaeufigkeit('+','÷',2))

    print("Anz gemeinsamer Ziffern von 9÷1x2 und 6+2+9:",anzGemeinsamerZiffern('9÷1x2','6+2+9'))

    listeAllerRechnungen = generiereListeAllerRechnungen()
    print(len(listeAllerRechnungen))

    generiereEinfachesRQ()