import streamlit as st
from user.users import User
import recognise as mr
import links

# Initialisierung der Session-Variablen
if 'state' not in st.session_state:
    st.session_state.state = 'start'
    st.session_state.username = ''
    st.session_state.email = ''
    st.session_state.password = ''
    st.session_state.logged_in_user = None
    st.session_state.show_about = False
    st.session_state.show_contact = False

# Funktion für Benachrichtigungen
def notify(message, type='info'):
    if type == 'info':
        st.sidebar.info(message)
    elif type == 'success':
        st.success(message)
    elif type == 'error':
        st.sidebar.error(message)

# Hinweis nach Anmeldung
def display_login_message():
    st.info("Bitte wählen Sie in der Sidebar nun 'Musik hochladen' oder 'Musik erkennen'.")

# Abmeldung
def logout():
    st.session_state.logged_in_user = None
    st.session_state.state = 'start'
    st.session_state.username = ''
    st.session_state.email = ''
    st.session_state.password = ''
    st.session_state.show_about = False
    st.session_state.show_contact = False
    st.sidebar.warning("Bitte melden Sie sich an, registrieren Sie sich oder setzen Sie die Sitzung als Gast fort.")

    action = st.radio('Wählen Sie Ihre Option:', ['Anmelden', 'Registrieren', 'Als Gast anmelden'])

    if action == 'Anmelden':
        st.title('Anmeldung')
        st.session_state.username = st.text_input('Benutzername', st.session_state.username)
        st.session_state.password = st.text_input('Passwort', type='password', value=st.session_state.password)
        
        if st.button('Anmelden'):
            if User.anmelden(st.session_state.username, st.session_state.password):
                st.session_state.logged_in_user = st.session_state.username
                notify(f'Erfolgreich als {st.session_state.username} angemeldet!', type='success')
                st.session_state.username = ''
                st.session_state.password = ''
                display_login_message()

    elif action == 'Registrieren':
        st.title('Registrierung')
        st.session_state.username = st.text_input('Benutzername', st.session_state.username)
        st.session_state.email = st.text_input('E-Mail', st.session_state.email)
        st.session_state.password = st.text_input('Passwort', type='password', value=st.session_state.password)
        
        if st.button('Registrieren'):
            if User.benutzer_existiert(st.session_state.username):
                notify("Benutzername bereits vergeben. Bitte wählen Sie einen anderen.", type='error')
            else:
                benutzer = User(st.session_state.username, st.session_state.email, st.session_state.password)
                benutzer.speichern()
                notify(f'Benutzer {st.session_state.username} erfolgreich registriert!', type='success')
                st.session_state.username = ''
                st.session_state.email = ''
                st.session_state.password = ''
                display_login_message()

    elif action == 'Als Gast anmelden':
        st.session_state.logged_in_user = 'Gast'
        notify('Erfolgreich als Gast angemeldet!', type='success')
        display_login_message()

# Sidebar
st.sidebar.image('pictures/Abschlussprojekt_Logo_userinterface.png', width=200)
st.sidebar.title('Wählen Sie aus')
option = st.sidebar.radio('Navigation', ['Nutzermanagement', 'Musik hochladen', 'Musik erkennen', 'About', 'Kontakt', 'Abmelden'])

# Startseite
if option == 'Nutzermanagement':
    if st.session_state.logged_in_user is None:
        st.sidebar.warning('Bitte melden Sie sich an, registrieren Sie sich oder setzen Sie die Sitzung als Gast fort.')

        action = st.radio('Wählen Sie Ihre Option:', ['Anmelden', 'Registrieren', 'Als Gast anmelden'])

        if action == 'Anmelden':
            st.title('Anmeldung')
            st.session_state.username = st.text_input('Benutzername', st.session_state.username)
            st.session_state.password = st.text_input('Passwort', type='password', value=st.session_state.password)
            
            if st.button('Anmelden'):
                if User.anmelden(st.session_state.username, st.session_state.password):
                    st.session_state.logged_in_user = st.session_state.username
                    notify(f'Erfolgreich als {st.session_state.username} angemeldet!', type='success')
                    st.session_state.username = ''
                    st.session_state.password = ''
                    display_login_message()

        elif action == 'Registrieren':
            st.title('Registrierung')
            st.session_state.username = st.text_input('Benutzername', st.session_state.username)
            st.session_state.email = st.text_input('E-Mail', st.session_state.email)
            st.session_state.password = st.text_input('Passwort', type='password', value=st.session_state.password)
            
            if st.button('Registrieren'):
                if User.benutzer_existiert(st.session_state.username):
                    notify("Benutzername bereits vergeben. Bitte wählen Sie einen anderen.", type='error')
                else:
                    benutzer = User(st.session_state.username, st.session_state.email, st.session_state.password)
                    benutzer.speichern()
                    notify(f'Benutzer {st.session_state.username} erfolgreich registriert!', type='success')
                    st.session_state.username = ''
                    st.session_state.email = ''
                    st.session_state.password = ''
                    display_login_message()

        elif action == 'Als Gast anmelden':
            st.session_state.logged_in_user = 'Gast'
            notify('Erfolgreich als Gast angemeldet!', type='success')
            display_login_message()

# Musikseite
elif option == 'Musik hochladen':
    if st.session_state.logged_in_user:
        st.title('Musik hochladen')
        st.write(f'Angemeldeter Benutzer: {st.session_state.logged_in_user}')
        uploaded_file = st.file_uploader("Wählen Sie eine Musikdatei aus", type=["mp3", "wav"])
        if uploaded_file is not None:
            try:
                title = st.text_input('Titel')
                artist = st.text_input('Künstler')
                album = st.text_input('Album')
                if st.button('Hochladen'):
                    mr.register_song(uploaded_file, artist, album, title)
                    st.success('Musikdatei erfolgreich hochgeladen!')
            except Exception as e:
                st.error(f'Fehler beim Hochladen der Musikdatei: {e}')
    else:
        st.warning("Bitte melden Sie sich zuerst an.")

elif option == 'Musik erkennen':
    if st.session_state.logged_in_user:
        st.title('Musik erkennen')
        st.write(f'Angemeldeter Benutzer: {st.session_state.logged_in_user}')
        recognition_option = st.radio("Wählen Sie eine Erkennungsoption:", ["Datei hochladen", "Über Mikrofon erkennen"])
        if recognition_option == "Datei hochladen":
            uploaded_file = st.file_uploader("Wählen Sie eine Musikdatei aus", type=["mp3", "wav"])
            if uploaded_file is not None:
                try:
                    song = mr.recognise_song(uploaded_file)
                    st.write(f"Titel: {song[2]}, Album: {song[1]}, Künstler: {song[0]}")
                except Exception as e:
                    st.error(f'Fehler beim Erkennen der Musikdatei: {e}')
        elif recognition_option == "Über Mikrofon erkennen":
            try:
                if st.button('Starten'):
                    song = mr.listen_to_song()
                    st.header("Erkannter Song")
                    st.write(f"Der erkannte song: {song[2]} aus dem Ablum: {song[1]} von {song[0]} wurde erkannt.")
                    youtuba_link = mr.get_youtube_search_url(song[2], song[0])
                    spotify_link = mr.get_spotify_search_url(song[2], song[0])
                    st.link_button(url=youtuba_link, label='Öffne YouTube Video')
                    st.link_button(url=spotify_link, label='Öffne Spotify Lied')
                    st.header("Song History")
                    history = mr.display_song_history()
                    st.dataframe(history)              
            except Exception as e:
                st.error(f'Fehler beim Erkennen der Musikdatei: {e}')
    else:
        st.warning("Bitte melden Sie sich zuerst an.")

# About und Kontakt
elif option == 'About':
    st.title('About')
    st.markdown(
        """
        <div>
          <p>Hier finden Sie eine kurze Beschreibung zur App.</p>
          <p>Die App wurde im Rahmen des Abschlussprojekts der Lehrveranstaltung "Softwaredesign" am MCI entwickelt.</p>
          <p>Die App ermöglicht es, dass sich als Nutzer registrieren, anmelden oder als Gast fortsetzen können.</p>
          <ol>
            <li>Schritt 1: Fahren Sie als Gast fort oder melden Sie sich an. Wenn Sie noch keinen Account haben, registrieren Sie sich.</li>
            <li>Schritt 2: Wählen Sie aus, ob Sie ein Lied hochladen möchten oder ein Lied erkennen möchten.</li>
            <li>Schritt 3: Um ein Lied hochzuladen, klicken Sie auf "Musik hochladen" und wählen Sie das Lied aus. Geben sie dazu noch den Titel, das Album und den Interpreten an</li>
            <li>Schritt 4: Um ein Lied zu erkennen, klicken Sie auf "Musik erkennen" und wählen Sie aus ob die das Lied mit einer Datei oder mit dem Microfon erkennen wollen.</li>
            <li>Schritt 5: Wenn das Lied erkannt wurde, wird der Titel, das Album und der Interpret angezeigt.</li>
          </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

elif option == 'Kontakt':
    st.title('Kontakt')
    st.markdown(
        """
        Hier finden Sie unsere Kontaktinformationen:
        - **Sandra Grüner** | E-Mail: [s.gruener@mci4me.at](mailto:s.gruener@mci4me.at)
        - **Tim Hornikel** | E-Mail: [t.hornikel@mci4me.at](mailto:t.hornikel@mci4me.at)
        - **Oskar Klöpfer** | E-Mail: [o.kloepfer@mci4me.at](mailto:o.kloepfer@mci4me.at)
        """,
        unsafe_allow_html=True
    )

elif option == 'Abmelden':
    logout()