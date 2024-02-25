import sqlite3

conn = sqlite3.connect('music_recognition.db')
cursor = conn.cursor()

# Tabelle erstellen, wenn sie noch nicht existiert
cursor.execute(""" DROP TABLE IF EXISTS sqlite_sequence; """)

conn.commit()
conn.close()