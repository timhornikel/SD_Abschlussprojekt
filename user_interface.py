import streamlit as st
from user.users import User
import recognise as mr
import matplotlib.pyplot as plt
import time
import tempfile



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

    st.success('Sie haben sich erfolreich abgemeldet. Sie können die App jetzt schließen oder sich im Nutzermanagement erneut anmelden.')



# Sidebar
st.sidebar.image('pictures/Abschlussprojekt_Logo_userinterface.png', width=200)
st.sidebar.title('Wählen Sie aus')
option = st.sidebar.radio('Navigation', ['Nutzermanagement', 'Musik hochladen', 'Musik erkennen', 'About', 'Kontakt', 'Abmelden'])



# Startseite
if option == 'Nutzermanagement':
    st.title(':busts_in_silhouette: Nutzermanagement')
    if st.session_state.logged_in_user:
        st.header(f':male-student: Angemeldeter Benutzer: {st.session_state.logged_in_user}')
        st.divider()
        st.info('Sie können nun Musik hochladen oder erkennen. Klicken Sie auf die entsprechende Option in der Sidebar.')
        st.warning('Um sich umzumelden klicken sie erst auf "Abmelden" und kommen dann wieder in das Nutzermanagement')
    elif st.session_state.logged_in_user is None:
        st.header('Sie sind nicht angemeldet')
        st.write('Bitte melden Sie sich an oder registrieren Sie sich, um die App zu nutzen.')
        st.divider()

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
                    st.rerun()

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
            st.rerun()



# Musikseite
elif option == 'Musik hochladen':
    if st.session_state.logged_in_user:
        st.title(':new: Musik hochladen')
        st.header(f':male-student: Angemeldeter Benutzer: {st.session_state.logged_in_user}')
        st.divider()
        uploaded_file = st.file_uploader("Wählen Sie eine Musikdatei aus", type=["mp3", "wav"])
        if uploaded_file is not None:
            try:
                # Create a temporary file with the appropriate extension
                tfile = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                tfile.write(uploaded_file.getvalue())
                tfile.close()

                title = st.text_input('Titel')
                artist = st.text_input('Künstler')
                album = st.text_input('Album')
                if st.button('Hochladen'):
                    with st.spinner("Hochladen der Musikdatei..."):
                        mr.register_song(tfile.name, artist, album, title)  # Pass the temporary file path
                        progress_bar = st.progress(0)
                        for i in range(21):
                            time.sleep(0.1)
                            progress_bar.progress(i*5, text=f'Musik wird verarbeitet. Fortschritt: {i*5}%')
                        time.sleep(0.8)
                        progress_bar.empty()
                    st.success('Musikdatei erfolgreich hochgeladen!')
            except Exception as e:
                st.error(f'Fehler beim Hochladen der Musikdatei: {e}')
    else:
        st.warning("Bitte melden Sie sich zuerst im Nutzermanagement an.")

elif option == 'Musik erkennen':
    if st.session_state.logged_in_user:
        st.title(f':studio_microphone: Musik erkennen')
        st.header(f':male-student: Angemeldeter Benutzer: {st.session_state.logged_in_user}')
        st.divider()
        recognition_option = st.radio("Wählen Sie eine Erkennungsoption:", [":file_folder: Datei hochladen", ":microphone: Über Mikrofon erkennen"])
        st.divider()
        if recognition_option == ":file_folder: Datei hochladen":
            uploaded_file = st.file_uploader("Wählen Sie eine Musikdatei aus", type=["wav"])
            if uploaded_file is not None:
                try:
                    # Create a temporary file
                    tfile = tempfile.NamedTemporaryFile(suffix=".wav" ,delete=False) 
                    tfile.write(uploaded_file.getvalue())
                    tfile.close()

                    if st.button('Erkennen'):
                        st.write("Musik wird verarbeitet...")
                        progress_bar = st.progress(0)
                        for i in range(21):
                            time.sleep(0.1)
                            progress_bar.progress(i*5, text=f'Musik wird verarbeitet. Fortschritt: {i*5}%')
                        time.sleep(0.8)
                        progress_bar.empty()
                        song = mr.recognise_song(tfile.name)  # Pass the temporary file path
                        mr.show_song_info(song)
                except Exception as e:
                    st.error(f'Fehler beim Erkennen der Musikdatei: {e}')
        elif recognition_option == ":microphone: Über Mikrofon erkennen":
            try:
                if st.button('Starten'):
                    with st.spinner("Starte Aufnahme..."):
                        song = mr.listen_to_song()
                        st.empty()
                    progress_bar = st.progress(0)
                    for i in range(21):
                        time.sleep(0.1)
                        progress_bar.progress(i*5, text=f'Musik wird verarbeitet. Fortschritt: {i*5}%')
                    time.sleep(0.8)
                    progress_bar.empty()
                    mr.show_song_info(song)
            except Exception as e:
                st.error(f'Fehler beim Erkennen der Musikdatei: {e}')
    else:
        st.warning("Bitte melden Sie sich zuerst im Nutzermanagement an.")



# About und Kontakt
elif option == 'About':
    st.title(':book: About')
    st.markdown(
        """
        <div>
            <h1 style="font-size: 24px; text-align: left;">Kurzbeschreibung der App</h1>
            <p>Die App wurde als Abschlussprojekt der Lehrveranstaltung "Softwaredesign" am MCI entwickelt. Sie ermöglicht das Registrieren, Anmelden oder Fortsetzen als Gast.</p>
            <ol>
                <li>Schritt 1: Loggen Sie sich ein oder fahren Sie als Gast fort.</li>
                <li>Schritt 2: Wählen Sie aus, ob Sie ein Lied hochladen oder erkennen möchten.</li>
                <li>Schritt 3: Um ein Lied hochzuladen, klicken Sie auf "Musik hochladen" und geben Sie Titel, Album und Interpret an.</li>
                <li>Schritt 4: Erkennen Sie ein Lied durch Auswahl einer .wav-Datei oder Aufnahme über das Mikrofon (8 Sekunden).</li>
                <li>Schritt 5: Wenn ein Lied erkannt wurde, werden Informationen (Titel, Album, Interpret) angezeigt. Zusätzlich erhalten Sie Links zu Spotify und Youtube, um das Lied zu hören. Ein Youtube-Video wird ebenfalls eingebettet, um das Lied direkt in der App anzuhören. Zudem werden die letzten 5 erkannten Lieder in der Historie angezeigt.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )


elif option == 'Kontakt':
    st.title('Kontakt :girl: :boy: :boy:')
    st.markdown(
        """
        Hier finden Sie unsere Kontaktinformationen:
        - :girl: **Sandra Grüner** | E-Mail: [s.gruener@mci4me.at](mailto:s.gruener@mci4me.at)
        - :boy: **Tim Hornikel** | E-Mail: [t.hornikel@mci4me.at](mailto:t.hornikel@mci4me.at)
        - :boy: **Oskar Klöpfer** | E-Mail: [o.kloepfer@mci4me.at](mailto:o.kloepfer@mci4me.at)
        """,
        unsafe_allow_html=True
    )

elif option == 'Abmelden':
    logout()
