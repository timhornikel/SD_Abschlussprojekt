import streamlit as st
from users import User

# Initialisierung der Session-Variablen
if 'state' not in st.session_state:
    st.session_state.state = 'start'
    st.session_state.username = ''
    st.session_state.email = ''
    st.session_state.password = ''
    st.session_state.logged_in_user = None
    st.session_state.show_about = False
    st.session_state.show_contact = False

# Funktion zum Zurückkehren zum Zustand 'start'
def main_button():
    if st.button('Zurück zum Start'):
        st.session_state.state = 'start'    

# Funktion für Benachrichtigungen
def notify(message, type='info'):
    if type == 'info':
        st.info(message)
    elif type == 'success':
        st.success(message)
    elif type == 'error':
        st.error(message)

# Zurück zur Startseite Button  
def main_button():
    if st.button('Zurück zum Start'):
        st.session_state.state = 'start'
        st.session_state.logged_in_user = None
        st.experimental_rerun()

# Startseite
if st.session_state.logged_in_user is None:
    st.title('Willkommen zu')
    logo = st.image('Abschlussprojekt_Logo_userinterface.png', width=300)

    action = st.radio('Wähle deine Option:', ['Anmelden', 'Registrieren', 'Als Gast anmelden'])

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
                st.experimental_rerun()
            else:
                notify('Falscher Benutzername oder Passwort. Bitte versuche es erneut.', type='error')

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
                st.experimental_rerun()

    elif action == 'Als Gast anmelden':
        st.session_state.logged_in_user = 'Gast'
        notify('Erfolgreich als Gast angemeldet!', type='success')
        st.experimental_rerun()

# Musikseite
elif st.session_state.logged_in_user:
    st.title('Willkommen zu')
    logo = st.image('Abschlussprojekt_Logo_userinterface.png', width=300) 

    if st.button('Musik hochladen'):
        st.session_state.state = 'upload_music'
        st.experimental_rerun()
    elif st.button('Musik erkennen'):
        st.session_state.state = 'recognize_music'
        st.experimental_rerun()

    elif st.session_state.state == 'upload_music':
        st.title('Musik hochladen')
        uploaded_file = st.file_uploader("Wähle eine Musikdatei aus", type=["mp3", "wav"])
        if uploaded_file is not None:
            st.success('Musikdatei erfolgreich hochgeladen!')

    elif st.session_state.state == 'recognize_music':
        st.title('Musik erkennen')
        st.write('Hier können Sie Musik erkennen lassen.')
        st.write('Code noch nicht implementiert')

# Abstandshalter
st.markdown("---")

# About und Kontakt
if st.button('About'):
    st.session_state.show_about = not st.session_state.show_about
if st.session_state.show_about:
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
    st.session_state.show_contact = not st.session_state.show_contact
if st.session_state.show_contact:
    st.write('Falls du Fragen hast, kontaktiere eine Person unseres Support Teams.')
    st.write('Name: Sandra Grüner | E-Mail: s.gruener@mci4me.at')
    st.write('Name: Tim Hornikel | E-Mail: t.hornikel@mci4me.at')
    st.write('Name: Oskar Klöpfer | E-Mail: o.kloepfer@mci4me.at')

# Zurück zur Startseite Button
main_button() 