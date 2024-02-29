# Softwaredesign_Abschlussprojekt

## Inhaltsverzeichnis

1. [Projektbeschreibung](#projektbeschreibung)
2. [Anleitung zur Installation und Ausführung](#anleitung-zur-installation-und-ausf%C3%BChrung)
3. [Erweiterungen](#erweiterungen)
4. [UML-Diagramme der Softwarestruktur](#uml-diagramme-der-softwarestruktur)
5. [Quellen](#quellen)

## Projektbeschreibung

Das Projekt umfasst die Entwicklung einer Anwendung zur Musikerkennung und einer Benutzeroberfläche zur Interaktion mit der Anwendung. Die Anwendung ermöglicht es Benutzern Musik hochzuladen und erkennen zu lassen, sowie über das Mikrofon des Gerätes die Musik erkennen zu lassen. Benutzer können sich registrieren und anmelden oder als Gast die Anwendung nutzen.

## Anleitung zur Installation und Ausführung

1. Laden Sie alle Dateien des Projekts herunter und speichern Sie sie in einem Ordner auf Ihrem Computer.
2. Stellen Sie sicher, dass Python installiert ist.
3. Öffnen Sie eine Befehlszeile oder ein Terminal und navigieren Sie zum Ordner, in dem sich die Dateien befinden.
4. Installieren Sie die erforderlichen Python-Bibliotheken, indem Sie den Befehl pip install -r requirements.txt ausführen.
5. Führen Sie die Datei datenbank.py aus, um die SQLite-Datenbank zu erstellen.
6. Führen Sie die Datei user_interface.py aus, um die Benutzeroberfläche der Anwendung zu starten.

Weitere Informationen oder Anleitungen zur Anwendung finden Sie auf unter Button "About" der Anwendung selbst.

## Erweiterungen

- Nutzermanagementsystem wurde erstellt mit dem angemeldet und registriert werden kann.
- Mikrofon zu Musikerkennung.
- Die Meta-Daten des Musikstückes werden angezeigt sowie das entsprechende Albumcover des Lieds.
- Links du dem erkannten Musikstück zu Youtube und Spotify wurden erstellt.
- Das Youtube Video kann direkt in dem Browser abgespielt und angehört werden.
- Eine Historie der letzten 5 erkannten Songs wurde gemacht und wird angezeigt.

## UML-Diagramme der Softwarestruktur

Das Klassendiagramm zeigt die Struktur der Klassen und deren Beziehungen zueinander. Es umfasst die Klassen User, Lied und relevante Hilfsklassen.

![UML-Diagramm](https://github.com/timhornikel/SD_Abschlussprojekt/assets/129284019/1a2abf46-cdfe-416f-b023-1e6e74c86de7)

## Quellen

- Python-Dokumentation (https://docs.python.org/)
- SQLite-Dokumentation (https://www.sqlite.org/docs.html)
- Streamlit-Dokumentation (https://docs.streamlit.io/)
- Librosa-Dokumentation (https://librosa.org/doc/main/index.html)
- Musikerkennung von Abracadabra (https://github.com/notexactlyawe/abracadabra/tree/master)
