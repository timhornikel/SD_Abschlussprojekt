import requests
import streamlit as st
import recognise


def get_album_cover_from_duckduckgo_api(artist, song):
    """Get the album cover from the DuckDuckGo API."""
    url = f"https://api.duckduckgo.com/?q={artist}+{song}+album+cover&format=json"
    response = requests.get(url)
    data = response.json()
    return data["Image"] if data["Image"] else None

st.title("Picture of the album cover")
artist = st.text_input("Artist")
song = st.text_input("Song")
if st.button("Get album cover"):
    try:
        if artist and song:
            album_cover = get_album_cover_from_duckduckgo_api(artist, song)
            if album_cover:
                st.image(album_cover, width=300)
            else:
                st.error("No album cover found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

#get metadata for a song
st.title("Metadata for a song")
if st.button("Get metadata"):
    if song and artist:
        try:
            song = recognise.get_meta_data_for_song(song, artist)
            if song:
                st.write(song)
            else:
                st.error("No metadata found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == '__main__':
    pass