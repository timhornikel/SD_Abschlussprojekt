import sqlite3

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('benutzer.db')
cursor = conn.cursor()

# Tabelle erstellen, wenn sie nicht existiert
cursor.execute('''CREATE TABLE IF NOT EXISTS Benutzer (
                    Benutzername TEXT PRIMARY KEY,
                    Email TEXT,
                    PasswortHash TEXT
                )''')

# Verbindung schließen
conn.close()

print("Datenbank und Tabelle erfolgreich erstellt.")