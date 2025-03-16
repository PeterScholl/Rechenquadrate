'''
Diese python-Datei erzeugt ein PDF-Dokument mit vier
Rechenquadraten. Die Datei wird in den Ordner Rechenquadrate
geschrieben und dort in Dateien mit aufsteigender Nummer

Autor: Peter Scholl (scholl@unterrichtsportal.org)
Datum: 15.03.25
'''

import os
import pdftk
import GPT_Rechenquadrat
import rqStatistiken as rqs

def rechenquadratInsPDF(pdf_canvas, rechenzeichen, ergebnisse, x, y, width, height):
    """
    erzeugt ein Rechenquadrat in einem PDF an der angegeben Position
    
    :param pdf_canvas: Das Canvas in das das Rechenquadrat soll
    :param rechenzeichen: String mit den Rechenzeichen - die ersten 6 sind die 3 Zeilen, die Zweiten 6 sind die beiden Spalten
    :param ergebnisse: eine Liste mit den sechs Ergebnissen: 3 zeilen, 3 spalten
    :param x: xPosition im PDF
    :param y: yPosition im PDF
    :param width: Breite des Rechenquadrats
    :param height: Höhe des Rechenquadrats
    """
    if len(rechenzeichen) != 12:
        raise ValueError("rechenzeichen has not the correct length of 12")
    if len(ergebnisse) != 6:
        raise ValueError("ergebnisse has not the correct length of 6")
    square_length = min (width,height)
    offset_x = (width-square_length)/2
    offset_y = (height-square_length)/2
    little_square = square_length//7
    fs = int(little_square*0.8) #Font-Size
    lg = 0.9 #Value for light_gray
    dg = 0.6 #Value for dark_gray
    #For debugging purposes: show borderline (Rahmen ausdrucken)
    #pdf_canvas.rect(x, y, width, height, stroke=1)
    for zeile in range(3):
        for spalte in range(3): #Die ersten drei Paare aus Ziffenfeld und Rechenzeichen bzw. =
            pdftk.createCenteredTextRect(pdf_canvas,x+offset_x+spalte*2*little_square,y+offset_y+(6-zeile*2)*little_square,
                                                little_square,little_square,"",
                                                font_name="Helvetica",font_size=fs,
                                                background_color=None)
            pdftk.createCenteredTextRect(pdf_canvas,x+offset_x+(2*spalte+1)*little_square,y+offset_y+(6-zeile*2)*little_square,
                                                little_square,little_square,rechenzeichen[zeile*2+spalte] if spalte<2 else "=",
                                                font_name="VeraSansMonoBold",font_size=fs,
                                                background_color=pdftk.colors.Color(lg,lg,lg))
        #Ergebnis der Zeile
        pdftk.createCenteredTextRect(pdf_canvas,x+offset_x+6*little_square,y+offset_y+(6-zeile*2)*little_square,
                                                little_square,little_square,str(ergebnisse[zeile]),
                                                font_name="VeraSansMonoBold",font_size=fs,
                                                background_color=pdftk.colors.Color(1,1,1))
        #Zeilenteil ohne Wertefelder
        for spalte in range(3): #Die zweiten drei Paare aus Rechenzeichen und grauem Feld
            pdftk.createCenteredTextRect(pdf_canvas,x+offset_x+2*spalte*little_square,y+offset_y+(5-zeile*2)*little_square,
                                                little_square,little_square,rechenzeichen[6+zeile*3+spalte] if zeile<2 else "=",
                                                font_name="VeraSansMonoBold",font_size=fs,
                                                background_color=pdftk.colors.Color(lg,lg,lg))
            pdftk.createCenteredTextRect(pdf_canvas,x+offset_x+(spalte*2+1)*little_square,y+offset_y+(5-zeile*2)*little_square,
                                                little_square,little_square,"",
                                                font_name="Helvetica",font_size=fs,
                                                background_color=pdftk.colors.Color(dg,dg,dg))
        #Schwarzes Feld am Ende
        pdftk.createCenteredTextRect(pdf_canvas,x+offset_x+6*little_square,y+offset_y+(5-zeile*2)*little_square,
                                                little_square,little_square,str(ergebnisse[zeile]),
                                                font_name="VeraSansMonoBold",font_size=fs,
                                                background_color=pdftk.colors.Color(0,0,0))
    #Zeile mit dne letzten Ergebnissen
    for spalte in range(3): #Die letzten drei Paare aus Ergebnis und schwarzem Feld
        pdftk.createCenteredTextRect(pdf_canvas,x+offset_x+2*spalte*little_square,y+offset_y+0*little_square,
                                            little_square,little_square,str(ergebnisse[3+spalte]),
                                            font_name="VeraSansMonoBold",font_size=fs,
                                            background_color=None )
        pdftk.createCenteredTextRect(pdf_canvas,x+offset_x+(spalte*2+1)*little_square,y+offset_y+0*little_square,
                                            little_square,little_square,"",
                                            font_name="Helvetica",font_size=fs,
                                            background_color=pdftk.colors.Color(0,0,0))
    #Schwarzes Feld am Ende
    pdftk.createCenteredTextRect(pdf_canvas,x+offset_x+6*little_square,y+offset_y+0*little_square,
                                            little_square,little_square,str(ergebnisse[zeile]),
                                            font_name="VeraSansMonoBold",font_size=fs,
                                            background_color=pdftk.colors.Color(0,0,0))
    
    
def einRechenquadratPDF(dateiname,rq):
    #Parameter prüfen
    if not (isinstance(dateiname,str)): #and isinstance(rq,GPT_Rechenquadrat.Rechenquadrat)):
        raise Exception("Wrong parameter types: string,Rechenquadrat: ",isinstance(dateiname,str) , isinstance(rq,GPT_Rechenquadrat.Rechenquadrat))
    
    infotext=("Es werden alle Zahlen von 1 bis 9 so eingetragen, dass die Rechnung schlüssig wird. " 
            "Keine Zahl darf zweimal vorkommen. Es gilt nicht die Regel \"Punkt- vor Strichrechnung\", " 
            "sondern es wird von oben nach unten bzw. von links nach rechts gerechnet.")

    width_a4,height_a4 = pdftk.A4
    filename = dateiname if dateiname[-4::]==".pdf" else dateiname+".pdf"
    #zunächst prüfen ob die Datei existiert
    if os.path.exists(filename):
        #Raise exception
        raise Exception("File name already exists");

    # PDF-Datei erstellen
    c = pdftk.canvas.Canvas(filename, pagesize=pdftk.A4)
    c.setTitle("Rechenquadrat "+dateiname)
    c.setAuthor("Peter Scholl")
    rechenquadratInsPDF(c,rq.get_rechenzeichen(),rq.ergebnisse,45,30+390,230,420)
    pdftk.write_text_in_rectangle(c,infotext,45,110+390,230,font_size=10,font="Caladea-Regular")
    pdftk.write_text_in_rectangle(c,"Das Spiel mit den Zahlen",45,360+390,230,font_size=10,font="Caladea-Regular")
    pdftk.write_text_in_rectangle(c,"Rechenquadrat",45,380+390,230,font_size=20,font="Caladea-Bold")

    pdftk.write_text_in_rectangle(c,"Rechenquadrat "+dateiname+" - Erstellt von peter.scholl@aeg-online.de",330,30,200,font_size=8,font="Helvetica")
    # Speichern Sie die PDF-Datei
    c.save()
    

if __name__ == "__main__":
    #Things to do if not imported
    print("Test")
    pass

    infotext=("Es werden alle Zahlen von 1 bis 9 so eingetragen, dass die Rechnung schlüssig wird. " 
            "Keine Zahl darf zweimal vorkommen. Es gilt nicht die Regel \"Punkt- vor Strichrechnung\", " 
            "sondern es wird von oben nach unten bzw. von links nach rechts gerechnet.")

    width_a4,height_a4 = pdftk.A4

    #Existiert das Verzeichnis für die Rechenquadrate schon - sonst erstellen
    directory_path = "Rechenquadrate"  
    if not os.path.exists(directory_path):
        # Verzeichnis existiert nicht, daher erstellen wir es
        os.makedirs(directory_path)
        print("Verzeichnis wurde erstellt.")
        
    #Dateinamen bestimmen
    nr = 1
    filename = directory_path+"/Rechenquadrat_"+str(nr)+".pdf"
    while os.path.exists(filename):
        nr+=1
        filename = directory_path+"/Rechenquadrat_"+str(nr)+".pdf"

    # PDF-Datei erstellen
    #zunächst prüfen ob die Datei existiert
    
    
    c = pdftk.canvas.Canvas(filename, pagesize=pdftk.A4)
    c.setTitle("Rechenquadrat "+str(nr))
    c.setAuthor("Peter Scholl")

    # Aufruf der Methode, um ein zentriertes Text-Rechteck zu erstellen
    #createCenteredTextRect(c, 100, 500, 300, 100, "Zentrierter Text", background_color=colors.lightgrey, border_width=2)
    rq = GPT_Rechenquadrat.Rechenquadrat()
    for i in range(4):
        #rq.setzeZufaelligeGueltigeRechenzeichen()
        #rq.bestimmeEinenZufaelligenEindeutigenZifferneintrag()
        rq = rqs.generiereEinfachesRQ()
        rechenquadratInsPDF(c,rq.get_rechenzeichen(),rq.ergebnisse,45+255*(i%2),30+390*(i//2),230,420)
        pdftk.write_text_in_rectangle(c,infotext,45+255*(i%2),110+390*(i//2),230,font_size=10,font="Caladea-Regular")
        pdftk.write_text_in_rectangle(c,"Das Spiel mit den Zahlen",45+255*(i%2),360+390*(i//2),230,font_size=10,font="Caladea-Regular")
        pdftk.write_text_in_rectangle(c,"Rechenquadrat",45+255*(i%2),380+390*(i//2),230,font_size=20,font="Caladea-Bold")
        #rechenquadratInsPDF(c,"+++++-++++++",[22,8,1,11,16,18],300,420,230,420)
        #rechenquadratInsPDF(c,"+++++-++++++",[22,8,1,11,16,18],45,0,230,420)
        #rechenquadratInsPDF(c,"+++++-++++++",[22,8,1,11,16,18],300,0,230,420)


    pdftk.write_text_in_rectangle(c,"Rechenquadrate Nr."+str(nr)+" - Erstellt von peter.scholl@aeg-online.de",330,30,200,font_size=8,font="Helvetica")
    # Speichern Sie die PDF-Datei
    c.save()
