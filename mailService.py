#Mail senden auf Anfrage
#Anfragekriterien sind: Bewertung 1-10, "Genre", Help, Besties (Bewertung 7 oder höher), Zufall,
#Help schickt kurze Infomail aus einer Textdatei erstellt und alle eingetragenen Genres
#

from time import sleep
import smtplib, ssl #Sende Mail
import poplib #Empfange Mail
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mailCycle = 30

def mailReceiver(server, user, password):
    #Frage Mails alle x Zyklen ab
    #Empfange und Lese Mail
    #Mailreihenfolge: Erste ist die aelteste auf dem Server!
    serverCon = poplib.POP3_SSL(server)
    serverCon.user(user)
    serverCon.pass_(password)
    
    countSize = serverCon.stat()
    print("\nMails im Postfach:", countSize[0], "\nGesamte Postfachgroesse:", countSize[1], "bytes")
    
    liste = []
    messageNrList = []
    receiverList = []
    senderList = []
    subjectList = []
    
    for i in range(0,countSize[0]):
        liste.append(serverCon.retr(i+1))
        messageNr = (i+1)
        
        inhalt = serverCon.top(messageNr,8)
        for line in inhalt[1]:
            if "Subject" in str(line):
                subject = line
        for line in inhalt[1]:
            if "From" in str(line):
                senderAdress = line
        for line in inhalt[1]:
            if "Envelope-To" in str(line):
                receiverAdress = line
        
        receiverAdress = str(receiverAdress).split("<")
        receiverAdress = receiverAdress[1].split(">")
        receiverAdress = receiverAdress[0]
        
        senderAdress = str(senderAdress).split("<")
        senderAdress = senderAdress[1].split(">")
        senderAdress = senderAdress[0]
        
        subject = str(subject).split(": ")
        subject = subject[1].split("'")
        subject = subject[0]
        
        messageNrList.append(messageNr)
        receiverList.append(receiverAdress)
        senderList.append(senderAdress)
        subjectList.append(subject)
        
        #Ausgabe
        print("\nNachricht:",messageNr)
        print("Empfaenger:",receiverAdress)
        print("Absender:",senderAdress)
        print("Betreff:",subject)
    else:
        try:
            completeList = [messageNrList, senderAdress, subjectList]
            return completeList
            print("\nAlle Mails ausgelesen!")
        except UnboundLocalError:
            print("\nDerzeit keine Anfrage!")
    
    serverCon.quit()

def mailSender(user, password, receiver, message):
    #Sende Email mit angefragten Infos
    #Message Header
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = receiver
    msg['Subject'] = "Dein Filmtipp von Alex Filmdatenbank"
    
    msg.attach(MIMEText(message, 'html'))
    #msg.attach(MIMEText(message, 'plain'))
    
    serverCon = smtplib.SMTP("mail.gmx.net", 587)
    serverCon.ehlo()
    serverCon.starttls()
    serverCon.ehlo()
    serverCon.login(user, password)
    try:
        serverCon.sendmail(user, receiver, msg.as_string())
    except SMTPRecipientsRefused:
        print("Empfänger derzeit nicht erreichbar. Neuer Versuch in 5 Sekunden...")
        sleep(5)
    
    serverCon.quit()

def mailDelete(server, user, password, whichDelete):
    #Loesche Mail vom Server, wenn fertig bearbeitet und geantwortet
    serverCon = poplib.POP3_SSL(server)
    serverCon.user(user)
    serverCon.pass_(password)
    
    serverCon.dele(whichDelete) #zu loeschende Nummer eintragen
    #Mailreihenfolge: Erste ist die aelteste auf dem Server!
    
    serverCon.quit()

def spamCounter(receiver, receiver_SET, blacklist, whitelist):
    #Sendet der gleiche Absender innerhalb einer Minute mehr als drei Mails,
    #dann Bearbeitungssperre von fuenf Minuten
    #Mehr als drei Sperren innerhalb einer Stunde, dann User auf Blacklist
    #Adressen auf der Whitelist koennen unendlich senden (Testzwecke!)
    if receiver in blacklist:
        flag = False
    elif receiver in whitelist:
        flag = True
    else:
        fiveMinuteCounter =  0
        oneHourCounter = 0

def mailLOGFile(logfile, receiver, subject, timestamp):
    #Liste alle Anfragen
    file = open(logfile, "a+")
    line = receiver + ";" + subject + ";" + timestamp + "\n"
    file.write(line)
    file.close()
    
def mailDataCarrier(mailingList, receiver):
    #Liste alle Mailadressen die angefragt haben
    file = open(mailingList, "r+")
    tempRead = file.read()
    if receiver not in tempRead:
        addReceiver = receiver + "\n"
        file.write(addReceiver)
    else:
        print("Empfänger bereits eingetragen.")
    file.close()
    

#Testroutinen (abschalten wenn als Modul genutzt wird
#receiver = "alexander.wiltz@gmx.de"
#subject = "Besties"

#completeList = mailReceiver(mailPOPServer, mailUser, mailPassword)
#message = mailAuswertung(subject, mailHelpFile)
#mailSender(mailUser, mailPassword, receiver, message)
#mailDelete(mailPOPServer, mailUser, mailPassword, 1)

