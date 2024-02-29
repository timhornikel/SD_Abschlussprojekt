from duckduckgo_search import DDGS
import requests
from urllib.parse import quote_plus



def get_album_cover(title, interpret):
    """get the album cover for a song."""    
    keywords = f"{title}{interpret} Albumcover"

    # Ergebnisse der Bildersuche abrufen
    with DDGS() as ddgs:
        ddgs_images_gen = ddgs.images(
            keywords,
            region="wt-wt",
            safesearch="off",
            size=None,
            color=None,
            type_image=None,
            layout=None,
            license_image=None,
            max_results=1,  # Anzahl der maximalen Ergebnisse
        )
        
        # Durch die Ergebnisse iterieren und die URL des ersten Bildes zurückgeben
        for result in ddgs_images_gen:
            return result['image']
    
    # Wenn keine Ergebnisse gefunden werden
    return None


def get_youtube_video(title, artist):
    """Get the youtube video for a song."""
    query = f"{title} {artist} official music video"
    url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    response = requests.get(url)
    if response.status_code == 200:
        video_id = None
        start_index = response.text.find('{"videoRenderer":{"videoId":"')
        if start_index != -1:
            end_index = response.text.find('"', start_index + 30)
            video_id = response.text[start_index + 29:end_index]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
    return None


def get_youtube_search_url(name, artist):
    """Get the youtube search link for a song."""
    youtube_search_url = f'https://www.youtube.com/results?search_query={name} {artist}'
    return youtube_search_url


def get_spotify_search_url(name, artist):
    """Get the spotify search link for a song."""
    spotify_search_url = f'https://open.spotify.com/search/{name} {artist}'
    return spotify_search_url