import platform
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def write_text_in_rectangle(pdf_canvas, text, x, y, width, font_size=12, font="Helvetica"):
    """
    Schreibt mehrzeiligen Text in einen rechteckigen Bereich im PDF-Dokument.
    Der Text wird an Leerzeichen aufgeteilt, um in die vorgegebene Breite zu passen.

    :param pdf_canvas: Das PDF-Canvas-Objekt.
    :param text: Der Text, der geschrieben werden soll.
    :param x: Die x-Koordinate der oberen linken Ecke des Textbereichs.
    :param y: Die y-Koordinate der oberen linken Ecke des Textbereichs.
    :param width: Die Breite des Textbereichs.
    :param font_size: Die Schriftgröße (Standard: 12).
    :param font: Die Schriftart (Standard: Helvetica)
    """
    pdf_canvas.setFont(font, font_size)
    pdf_canvas.setFillColor(colors.black)

    lines = []
    current_line = ""
    words = text.split()
    for word in words:
        test_line = current_line + ("" if len(current_line) == 0 else " ") + word
        text_width = pdf_canvas.stringWidth(test_line, font, font_size)
        if text_width <= width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    for line in lines:
        pdf_canvas.drawString(x, y, line)
        y -= font_size * 1.2  # Zeilenabstand anpassen


def createCenteredTextRect(pdf_canvas, x, y, width, height, text, font_name="Helvetica", font_size=12, text_color=colors.black, background_color=None, border_width=1):
    # Rechteck zeichnen
    if background_color:
        pdf_canvas.setFillColor(background_color)
        pdf_canvas.rect(x, y, width, height, fill=True, stroke=True)
    else:
        pdf_canvas.rect(x, y, width, height, stroke=border_width)

    # Text hinzufügen
    pdf_canvas.setFont(font_name, font_size)
    text_width = pdf_canvas.stringWidth(text, font_name, font_size)
    while text_width>0.9*width and font_size > 8:
        font_size-=1
        pdf_canvas.setFont(font_name, font_size)
        text_width = pdf_canvas.stringWidth(text, font_name, font_size)
    
    #print("Text_Width",text_width)
    text_x = x + (width - text_width) / 2
    text_y = y + (height - 0.7*font_size) / 2
    pdf_canvas.setFillColor(text_color)
    pdf_canvas.drawString(text_x, text_y, text)


#Zeichensatz registrieren
# Betriebssystem erkennen
if platform.system() == "Windows":
    font_path_mono = r"C:\Windows\Fonts\Courier New.ttf"  # Alternativ Arial oder Consolas
    font_path_mono_bold = r"C:\Windows\Fonts\Courier New Bold.ttf"
else:  # Linux/macOS
    font_path_mono = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
    font_path_mono_bold = "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"

# Falls die Schriftart nicht existiert, Abbruch vermeiden
if os.path.exists(font_path_mono):
    pdfmetrics.registerFont(TTFont("FreeMono", font_path_mono))
if os.path.exists(font_path_mono_bold):
    pdfmetrics.registerFont(TTFont("FreeMonoBold", font_path_mono_bold))

font_path = "./fonts/MonospaceTypewriter.ttf"
pdfmetrics.registerFont(TTFont("MonospaceTypewriter", font_path))
#font_path = "./fonts/VeraMoBd.ttf"
font_path = "C:\Windows\Fonts\consolab.ttf"
pdfmetrics.registerFont(TTFont("VeraSansMonoBold", font_path))
font_path = "./fonts/Caladea-Regular.ttf"
pdfmetrics.registerFont(TTFont("Caladea-Regular", font_path))
font_path = "./fonts/Caladea-Bold.ttf"
pdfmetrics.registerFont(TTFont("Caladea-Bold", font_path))

if __name__ == "__main__":
    from reportlab.pdfbase.pdfmetrics import getRegisteredFontNames
    print("Registerd Fonts:",getRegisteredFontNames())
    
    # PDF-Datei erstellen
    c = canvas.Canvas("zentriertes_text_rechteck.pdf", pagesize=A4)

    # Aufruf der Methode, um ein zentriertes Text-Rechteck zu erstellen
    createCenteredTextRect(c, 100, 500, 300, 100, "Zentrierter Text", background_color=colors.lightgrey, border_width=2)

    text = "Dies ist ein langer Text, der in einen vorgegebenen rechteckigen Bereich geschrieben wird. Er wird automatisch in mehrere Zeilen aufgeteilt, wenn er zu breit ist."

    # Festlegen des Textbereichs (x, y, Breite)
    x = 100
    y = 400
    width = 300

    write_text_in_rectangle(c, text, x, y, width)

# Speichern Sie die PDF-Datei
    c.save()
