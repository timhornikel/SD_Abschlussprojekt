import uuid
import numpy as np
import music_recognition.setting as setting
from pydub import AudioSegment
from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter
import setting


def generate_spectogram(audio):
    """Generates a spectrogram from audio."""
    nperseg = int(setting.SAMPLE_RATE * setting.FFT_WINDOW_SIZE)
    return spectrogram(audio, setting.SAMPLE_RATE, nperseg=nperseg)


def convert_file_to_spectogram(filename):
    """Converts a file to a spectrogram."""
    a = AudioSegment.from_file(filename).set_channels(1).set_frame_rate(setting.SAMPLE_RATE)
    audio = np.frombuffer(a.raw_data, np.int16)
    return generate_spectogram(audio)


def get_peaks(Sxx):
    """Finds peaks in a spectrogram."""
    data_max = maximum_filter(Sxx, size=setting.PEAK_BOX_SIZE, mode='constant', cval=0.0)
    peak_goodmask = (Sxx == data_max)
    y_peaks, x_peaks = peak_goodmask.nonzero()
    peak_values = Sxx[y_peaks, x_peaks]
    i = peak_values.argsort()[::-1]
    j = [(y_peaks[idx], x_peaks[idx]) for idx in i]
    total = Sxx.shape[0] * Sxx.shape[1]
    peak_target = int((total / (setting.PEAK_BOX_SIZE**2)) * setting.POINT_EFFICIENCY)
    return j[:peak_target]


def idxs_to_tf_pairs(idxs, t, f):
    """Converts a list of indices to a list of time/frequency pairs."""
    return np.array([(f[i[0]], t[i[1]]) for i in idxs])


def generate_hash_point_pair(p1, p2):
    """Generates a hash from a pair of points."""
    return hash((p1[0], p2[0], p2[1]-p2[1]))


def generate_target_zone(anchor, points, width, height, t):
    """Generates the target zone for a peak."""
    x_min = anchor[1] + t
    x_max = x_min + width
    y_min = anchor[0] - (height*0.5)
    y_max = y_min + height
    for point in points:
        if point[0] < y_min or point[0] > y_max:
            continue
        if point[1] < x_min or point[1] > x_max:
            continue
        yield point


def generate_hash_points(points, filename):
    """Generates hashes from a list of points."""
    hashes = []
    song_id = uuid.uuid5(uuid.NAMESPACE_OID, filename).int
    for anchor in points:
        for target in generate_target_zone(
            anchor, points, setting.TARGET_T, setting.TARGET_F, setting.TARGET_START
        ):
            hashes.append((
                generate_hash_point_pair(anchor, target),
                anchor[1],
                str(song_id)
            ))
    return hashes


def fingerprint_file(filename):
    """Generate hashes for an audio file."""
    f, t, Sxx = convert_file_to_spectogram(filename)
    peaks = get_peaks(Sxx)
    peaks = idxs_to_tf_pairs(peaks, t, f)
    return generate_hash_points(peaks, filename)


def fingerprint_audio(frames):
    """Generate hashes for audio frames."""
    f, t, Sxx = generate_spectogram(frames)
    peaks = get_peaks(Sxx)
    peaks = idxs_to_tf_pairs(peaks, t, f)
    return generate_hash_points(peaks, "recorded")