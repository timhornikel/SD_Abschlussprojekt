import sqlite3

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('music_database.db')
cursor = conn.cursor()

# Zeile löschen, wo der Name gleich einem bestimmten Wert ist
cursor.execute('''DELETE FROM songs WHERE ID = ?''', ('1'))

# Verbindung schließen
conn.commit()
conn.close()