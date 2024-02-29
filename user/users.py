import sqlite3
import hashlib

class User:
    """Klasse zur Repräsentation eines Benutzers."""
    def __init__(self, benutzername, email, passwort):
        """Initialisiert einen neuen Benutzer."""
        self.benutzername = benutzername
        self.email = email
        self.passwort_hash = hashlib.sha256(passwort.encode()).hexdigest()

    def speichern(self):
        """Speichert den Benutzer in der Datenbank."""
        conn = sqlite3.connect('benutzer.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Benutzer (Benutzername, Email, PasswortHash) 
                          VALUES (?, ?, ?)''', (self.benutzername, self.email, self.passwort_hash))
        conn.commit()
        conn.close()

    @staticmethod
    def benutzer_existiert(benutzername):
        """Überprüft, ob ein Benutzer bereits existiert."""
        conn = sqlite3.connect('benutzer.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Benutzername FROM Benutzer WHERE Benutzername=?", (benutzername,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    @staticmethod
    def anmelden(benutzername, passwort):
        """Überprüft, ob die Anmeldedaten korrekt sind."""
        conn = sqlite3.connect('benutzer.db')
        cursor = conn.cursor()
        cursor.execute("SELECT PasswortHash FROM Benutzer WHERE Benutzername=?", (benutzername,))
        stored_passwort_hash = cursor.fetchone()
        if stored_passwort_hash is not None:
            passwort_hash = hashlib.sha256(passwort.encode()).hexdigest()
            if passwort_hash == stored_passwort_hash[0]:
                return True
            else:
                return False
        return False

    @staticmethod
    def benutzer_loeschen(benutzername, passwort):
        """Löscht einen Benutzer aus der Datenbank."""
        conn = sqlite3.connect('benutzer.db')
        cursor = conn.cursor()
        cursor.execute("SELECT PasswortHash FROM Benutzer WHERE Benutzername=?", (benutzername,))
        stored_passwort_hash = cursor.fetchone()
        passwort_hash = hashlib.sha256(passwort.encode()).hexdigest()
        if passwort_hash != stored_passwort_hash[0]:
            return False
        cursor.execute("DELETE FROM Benutzer WHERE Benutzername=?", (benutzername,))
        conn.commit()
        conn.close()
        return True