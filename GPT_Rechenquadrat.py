import copy
import random

class Rechenquadrat:
    def __init__(self):
        # 9 Ziffernfelder - 0 meint leer - die ersten 3 sind die erste Zeile
        self.ziffernfelder = [0] * 9
        
        # 12 Rechenzeichen - die ersten 6 sind die in den 3 Zeilen, die zweiten 6 in den drei Spalten
        # wobei ersteZeile,ersteZeile,2Zeile,2Zeile,3Zeile,3Zeile,1Spalte,2Spalte,3Spalte,1Spalte,2Spalte,3Spalte
        self.rechenzeichen = [' '] * 12
        
        # 6 Ergebnisse 
        self.ergebnisse = [None] * 6
    
    def set_ziffer(self, position, wert):
        if position >= 0 and position < 9:
            self.ziffernfelder[position] = wert
            
    def set_ziffer_zs(self, zeile, spalte, wert):
        if  zeile <= 3 and zeile >= 1 and spalte <= 3 and spalte >= 1:
            position = (zeile-1)*3+(spalte-1)
            self.ziffernfelder[position] = wert
        
    def set_rechenzeichen(self, position, zeichen):
        if position >= 0 and position < 12:
            self.rechenzeichen[position] = zeichen
    
    def set_rechenzeichen_zeile(self, zeile, position, zeichen):
        if position >= 1 and position <= 2 and zeile >= 1 and zeile <= 3:
            self.rechenzeichen[(zeile-1)*2+(position-1)] = zeichen
    
    def set_rechenzeichen_spalte(self, spalte, position, zeichen):
        if position >= 1 and position <= 2 and spalte >= 1 and spalte <= 3:
            self.rechenzeichen[6+(spalte-1)+(position-1)*3] = zeichen
    
    def set_ergebnis(self, position, ergebnis):
        if position >= 0 and position < 6:
            self.ergebnisse[position] = ergebnis
    
    def set_ergebnis_zeile(self, zeile, ergebnis):
        if zeile >= 1 and zeile <= 3:
            self.ergebnisse[zeile-1] = ergebnis

    def set_expression_zeile(self, zeile, expression):
        #expression valid?
        self.set_rechenzeichen_zeile(zeile,1,expression[1])
        self.set_rechenzeichen_zeile(zeile,2,expression[3])
        self.set_ziffer((zeile-1)*3,int(expression[0]))
        self.set_ziffer((zeile-1)*3+1,int(expression[2]))
        self.set_ziffer((zeile-1)*3+2,int(expression[4]))
        self.set_ergebnis_zeile(zeile,self.evaluate_expression(expression)[0])

    def set_ergebnis_spalte(self, spalte, ergebnis):
        if spalte >= 1 and spalte <= 3:
            self.ergebnisse[3+spalte-1] = ergebnis

    def set_expression_spalte(self, spalte, expression):
        #expression valid?
        self.set_rechenzeichen_spalte(spalte,1,expression[1])
        self.set_rechenzeichen_spalte(spalte,2,expression[3])
        self.set_ziffer((spalte-1),int(expression[0]))
        self.set_ziffer((spalte-1)+3,int(expression[2]))
        self.set_ziffer((spalte-1)+6,int(expression[4]))
        self.set_ergebnis_spalte(spalte,self.evaluate_expression(expression)[0])

    def get_ziffernfelder(self):
        return self.ziffernfelder
    
    def get_rechenzeichen(self):
        """
        gibt die Rechenzeichen als String zurück
        
        :return: String der Rechenzeichen
        """
        return ''.join(self.rechenzeichen)
    
    def get_ergebnisse(self):
        return self.ergebnisse
    
    def evaluate_expression(self,expression):
        """
        Diese Funktion wertet einen Mathematischen Ausdruck in Stringform von links nach
        rechts aus
        
        :param expression: der String mit dem Rechenausdruck
        :return: result (int Value), resultIsInt(boolean), alwaysInteger(boolean), alwaysPositive(boolean)
        """

        tokens = []
        current_token = ""
        
        # Schritt 1: Token aus dem Ausdruck extrahieren
        for char in expression:
            if char.isdigit():
                current_token += char
            else:
                if current_token:
                    tokens.append(current_token)
                tokens.append(char)
                current_token = ""
        if current_token:
            tokens.append(current_token)

        #print("Tokens",tokens)
        
        # Schritt 2: Ausdruck auswerten
        result = float(tokens[0])  # Der erste Wert ist immer eine Zahl
        pureInteger=True
        alwaysPositive = (result > 0)
        operator = None
        
        for token in tokens[1:]:
            if token in "+-*/÷x":
                operator = token
            else:
                num = int(token)
                if operator == "+":
                    result += num
                elif operator == "-":
                    result -= num
                elif operator == "*" or operator =="x":
                    result *= num
                elif operator == "/" or operator == "÷":
                    if num == 0:
                        raise ValueError("Division durch Null ist nicht erlaubt.")
                    result /= num
            pureInteger&=result.is_integer()
            alwaysPositive&=(result > 0)
        
        return int(result), result.is_integer(), pureInteger, alwaysPositive

    def evaluate_zeile(self,zeile):
        if zeile >= 1 and zeile <= 3:
            #String erzeugen
            linestring=""
            for j in range(3):
                ziffer = self.ziffernfelder[(zeile-1) * 3 + j]
                linestring += str(ziffer) + (self.rechenzeichen[(zeile-1)*2+j] if j < 2 else "")
            return self.evaluate_expression(linestring)
        return None

    def evaluate_spalte(self, spalte):
        if spalte >= 1 and spalte <= 3:
            # String erzeugen
            spaltenstring = ""
            for i in range(3):
                ziffer = self.ziffernfelder[i * 3 + (spalte-1)]
                spaltenstring += str(ziffer) + (self.rechenzeichen[6+i*3+(spalte-1)] if i < 2 else "")
            #print("SpString",spaltenstring)
            return self.evaluate_expression(spaltenstring)
        return None
    
    def pruefeZeile(self,zeile):
        if zeile>=1 and zeile <=3:
            res,valid,alwaysInt,alwaysPos = self.evaluate_zeile(zeile)
            return valid and alwaysInt and alwaysPos and res == self.ergebnisse[zeile-1]
        return False
    
    def pruefeSpalte(self,spalte):
        if spalte>=1 and spalte <=3:
            res,valid,alwaysInt,alwaysPos = self.evaluate_spalte(spalte)
            return valid and alwaysInt and alwaysPos and res == self.ergebnisse[3+spalte-1]
        return False

    def berechneErgebnisse(self):
        """
        Berechnet die Ergebnisse aller Zeilen und Spalten aus den gegebenen Ziffern
        """
        for i in range(3):
            self.ergebnisse[i]=self.evaluate_zeile(i+1)[0]
            self.ergebnisse[3+i]=self.evaluate_spalte(i+1)[0]
            
    def solve(self):
        #Prüfen ob alle Rechenzeichen und Ergebnisse in Ordnung sind
        loesungen = []
        #alle Ziffern auf 0 setzen
        self.ziffernfelder = [0] * 9
        position = 0 #Aktuelle position
        while position >=0 and position < 9:
            #if position>6:
            #    print(position,self.ziffernfelder)
            if self.ziffernfelder[position]>=9:
                self.ziffernfelder[position]=0
                position-=1
            else:
                self.ziffernfelder[position]+=1
                if self.ziffernfelder[position] in self.ziffernfelder[0:position]:
                    pass
                elif position < 2:
                    position+=1
                elif position==2: #erste Zeile vollständig
                    if self.pruefeZeile(1):
                        position+=1
                elif position < 5:
                    position+=1
                elif position == 5: #zweite Zeile vollständig
                    if self.pruefeZeile(2):
                        position+=1
                elif position == 6: #erste Spalte vollständig
                    if self.pruefeSpalte(1):
                        position+=1
                elif position == 7: #zweite Spalte vollständig
                    if self.pruefeSpalte(2):
                        position+=1
                elif position == 8: #Quadrat vollständig
                    if self.pruefeZeile(3) and self.pruefeSpalte(3):
                        #gueltigeLösung gefunden
                        loesungen.append(copy.deepcopy(self.ziffernfelder))
                else:
                    raise Exception("Error this case position = 9 should not be reached")
                
        return loesungen
            
    def allValidCiffers(self):
        """
        Bestimmt alle Zifferneinträge bei denen keine negativen oder Kommazahlen in den Rechnungen vorkommen
        Dabei ist nicht gesagt, dass das Rätsel dann eindeutig lösbar ist
        
        :return: eine Liste aller Eintragsmöglichkeiten
        """
        #Alle Ziffern bestimmen bei denen die Lösung ganzzahlig und ohne negative Zwischenwerte möglich ist
        loesungen = []
        #alle Ziffern auf 0 setzen
        self.ziffernfelder = [0] * 9
        position = 0 #Aktuelle position
        while position >=0 and position < 9:
            if self.ziffernfelder[position]>=9:
                self.ziffernfelder[position]=0
                position-=1
            else:
                self.ziffernfelder[position]+=1
                if self.ziffernfelder[position] in self.ziffernfelder[0:position]:
                    pass
                elif position < 2:
                    position+=1
                elif position==2: #erste Zeile vollständig
                    if self.evaluate_zeile(1)[1::]==(True,True,True):
                        position+=1
                elif position < 5:
                    position+=1
                elif position == 5: #zweite Zeile vollständig
                    if self.evaluate_zeile(2)[1::]==(True,True,True):
                        position+=1
                elif position == 6: #erste Spalte vollständig
                    if self.evaluate_spalte(1)[1::]==(True,True,True):
                        position+=1
                elif position == 7: #zweite Spalte vollständig
                    if self.evaluate_spalte(2)[1::]==(True,True,True):
                        position+=1
                elif position == 8: #Quadrat vollständig
                    if self.evaluate_zeile(3)[1::]==(True,True,True) and self.evaluate_spalte(3)[1::]==(True,True,True):
                        #gueltigeLösung gefunden
                        loesungen.append(copy.deepcopy(self.ziffernfelder))
                else:
                    raise Exception("Error this case position = 9 should not be reached")
                
        return loesungen
    
    def bestimmeEindeutigeZifferneintraege(self, max_results=100):
        """
        Ermitteln Zifferneinträge bei den gegebenen Rechenzeichen, bei denen das Rätsel eindeutig lösbar ist
        
        :return: eine Liste von Zifferneintrag
        """
        l1 = self.allValidCiffers()
        print("Liste gueltiger Zifferneintraege bei diesen Rechenzeichen erstellt:",self.rechenzeichen)
        result = []
        for entry in l1:
            self.ziffernfelder = entry
            self.berechneErgebnisse()
            if len(self.solve())==1:
                #print("Result found:",entry)
                result.append(entry)
                if len(result)>=max_results:
                    return result
        return result

    def bestimmeEinenZufaelligenEindeutigenZifferneintrag(self,max_tries=100):
        """
        Ermittelt einen Zifferneintrag bei den gegebenen Rechenzeichen, bei dem das Rätsel eindeutig lösbar ist
        
        :return: ein Zifferneintrag der durch die Ergebnisse und Rechenzeichen eindeutig bestimmbar ist
        """
        l1 = self.allValidCiffers()
        print("Liste gueltiger Zifferneintraege bei diesen Rechenzeichen erstellt:",self.rechenzeichen)
        tries=0
        while tries<max_tries:
            tries+=1
            dice = random.randint(0,len(l1)-1)
            
            self.ziffernfelder = l1[dice]
            self.berechneErgebnisse()
            if len(self.solve())==1:
                #print("Result found:",entry)
                self.ziffernfelder = l1[dice]
                return l1[dice]
        return None

    def setzeZufaelligeGueltigeRechenzeichen(self):
        """
        Setzt die Rechenzeichen des gesamten Quadrates auf eine zufällige Auswahl, so dass es eine nach
        den Regeln gültige Lösung geben kann
        """
        lsg = []
        while len(lsg)==0:
            self.rechenzeichen=[]
            for i in range(12):
                z = "+-x÷"[random.randint(0,3)]
                self.rechenzeichen.append(z)
            lsg = self.allValidCiffers()

    def loesungenGleichung(self,rechenzeichen1,rechenzeichen2,ergebnis):
        """
        Bestimmt alle Lösungen einer Rechnung aus zwei Rechenzeichen und dem gegebenen Ergebnis
        
        :return: eine Liste aller Lösungsmöglichkeiten in korrekter Reihenfolge
        """
        #Alle Ziffern bestimmen bei denen die Rechnung korrekt gelöst ist
        loesungen = []
        #alle Ziffern auf 0 setzen
        ziffern = [0] * 3
        position = 0 #Aktuelle position
        while position >=0 and position < 3:
            if ziffern[position]>=9: #Maximale Ziffer erreicht
                ziffern[position]=0
                position-=1
            else:
                ziffern[position]+=1
                if ziffern[position] in ziffern[0:position]:
                    pass
                elif position < 2: #Gleichung noch nicht vollständig
                    position+=1
                elif position==2: #Gleichung vollständig
                    expr = str(ziffern[0])+rechenzeichen1+str(ziffern[1])+rechenzeichen2+str(ziffern[2])
                    wert = self.evaluate_expression(expr)
                    #print(expr,wert)
                    if wert[0]==ergebnis and wert[1] and wert[2] and wert[3]:
                        #Lösung anhängen
                        loesungen.append(copy.deepcopy(ziffern))
                else:
                    raise Exception("Error this case position = 3 should not be reached")
                
        return loesungen
        
    def loesungenAufPosition(self,glloesungen):
        """
        Verteilt die dreistelligen loesungen in loesungen auf die einzelnen Positionen
        
        :return: liste von drei sets(!), die die Ziffern auf der jeweiligen Position enthalten
        """
        loesungen = [set(),set(),set()]
        for i in glloesungen:
            for j in range(3):
                loesungen[j].add(i[j])
        return loesungen
    
    def loeseRechenquadratStrategisch(self):
        """
        Bestimmt die Lösungen des Rechenquadrates systematisch und versucht die Schwierigkeit des Rechenquadrats
        zu beurteilen
        """
        loes_zeile1 = self.loesungenGleichung(self.rechenzeichen[0],self.rechenzeichen[1],self.ergebnisse[0])
        loes_zeile2 = self.loesungenGleichung(self.rechenzeichen[2],self.rechenzeichen[3],self.ergebnisse[1])
        loes_zeile3 = self.loesungenGleichung(self.rechenzeichen[4],self.rechenzeichen[5],self.ergebnisse[2])
        loes_spalte1 = self.loesungenGleichung(self.rechenzeichen[6],self.rechenzeichen[9],self.ergebnisse[3])
        loes_spalte2 = self.loesungenGleichung(self.rechenzeichen[7],self.rechenzeichen[10],self.ergebnisse[4])
        loes_spalte3 = self.loesungenGleichung(self.rechenzeichen[8],self.rechenzeichen[11],self.ergebnisse[5])
        print("Anzahl der Lösungen:")
        print("Zeilen:", len(loes_zeile1),len(loes_zeile2),len(loes_zeile3))
        print("Spalten:",len(loes_spalte1), len(loes_spalte2),len(loes_spalte3))
        #Lösungen aus den drei Zeilen pro Feld bestimmen
        zl = self.loesungenAufPosition(loes_zeile1)
        zl +=self.loesungenAufPosition(loes_zeile2)
        zl +=self.loesungenAufPosition(loes_zeile3)
        print("Anzahlen der Lösungen auf den 9 Positionen aus den Zeilen")
        #print(zl)
        for i in zl:
            print(len(i),end=" ")
        print()

        #Lösungen aus den drei Spalten pro Feld bestimmen
        slb = self.loesungenAufPosition(loes_spalte1)
        slb +=self.loesungenAufPosition(loes_spalte2)
        slb +=self.loesungenAufPosition(loes_spalte3)
        sl=[] #zum umsortieren
        for i in range(3):
            sl+=[slb[i],slb[i+3],slb[i+6]]
        print("Anzahlen der Lösungen auf den 9 Positionen aus den Spalten")
        #print(sl)
        for i in sl:
            print(len(i),end=" ")
        print()
        
        #Schnittmengen bilden
        schnitt = [0]*9
        for i in range(9):
            schnitt[i] = zl[i] & sl[i]
        print("Schnittmengen auf den neun Positionen")
        print(schnitt)
        print("Anzahl auf den Postionen nach Schnitt")
        print(list(map(len,schnitt)))
        
        #Tabelle erzeugen lsg_tab[position][ziffer] - True wenn möglich, False wenn nicht mehr möglich
        lsg_tab = [[True for _ in range(9)] for _ in range(9)]
        #Eintragen
        for pos in range(9):
            for zif in range(9):
                if not zif+1 in schnitt[pos]:
                    lsg_tab[pos][zif]=False
        #print(lsg_tab)
        #Zuordnungstabelle lesbar ausgeben
        print("Welche Ziffern (Spalten) sind in welcher Position(Zeilen) möglich:")
        print(" 123456789")
        for i in range(9):
            print(i+1,end="")
            print(''.join(map(lambda x: '+' if x else '.',lsg_tab[i])))
            
        #TODO:
        # - Wenn es schon eindeutige Ergebnisse gibt?!
        # - Wenn es zwei Möglichkeiten gibt, wie geht man mit wenn/dann bzw. Fallunterscheidungen um...
                    
        

    def ausgabe(self):
        output = ""
        
        for i in range(3): #Zeilen durchlaufen (bestehen jeweils aus zwei Ausgabezeilen)
            # Ziffern, Rechenzeichen und Ergebnis des ersten Blocks ausgeben
            for j in range(3):
                ziffer = self.ziffernfelder[i * 3 + j]
                output += (str(ziffer) if ziffer > 0 else " ") +" "+ (self.rechenzeichen[i*2+j] if j < 2 else "=") +" "
            output += str(self.ergebnisse[i])+"\n"
            
            # Rechenzeichen ausgeben
            for j in range(3):
                output += self.rechenzeichen[6+i * 3 + j] if i < 2 else "="
                if j < 2:
                    output += "   "
            output += "\n"
            
        #Einzelne Ziffern der Spaltenergebnisse ausgeben (ergebnisse[3:6])
        anz_max_Stellen = len(str(max((x for x in self.ergebnisse[3:6] if x is not None), default=1)))
        #print("Stellen:"+str(anz_max_Stellen))
        ergebnisse_als_String = list(map(lambda x: str(x).rjust(anz_max_Stellen),self.ergebnisse[3:6]))
        for i in range(anz_max_Stellen):
            for j in range(3):
                output+= ergebnisse_als_String[j][i]
                if j < 2:
                    output += "   "
            output += "\n"
                
        
        print(output)

if __name__ == "__main__":
    # Beispielverwendung
    rq = Rechenquadrat()
    rq.set_ziffer(0, 9)
    rq.set_ziffer(1, 8)
    rq.set_ziffer(2, 7)
    rq.set_ziffer(3, 6)
    rq.set_ziffer(4, 5)
    rq.set_ziffer(5, 2)
    rq.set_ziffer(6, 4)
    rq.set_ziffer(7, 1)
    rq.set_ziffer(8, 3)
    rq.set_rechenzeichen(0, '-')
    rq.set_rechenzeichen(1, '+')
    rq.set_rechenzeichen(2, '*')
    rq.set_rechenzeichen(3, '+')
    rq.set_rechenzeichen(4, '+')
    rq.set_rechenzeichen(5, '*')
    rq.set_rechenzeichen(6, '*')
    rq.set_rechenzeichen(7, '*')
    rq.set_rechenzeichen(8, '+')
    rq.set_rechenzeichen(9, '-')
    rq.set_rechenzeichen(10, '+')
    rq.set_rechenzeichen(11, '÷')
    rq.set_ergebnis(0, (rq.evaluate_zeile(1)[0]))
    rq.set_ergebnis(1, (rq.evaluate_zeile(2)[0]))
    rq.set_ergebnis(2, (rq.evaluate_zeile(3)[0]))
    rq.set_ergebnis(3, (rq.evaluate_spalte(1)[0]))
    rq.set_ergebnis(4, (rq.evaluate_spalte(2)[0]))
    rq.set_ergebnis(5, (rq.evaluate_spalte(3)[0]))

    rq.ausgabe()

    # Beispielverwendung der Auswertung
    expression = "3+7/2"
    result,fRI,pI,aP = rq.evaluate_expression(expression)
    print(expression,"=",result,pI)
    expression = "5÷2*4"
    result,fRI,pI,aP = rq.evaluate_expression(expression)
    print(expression,"=",result,pI)
    

