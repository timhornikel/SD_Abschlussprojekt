import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter
import sqlite3
import settings as set

class Lied:
    '''
    Klasse für die Verarbeitung von Audiodateien
    '''

    def __init__(self, titel, interpret, album, dateipfad):
        self.titel = titel
        self.interpret = interpret
        self.album = album
        self.dateipfad = dateipfad

    def process_audio(self):
        '''
        Audio-Datei laden, Spectogramm erstellen und Peaks finden
        '''

        # Audiodatei laden und spectogramm erstellen
        y, sr = librosa.load(self.dateipfad, sr=set.SAMPLE_RATE)  # Setzen der Samplingrate auf den festen Wert
        original_spectogram = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=set.FFT_WINDOW_SIZE)), ref=np.max)
        filtered_spectogram = maximum_filter(original_spectogram, size=(set.PEAK_BOX_SIZE, set.PEAK_BOX_SIZE+5), mode='constant', cval=-np.inf)

        # Frames berechnen (Anzahl + Dauer)
        num_frames = original_spectogram.shape[1]
        total_duration = librosa.get_duration(y=y, sr=sr)
        frame_duration = total_duration / num_frames
        times = np.arange(0, num_frames) * frame_duration
        
        # Finde die Indizes der Peaks im gefilterten Spectogram
        peaks_indices = np.argwhere((original_spectogram == filtered_spectogram) & (original_spectogram > set.MIN_DB_FILTER))

        # Erstellen der Plots
        fig, ax = plt.subplots(3, 1, figsize=(10, 12))

        # Plot originales Spectogram
        img_original = librosa.display.specshow(original_spectogram, sr=set.SAMPLE_RATE, x_axis='s', y_axis='log', ax=ax[0])
        ax[0].set_title('Original Spectrogram')
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel('Frequency')
        plt.colorbar(img_original, ax=ax[0], format='%+2.0f dB')

        # Plot gefiltertes Spectogram
        img_filtered = librosa.display.specshow(filtered_spectogram, sr=set.SAMPLE_RATE, x_axis='s', y_axis='log', ax=ax[1])
        ax[1].set_title('Filtered Spectrogram (Peaks Highlighted)')
        ax[1].set_xlabel('Time')
        ax[1].set_ylabel('Frequency')
        plt.colorbar(img_filtered, ax=ax[1], format='%+2.0f dB')

        # Scatterplot der Peaks
        ax[2].scatter(times[peaks_indices[:, 1]], peaks_indices[:, 0], c='r', marker='o', s=5)
        ax[2].set_title('Constellation Map (Downsampled)')
        ax[2].set_xlabel('Time')
        ax[2].set_ylabel('Frequency')

        # Hashes erstellen
        hashes = Lied.create_hashes(peaks_indices, times)
        return fig, peaks_indices, times, hashes

    @staticmethod
    def create_hashes(peaks_indices, times):
        '''
        Erstellt Hashes aus den Peaks
        '''

        # Sample settings for demonstration
        TARGET_T = 5
        TARGET_F = 100
        TARGET_START_DELAY = 1

        time_resolution = TARGET_T
        frequency_resolution = TARGET_F
        delay = TARGET_START_DELAY

        hashes = []
        for i, anchor_point in enumerate(peaks_indices):
            anchor_time = times[anchor_point[1]]  # Zeitpunkt des Ankerpunkts
            for j, target_point in enumerate(peaks_indices[i + 1:], start=i+1):
                target_time = times[target_point[1]]  # Zeitpunkt des Zielpeaks
                # Überprüfen, ob der Zeitpunkt des Zielpeaks später als der Zeitpunkt des Ankerpunkts ist
                if target_time > anchor_time:
                    # Prüfen, ob der Ziel-Punkt innerhalb der Zeit- und Frequenzauflösung um den Ankerpunkt liegt
                    if (target_point[0] - anchor_point[0]) >= delay and abs(target_point[0] - anchor_point[0] - delay) <= time_resolution and abs(target_point[1] - anchor_point[1]) <= frequency_resolution:
                        # Hash-Tupel erstellen: (freq_A, freq_B, zeit_delta, Zeitpunkt von Ankerpunkt)
                        hash_tuple = (int(anchor_point[1]), int(target_point[1]), target_time - anchor_time, anchor_time)
                        # Das Hash-Tupel der Liste der Hashes hinzufügen
                        hashes.append(hash_tuple)
        return hashes

    def save_to_db(self, hashes):
        '''
        Speichert die Hashes in der MusicRecognition.db SQLite-Datenbank
        '''

        # Verbindung zur SQLite-Datenbank herstellen
        conn = sqlite3.connect('MusicRecognition.db')
        c = conn.cursor()

        # Datenbanktabelle erstellen, wenn sie nicht existiert
        c.execute('''CREATE TABLE IF NOT EXISTS {}_fingerprint
                     (anchor_freq INTEGER, target_freq INTEGER, delta_time REAL, anchor_time REAL, Title TEXT, Interpret TEXT, Album TEXT)'''.format(self.titel))

        # Hashes in die Datenbank einfügen
        c.executemany('INSERT INTO {}_fingerprint VALUES (?,?,?,?,?,?,?)'.format(self.titel), [(anchor, target, delta_time, anchor_time, self.titel, self.interpret, self.album) for anchor, target, delta_time, anchor_time in hashes])

        # Änderungen in der Datenbank speichern
        conn.commit()

        # Verbindung zur Datenbank trennen
        conn.close()
    
    def show_plot(self, figure):
        '''
        Zeigt den Plot an
        '''

        plt.show()  

    def get_hashes(self):
        '''
        Holt die Hashes aus der Datenbank
        '''

        # Verbindung zur SQLite-Datenbank herstellen
        conn = sqlite3.connect('MusicRecognition.db')
        c = conn.cursor()

        # Hashes aus der Datenbank abfragen
        c.execute('SELECT * FROM {}_fingerprint'.format(self.titel))
        hashes = c.fetchall()

        # Verbindung zur Datenbank trennen
        conn.close()

        return hashes

if __name__ == '__main__':
    #lied = Lied('Cantina_band', 'Yoda', 'Star_Wars', 'songs/CantinaBand60.wav')
    #fig, peak_indices, times, hashes = lied.process_audio()
    #lied.save_to_db(hashes)
    #lied.show_plot(fig)
    #print('Lied 1 geladen')
    #lied2 = Lied('StarWars', 'Obi_Wan_Kenobi', 'Star_Wars', 'songs/StarWars60.wav')
    #fig2, peak_indices2, times2, hashes2 = lied2.process_audio()
    #lied2.save_to_db(hashes2)
    #lied2.show_plot(fig2)
    #print('Lied 2 geladen')

    # Liedausschnitt erkennen
    pass