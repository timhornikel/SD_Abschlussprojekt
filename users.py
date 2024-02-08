import sqlite3
import hashlib

class User:
    def __init__(self, benutzername, email, passwort):
        self.benutzername = benutzername
        self.email = email
        self.passwort_hash = hashlib.sha256(passwort.encode()).hexdigest()

    def speichern(self):
        conn = sqlite3.connect('benutzer.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Benutzer (Benutzername, Email, PasswortHash) 
                          VALUES (?, ?, ?)''', (self.benutzername, self.email, self.passwort_hash))
        conn.commit()
        conn.close()

    @staticmethod
    def benutzer_existiert(benutzername):
        conn = sqlite3.connect('benutzer.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Benutzername FROM Benutzer WHERE Benutzername=?", (benutzername,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    @staticmethod
    def anmelden(benutzername, passwort):
        conn = sqlite3.connect('benutzer.db')
        cursor = conn.cursor()
        cursor.execute("SELECT PasswortHash FROM Benutzer WHERE Benutzername=?", (benutzername,))
        stored_passwort_hash = cursor.fetchone()
        if stored_passwort_hash is not None:
            passwort_hash = hashlib.sha256(passwort.encode()).hexdigest()
            if passwort_hash == stored_passwort_hash[0]:
                return True
        return False