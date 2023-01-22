# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/calendar.svg" card_color="#22A7F0" width="50" height="50" style="vertical-align:bottom"/> Si Calendar
Gruppe 5 - Yekta Kücük

# Pflichtenheft

## Einleitung

	- Aufgabe ist es mit Mycroft, einem Open-Source-Sprachassistenten, und vorhandener Hardware einen eigenen Skill zu entwickeln
	- Man soll mit einem Sprachkommando einen Kalender managen können, heißt einträge erstellen, abfragen, umbennenen und löschen
	- Dazu soll eine Dokumentation erstellt werden mit einem klaren Überblick und der Erläuterung der Vorgehensweise

	Beispielhafte Nutzung des Skills

		- User: "Hey MyCroft, what's my next appointment?"  
		- Picroft: "Your next appointment is "speech interaction" on December 20, 2022 at 11:45 am."

		- User: "Hey MyCroft, create an appointment for every Friday at 08:00 am called "study time"."
		- Picroft: " Appointment "study time" set for every Friday on 08:00 am."

		- User: "Hey MyCroft what appointments do I have on this Wednesday?"
		- Picroft: "Wednesday you have an appointment "dentist" at 11:30 am and an appointment "world cup final" at 04:00 pm."

## Auftrag

	Modul: Speech Interaction
	Aufgabe: Mycroft Projekt
	Hardware: 
		- LABIST Starter Kit Raspberyy Pi4
		- Lautsprecher
		- Logitech c270 Webcam (als Mikrofon)
		- Tastatur
		- Display
		- LAN-Kabel
	Voraussetzungen:
		- Erfahrungen mit Python
		- Kentnisse im Umgang mit Git
		- Linux Betriebssystem
	Ziel: 
		- Mycroft Programmieraufgabe mit dem Ziel einen Kalender per Sprachkommando zu managen.
		- Eigenen Skill entwickeln
		- Alle Termine eines bestimmten Tages abfragen und ausliefern können
		- Neue Termine anlegen per Sprachkommando
		- Bestehende Termine umbennenen per Sprachkommando
		- Bestehenden Termin löschen nach Sicherheitsbestätigung per Sprachkommando
		- Seperate schriftliche Dokumentation zur Aufgabe mit Überblick über die Aufgabenstellung und Erläuterung der Vorgehensweise
	

## Funktionale Anforderungen

	- Eigener Skill soll per Sprachkommando Kalender nach Termin abfragen können
	- Eigener Skill soll per Sprachkommando einen bestehenden Termin  umbennenen können
	- Eigener Skill soll per Sprachkommando einen bestehenden Termin nach Sicherheitsbestätigung vom Nutzer löschen können
	- Eigener Skill soll per Sprachkommando alle Termine eines bestimmten Tages abfragen können

## Nicht-funktionale Anforderungen

	- Sicherheitsabfragen zum Schutz von Daten
	- Nach Fehlerhaften Eingaben bei Sicherheitsfragen System Sperren für 30 Sekunden
	- Benutzer soll abfragen können welche Funktionen der Skill bietet

## Ausgeschlossene Funktionalität ("future work")

	- Termine ändern können (Datum ändern)
	- Beim Anlegen eines Termins bestimmen können ob der Termin täglich, wöchentlich, monatlich oder jährlich stattfindet
	- An Termine per Sprachnachricht erinnert werden

## Zeit- und Personalplanung

	- Personen die am Projekt arbeiten: Yekta Kücük
	- Zeitplanung:
		Deadline: 24.01.2023 um 13 Uhr

	- Die ersten zwei Wochen --> Einrichtung des Raspberry Pi4 und Mycroft
	- Nach der zweiten Woche --> Am eigenen Skill arbeiten und seperat die Dokumentation beginnen
	- Bis ende Dezember 2022 sollte der eigene Skill schon fertig programmiert sein und funktionieren
	- Von Anfang Januar bis zur Deadline sollten Fehler ausgebessert werden und die Dokumentation fertig gestellt werden
