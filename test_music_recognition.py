import scipy.io.wavfile as wavfile
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf

def audio_aufnehmen(dauer=10, samplerate=44100, dateiname="aufnahme.wav"):
        print(f"Aufnahme startet für {dauer} Sekunden...")
        audio = sd.rec(int(dauer * samplerate), samplerate=samplerate, channels=1, dtype="float32")
        sd.wait()
        sf.write(dateiname, audio, samplerate)
        print(f"Aufnahme beendet. Datei gespeichert als {dateiname}")


def audio_plot(datei):

    samplerate, data = wavfile.read(datei)

    # Zeitvektor erstellen
    zeit = np.arange(0, len(data)) / samplerate

    # Zeit-Amplituden-Plot
    plt.subplot(2, 1, 1)
    plt.plot(zeit, data)
    plt.xlabel('Zeit (s)')
    plt.ylabel('Amplitude')
    plt.title('Audio-Daten')

    # Spektrogramm
    plt.subplot(2, 1, 2)
    plt.specgram(data, Fs=samplerate)
    plt.xlabel('Zeit (s)')
    plt.ylabel('Frequenz (Hz)')
    plt.title('Spektrogramm')

    plt.tight_layout()
    plt.show()



#audio_aufnehmen(dateiname='test_1.wav')
audio_plot('Songs/CantinaBand3.wav')
audio_plot('Songs/CantinaBand60.wav')


