import uuid
import sqlite3
from collections import defaultdict
from contextlib import contextmanager
import setting
import pandas as pd

@contextmanager
def get_cursor():
    """Get a cursor for the database."""
    try:
        conn = sqlite3.connect(setting.DB_PATH, timeout=30)
        yield conn, conn.cursor()
    finally:
        conn.close()


def setup_db():
    """Initialise the database."""
    with get_cursor() as (conn, c):
        c.execute("CREATE TABLE IF NOT EXISTS hash (hash int, offset real, song_id text)")
        c.execute("CREATE TABLE IF NOT EXISTS song_info (artist text, album text, title text, song_id text)")
        c.execute("CREATE TABLE IF NOT EXISTS song_history (Id INTEGER PRIMARY KEY AUTOINCREMENT, title text, album text, artist text)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_hash ON hash (hash)")
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA wal_autocheckpoint=300")

def delete_table(table_name):
    """delete a table from the database"""
    with get_cursor() as (conn, c):
        c.execute(f"DROP TABLE IF EXISTS {table_name}")    


def get_song_history():
    """get the last 5 songs recognised
    
    Returns:
        list: The last 5 songs recognised.
    """
    with get_cursor() as (conn, c):
        c.execute("SELECT title, album, artist FROM song_history ORDER BY Id DESC LIMIT 5")
        return c.fetchall()


def save_song_history(title, album, artist):
    """save a song in the database in song_history table"""
    with get_cursor() as (conn, c):
        c.execute("INSERT INTO song_history (title, album, artist) VALUES (?, ?, ?)", (title, album, artist))
        conn.commit()


def checkpoint_db():
    with get_cursor() as (conn, c):
        c.execute("PRAGMA wal_checkpoint(FULL)")


def song_in_db(filename):
    """Check if a song is already in the database.
    
    Returns:
        bool: True if the song is in the database, False otherwise.
    """
    with get_cursor() as (conn, c):
        song_id = str(uuid.uuid5(uuid.NAMESPACE_OID, filename).int)
        c.execute("SELECT * FROM song_info WHERE song_id=?", (song_id,))
        return c.fetchone() is not None


def store_song(hashes, song_info):
    """Store a song in the database."""
    if len(hashes) < 1:
        return
    with get_cursor() as (conn, c):
        c.executemany("INSERT INTO hash VALUES (?, ?, ?)", hashes)
        insert_info = [i if i is not None else "Unknown" for i in song_info]
        c.execute("INSERT INTO song_info VALUES (?, ?, ?, ?)", (*insert_info, hashes[0][2]))
        conn.commit()


def get_matches(hashes, threshold=5):
    """Get matches for a set of hashes.
    
    Returns:
        dict: The matches.
    """
    h_dict = {}
    for h, t, _ in hashes:
        h_dict[h] = t
    in_values = f"({','.join([str(h[0]) for h in hashes])})"
    with get_cursor() as (conn, c):
        c.execute(f"SELECT hash, offset, song_id FROM hash WHERE hash IN {in_values}")
        results = c.fetchall()
    result_dict = defaultdict(list)
    for r in results:
        result_dict[r[2]].append((r[1], h_dict[r[0]]))
    return result_dict


def get_info_for_song_id(song_id):
    """Get song info for a song_id.
    
    Returns:
        tuple: The song info.
    """
    with get_cursor() as (conn, c):
        c.execute("SELECT artist, album, title FROM song_info WHERE song_id = ?", (song_id,))
        return c.fetchone()
    


if __name__ == "__main__":
    #setup_db()
    pass