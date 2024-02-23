import sqlite3

conn = sqlite3.connect('benutzer.db')
cursor = conn.cursor()

# Tabelle erstellen, wenn sie noch nicht existiert
cursor.execute('''CREATE TABLE IF NOT EXISTS Benutzer (
                  Benutzername TEXT PRIMARY KEY,
                  Email TEXT,
                  PasswortHash TEXT)''')

conn.commit()
conn.close()