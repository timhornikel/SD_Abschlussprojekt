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
        st.info(message)
    elif type == 'success':
        st.success(message)
    elif type == 'error':
        st.error(message)



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
    # Überprüfen, ob ein Benutzer angemeldet ist
    if st.session_state.logged_in_user:
        st.header(f':male-student: Angemeldeter Benutzer: {st.session_state.logged_in_user}')
        st.divider()
        st.info('Sie können nun Musik hochladen oder erkennen. Klicken Sie auf die entsprechende Option in der Sidebar.')
        st.warning('Um sich umzumelden klicken sie erst auf "Abmelden" und kommen dann wieder in das Nutzermanagement')
    elif st.session_state.logged_in_user is None:
        st.header('Sie sind nicht angemeldet')
        st.write('Bitte melden Sie sich an oder registrieren Sie sich, um die App zu nutzen.')
        st.divider()

        action = st.radio('Wählen Sie Ihre Option:', ['Anmelden', 'Registrieren', 'Als Gast anmelden', 'Nutzer löschen'])

        # Anmeldung für für registrierte benutzer
        if action == 'Anmelden':
            st.title('Anmeldung')
            st.session_state.username = st.text_input('Benutzername', st.session_state.username)
            st.session_state.password = st.text_input('Passwort', type='password', value=st.session_state.password)
            
            if st.button('Anmelden'):
                if User.benutzer_existiert(st.session_state.username):
                    if User.anmelden(st.session_state.username, st.session_state.password):
                        st.session_state.logged_in_user = st.session_state.username
                        notify(f'Erfolgreich als {st.session_state.username} angemeldet!', type='success')
                        st.session_state.username = ''
                        st.session_state.password = ''
                        display_login_message()
                        st.rerun()
                    else:
                        notify(f"Anmeldung fehlgeschlagen. Bitte überprüfen Sie Ihre Anmeldedaten.", type='error')
                else:
                    notify(f"Benutzer {st.session_state.username} existiert nicht. Registrieren sie sich erst.", type='error')

        # Registrierungsmanagement zum anlegen neue benutzer
        elif action == 'Registrieren':
            st.title('Registrierung')
            st.session_state.username = st.text_input('Benutzername', st.session_state.username)
            st.session_state.email = st.text_input('E-Mail', st.session_state.email)
            st.session_state.password = st.text_input('Passwort', type='password', value=st.session_state.password)
            
            if st.button('Registrieren'):
                # Überprüfen, ob der Benutzername bereits existiert
                if User.benutzer_existiert(st.session_state.username):
                    notify("Benutzername bereits vergeben. Bitte wählen Sie einen anderen.", type='error')
                else:
                    # Lege Benutzer an wenn noch nicht vorhanden
                    benutzer = User(st.session_state.username, st.session_state.email, st.session_state.password)
                    benutzer.speichern()
                    notify(f'Benutzer {st.session_state.username} erfolgreich registriert!', type='success')
                    st.session_state.username = ''
                    st.session_state.email = ''
                    st.session_state.password = ''
                    notify('Nutzer erfolgreich angelegt, sie können sich jetzt anemelden', type='success')

        # Als gast anmelden für diejenigen, die sich nicht anmelden wollen
        elif action == 'Als Gast anmelden':
            st.session_state.logged_in_user = 'Gast'
            notify('Erfolgreich als Gast angemeldet!', type='success')
            display_login_message()
            st.rerun()
        
        # Löschen von Benutzern
        elif action == 'Nutzer löschen':
            st.title('Nutzer löschen')
            st.session_state.username = st.text_input('Benutzername', st.session_state.username)
            st.session_state.password = st.text_input('Passwort', type='password', value=st.session_state.password)

            if st.button('Nutzer löschen'):
                # Überprüfen, ob der Benutzer existiert
                if User.benutzer_existiert(st.session_state.username):
                    # Löschen wenn der Benutzer das richtige Passwort eingegeben hat -> Sicherheitsabfrage
                    if User.benutzer_loeschen(st.session_state.username, st.session_state.password):
                        notify(f'Benutzer {st.session_state.username} erfolgreich gelöscht!', type='success')
                        st.session_state.username = ''
                        st.session_state.password = ''
                    else:
                        notify(f"Benutzer {st.session_state.username} konnte nicht gelöscht werden. Bitte überprüfen Sie Ihre Anmeldedaten.", type='error')
                else:
                    notify(f"Benutzer {st.session_state.username} existiert nicht.", type='error')



# Musikseite
elif option == 'Musik hochladen':
    # Überprüfen, ob ein Benutzer angemeldet ist
    if st.session_state.logged_in_user:
        st.title(':new: Musik hochladen')
        st.header(f':male-student: Angemeldeter Benutzer: {st.session_state.logged_in_user}')
        st.divider()
        # File uploader für Musikdateien
        uploaded_file = st.file_uploader("Wählen Sie eine Musikdatei aus", type=["wav"])
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
                        # Lade den Song in die Datenbank hoch
                        mr.register_song(tfile.name, artist, album, title) 
                        # zeige Progressbar für die Bearbeitung
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
    # Überprüfen, ob ein Benutzer angemeldet ist
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
                    # temporäre Datei erstellen für 
                    tfile = tempfile.NamedTemporaryFile(suffix=".wav" ,delete=False) 
                    tfile.write(uploaded_file.getvalue())
                    tfile.close()

                    if st.button('Erkennen'):
                        # progress bar für die erkennung
                        progress_bar = st.progress(0)
                        for i in range(21):
                            time.sleep(0.1)
                            progress_bar.progress(i*5, text=f'Musik wird Hochgeladen. Fortschritt: {i*5}%')
                        time.sleep(0.8)
                        progress_bar.empty()
                        # Ansicht wenn die Musikerkennung länger läuft
                        with st.spinner("Erkennen der Musikdatei..."):
                            song = mr.recognise_song(tfile.name, st.session_state.logged_in_user)  # Pass the temporary file path
                            st.empty()
                            # Zeige die Musikinformationen
                        mr.show_song_info(song, st.session_state.logged_in_user)
                except Exception as e:
                    st.error(f'Fehler beim Erkennen der Musikdatei: {e}')
        elif recognition_option == ":microphone: Über Mikrofon erkennen":
            try:
                if st.button('Starten'):
                    # Ansicht für die Aufnahme
                    with st.spinner("Nimmt Audio auf..."):
                        # Nimm Song auf und speicher 
                        song = mr.listen_to_song(user=st.session_state.logged_in_user)
                        st.empty()
                    # Wenn es fertig aufgenommen ist zeige Progressbar und zeige die Musikinformationen
                    progress_bar = st.progress(0)
                    for i in range(21):
                        time.sleep(0.1)
                        progress_bar.progress(i*5, text=f'Musik wird verarbeitet. Fortschritt: {i*5}%')
                    time.sleep(0.8)
                    progress_bar.empty()
                    # Zeige Infos von dem Song
                    mr.show_song_info(song, st.session_state.logged_in_user)
            except Exception as e:
                st.error(f'Fehler beim Erkennen der Musikdatei: {e}')
    else:
        st.warning("Bitte melden Sie sich zuerst im Nutzermanagement an.")



# About und Kontakt
elif option == 'About':
    st.title(':book: About')
    # Kurzer Text zu der App und Funktionsweise
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
                <li>Schritt 5: Wenn ein Lied erkannt wurde, werden Informationen (Titel, Album, Interpret) angezeigt sowie ein zugehöriges Albumcover. Zusätzlich erhalten Sie Links zu Spotify und Youtube, um das Lied zu hören. Ein Youtube-Video wird ebenfalls eingebettet, um das Lied direkt in der App anzuhören. Zudem werden die letzten 5 erkannten Lieder in der Historie zu dem angemeldeten Benutzer angezeigt.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )


elif option == 'Kontakt':
    st.title('Kontakt :girl: :boy: :boy:')
    # Kontaktinformationen
    st.markdown(
        """
        Hier finden Sie unsere Kontaktinformationen:
        - :girl: **Sandra Grüner**  | E-Mail: [Sandra Grüner](mailto:s.gruener@mci4me.at)
                                    | GitHub: [Sandra Gruener](https://github.com/Sandys00)
        - :boy: **Tim Hornikel**    | E-Mail: [Tim Hornikel](mailto:t.hornikel@mci4me.at)
                                    | GitHub: [Tim Hornikel](https://github.com/timhornikel)
        - :boy: **Oskar Klöpfer** | E-Mail: [Oskar Kloepfer](mailto:o.kloepfer@mci4me.at)
                                    | GitHub: [Oskar Kloepfer](https://github.com/Docterpanzen)
        """,
        unsafe_allow_html=True
    )

elif option == 'Abmelden':
    # Überprüfen, ob ein Benutzer angemeldet ist
    if st.session_state.logged_in_user:
        # Abmelden wenn ein user angemeldet ist, wenn nicht dann wird eine Warnung ausgegeben
        logout()
    else:
        st.warning("Sie sind nicht angemeldet.")
