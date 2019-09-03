import mailService
from time import sleep
import random
import datetime
from os import path

#Grundparameter festelegen
datenbankDatei = "filmdatenbank.txt" #Name für Verwaltung

#Emailvariablen
mailSubject = "E-Mail von Alex Filmdatenbank" #Betreff fuer das versenden
mailUser = "" #Userlogin Mailserver
mailPOPServer = "pop.gmx.net" #Postserver
mailPassword = "" #Passwort Mailserver
mailHelpFile_1 = "helptext1.txt"
mailHelpFile_2 = "helptext2.txt"
mailHelpFile = "helptext.txt"
mailLogFile = "mailingLOGFile.txt" #Liste alle Anfragen
mailingList = "mailingList.txt" #Liste alle Emailadressen als Datensammler

#Pruefen ob Datei vorhanden, wenn nicht, neue Datei anlegen, inkl Rueckmeldung
def fileCheck(file):
    if not path.exists(file):
        print("Hinweis: Datei:", file, "fehlt!")
        datei = open(file, "w")
        print("Datei mit dem Namen", file, "wurde erfolgreich angelegt.\n")
        datei.close()

def genreListeGenerieren():
    datei = open(datenbankDatei, "r")
    listKnownGenres = []
    for nummer, zeile in enumerate(datei):
        obj = zeile.split(";")
        if obj[3] not in listKnownGenres:
            listKnownGenres.append(obj[3])
    listKnownGenres.sort()
    datei.close()
    return listKnownGenres

#Funktionen
def mailAuswertung(subject, helpfile1, helpfile2, helpfile):
    #Werte empfangene Mail aus, dann uebergebe Flag zum entfernen
    if "Bewertung" in subject:
        subjectTemp = subject.split(" ")
        subject = subjectTemp[0]
        subjectTemp = int(subjectTemp[1])
        
    message = ""
    if subject == "Hilfe":
        newList = ""
        listeGenres = genreListeGenerieren()
        for line in listeGenres:
            newList = line + ", " + newList

        file1 = open(helpfile1,"r")
        part1 = file1.read()
        file1.close()
                
        file2 = open(helpfile2, "r")
        part2 = file2.read()
        file2.close()

        file = open(helpfile, "w")
        message = part1 + "<p><u>Aktuelle Genres:</u><br />" + newList + "</p>" + part2
        file.write(message)
        file.close()
        
        return message
    elif subject == "Genrehilfe":
        #Lese alle Genres
        genreListe = genreListeGenerieren()
        string = ""
        for line in genreListe:
            string = string + line + "<br>"
        message = "<b>Liste aller eingetragenen Genres</b><br><br>"+string
        info = "<br><br><br>Für alle Filmfreunde: <a href='https://www.imdb.com/calendar?region=DE&ref_=rlm'>Filmneuerscheinungen</a>"
        message = message + info
        return message
    elif subject == "Besties":
        #Sende alle Filme mit Bewertungen 8 oder besser
        stringliste = list()
        i = 0
        string = ""
        datei = open(datenbankDatei,"r")
        for nummer, zeile in enumerate(datei):
            objekt = zeile.split(";")
            objekt = objekt[4].split("\n")
            if int(objekt[0]) in range(8, 11):
                ausgabe = zeile.split("\n")
                ausgabe = ausgabe[0].split(";")
                stringliste.append(ausgabe[0]+"<br>")
                i += 1
        stringliste.append("<br>")
        stringliste.append("<br>"+str(i)+" von "+ str(nummer) + " Einträgen gesendet.")
        datei.close()
        for line in stringliste:
            string = string + line
        message = "<b>Liste aller Filme bewertet mit 8 oder höher</b><br><br>"+string
        info = "<br><br><br>Für alle Filmfreunde: <a href='https://www.imdb.com/calendar?region=DE&ref_=rlm'>Filmneuerscheinungen auf IMDB</a>"
        message = message + info
        return message
    elif subject == "Bewertung":
        #Sende alle Filme mit Bewertung x
        #subjectTemp enthält Bewertungszahl
        stringliste = list()
        i = 0
        string = ""
        datei = open(datenbankDatei,"r")
        for nummer, zeile in enumerate(datei):
            objekt = zeile.split(";")
            objekt = objekt[4].split("\n")
            if int(objekt[0]) in range(subjectTemp, subjectTemp+1):
                ausgabe = zeile.split("\n")
                ausgabe = ausgabe[0].split(";")
                stringliste.append(ausgabe[0]+"<br>")
                i += 1
        stringliste.append("<br>")
        stringliste.append("<br>"+str(i)+" von "+ str(nummer) + " Einträgen gesendet.")
        datei.close()
        for line in stringliste:
            string = string + line
        message = "<b>Film mit Bewertung " + str(subjectTemp)+"</b><br><br>"+string
        info = "<br><br><br>Für alle Filmfreunde: <a href='https://www.imdb.com/calendar?region=DE&ref_=rlm'>Filmneuerscheinungen auf IMDB</a>"
        message = message + info
        return message
    elif subject == "Zufall":
        #Sendet zufallsfilm
        k = 0
        string = ""
        datei = open(datenbankDatei,"r")
        for i in datei:
            k += 1
        zahl = random.randint(0,k)
        datei.close()
        datei = open(datenbankDatei,"r")
        for nummer, zeile in enumerate(datei):
            if zahl == nummer:
                string = zeile
        string = string.split(";")
        string = string[0]
        datei.close()
        message = "<b>Ihr Zufallsfilm ist:<br><br></b>" + string 
        info = "<br><br><br>Für alle Filmfreunde: <a href='https://www.imdb.com/calendar?region=DE&ref_=rlm'>Filmneuerscheinungen auf IMDB</a>"
        message = message + info
        return message
    elif subject == "Alles":
        #Schickt eine Übersicht aller eingetragenen Filme
        string = ""
        tempstring = list()
        datei = open(datenbankDatei,"r")
        for i, a in enumerate(datei):
            i= i+1
            #Führende Nullen der Optik halber eingeben, bis 999 Einträge passend
            if i < 10:
                i = "00" + str(i)
            elif i < 100:
                i = "0" + str(i)
            line = a.split("\n")
            part = line[0].split(";")
            tempstring.append(str(i) + ": <b>"+part[0] + "</b><ul><u>Erscheinungsjahr:</u> "+part[1]+ " <u>Regisseur:</u> "+part[2]+" <u>Genre:</u> "+part[3]+" <u>Bewertung:</u> "+ part[4]+"</ul>")
            for j in tempstring:
                tempstring_b = j
            string = string + "<br>" + tempstring_b
        datei.close()
        message = "<b>Alle eingetragenen Filme:<br></b>" + string 
        info = "<br><br><br>Für alle Filmfreunde: <a href='https://www.imdb.com/calendar?region=DE&ref_=rlm'>Filmneuerscheinungen auf IMDB</a>"
        message = message + info
        return message
    else:
        file = open(helpfile, "r")
        for line in file:
            message = message+line
        file.close()
        message = "<font color='red'>Fehler! Befehl konnte nicht zugeordnet werden!</font> \n\n" + message
        return message

#Hauptprogrammschleife
loop = True
    
while loop:
    #Datum und Uhrzeit bestimmen
    aktuellesDatum = datetime.datetime.now()
    istDatum = str(aktuellesDatum.day) + "." + str(aktuellesDatum.month) + "." + str(aktuellesDatum.year)
    istUhrzeit = str(aktuellesDatum.hour) + ":" + str(aktuellesDatum.minute) + ":" + str(aktuellesDatum.second)

    #Alle Mails vom Server einlesen und aus mehrdimensionaler Liste Betreff und lfd Nummer filtern
    completeList = mailService.mailReceiver(mailPOPServer, mailUser, mailPassword)
    try:
        number = completeList[0][0]
        receiver = completeList[1]
        subject = completeList[2][0]
        timestamp = istDatum + " " + istUhrzeit
        
        #Pruefe Empfaenger fuer Whitelist, Blacklist und Sperren
        #fileCheck(whitelist)
        #fileCheck(blacklist)
        
        #Schreibe Anfrage in LOGFile
        fileCheck(mailLogFile)
        fileCheck(mailingList)
        
        mailService.mailLOGFile(mailLogFile, receiver, subject, timestamp)
        mailService.mailDataCarrier(mailingList, receiver)
        
        #Gelesene Mail auswerten und Befehl weitergeben zum Senden
        message = mailAuswertung(subject, mailHelpFile_1, mailHelpFile_2, mailHelpFile)

        #Versende E-Mail
        mailService.mailSender(mailUser, mailPassword, receiver, message)

        #Nach Versand, Mail vom Server loeschen
        mailService.mailDelete(mailPOPServer, mailUser, mailPassword, 1)
    except TypeError:
        None

    #Wartezeit bis zum naechsten Abruf um Mailserver nicht zu ueberlasten
    sleep(5)