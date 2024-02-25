SAMPLE_RATE = 22050
"""The sample rate to use for audio processing."""

PEAK_BOX_SIZE = 30
"""The size of the region around each peak to consider when finding peaks in a spectrogram."""

POINT_EFFICIENCY = 0.8
"""The proportion of peaks to return when finding peaks in a spectrogram."""

TARGET_START = 0.05
"""The start of the target zone in the spectrogram."""

TARGET_T = 1.8
"""The width of the target zone (seconds (s)) in the spectrogram."""

TARGET_F = 4000
"""The height of the target zone (frequency (Hz)) in the spectrogram."""

FFT_WINDOW_SIZE = 0.2
"""The size of the window to use for the FFT."""

DB_PATH = "music_recognition.db"
"""The path to the database file."""

NUM_WORKERS = 24
"""The number of workers to use when registering songs."""

def test():
    print('Im setting.py')

if __name__ == "__main__":
    print('Im module setting')