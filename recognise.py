import os
import logging
from multiprocessing import Pool, Lock, current_process
import numpy as np
from tinytag import TinyTag
from record import record_audio
from fingerprinting import fingerprint_file, fingerprint_audio
from storage import store_song, get_matches, get_info_for_song_id, song_in_db, checkpoint_db, get_song_history, save_song_history
import setting
import pandas as pd

KNOWN_EXTENSIONS = ["mp3", "wav", "flac", "m4a"]


def register_song(filename, artist, album, title):
    """Register a song in the database."""
    if song_in_db(filename):
        print(f"{filename} already in database")
        return
    hashes = fingerprint_file(filename)
    song_info = (artist, album, title)
    try:
        logging.info(f"{current_process().name} waiting to write {filename}")
        with lock:
            logging.info(f"{current_process().name} writing {filename}")
            store_song(hashes, song_info)
            logging.info(f"{current_process().name} wrote {filename}")
    except NameError:
        logging.info(f"Single-threaded write of {filename}")
        # running single-threaded, no lock needed
        store_song(hashes, song_info)


def register_directory(path):
    """Register a directory of songs in the database."""
    def pool_init(l):
        """Initialise the lock for the pool."""
        global lock
        lock = l
        logging.info(f"Pool init in {current_process().name}")

    to_register = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.split('.')[-1] not in KNOWN_EXTENSIONS:
                continue
            file_path = os.path.join(path, root, f)
            to_register.append(file_path)
    l = Lock()
    with Pool(setting.NUM_WORKERS, initializer=pool_init, initargs=(l,)) as p:
        p.map(register_song, to_register)
    # speed up future reads
    checkpoint_db()


def score_match(offsets):
    """Scores a set of offsets for a song."""
    # Use bins spaced 0.5 seconds apart
    binwidth = 0.5
    tks = list(map(lambda x: x[0] - x[1], offsets))
    hist, _ = np.histogram(tks,
                           bins=np.arange(int(min(tks)),
                                          int(max(tks)) + binwidth + 1,
                                          binwidth))
    return np.max(hist)


def best_match(matches):
    """Finds the best match from a set of matches."""
    matched_song = None
    best_score = 0
    for song_id, offsets in matches.items():
        if len(offsets) < best_score:
            continue
        score = score_match(offsets)
        if score > best_score:
            best_score = score
            matched_song = song_id
    return matched_song


def recognise_song(filename):
    """Recognises a song from a file."""
    hashes = fingerprint_file(filename)
    matches = get_matches(hashes)
    matched_song = best_match(matches)
    info = get_info_for_song_id(matched_song)
    save_song_history(info[2], info[1], info[0])
    if info is not None:
        return info
    return matched_song


def listen_to_song(filename=None):
    """Listens to a song and recognises it."""
    audio = record_audio(filename=filename)
    hashes = fingerprint_audio(audio)
    matches = get_matches(hashes)
    matched_song = best_match(matches)
    info = get_info_for_song_id(matched_song)
    save_song_history(info[2], info[1], info[0])
    if info is not None:
        return info
    return matched_song


def display_song_history():
    """Get the song history from the database."""
    history = get_song_history()
    df = pd.DataFrame(history, columns=["artist", "album", "title"])
    if df.empty:
        return "No song history"
    else:
        return df


def get_youtube_search_url(name, artist):
    """Get the youtube search link for a song."""
    youtube_search_url = f'https://www.youtube.com/results?search_query={name} {artist}'
    return youtube_search_url


def get_spotify_search_url(name, artist):
    """Get the spotify search link for a song."""
    spotify_search_url = f'https://open.spotify.com/search/{name} {artist}'
    return spotify_search_url



if __name__ == "__main__":
    pass
    path = "song/Desachantee.wav"
    register_song(path, "Kate Ryan", "Desachantée", "Desachantée")
    print(recognise_song(path))
    
