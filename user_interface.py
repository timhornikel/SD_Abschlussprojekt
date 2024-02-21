import streamlit as st
from users import User

# Initialisierung der Session-Variablen
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'state' not in st.session_state:
    st.session_state.state = None

# Seitenüberschrift und Logo
st.title('Willkommen zu Abschlussprojekt')
st.image('Abschlussprojekt_Logo_userinterface.png', width=300)

# Menü für Aktionen
action = st.sidebar.radio('Wähle deine Option:', ['Anmelden', 'Registrieren', 'Als Gast anmelden'])

# Anmeldeformular
if action == 'Anmelden':
    st.header('Anmeldung')
    username = st.text_input('Benutzername')
    password = st.text_input('Passwort', type='password')
    if st.button('Anmelden'):
        if User.anmelden(username, password):
            st.session_state.logged_in_user = username
            st.success(f'Erfolgreich als {username} angemeldet!')
        else:
            st.error('Falscher Benutzername oder Passwort. Bitte versuche es erneut.')

# Registrierungsformular
elif action == 'Registrieren':
    st.header('Registrierung')
    username = st.text_input('Benutzername')
    email = st.text_input('E-Mail')
    password = st.text_input('Passwort', type='password')
    if st.button('Registrieren'):
        if User.benutzer_existiert(username):
            st.error("Benutzername bereits vergeben. Bitte wählen Sie einen anderen.")
        else:
            benutzer = User(username, email, password)
            benutzer.speichern()
            st.success(f'Benutzer {username} erfolgreich registriert!')

# Gastanmeldung
elif action == 'Als Gast anmelden':
    st.session_state.logged_in_user = 'Gast'
    st.success('Erfolgreich als Gast angemeldet!')

# Musikfunktionen
st.markdown("---")

if st.session_state.logged_in_user:
    st.header('Musikfunktionen')
    if st.button('Musik hochladen'):
        st.session_state.state = 'upload_music'
        st.success('Wähle eine Musikdatei aus und lade sie hoch.')
    elif st.button('Musik erkennen'):
        st.session_state.state = 'recognize_music'
        st.info('Wähle eine Musikdatei aus und lass sie erkennen.')

    if st.session_state.state == 'upload_music':
        uploaded_file = st.file_uploader("Wähle eine Musikdatei aus", type=["mp3", "wav"])
        if uploaded_file is not None:
            st.success('Musikdatei erfolgreich hochgeladen!')

    elif st.session_state.state == 'recognize_music':
        st.write('Hier können Sie Musik erkennen lassen.')
        st.write('Code für Musikerkennung muss noch implementiert werden.')

# About und Kontakt
st.markdown("---")

if st.button('About'):
    st.write('Hier findest du eine kurze Beschreibung zur App.')
    st.write('Die App wurde im Rahmen des Abschlussprojekts der Lehrveranstaltung "Softwaredesign" am MCI entwickelt.')
    st.write('Die App ermöglicht es, dass sich Nutzer registrieren, anmelden oder als Gast fortfahren können.')
    st.write('Schritt 1: Fahre als Gast fort oder melde dich an. Wenn du noch keinen Account hast, registriere dich.')
    st.write('Schritt 2: Wähle aus ob du ein Lied hochladen möchtest oder ein Lied erkennen möchtest.')
    st.write('Schritt 3: Um ein Lied hochzuladen, klicke auf "Lied hochladen" und wähle das Lied aus.')
    st.write('Schritt 4: Wenn das Lied hochgeladen wurde, gib den Titel und den Künstler ein und klicke auf "Lied registrieren".')
    st.write('Schritt 5: Um ein Lied zu erkennen, klicke auf "Lied erkennen" und wähle das Lied aus.')
    st.write('Schritt 6: Wenn das Lied erkannt wurde, wird der Titel und der Künstler angezeigt.')

if st.button('Kontakt'):
    st.write('Falls du Fragen hast, kontaktiere eine Person unseres Support Teams.')
    st.write('Name: Sandra Grüner | E-Mail: s.gruener@mci4me.at')
    st.write('Name: Tim Hornikel | E-Mail: t.hornikel@mci4me.at')
    st.write('Name: Oskar Klöpfer | E-Mail: o.kloepfer@mci4me.at')
