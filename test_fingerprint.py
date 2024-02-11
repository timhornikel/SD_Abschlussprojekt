import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import numpy as np
import hashlib
import sqlite3

class Lied:
    @staticmethod
    def create_spectrogram(filename, sampling_rate=22050):
        # Audio-Datei laden
        sample_rate, data = wavfile.read(filename)
        
        # Spektrogramm berechnen
        frequencies, times, Sxx = spectrogram(data, fs=sample_rate, window='hann', nperseg=512, noverlap=256)
        
        return frequencies, times, Sxx
    
    @staticmethod
    def plot_spectrogram(frequencies, times, spectrogram):
        plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram), shading='auto')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.title('Spectrogram')
        plt.colorbar(label='Intensity [dB]')
        plt.show()
    
    @staticmethod
    def create_fingerprint(spectrogram):
        # Find peaks in the spectrogram
        peaks = np.where(spectrogram == np.max(spectrogram))
        
        # Convert peak indices to a hashable tuple
        peak_indices = tuple(zip(peaks[0], peaks[1]))
        
        # Generate fingerprint from peak locations
        fingerprint = hash(peak_indices)
        
        return fingerprint
    
    @staticmethod
    def store_fingerprint(filename, fingerprint, name=None):
        # Verbindung zur SQLite-Datenbank herstellen (oder erstellen, falls sie nicht existiert)
        conn = sqlite3.connect('music_database.db')
        cursor = conn.cursor()
        
        # Tabelle für die Songs erstellen, wenn sie noch nicht existiert
        cursor.execute('''CREATE TABLE IF NOT EXISTS songs
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, fingerprint TEXT)''')

        # Berechnen Sie einen eindeutigen Hash für den Fingerabdruck
        fingerprint_hash = hashlib.sha1(bytes(str(fingerprint), 'utf-8')).hexdigest()
        
        # Speichern Sie den Hash und den Dateinamen in der Datenbank
        cursor.execute("INSERT INTO songs (name, fingerprint) VALUES (?, ?)", (name, fingerprint_hash))
        conn.commit()
        
        # Verbindung schließen
        conn.close()
    
    @staticmethod
    def recognize_song(fingerprint):
        # Verbindung zur SQLite-Datenbank herstellen (oder erstellen, falls sie nicht existiert)
        conn = sqlite3.connect('music_database.db')
        cursor = conn.cursor()
        
        # Berechnen Sie den Fingerabdruck des Songs, den Sie erkennen möchten
        fingerprint_hash = hashlib.sha1(bytes(str(fingerprint), 'utf-8')).hexdigest()
        
        # Suchen Sie den Fingerabdruck in der Datenbank
        cursor.execute("SELECT filename FROM songs WHERE fingerprint=?", (fingerprint_hash,))
        result = cursor.fetchone()
        
        # Verbindung schließen
        conn.close()
        
        if result:
            return result[0]  # Den Dateinamen des erkannten Songs zurückgeben
        else:
            return "Song not found in database"

# Beispielanwendung
filename = 'Songs/CantinaBand3.wav'
frequencies, times, spectrogram = Lied.create_spectrogram(filename)
#Lied.plot_spectrogram(frequencies, times, spectrogram)
fingerprint = Lied.create_fingerprint(spectrogram)
print("Fingerprint erstellt:", fingerprint)
#Lied.store_fingerprint(filename, fingerprint, name="Cantina Song")
erkannter_song = Lied.recognize_song(fingerprint)
