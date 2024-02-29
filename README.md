# Softwaredesign_Abschlussprojekt

## Inhaltsverzeichnis

1. [Projektbeschreibung](#projektbeschreibung)
2. [Installation](#Installation)
3. [Anleitung](#anleitung)
4. [Erweiterungen](#erweiterungen)
5. [UML-Diagramme der Softwarestruktur](#uml-diagramme-der-softwarestruktur)
6. [Hinweise](#hinweise)
7. [Mitwirkende](#mitwirkende)
8. [Quellen](#quellen)

## Projektbeschreibung

Das Projekt umfasst die Entwicklung einer Anwendung zur Musikerkennung und einer Benutzeroberfläche zur Interaktion mit der Anwendung. Die Anwendung ermöglicht es Benutzern Musik hochzuladen und erkennen zu lassen, sowie über das Mikrofon des Gerätes die Musik erkennen zu lassen. Benutzer können sich registrieren und anmelden oder als Gast die Anwendung nutzen. In dem About-Reiter in Streamlit steht auch nochmal kurz geschrieben was die App kann und wie diese zu bedienen ist.


## Installation

1. Klonen Sie dieses Repository:

    ```bash
    git clone https://github.com/Docterpanzen/3D_Druck_Interface
    ```

2. Wechseln Sie in das Verzeichnis:

    ```bash
    cd SD_Abschlussprojekt
    ```

3. Installieren Sie die erforderlichen Pakete:

    ```bash
    pip install -r requirements.txt
    ```

4. Starten sie Streamlit um die Benutzeroberfläche zu starten:

    ```bash
    streamlit run user_interface.py
    ```

5. **Streamlit-Webanwendung:** Wenn der Benutzer das Programm ausführt, öffnet sich automatisch ein neues Browserfenster mit der Streamlit-Oberfläche, die alle Funktionen und Erweiterungen des Systems enthält.


## Anleitung

- **Nutzermanagement:** Sie können sich in dem Nutzermanagement als Gast anmelden oder registrieren und mit dem Benutzer anmelden. Des weiteren steht zur Auswahl dass der Benutzereintrag aus der Datenbank gelöscht werde, dafür braucht man aber den Benutzername und das Passwort damit man nicht ein Fremden Nutzer rauslöschen kann.
- **Musik hochladen:** Die Musikstücke hochladen geht nur wenn ein Nutzer angemeldet ist. Es können nur Dateien mit dem .wav Format hochgeladen werden. Aus den Hochgeladenen Songs werden dann Fingerprints erstellt und diese dann in die Datenbank samt den Meta-Daten abgespeichert. Die Metadaten haben in diesem Fall eine andere Tabelle als die Fingerprints und sind über eine ID miteinander verbunden.
- **Musik erkennen:** Das Erkennen von Musik funktioniert, gleich wie das Hochladen von Musik, nur wenn ein Nutzer angemeldet ist. Um Musik hochzuladen muss erstmal ausgewählt werden wie Musik hochgeladen werden soll. Entweder durch eine .wav Datei welche man einfügen kann oder mithilfe von dem Mikrofon. Bei der Eingabe durch das Mikrofon werden 8 Sekunden Audio aufgenommen und diese dann, gleich wie die .wav Datei, verarbeitet. Wenn ein Lied erkannt wurde dann kommt man zu der Ausgabe der Hinterlegten Daten. Dort werden als erstes die Meta-Daten des erkannten Musikstückes preisgegeben, sowie ein Albumcover welches in der DuckDuckGo-API gesucht wurde. Dann kommen diverse Links zu dem Musikstück welche auf die Youtube und Spotify Seite führen. In diesem Absatz wird direkt auch noch ein Youtube-Video zu dem erkannten Song angezeigt. Die letzte Ausgabe bei erfolgreich erkannten Songs ist die Historie der letzten erkannten Songs.



## Erweiterungen

- **Nutzermanagementsystem:** Ein Nutzermanagementsystem wurde implementiert, um die Behandlung der Nutzer zu verbessern.
- **Mikrofon zur Musikerkennung:** Das System kann nun Musikstücke anhand des Mikrofons erkennen.
- **Anzeige von Meta-Daten:** Die Meta-Daten des erkannten Musikstücks werden angezeigt, ebenso wie das entsprechende Albumcover.
- **Youtube- und Spotify-Links:** Direkte Links zum erkannten Musikstück auf Youtube und Spotify wurden hinzugefügt.
- **Youtube-Video-Player:** Das Youtube-Video kann direkt im Browser abgespielt werden.
- **Historie der letzten 5 Songs:** Es wird eine Historie der letzten 5 erkannten Songs angelegt und angezeigt.


## UML-Diagramme der Softwarestruktur

Das Klassendiagramm zeigt die Struktur der Klassen und deren Beziehungen zueinander. Es umfasst die Klassen User, Lied und relevante Hilfsklassen.

![UML-Diagramm](https://github.com/timhornikel/SD_Abschlussprojekt/assets/129284019/1a2abf46-cdfe-416f-b023-1e6e74c86de7)


## Hinweise

Für die Entwicklung und Implementierung dieses Systems wurden Teile des Codes von Cameron MacLeod (@notexactlyawe) verwendet. Das ursprüngliche Programm kann in seinem GitHub-Repository [hier](https://github.com/notexactlyawe/abracadabra) eingesehen werden.

Wir danken Cameron MacLeod für seine wertvolle Arbeit und seine Bereitschaft, den Code zur Verfügung zu stellen. Sein Beitrag war entscheidend für die Umsetzung einiger Funktionen in unserem System, und seine Arbeit hat es uns ermöglicht, ein leistungsfähigeres und effizienteres System zu erstellen.


## Mitwirkende

- **Sandra Grüner:** [Sandra Grüner](https://github.com/SandysOO)
- **Tim Hornikel:** [Tim Hornikel](https://github.com/timhornikel)
- **Oskar Klöpfer:** [Oskar Klöpfer](https://github.com/Docterpanzen)


## Quellen

- Python-Dokumentation: https://docs.python.org/
- SQLite-Dokumentation: https://www.sqlite.org/docs.html
- Streamlit-Dokumentation: https://docs.streamlit.io/
- Librosa-Dokumentation: https://librosa.org/doc/main/index.html