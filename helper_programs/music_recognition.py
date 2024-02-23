import librosa
import numpy as np
import sqlite3
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import librosa.display

class Lied:
    def _init_(self, dateipfad):
        self.dateipfad = dateipfad
    
    def fingerprint_erstellen(self):
        # Laden des Audiofiles und Berechnung der Mel-Frequenz-Cepstrum-Koeffizienten (MFCCs)
        audio, sampling_rate = librosa.load(self.dateipfad)
        mfccs = librosa.feature.mfcc(y=audio, sr=sampling_rate)
        
        # Aus den MFCCs den Fingerabdruck (Fingerprint) erstellen
        fingerprint = np.mean(mfccs.T, axis=0)
        
        return fingerprint

    def spektrogramm_erstellen(self):
        # Laden des Audiofiles
        audio, sampling_rate = librosa.load(self.dateipfad, sr=22050)  # Beachten Sie die Samplingrate
        
        # Erstellen des Spektrogramms
        spektrogramm = librosa.feature.melspectrogram(y=audio, sr=sampling_rate)
        
        return spektrogramm

    def fingerprint_in_db_speichern(self, fingerprint, db_datei):
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect(db_datei)
        c = conn.cursor()
        
        # Fingerabdruck in die Datenbank einfügen
        c.execute("INSERT INTO fingerprints (dateipfad, fingerprint) VALUES (?, ?)", (self.dateipfad, fingerprint))
        
        # Änderungen bestätigen und Verbindung schließen
        conn.commit()
        conn.close()

    @staticmethod
    def datenbank_initialisieren(db_datei):
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect(db_datei)
        c = conn.cursor()
        
        # Tabelle erstellen, wenn sie noch nicht existiert
        c.execute('''CREATE TABLE IF NOT EXISTS fingerprints
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      dateipfad TEXT,
                      fingerprint BLOB)''')
        
        # Verbindung schließen
        conn.close()

    @staticmethod
    def audio_aufnehmen(dauer=5, samplerate=44100, dateiname="aufnahme.wav"):
        print(f"Aufnahme startet für {dauer} Sekunden...")
        audio = sd.rec(int(dauer * samplerate), samplerate=samplerate, channels=1, dtype="float32")
        sd.wait()
        sf.write(dateiname, audio, samplerate)
        print(f"Aufnahme beendet. Datei gespeichert als {dateiname}")

    def audio_vergleichen(self, db_datei):
        # Fingerabdruck des aufgenommenen Audio erstellen
        aufnahme_fingerprint = self.fingerprint_erstellen()
        
        # Fingerabdrücke aus der Datenbank abrufen
        conn = sqlite3.connect(db_datei)
        c = conn.cursor()
        c.execute("SELECT * FROM fingerprints")
        fingerprints = c.fetchall()
        conn.close()
        
        # Ähnlichkeit der Fingerabdrücke berechnen und den am ähnlichsten klingenden Titel zurückgeben
        best_match = None
        best_similarity = 0
        for row in fingerprints:
            db_fingerprint = np.frombuffer(row[2], dtype=float)
            similarity = np.dot(aufnahme_fingerprint, db_fingerprint) / (np.linalg.norm(aufnahme_fingerprint) * np.linalg.norm(db_fingerprint))
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = row[1]
        
        return best_match, best_similarity

# Beispiel für die Verwendung der Klasse Lied
if __name__ == "__main__":
    # Initialisieren der Datenbank
    Lied.datenbank_initialisieren("fingerprints.db")

    # Beispiel für die Aufnahme von Audio
    Lied.audio_aufnehmen()

    # Vergleich des aufgenommenen Audio mit der Datenbank
    aufnahme = Lied("aufnahme.wav")
    best_match, best_similarity = aufnahme.audio_vergleichen("fingerprints.db")
    print(f"Das aufgenommene Audio klingt am ähnlichsten wie '{best_match}' mit einer Ähnlichkeit von {best_similarity}")

    # Beispiel für das Erstellen eines Spektrogramms
    beispiel_dateipfad = "beispiel.mp3"
    lied = Lied(beispiel_dateipfad)
    spektrogramm = lied.spektrogramm_erstellen()

    # Anzeigen des Spektrogramms
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.power_to_db(spektrogramm, ref=np.max), y_axis='mel', fmax=8000, x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-Spektrogramm')
    plt.show()
