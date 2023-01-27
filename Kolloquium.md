# SI - Gruppe 5 Yekta Leon Kücük

# Kolloquium 

Dokumentation Mycroft-Projekt

Aufgabe dieses Projekts war die Konzeption und Erstellung eines eigenen Mycroft-Skills zum verwalten eines CalDAV basierten Kalenders, der von einem NextCloud System gehosted wird.

# Einleitung

Genutzte Hardware: 
- LABIST Starter Kit Raspberry Pi4
- Lautsprecher
- Logitech c270 Webcam (verwendet als Mikrofon)
- Tastatur
- Display/Monitor
- LAN Anschluss/Kabel

Zu Beginn wird der Raspberry Pi an die Spannungsversorgung angeschlossen und die o.a. Hardware wie Mikrofon/Webcam, Tastatur, Display, etc. amgeschlossen.
Nachdem der Raspberyy Pi gestartet und die benötige Hardware angeschlossen wurde, kann mit der Einrichtung der Software begonnen werden.
Auf dem Pi4 sollte das Mycroft Picroft Image vorinstalliert sein. Falls dies nicht der Fall, muss dies im nächsten Schritt getan werden. 
Weitere Informationen zur Mycroft Installation findet man dieser auf dieser Seite: https://mycroft-ai.gitbook.io/docs/using-mycroft-ai/get-mycroft/picroft

Beim Starten des Pi4 sollte die Mycroft Installation automatisch starten. Dabei folgt man einfach den Anweisungen dem Bildschirm
und wählt beispielsweise Audio Output, Audio Input, etc. aus. Dabei zu beachten, dass der Raspberry Pi eine stabile Internetverbidung hat.
Bei Problemen oder Fragen kann man auf die Dokumentation der o.a. Website zugreifen: https://mycroft-ai.gitbook.io/docs/using-mycroft-ai/get-mycroft/picroft
Hier wird auch Einrichtung nochmals Schritt für Schritt erläutert.

Nach der Einrichtung sollte man im mycroft-cli-client Screen landen.
Es besteht die Möglichkeit, bei Mycroft per Sprach- oder Tastatureingabe Kommandos einzugeben. 
So kann man beispielsweise Mycroft mit dem Befehl "Hey Mycroft, what's your IP adress?" die IP Adresse des Geräts ausgeben lassen. 
Mit dieser IP-Adresse des Pi4 kann man per SSH Shell eine Verbindung zum Raspberry aufbauen
Natürlich kann man auch per Tastatur und separratem Bildschirm mit dem Pi4 arbeiten. Eine remote SSH Verbindung ist deutlich einfacher und komfortabler, das Mycroft ja keine graphische Benutzeroberfläche bereitstellt.

Den Mycroft CLI (Command Line Interface) Client kann man mit dem Befehl mycroft-cli-client starten  und mit CTRL-C bzw. dem Kommando ":exit" jederzeit verlassen. 
Das Gerät sollte man nicht einfach per Netzschalter oder durch herrausziehen des Netzsteckers ausschalten, da es sonst zu schweren Fehlern des Dateisystems führen kann. Zum Herunterfahren kann man in der Shell das Kommando "sudo shutdown now" eingeben, um den Pi4 sauber herunterzufahren.
Mit dem Kommando "sudo reboot" lässt sich das Gerät neu starten.

Über den CLI Client können die installierten bzw. konfigurierten Skills genutzt werden. Beispielweise kann der vorinstallierte Skill "Wiki" genutzt werden, um eine Wikipedia Abfrage abzusetzen. Per Sprachbefehl oder Tastatureingabe lassen sich auch Skills über den Skills Marketplace suchen und installieren.

# Skills installieren

Zur Erstellung bzw. Installation eines Skills empfihelt Mycroft die Nutzung von mycroft-msk create. 
Mit diesem Befehl kann auf dem Gerät direkt ein neuer Skill erstellt werden.
Die genaue Ausführung und Parametrisierung des Befehls wird auf dieser Mycroft Seite im Detail erläutert (https://mycroft-ai.gitbook.io/docs/skill-development/introduction/your-first-skill)

Den Aufbau eines Skills kann man hier nachlesen: https://mycroft-ai.gitbook.io/docs/skill-development/skill-structure
In diesem Kapitel werden auch Fragen zum Python Code beantwortet und die lokale Verzeichnissstruktur erklkärt.

Ein auf diese Weise erstelltes Template befindet sich im MI-GitLab. 
Dieses Template lässt sich forken und mit dem Kommando mycroft-msm install "https://gitlab.mi.hdm-stuttgart.de/Pfad/zum/eigenen/forked/skill" installieren.
Die Skills befinden sich im Verzeichnis /opt/mycroft/skills/<beispiel_skill>. In diesem Verzeichnis können dann auch Änderungen bzw Updates per git pull Kommando  heruntergeladen werden.
Mit dem Befehl git pull werden jedoch nicht die Abhängigkeiten (dependencies) auf dem Gerät installiert. Dies müssen manuell mit mycroft-pip oder apt-get aufgelöst werden.

# Eigener Kalender Skill

In diesem Projekt gilt es einen eigenen Skill zu entwickeln, der Termine eines CalDAV basierten Kalenders eines Nextcloud Systems verwalten kann.
Über Sprachkommandos soll es dem Benutzer möglich sein, neue Termine anzulegen und bestehende Termine umzubennen oder diese zu löschen.

Die Kommunikation mit dem Nextcloud Kalender wird über das CalDAV Protokoll realisiert.
Hierzu muss das Caldav Modul auf dem Pi4 installiert werden: mycroft-pip install caldav.
Dabei kann es natürlich zu Fehlern kommen. In meinem Fall trat der Fehler "ImportError: libxslt.so.1: cannot open shared object file: No such file or directory" auf. 
Dies kann bei der Verwendung von der caldav Bibliothek durchaus auftreten. 
Mir hat in diesem Fall die nachträgliche Installation der XSLT Bibliothek "sudo apt-get install libxslt-dev" geholfen.

Zur Fehleranalyse sollte man sich immer die System Logs anzeigen lassen, da dies bei der Lokalisierung und Behebung der Fehler hilft.
Mycroft gibt seine Status und Fehler in vier Dateien aus, die sich im Verzeichnis /var/log/mycroft befinden: audio.log, bus.log, skills.log, und voice.log
In der Datei skills.log werden Fehler ausgegeben, die mit der Installation und Nutzung der Skills zu tun haben.
Weitere Infos zu den log files findet man in der Dokumentation: https://mycroft-ai.gitbook.io/docs/using-mycroft-ai/troubleshooting/log-files

Damit sich Mycroft beim NextCloud Service des Benutzers authorisieren kann, müssen sowohl Benutzername (login) als auch das Kennwort übermittelt werden. Grundsäzlich stehen dabei zwei Methoden zur Auswahl:
(a) Authorisierung über lokale Dateien: Hier werden die Zugangsdaten des Benutzers (login und password) aus einer selbst angelegten Datei herausgelesen
(b) Benutzername und Kennwort werden aus den JSON Settings herausgelesen.
Sicherheithinweis: In beiden Fällen wird das Kennwort als Klartext in den Dateien abgespeichert.
Beide Login Informationen werden über den Python Code extrahiert.

In meinem Code haben ich beide Informationen aus der JSON Settings Datei augelesen (__init__.py)

Dabei habe ich micht an die Dokumentation auf der folgenden Seite angelehnt: https://mycroft-ai.gitbook.io/docs/skill-development/skill-structure/skill-settings

# Funktionen des Kalenders

Hier kann erneut auf die Website: https://mycroft-ai.gitbook.io/docs/skill-development/skill-structure verwiesen werden.
Es werden hier die Intent Handler und weitere Methoden erklärt.

- def log_in (self): Diese Funktion versucht sich mit einem NextCloud Calender Service über das CalDAV-Protokoll anzumelden.
abzulegen. Obwohl diese Lösung funktioniert, habe ich den Programmcode später auskommentiert und durch eine andere Variante ersetzt.
In der 2. Version habe ich die Login Informationen "user" und "password" aus der vorhandenen settingsmeta.yaml Datei ausgelesen. 
Somit musste keine zusätzliche Datei angelegt werden. Allerdings hatte ich - obwohl ich die Dokumentation ausführlich studiert habe - keinen Erfolg beim Auslesen gehabt. Ich vermute, dass es an Pfadeinstelungen der YAML Datei lag.
In der letzten Variante habe ich versucht, die Parameter aus der automatisch generierten JSON Datei auszulesen.

- def sort_events(self):  In dieser Funktion wird zunächst die aktuelle Zeit abgefragt. Anschließend werden alle Termine aus dem Kalender extrahiert und durchlaufen, die 
dann einer Liste hinzugefügt werden. Anschliessend werden die ausglesenen Termin chronologisch sortiert. Nach der Sortierung werden die Termine in zwei Blöcke unterteilt: (a) Termine heute, und (b) Termine in der Zukunft, in den zwei Arrays results_today und results_future.

- def get_all_events(self): In dieser Funktion werden alle Terminen aus dem Kalender abgerufen. Es werden die sortierten Termineinträge aufgerufen. Anschließend wird die aktuelle Zeit ermittelt, um die Termine herauszufiltern die zum aktuell anstehen. Anschließend wird geprüft, ob die Termine gerade anstehen oder erst in der Zukunft anstehen. Verstrichene Termine interessieren uns in diesem Fall nicht. Je nachdem, ob dann ein Termin gefunden wurde oder nicht, wird der passende Dialog abgerufen.

- def create_event(self, message):  In dieser Funktion wird ein neuer Termin (event) erstellt. Dabei wird nach dem Name und der Zeit des Termins gefragt. Zuerst wird die Startzeit und anschliessend die Endezeit des Termins abgefragt. Es wird auch wieder überprüft, ob die Zeitangaben plausibel sind (Termin liegt in der Gegenwart oder Zukunft).

- def get_events_for_date(self, message): In dieser Funktion wird nach Eingabe eines Datums nach den entsprechenden Terminen gesucht. Hierzu muss das eingegebene Datum mit der Startdatum des Termins übereinstimmen, damit es in die Ergebnisliste aufgenommen und ausgegeben wird.
Falls kein Termin für den angegebenen Zeitraum gefunden wurde, wird eine entsprechende Rückmeldung ausgegeben (no events on date).

- def get_next_event(self): In dieser Funktion wird der nächste zeitlich anstehende Termin (aktuelles Datum) extrahiert und zurückgegeben.
Hierzu werden die Termine des aktuellen Tags untersucht und derjenige ausgegeben, der an diesem Tag (noch) ansteht.

- def search_for_event(self, target_event): Diese Funktion ist für das Löschen bzw. Umbennenen von Terminen zuständig. Es wird nach einem bestimmten Termin
gesucht, der mit dem eingegebenen Namen übereinstimmt.

- def remove_event(self, message): Diese Funktion sucht nach einem Termin, der mit dem eingegebenen Namen übereinstimmt. Wenn ein Termin mit dem übergebenen Namen übereinstimmt, wird dieser aus dem Kalender gelöcht. Zvor wird nachgefagr, ob der Benutzer den gefundenen Kalendereintrag wirklich löschen möchte (yes) oder nicht (no).

- def rename_event(self, message): Auch in dieser Funktion wird zunächste nach einem Kalendereintrag gesucht, der mit dem eingegebenen Namen übereinstimmt. 
Wenn ein Termin mit dem übergebenen Namen übereinstimmt, wird dieser nach Abfrage des neuen Namens umbenannt. Der Benutzer bekommt nach bei erfolgreicher Umbenennung eine ensprechende Bestätigung, ansonsten eine Fehlermeldung.

- def __init__(self): Das ist der Konstruktor und dient zu Initialisierung der Klasse

- def initialize(self): Diese Funktion wird nach dem Konstruktor aufgerufen. Hier wird die Login Funktion augerufen und u.a. auch die lokale Zeitzone gesetzt.

- def create_skill(): Gibt den erstellten Skill zurück

# Fehler und Probleme

Eines der größten Probleme, auf die ich bei diesem Projekt gestoßen bin, war dass ich den Umfang der Aufgabe unterschätzt hatte und dachte, ich könne die Aufgabe alleine erledigen. Das hat dazu geführt, dass ich neben den anderen Projekten und Abgaben im Semester oft zeitlich hinterher war und Probleme mit meinem Zeitmanagement hatte. Zudem fiel es mir oft schwer, Probleme im Alleingang zu lösen. Die informative Wiki Seite hat mir dabei stets geholfen.

Oftmals fehlte eine zweite Meinung oder eine alternative Herangehensweise. Hier versuchte ich, andere vorhandene Skills als Vorlage zu nutzen und schaute wie diese implementiert wurden.

Ein weiteres Problem das ich hatte war, dass ich erst spät Log Files kennegelernt haben, um hilfreiche Hinweise zur Fehlerbehebung zu bekommen.
Ich habe so viel Zeit verloren, da ich die Probleme nicht unmittelbar und allein lösen konnte. Nachdem ich mir die Log Files angeschaut hate (mit dem Befehl tail -f /var/log/mycroft/skills.log) konnte ich viel schneller die Lösung der Fehler angehen.

Die in der Wiki beschriebenen häufig auftretenden Probleme sind auch bei mir augetreten, so dass diese Dokumentation gut weitergeholfen hat.

Eine weitere Herausforderung die ich hatte war, dass ich auf die harte Tour lernen musste, dass es beim Arbeiten mit der Linux Shell keinen Papierkorb gibt und somit gelöschte Dateien unwiderruflich verloren gehen. Aus Versehen hatte ich meinen fertiggestellten Skill mit dem Kommando "rm" gelöscht! Somit konnte ich den mycroft-cli-client nicht mehr starten starten. Den gelöschten Skill musste erneut instalieren und testen.

Auch die Implementierung war zeitaufwendig, da ich jede einzelne Funktion zum Zugriff auf den Kalender testen musste. Dabei habe ich sowohl die Mycroft Befehlszeile als auch die Spracheingabe genutzt. Auch hier haben mir Vorlagen zu den allgeminen CalDAV Kalenderfunktionen geholfen.


