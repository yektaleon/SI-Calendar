# SI - Gruppe 5 Yekta Leon Kücük

# Kolloquium

# Einleitung

Genutzte Hardware: 
- LABIST Starter Kit Raspberyy Pi4
- Lautsprecher
- Logitech c270 Webcam (als Mikrofon)
- Tastatur
- Display
- LAN-Kabel

Zu anfang wird der Raspberry Pi angeschlossen und die weitere Hardware (Mikrofon in form von der Webcam, Tastatur, Display usw.)
Nachdem der Raspberyy Pi strom hat und die nötige Hardware angeschlossen wurde kann mit der Einrichtung begonnen werden.
Auf dem Gerät sollte ein Mycroft Picroft Image vorinstalliert sein. Falls dies nicht der Fall sein sollte oder man hierzu weitere Informationen
benötigt findet man dieser auf dieser Seite :https://mycroft-ai.gitbook.io/docs/using-mycroft-ai/get-mycroft/picroft

Beim Starten des Geräts sollte dieses mit der Installation beginnen. Dabei folgt man einfach den Instruktionen auf dem Bildschirm
und wählt beispielsweise Audio output und input aus usw. Dabei ist wichtig das der Raspberry Pi eine stabile Internetverbidung hat.
Bei erneuten Problemen oder Fragen kann man erneut auf die vorhin erwähnte Website zugreifen: https://mycroft-ai.gitbook.io/docs/using-mycroft-ai/get-mycroft/picroft
Hier wird auch die Einrichtung nochmals durchgegangen.

Nach der Einrichtung sollte man im mycroft-cli-client screen sein. 
Es besteht die Möglichkeit bei Mycroft im  per Sprach- oder Tastatureingabe Kommandos zu geben. So kann man 
Mycroft mit dem Befehl "Hey Mycroft, what's your IP adress?" einem die IP Adresse des Geräts ausgeben. Hierdurch hat man die Möglichkeit
per SSH verbindung mit den eigenen Rechner auf den Pi zuzugreifen. Dies ist keine notwendigkeit erspart jedoch etwas an Aufbau und erleichtert
das Arbeiten am eigenen Skill im späteren Verlauf. 

Den Mycroft CLI client kann man starten mit dem Befehl mycroft-cli-client und mit STRG +C oder ":exit" verlassen. Das Gerät sollte man
nicht einfach per Schalter oder durch rausziehen des Steckers ausschalten. Zum Herunterfahren kann man in der Shell per "sudo shutdown now" eingeben
oder auch "sudo reboot" falls man nur einen Neustart benötigt.

Im CLI client können dann die installierten Skills genutzt werden um beispielsweise Wiki abfragen zu starten oder ähnliches. Man kann auch
per Sprachbefehl oder Tastatur eingabe Skills installieren, wenn diese im Skills Marketplace vorhanden sind.

# Skills installieren

Mycroft selbst empfiehlt die Nutzung von mycroft-msk create. Dies kann auf dem Gerät direkt ein neuen Skill erstellen. Die Abfolge und die Nutzung dieses Befehls
werden auf dieser Website nochmals genauer erklärt:
https://mycroft-ai.gitbook.io/docs/skill-development/introduction/your-first-skill

Den Aufbau eines Skills kann man hier nachschauen:https://mycroft-ai.gitbook.io/docs/skill-development/skill-structure
Falls Fragen bezüglich des Python Codes aufkommen oder den Verzeichnissen wie dem Locale Verzeichniskann hier nachgeschlagen werden.

Ein auf diese Weise erstelltes Template befindet sich im MI-GitLab. Dieses kann man forken und mit mycroft-msm install "https://gitlab.mi.hdm-stuttgart.de/Pfad/zum/eigenen/forked/skill"
Die skills befinden sich im Verzeichnis /opt/mycroft/skills/"Beispielskill". In diesem Verzeichnis können dann auch Änderungen bzw Updates per git pull herunter gezogen werden.
Mit dem git pull pefehl werden jedoch nicht die dependencies auf dem Gerät installiert. Dies muss man manuell mit beispielsweise mycroft-pip oder apt-get erledgit werden.

# Eigener Kalender Skill

Aufgabe ist es einen Skill zu entwickeln welcher Termine eines nextcloud-Systems verwaltet. Es sollen per Sprachkommando neue Termine angelegt werden,
bestehende Termine umbenannt werden und auch Termine gelöscht werden können.

Für die Kommunikation mit dem Kalender wurde caldav verwendet. Caldav kann man einfach per "mycroft-pip install caldav" auf dem Gerät installieren.
Es könnte, wie in meinem Fall ein Fehler auftreten. "ImportError: libxslt.so.1: cannot open shared object file: No such file or directory"
Dies kann bei der Verwendung von der caldav library auftreten. Mir hat in diesem Fall "sudo apt-get install libxslt-dev" geholfen den Fehler zu beheben.
Am besten greift man auch auf die logs des skills zu um nach den Fehlermeldungen zu suchen. Die Logs sollten in diesem Verzeichnis sich befinden: /var/log/mycroft/
Weitere Infos zu den log files findet man hier: https://mycroft-ai.gitbook.io/docs/using-mycroft-ai/troubleshooting/log-files

Für die nextcloud Daten des Users gibt es die Möglichkeit 2 Files zu erstellen mit dem Usernamen und Passwort welche mithilfe vom Code extrahiert werden können.
Ich habe den Versuch unternommen die Daten aus der settingsmeta.yaml zu lesen. Den Code dazu habe ich schon geschrieben jedoch entnimmt es die Daten nicht aus der settingsmeta.yaml
sondern die Values welche ich in der __init__.py stehen habe. Die Informationen mit denen ich gearbeitet habe befinden sich auf dieser Website: https://mycroft-ai.gitbook.io/docs/skill-development/skill-structure/skill-settings

# Funktionen des Kalenders

Hier kann erneut auf die Website: https://mycroft-ai.gitbook.io/docs/skill-development/skill-structure
verwiesen werden
Es werden hier die Intent handler und weitere Methoden erklärt.

- def log_in (self): Diese Funktion versucht, sich mit einem Nextcloud-Kalenderservice mithilfe des CalDAV-Protokolls anzumelden.
Zuerst nutzte ich hierbei die lokalen Datein "userNameFile.txt" und "passwFile.txt" welche die Login Informationen fürs Nextcloud-System enthalten.
Da diese Lösung zwar funktionierte jedoch nicht optimal war wurde sie auskommentiert und versucht die Daten in der settingsmeta.yaml abzuspeichern und daraufhin
von dort auszulesen. Dies funktioniert jedoch nicht. Die Werte habe ich manuell angegeben sie werden also nicht aus der settingsmeta.yaml entnommen.

- def sort_events(self): Hier wird zunächst die aktuelle Zeit abgerufen. Anschließend werden alle Termine aus dem Kalender abgerufen und durchlaufen
welche dann einer Liste hinzugefügt werden und mit der sort methode sortiert werden. Nach Sortierung wird unterteilt zwischen Terminen die in der Zukunft stattfinden und Terminen
welche zum aktuellen Datum stattfinden (results_today, results_future).

- def get_all_events(self): Hier werden alle Terminen aus dem Kalender abgerufen. Es werden die sortierten Termineinträge aufgerufen. Anschließend wird die aktuelle Zeit
wieder abgerufen um die Termine herauszufiltern welche aktuell beginnen. Es wird dann geprüft ob die Termine aktuell stattfinden oder in der Zukunft, vergangene Termine interessieren uns in diesem Fall nicht.
Je nachdem ob dann ein Termin gefunden wurde oder nicht wird der passende Dialog abgerufen.

- def create_event(self, message): Hier wird ein Termin (event) erstellt. Dabei wird der Name abgefragt und Zeit des Termins. Zuerst wird Startzeit und dann Ende des Termins abgefragt.
Es wird auch wieder überprüft ob die Zeitangaben logsich sind (Termin liegt in der Gegenwart oder Zukunft).

- def get_events_for_date(self, message): Hier wird nach Input eines Datums nach den Terminen gesucht welche mit dem Datum übereinstimmen und diese Termine werden daraufhin ausgegeben.
Falls kein Termin für den angegebenen Zeitraum gefunden wurde wird entsprechend die Antwort ausgegeben no events on date.

- def get_next_event(self): In dieser Funktion wird einfach der nächste zeitlich dem aktuellen Datum folgende Termin geholt und zurück gegeben.
Hierzu schaut er sich die Termine am heutigen Tag an und wenn nichts gefunden wird, wird der nächste Tag angeschaut.

- def search_for_event(self, target_event): Diese funktion ist wichtig für das Löschen oder Umbennenen von Terminen. Hier wird nach einem bestimmten Termin
gesucht per Name.

- def remove_event(self, message): Hier wird nach einem Termin gesucht mithilfe der vorherigen Funktion. Daraufhin wird falls der Name gefunden wurde
eine Abfrage gestartet ob der Termin auch wirklich gelöscht werden soll. Je nach "Yes" oder "No" wird der Termin gelöscht oder eben nicht und eine entsprechende Nachricht wird abgespielt.

- def rename_event(self, message): Hier wird auch wieder nach dem Termin per Name abgefragt und gesucht um diesen dann umzubennenen. Der Nutzer
kriegt auch bei erfolgreicher umbennenung eine Nachricht oder bei einem Fehler auch entsprechend eine Nachricht

- def __init__(self): Das ist der Konstruktor

- def initialize(self): Wird nach konstruktion des Skills abgerufen. Hier wird der Login aufgerufen und die lokale Zeitzone gesetzt

- def create_skill(): Gibt uns unseren erstellten Skill zurück

# Fehler und Probleme

Eines der größten Probleme welche ich bei diesem Projekt hatte war das ich den Umfang unterschätzt habe und dachte ich könnte die Aufgaben alleine erledigen.
Dies führte dazu das ich neben den anderen Projekten und Abgaben im Studium oft hinterher hing und probleme mit dem Zeitmanagement hatte.
Zudem fiel es mir oft schwer Probleme allein zu lösen. Die Wiki half dabei jedoch oft gut aus.

Oftmals fehlte eine zweite Meinung oder eine weitere Angehensweise. Hier versuchte ich andere vorhandene Skills als Beispiele zu nehmen und schaute wie diese Implementiert wurden.

Ein weiteres Problem was ich hatte war das ich zu spät die Log Files überprüft habe bei Fehlermeldungen. Ich habe so viel Zeit verloren da ich die Probleme 
nicht lösen konnte da ich nicht wusste wo der Fehler lag. Nachdem ich mir die Log files angeschaut habe mit dem Befehl tail -f /var/log/mycroft/skills.log
konnte ich viel schneller meine Probleme lösen.

Die in der Wiki beschriebenen Probleme die oft auftreten sind bei mir ebenfalls aufgetretetn diese konnte ich jedoch dank der Wiki relativ schnell lösen.

Ein weiteres Problem das ich hatte war das ich auf die harte Tour lernen musste das Linux beim Löschen von Dateien nicht verzeiht. Ich habe dadurch den Skill gelöscht
gehabt und einige Probleme bei der reinstallation gehabt. So konnte ich einige Zeit das mycroft-cli-client nicht starten und musste den Raspberry Pi oft rebooten.

Auch bei der Implementierung hat es oft mehrere Anläufe gebraucht und es mussten ständig optimierungen vorgenommen werden. 




