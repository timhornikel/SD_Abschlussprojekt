import os
import requests
from PIL import Image

def get_album_cover(song_title, artist):
    query = f"{song_title} {artist} album cover"
    response = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json")
    data = response.json()

    if 'Image' in data['Abstract']:
        image_url = data['Abstract']['Image']
        image_response = requests.get(image_url, stream=True)
        image_response.raise_for_status()

        with open(f"{song_title}_{artist}_cover.png", "wb") as image_file:
            image_file.write(image_response.content)
        
        return f"{song_title}_{artist}_cover.png"
    else:
        return None


if __name__ == '__main__':
    pass