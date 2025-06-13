######## 1. Benötigte Pakete einbinden ########
import os
from pathlib import Path
import exiftool
import re
from collections import defaultdict # Für case 1.7



######## 2. Parameter eingeben ########
pfad = r"..."



ger = "iPhone16"
#Gerät, z. B.
#- iPhone16
#- iPhone13
#- iPhone10
#- iPhone6
#- iPhone4S
#- SonyA6000

#counter = 2459                                                                     # Wird nur benötigt, falls Dateiname in der Form "2015-11-27 21.25.28.JPG" ist


case = "1.8"



######## 3. Programmablauf ########
os.chdir(pfad)                                                                      # "change direction" wechselt in den angegeben Pfad
a = sorted(os.listdir())                                                            # Erzeugt aus den Dateien im Ordner "Test" eine sortierte Liste a

dat = []
tim = []
num = []
end = []

if ger == "iPhone6" or ger == "iPhone10" or ger == "iPhone13" or ger == "iPhone16":
    dat_extract_pattern = "[0-9]{4}\\-[0-9]{2}\\-[0-9]{2}"
    tim_extract_pattern = "[0-9]{2}\\.[0-9]{2}\\.[0-9]{2}"
    num_extract_pattern = "[0-9]{3,4}[.]"                                           #Man muss den Punkt [.] hinzufügen, sonst würde er auch die Jahreszahlen (z. B. 2015) als Nummerierung erkennen
    numZus_extract_pattern = "[0-9]{3,4}[E.]"
    zus_extract_pattern = "[-][0-9]{1}[.]"                                          #Man muss den Punkt [.] hinzufügen, sonst würde er auch die Monats- oder Tageszahl (z. B. -11) als Zusatz erkennen erkennen
    pattern = re.compile(r"^(?P<datum>\d{4}-\d{2}-\d{2})_(?P<geraet>iPhone\d+)_E(?P<num>\d{4})(?P<rest>.*)$", re.IGNORECASE) # Von ChatGPT für case 1.6

    with exiftool.ExifTool() as et: # Es ist schneller, wenn man exiftool nur 1x öffnet, also vor der for-Schleife :) Anstatt vor: datum_mod = et.get_tag("FileModifyDate", file)
        for k in range(0,len(a)):
            #######################################################################################################
            ### Fall 1: Falls die Nummerierung, die bereits im Dateinamen steht, auch BEIBEHALTEN werden soll! ###
            #######################################################################################################
            if case == '1.1' or case == '1.2' or case == '1.3' or case == '1.4' or case == '1.5' or case == '1.6' or case == '1.7' or case == '1.8':
            
                ### Fall 1.1: "IMG_7135.JPG" -> "2021-05-09_iPhone13_7135.jpg" (Zahlen direkt (ohne RegEx (re)) auslesen. Schneller mit regEx (re))
                if case == '1.1':
                    try:
                        pre = "IMG_"                                                      # Anpassen!!!
                        g = a[k].split(".")[0].split(pre, 4)[1]                           # Gibt die Zahl im Dateinamen als String aus; split(".")[0] wird vor split("IMG")[1] ausgeführt
                        end = a[k].split(".")[1]
                        file = pfad + pre + g + "." + end
                        
                        datum_mod = et.get_tag("FileModifyDate", file)                  #Er gibt hier also den Wert der Eigenschaft "FileModifyDate" für das Bild mit dem Namen file aus.
                        datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")          #Ohne Uhrzeit
                        
                        neu = pfad + datum_mod_2 + '_' + ger + '_' + g + "." + end
                        
                        print(f"{file} -> {neu}")
                        os.rename(file, neu)
                    except Exception as e:
                        print(f"Mistake1: {e}")
                
                
                ### Für die Fälle 1.2 - 1.5 benötigt:
                dat = re.findall(dat_extract_pattern, a[k])                                 #Das ist eine List & kein string!!!
                #tim = re.findall(tim_extract_pattern, a[k])
                num = re.findall(num_extract_pattern, a[k])
                numZus = re.findall(numZus_extract_pattern, a[k])
                #end = a[k].rsplit(".",1)[-1]                                                #string.rsplit(separator, maxsplit)
                
                
                ### Fall 1.2: "IMG_7135.JPG" -> "2021-05-09_iPhone13_7135.jpg" (Zahlen mit RegEx (re) auslesen. Langsamer als ohne RegEx (re))
                if case == '1.2':
                    try:
                        if len(dat) == 0 and len(num) != 0:
                            num_MitPunkt = num[0]                                               # Wandelt List zu string um
                            num_s = num_MitPunkt.replace('.', '')
                            file = pfad + "IMG_" + num_s + "." + end     # Anpassen!!!
                            print(file)
                            datum_mod = et.get_tag("FileModifyDate", file)                  #Er gibt hier also den Wert der Eigenschaft "FileModifyDate" für das Bild mit dem Namen file aus.
                            datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")          #Ohne Uhrzeit
                            os.rename(file, pfad + datum_mod_2 + '_' + ger + '_' + "%04d" % int(num_s) + "." + end)
                    except:
                        print("Mistake2")
                
                
                ### Fall 1.3: "IMG_E7135.JPG" -> "2021-05-09_iPhone13_7135E.jpg" (Zahlen direkt (ohne RegEx (re)) auslesen. Schneller mit regEx (re))
                if case == '1.3':
                    try:
                        if len(dat) == 0 and len(num) != 0:
                            g = a[k].split(".")[0].split("IMG_E", 4)[1]                           # Gibt die Zahl im Dateinamen als String aus; split(".")[0] wird vor split("IMG")[1] ausgeführt
                            en = a[k].split(".")[1]
                            num_MitPunkt = num[0]                                               # Wandelt List zu string um
                            num_s = num_MitPunkt.replace('.', '')
                            file = pfad + "IMG_E" + num_s + "." + end     # Anpassen!!!
                            print(file)
                            datum_mod = et.get_tag("FileModifyDate", file)                  #Er gibt hier also den Wert der Eigenschaft "FileModifyDate" für das Bild mit dem Namen file aus.
                            datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")          #Ohne Uhrzeit
                            os.rename(file, pfad + datum_mod_2 + '_' + ger + '_' + "%04d" % int(num_s) + "E." + end)            #Ich mag das "E" lieber nach der Zahl, da so die Sortierung übersichtlicher wird (Man hat die zusammengehörenden Bilder dann auch wirklich hintereinander).
                    except:
                        print("Mistake3")
                
                
                ### Fall 1.4: "2021-05-09_iPhoneX_0086.jpg" -> "2021-05-09_iPhone10_0086.jpg"
                if case == '1.4':
                    try:
                        if len(dat) != 0 and len(num) != 0:
                            dat_s = dat[0]
                            num_MitPunkt = num[0]
                            num_s = num_MitPunkt.replace('.', '')
                            #file = pfad + "IMG_" + num_s + "." + end
                            file = pfad + dat_s + "_iPhoneX_" + num_s + "." + end
                            os.rename(file, pfad + dat_s + '_' + ger + '_' + "%04d" % int(num_s) + "." + end)
                    except:
                        print("Mistake4")
                
                
                # Fall 1.5: Bild aus LR exportiert & davor bereits umbenannt: "2015-08-16_iPhone6_0002.jpg" -> "2015-08-16_iPhone6_0002_LR-2023-06-24.jpg"
                if case == '1.5':
                    try:
                        if len(dat) != 0 and (len(num) != 0 or len(numZus) != 0) and not "LR" in a[k]:      #Ohne die "LR"-Abfrage würden bei Bildern, die bei einem vorherigen Durchlauf bereits umbenannt wurden, nochmal "LR..." drangehängt werden
                            pre = a[k].split(".")[0]                                                  # Gibt die Zahl im Dateinamen als String aus; split(".")[0] wird vor split("IMG")[1] ausgeführt
                            en = a[k].split(".")[1]                                                   # Dateiendung (sofern Dateiname sonst keinen Punkt enthält); a[k] ist der Dateiname der k-ten Datei in der Liste a
                            file = pfad + pre + "." + en
                            datum_mod = et.get_tag("FileModifyDate", file)                        #Änderungsdatum (Wann Bild aus LR exportiert wurde)
                            datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")                #Ohne Uhrzeit
                            os.rename(file, pfad + pre + "_LR-" + datum_mod_2 + "." + en)
                    except:
                        print("Mistake5")
                        
                        
                # Fall 1.6: "2021-05-09_iPhone13_E7135.jpg" -> "2021-05-09_iPhone13_7135E.jpg"
                if case == '1.6':
                    file_name = a[k]
                    full_path = os.path.join(pfad, file_name)
                
                    if os.path.isfile(full_path):
                        match = pattern.match(file_name)
                        if match:
                            new_name = f"{match.group('datum')}_{match.group('geraet')}_{match.group('num')}E{match.group('rest')}"
                            new_path = os.path.join(pfad, new_name)

                            print(f"{file_name} → {new_name}")
                            os.rename(full_path, new_path)


                # Fall 1.7: Erweiterung von Fall 1.6
                # 2025-04-03_iPhone16_E0021.JPG             -> 2025-04-03_iPhone16_0021E.JPG
                # 2025-04-03_iPhone16_E0022.JPG             -> 2025-04-03_iPhone16_0022E1.JPG
                # 2025-04-03_iPhone16_E0022 - Kopie.JPG     -> 2025-04-03_iPhone16_0022E2.JPG                            
                if case == '1.7':
                    counts = defaultdict(int)
                    for dateiname in a:
                        match = pattern.match(dateiname)
                        if match:
                            nummer = match.group('num')
                            counts[nummer] += 1

                    counter = defaultdict(int)  # zählt umbenannte Dateien pro Nummer

                    for dateiname in a:
                        if os.path.isfile(os.path.join(pfad, dateiname)):
                            match = pattern.match(dateiname)
                            if match:
                                datum = match.group('datum')
                                geraet = match.group('geraet')
                                nummer = match.group('num')
                                rest = match.group('rest')
                                endung = os.path.splitext(dateiname)[1]

                                alt = os.path.join(pfad, dateiname)

                                if counts[nummer] == 1:
                                    neuer_name = f"{datum}_{geraet}_{nummer}E{endung}"
                                else:
                                    counter[nummer] += 1
                                    neuer_name = f"{datum}_{geraet}_{nummer}E{counter[nummer]}{endung}"

                                neu = os.path.join(pfad, neuer_name)

                                print(f"{dateiname} -> {os.path.basename(neu)}")
                                os.rename(alt, neu)
        
        
                # Fall 1.8: Für Videos
                # CRRU1966.MP4             -> 2025-04-03_iPhone16_CRRU1966.MP4
                if case == '1.8':   
                    umbenannt_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}_iPhone\d+_.*\.(mp4|mov)$", re.IGNORECASE) # Regex für bereits umbenannte Dateien, z. B. 2025-06-03_iPhone16_9980.mov
                    for dateiname in a:
                        if not dateiname.lower().endswith((".mp4", ".mov")):
                            continue  # Nur Videos

                        if umbenannt_pattern.match(dateiname):
                            continue  # Datei ist schon korrekt benannt

                        file_path = os.path.join(pfad, dateiname)
                        datum_mod = et.get_tag("FileModifyDate", file_path)

                        if datum_mod:
                            datum = datum_mod.split(" ")[0].replace(":", "-")
                            name_ohne_endung, endung = os.path.splitext(dateiname)
                            endung = endung.upper()

                            if name_ohne_endung.upper().startswith("IMG_"):
                                nummer = name_ohne_endung.split("_")[1]
                                neuer_name = f"{datum}_{ger}_{nummer}{endung}"
                            else:
                                neuer_name = f"{datum}_{ger}_{name_ohne_endung}{endung}"

                            neuer_path = os.path.join(pfad, neuer_name)
                            print(f"{dateiname} → {os.path.basename(neuer_path)}")
                            os.rename(file_path, neuer_path)

                        else:
                            print(f"Keine Metadaten für: {dateiname}")
        
        
        
        
        
        ###########################################################################################################################################################################################
        ### Fall 2: Falls die Nummerierung, die bereits im Dateinamen steht, NICHT BEIBEHALTEN werden soll! ######################################################################################
        ### Achtung: Verwende dieses Programm NICHT, wenn die Nummerierung, die bereits im Dateinamen steht, auch beibehalten werden soll! ########################################################
        ### Mit diesem Programm erfolgt die Nummerierung der Reihe nach (Wenn also die Bilder bereits mit z. B. 0003, 0015, ... nummeriert sind, so werden sie zu 0001, 0002, ... umnummeriert! ###
        ### Verlasse im Explorer den Ordner während das Python-Programm läuft. Sonst hängt sich Laptop auf!########################################################################################
        ###########################################################################################################################################################################################
        if case == '2.1' or case == '2.2' or case == '2.3' or case == '2.4' or case == '2.5':
            counter = counter + 1       #Diese Inkrementierung muss hier eingefügt werden, da es am Ende des Programms nicht immer durchgeführt werden würde (z. B. wenn except-Schleife durchlaufen wird
            
            dat = re.findall(dat_extract_pattern, a[k])     #Das ist eine List & kein string!!!
            tim = re.findall(tim_extract_pattern, a[k])
            zus = re.findall(zus_extract_pattern, a[k])
            end = a[k].rsplit(".",1)[-1]
            
            #num_extract_pattern = "[0-9]{3,4}[.]"           #Man muss den Punkt [.] hinzufügen, sonst würde er auch die Jahreszahlen (z. B. 2015) als Nummerierung erkennen
            num_extract_pattern = "[_][0-9]{3,4}"
            num = re.findall(num_extract_pattern, a[k])
            
            
            ### Entferne HDR im Dateinamen (Muster-Dateiname "2015-08-17 20.21.28 HDR.jpg")
            if " HDR" in a[k]:                      
                dat_s = dat[0]
                tim_s = tim[0]
                file = pfad + dat_s + " " + tim_s + " HDR." + end
                os.rename(file, pfad + dat_s + '_' + ger + '_' + "%04d" % counter + "." + end)
            
            
            ### Fall 2.1: Muster-Dateiname "2015-08-16_iPhone6_0002.jpg"
            if case == '2.1':
                try:
                    if len(dat) != 0 and len(num) != 0 and len(zus) == 0:     
                        dat_s = dat[0]
                        num_s_MitPunkt = num[0]
                        #num_s = num_s_MitPunkt.replace('.', '')
                        num_s = num_s_MitPunkt.replace('_', '')
                        file = pfad + dat_s + "_" + ger + "_" + num_s + "." + end
                        os.rename(file, pfad + dat_s + '_' + ger + '_' + "%04d" % counter + "." + end)
                except:
                    print("Mistake2")
                    counter = counter + 1
                    os.rename(file, pfad + dat_s + '_' + ger + '_' + "%04d" % (counter+4000) + "." + end)       #TRICK: +4000 da ansonsten manchmal Bilder nicht umbenannt werden könnten, falls Nummerierung genau mit der Nummerierung des nächsten Bildes übereinstimmen würde.
                
            
            ### Fall 2.2: Muster-Dateiname "2015-08-16_iPhone6_0002-2.jpg"
            if case == '2.2':
                try:
                    if len(dat) != 0 and len(num) != 0 and len(zus) != 0:
                        print("Hey")
                        dat_s = dat[0]
                        num_s_MitPunkt = num[0]
                        #num_s = num_s_MitPunkt.replace('.', '')
                        num_s = num_s_MitPunkt.replace('_', '')
                        zus_s = zus[0]
                        zus_i = zus_s.replace('-', '').replace('.', '')
                        print(zus_i)
                        file = pfad + dat_s + "_" + ger + "_" + num_s + zus_s + end
                        os.rename(file, pfad + dat_s + '_' + ger + '_' + "%04d" % counter(-zus_i) + "-" + zus_s + "." + end)
                except:
                    print("Mistake2")
                    counter = counter + 1
                    os.rename(file, pfad + dat_s + '_' + ger + '_' + "%04d" % (counter+4000) + "." + end)       #TRICK: +4000 da ansonsten manchmal Bilder nicht umbenannt werden könnten, falls Nummerierung genau mit der Nummerierung des nächsten Bildes übereinstimmen würde.
            
            
            ### Fall 2.3: Muster-Dateiname "2015-08-17 20.21.28.jpg"
            if case == '2.3':
                try:
                    if len(dat) != 0 and len(tim) != 0 and len(zus) == 0 and " HDR" not in a[k]:
                        dat_s = dat[0]
                        tim_s = tim[0]
                        file = pfad + dat_s + " " + tim_s + "." + end
                        os.rename(file, pfad + dat_s + '_' + ger + '_' + "%04d" % counter + "." + end)
                except:
                    # try:
                        # for i in range(1,3):
                            # file = pfad + dat_s + " " + tim_s + "-" + str(i) + "." + end
                            # os.rename(file, pfad + dat_s + '_' + ger + '_' + "%04d" % counter + "." + end)
                    # except:
                    print("Mistake3")
                    counter = counter + 1
                    os.rename(file, pfad + dat_s + '_' + ger + '_' + "%04d" % (counter+4000) + "." + end)
                

            ### Fall 2.4: Muster-Dateiname "2015-08-17 20.21.28-2.jpg" (Falls mehrere Bilder in derselben Sekunde gemacht wurden)
            if case == '2.4':
                try:
                    if len(dat) != 0 and len(tim) != 0 and len(zus) != 0 and " HDR" not in a[k]:
                        dat_s = dat[0]
                        tim_s = tim[0]
                        zus_s = zus[0]
                        file = pfad + dat_s + " " + tim_s + zus_s + end
                        os.rename(file, pfad + dat_s + '_' + ger + '_' + "%04d" % counter + zus_s + end)
                        counter = counter - 1
                except:
                    # try:
                        # for i in range(1,3):
                            # file = pfad + dat_s + " " + tim_s + "-" + str(i) + "." + end
                            # os.rename(file, pfad + dat_s + '_' + ger + '_' + "%04d" % counter + "." + end)
                    # except:
                    print("Mistake4")
                    counter = counter + 1
                
            
            ### Fall 2.5: Muster-Dateiname "080.JPG"
            if case == '2.5':
                if len(dat) == 0:
                    num_MitPunkt = num[0]
                    #num_s = num_MitPunkt.replace('.', '')
                    num_s = num_MitPunkt.replace('_', '')
                    file = pfad + "IMG_" + num_s + "." + end
                    with exiftool.ExifTool() as et:
                        datum_mod = et.get_tag("FileModifyDate", file)                        #Er gibt hier also den Wert der Eigenschaft "FileModifyDate" für das Bild mit dem Namen file aus.
                        datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")                #Ohne Uhrzeit
                    os.rename(file, pfad + datum_mod_2 + '_' + ger + '_' + "%04d" % int(num_s) + "." + end)

            print(file)
            

if ger == "SonyA6000":
    for k in range(0,len(a)):
        try:       #Arbeite hier mit try, da die Zahl zwischen "IMG_" und ".ENDUNG" nicht immer eindeutig bestimmt werden kann & dann diese Befehle einfach übersprungen werden sollen & except ausgeführt werden soll.
            # Fall 1: Normal
            if case == '3.1':
                g = a[k].split(".")[0].split("_DSC", 4)[1]                                   # Gibt die Zahl im Dateinamen als String aus; split(".")[0] wird vor split("IMG")[1] ausgeführt
                en = a[k].split(".")[1]                                                     # Dateiendung (sofern Dateiname sonst keinen Punkt enthält); a[k] ist der Dateiname der k-ten Datei in der Liste a
                file = pfad + "_DSC" + g + "." + en
                with exiftool.ExifTool() as et:
                    datum_mod = et.get_tag("DateTimeOriginal", file)                          #Änderungsdatum
                    datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")                  #Ohne Uhrzeit
                os.rename(file, pfad + datum_mod_2 + '_' + ger + '_' + "%04d" % int(g) + "." + en)
            
            # Fall 2: Bild aus LR exportiert
            if case == '3.2':
                g = a[k].split(".")[0].split("_DSC", 4)[1]                                   # Gibt die Zahl im Dateinamen als String aus; split(".")[0] wird vor split("IMG")[1] ausgeführt
                en = a[k].split(".")[1]                                                     # Dateiendung (sofern Dateiname sonst keinen Punkt enthält); a[k] ist der Dateiname der k-ten Datei in der Liste a
                file = pfad + "_DSC" + g + "." + en
                with exiftool.ExifTool() as et:
                    datum_ori = et.get_tag("DateTimeOriginal", file)                      #Aufnahmedatum
                    datum_mod = et.get_tag("FileModifyDate", file)                        #Änderungsdatum (Wann Bild aus LR exportiert wurde)
                    datum_ori_2 = datum_ori.split(" ")[0].replace(":","-")                #Ohne Uhrzeit
                    datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")                #Ohne Uhrzeit
                os.rename(file, pfad + datum_ori_2 + '_' + ger + '_' + "%04d" % int(g) + "_LR-" + datum_mod_2 + "." + en)
            
            # Fall 3: Bild aus LR exportiert & davor bereits umbenannt (Bsp.: 2015-08-16_iPhone6_0002.jpg -> 2015-08-16_iPhone6_0002_LR-2023-06-24.jpg)
            if case == '3.3':
                g = a[k].split(".")[0]                                   # Gibt die Zahl im Dateinamen als String aus; split(".")[0] wird vor split("IMG")[1] ausgeführt
                en = a[k].split(".")[1]                                                     # Dateiendung (sofern Dateiname sonst keinen Punkt enthält); a[k] ist der Dateiname der k-ten Datei in der Liste a
                file = pfad + g + "." + en
                with exiftool.ExifTool() as et:
                    datum_mod = et.get_tag("FileModifyDate", file)                        #Änderungsdatum (Wann Bild aus LR exportiert wurde)
                    datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")                #Ohne Uhrzeit
                os.rename(file, pfad + g + "_LR-" + datum_mod_2 + "." + en)
            
        except:
            print("Umbenennung nicht möglich, da die Zahl zwischen '_DSC' und '.ENDUNG' nicht eindeutig bestimmt werden kann.")

        #else:       #Mgl. 2
            # pre = a[k].split(".")[0]                                                  #Präfix
            # end = a[k].split(".")[1]                                                  #Dateiendung
            # file = pfad + pre + "." + end
            # with exiftool.ExifTool() as et:
                # datum_mod = et.get_tag("FileModifyDate", file)                        #Er gibt hier also den Wert der Eigenschaft "FileModifyDate" für das Bild mit dem Namen file aus.
                # datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")                #Ohne Uhrzeit
            # os.rename(file, pfad + datum_mod_2 + '_' + ger + '_' + pre + "." + end)


if ger == "iPadAir":
    for k in range(0,len(a)):
        try:       #Arbeite hier mit try, da die Zahl zwischen "IMG_" und ".ENDUNG" nicht immer eindeutig bestimmt werden kann & dann diese Befehle einfach übersprungen werden sollen & except ausgeführt werden soll.
            g = a[k].split(".")[0].split("IMG_")[1]                                     # Gibt die Zahl im Dateinamen als String aus; split(".")[0] wird vor split("IMG")[1] ausgeführt
            en = a[k].split(".")[1]                                                     # Dateiendung (sofern Dateiname sonst keinen Punkt enthält); a[k] ist der Dateiname der k-ten Datei in der Liste a
            file = pfad + "IMG_" + g + "." + en
            with exiftool.ExifTool() as et:
                datum_mod = et.get_tag("FileModifyDate", file)                          #Er gibt hier also den Wert der Eigenschaft "FileModifyDate" für das Bild mit dem Namen file aus.
                datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")                  #Ohne Uhrzeit
            os.rename(file, pfad + datum_mod_2 + '_' + ger + '_' + "%04d" % int(g) + "." + en)
            
        except:
            print("Umbenennung nicht möglich, da die Zahl zwischen 'IMG_' und '.ENDUNG' nicht eindeutig bestimmt werden kann.")

        #else:       #Mgl. 2
            # pre = a[k].split(".")[0]                                                  #Präfix
            # end = a[k].split(".")[1]                                                  #Dateiendung
            # file = pfad + pre + "." + end
            # with exiftool.ExifTool() as et:
                # datum_mod = et.get_tag("FileModifyDate", file)                        #Er gibt hier also den Wert der Eigenschaft "FileModifyDate" für das Bild mit dem Namen file aus.
                # datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")                #Ohne Uhrzeit
            # os.rename(file, pfad + datum_mod_2 + '_' + ger + '_' + pre + "." + end)


if ger == "PanasonicTZ22" or ger == "PanasonicTZ31":
    for k in range(0,len(a)):
        try:       #Arbeite hier mit try, da die Zahl zwischen "IMG_" und ".ENDUNG" nicht immer eindeutig bestimmt werden kann & dann diese Befehle einfach übersprungen werden sollen & except ausgeführt werden soll.
            g = a[k].split(".")[0].split("P")[1]                                        # Gibt die Zahl im Dateinamen als String aus; split(".")[0] wird vor split("IMG")[1] ausgeführt
            en = a[k].split(".")[1]                                                     # Dateiendung (sofern Dateiname sonst keinen Punkt enthält); a[k] ist der Dateiname der k-ten Datei in der Liste a
            file = pfad + "P" + g + "." + en
            
            # Fall 1: Normal
            if case == '4.1':
                with exiftool.ExifTool() as et:
                    datum_mod = et.get_tag("DateTimeOriginal", file)                        #Aufnahmedatum
                    datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")                  #Ohne Uhrzeit
                os.rename(file, pfad + datum_mod_2 + '_' + ger + '_' + "%07d" % int(g) + "." + en)
            
            # Fall 2: Bild aus LR exportiert
            if case == '4.2':
                with exiftool.ExifTool() as et:
                    datum_ori = et.get_tag("DateTimeOriginal", file)                      #Aufnahmedatum
                    datum_mod = et.get_tag("FileModifyDate", file)                        #Änderungsdatum (Wann Bild aus LR exportiert wurde)
                    datum_ori_2 = datum_ori.split(" ")[0].replace(":","-")                #Ohne Uhrzeit
                    datum_mod_2 = datum_mod.split(" ")[0].replace(":","-")                #Ohne Uhrzeit
                os.rename(file, pfad + datum_ori_2 + '_' + ger + '_' + "%04d" % int(g) + "_LR-" + datum_mod_2 + "." + en)
            
        except:
            print("Umbenennung nicht möglich, da die Zahl zwischen 'P' und '.ENDUNG' nicht eindeutig bestimmt werden kann.")
















# Dateiformate:
#- HEIC: Fotos, die (normal) mit der iPhone Kamera gemacht werden (3024 x 4032 px)
#- JPG: Fotos, die (normal) mit der iPhone Kamera gemacht werden
#- PNG: Screenshots (Enthält kein EXIF:Model)
#- WEBP: In Safari über "In Fotos sichern" gespeichert
#- MP4:
#       - Bildschirmaufnahmen
#       - Videos, die ich auf sozialen Medien geteilt habe
#- MOV:
#       - Videoeufnahme
#       - Falls Live-Bild in iPhone aktiviert war
#- XCF: Gimp
#- AAE: Enthält Informationen zu Bearbeitungen innerhalb der App "Apple Fotos" (Falls Bild auf iPhone mit der App "Apple Fotos" bearbeitet wurde)
#- IMG_EXXXX: Beim iPhone: "Editet".
#       - Falls Live-Bild/HDR/Portraitmodus/Schwarz-Weiß/... bei Aufnahme des Bildes aktiviert war ODER
#       - Falls Bild nachträglich in der Fotos-App bearbeitet wurde.
#- BBBBZZZZ.JPG: (2160 x 3840 px)
#       - Bilder, die direkt in der Whatsapp-App aufgenommen und versandt wurden (3840 x 2160 px, 2160 x 3840 px, Format 16:9) bzw. Bilder die per Whatsapp empfangen wurden (Beginn - 2022). ODER
#       - Bilder, die aus Instagram exportiert wurden? (Können auch größere Abmessungen haben. Z. B. 4032 x 5040 px)
#       - Bilder, die aus LR exportiert wurden
#       - Bilder, die aus der "instasize"-App exportiert wurden (1440 x 960 px, 1440 x 1800 px)
#- xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.jpg wobei x=hexadezimales Zeichen
#       - Bilder, die direkt in der Whatsapp-App aufgenommen und versandt wurden bzw. Bilder die per Whatsapp empfangen wurden (Seit 2023 nutzt Whatsapp UUID, statt wie oben BBBBZZZZ.JPG (2023 - ...)
#- PZZZZZZZ.JPG: Bilder, die aus Dropbox exportiert wurden (Abmessung abhängig von der Abmessung, mit der das Foto auf Dropbox geladen wurde (Also meist vom anderen Gerät, mit dem das Foto ursprünglich aufgenommen wurde))

#Notation:
#- Angabe der Abmessungen: Breite x Höhe
#- B: Großbuchstabe, Z: Ziffer
