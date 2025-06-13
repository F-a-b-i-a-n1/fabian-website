import os
import json
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
from fractions import Fraction

# === EXIF auslesen ===
def get_exif_daten(bildpfad):
    try:
        bild = Image.open(bildpfad)
        exif = bild._getexif()
        if not exif:
            return None
        exif_daten = {TAGS.get(tag): wert for tag, wert in exif.items() if tag in TAGS}
        return exif_daten
    except Exception as e:
        print(f"Fehler bei {bildpfad}: {e}")
        return None

def parse_exif(exif):
    if not exif:
        return None, None, None

    def to_float(value):
        if isinstance(value, tuple) and len(value) == 2 and value[1] != 0:
            return value[0] / value[1]
        return float(value)

    brennweite = to_float(exif.get("FocalLength")) if exif.get("FocalLength") else None
    blende = to_float(exif.get("FNumber")) if exif.get("FNumber") else None
    belichtungszeit = exif.get("ExposureTime")

    return brennweite, blende, belichtungszeit

def lade_bildbeschreibungen(pfad):
    if os.path.exists(pfad):
        with open(pfad, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def generiere_slides(ordnerpfad, beschreibungen, fotos_root):
    slides = []
    for dateiname in sorted(os.listdir(ordnerpfad)):
        if not dateiname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        pfad = os.path.join(ordnerpfad, dateiname)
        exif = get_exif_daten(pfad)
        brennweite, blende, belichtung = parse_exif(exif)

        info = beschreibungen.get(dateiname, "")
        if isinstance(info, dict):
            alt_text = info.get("alt", "")
            beschreibung = info.get("description", "")
        else:
            alt_text = ""
            beschreibung = info

        brennweite_anzeige = int(round(brennweite)) if brennweite else None
        blende_anzeige = round(blende, 1) if blende else None

        belichtung_bruch = ""
        if belichtung:
            try:
                belichtung_bruch = str(Fraction(belichtung).limit_denominator())
            except Exception:
                belichtung_bruch = str(belichtung)

        description_text = ""
        if beschreibung:
            description_text = beschreibung
            if brennweite_anzeige and blende_anzeige and belichtung_bruch:
                description_text += f"<br>Brennweite: {brennweite_anzeige}mm<br>f: {blende_anzeige}<br>Belichtungszeit: {belichtung_bruch}s"
        else:
            if brennweite_anzeige and blende_anzeige and belichtung_bruch:
                description_text = f"Brennweite: {brennweite_anzeige}mm<br>f: {blende_anzeige}<br>Belichtungszeit: {belichtung_bruch}s"

        rel_path = os.path.relpath(pfad, fotos_root).replace("\\", "/")
        src = f"Fotos/{rel_path}"

        slide = {
            "src": src,
            "alt": alt_text,
            "description": description_text
        }
        slides.append(slide)

    return slides

# === Hauptlauf ===
def main():
    skriptverzeichnis = os.path.dirname(os.path.abspath(__file__))
    fotos_root = os.path.join(skriptverzeichnis, "Fotos")

    if not os.path.isdir(fotos_root):
        print(f"Ordner 'Fotos' nicht gefunden unter {fotos_root}")
        return

    slideshow_daten = {}

    for eintrag in os.listdir(fotos_root):
        unterordner = os.path.join(fotos_root, eintrag)
        if not os.path.isdir(unterordner):
            continue

        beschreibungs_datei = os.path.join(unterordner, f"bildbeschreibungen_{eintrag}.json")
        beschreibungen = lade_bildbeschreibungen(beschreibungs_datei)

        slides = generiere_slides(unterordner, beschreibungen, fotos_root)
        if slides:
            slideshow_daten[eintrag] = slides
            print(f"Verarbeitet: {eintrag} ({len(slides)} Bilder)")
        else:
            print(f"Keine Bilder in {eintrag}")

    output_datei = os.path.join(fotos_root, "output.json")
    with open(output_datei, "w", encoding="utf-8") as f:
        json.dump(slideshow_daten, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Alle Slideshows gespeichert in: {output_datei}")

if __name__ == "__main__":
    main()