import streamlit as st
from users import User

# Initialisierung des session_state-Objekts
if 'state' not in st.session_state:
    st.session_state.state = 'start'
    st.session_state.username = ''
    st.session_state.email = ''
    st.session_state.password = ''
    st.session_state.logged_in_user = ''


# Startseite
st.title('Willkommen zu')
logo = st.image('Abschlussprojekt_Logo.png', width=500)  # Ändere die width nach Bedarf)

# Anzeigen des angemeldeten Benutzers
if 'logged_in_user' in st.session_state:
    st.subheader(f'Angemeldet als: {st.session_state.logged_in_user}')

# Überprüfe, welcher Button geklickt wurde
if st.session_state.state == 'start':
    if st.button('Registrieren', key='register_button'):
        st.session_state.state = 'registration'

    elif st.button('Anmelden', key='login_button'):
        st.session_state.state = 'login'

    elif st.button('Benutzer löschen', key='delete_button'):
        st.session_state.state = 'delete_user'

    elif st.button('Als Gast fortfahren', key='guest_button'):
        st.session_state.state = 'guest'
    
    elif st.button('About', key='about_button'):
        st.session_state.state = 'about'
    
    elif st.button('Contact', key='contact_button'):
        st.session_state.state = 'contact'


if st.session_state.logged_in_user:
    st.write(f'Eingeloggt als: {st.session_state.logged_in_user}')

# Registrierung
if st.session_state.state == 'registration':
    st.title('Registrierung')

    st.session_state.username = st.text_input('Benutzername', st.session_state.username)
    st.session_state.email = st.text_input('E-Mail', st.session_state.email)
    st.session_state.password = st.text_input('Passwort', type='password', value=st.session_state.password)
    
    if st.button('Registrieren', key='register_action_button'):
        if User.benutzer_existiert(st.session_state.username):
            st.error("Benutzername bereits vergeben. Bitte wählen Sie einen anderen.")
        else:
            benutzer = User(st.session_state.username, st.session_state.email, st.session_state.password)
            benutzer.speichern()
            st.success(f'Benutzer {st.session_state.username} erfolgreich registriert!')
            st.session_state.state = 'start'
            st.session_state.username = ''
            st.session_state.email = ''
            st.session_state.password = ''


# Anmeldung
if st.session_state.state == 'login':
    st.title('Anmeldung')

    st.session_state.username = st.text_input('Benutzername', st.session_state.username)
    st.session_state.password = st.text_input('Passwort', type='password', value=st.session_state.password)
    
    if st.button('Anmelden', key='login_action_button'):
        if User.anmelden(st.session_state.username, st.session_state.password):
            st.success(f'Erfolgreich als {st.session_state.username} angemeldet!')
            st.session_state.logged_in_user = st.session_state.username  # Den angemeldeten Benutzer festhalten
            st.session_state.state = 'start'
            st.session_state.username = ''
            st.session_state.password = ''
        else:
            st.error('Falscher Benutzername oder Passwort. Bitte versuche es erneut.')
    if st.button('zum Hauptmenü zurückgehen', key='login_menu_button'):
        st.session_state.state = 'start'
        st.session_state.username = ''
        st.session_state.password = ''

# Als Gast fortsetzen
if st.session_state.state == 'guest':
    st.title('Als Gast fortfahren')
    # Code für die Gastseite einfügen

# Leite zu neuer Seite weiter
    st.empty()
    if st.button('Musik hochladen und registrieren'):
        st.title('Lied hochladen und registrieren')
        # Füge den Code für das Hochladen und Registrieren hier ein

# Neue Seite mit Buttons für Musik hochladen und registrieren oder Musik erkennen
if st.button('Musik erkennen'):
    st.title('Lied erkennen')
    # Füge den Code für die Musikerkennung hier ein

if st.session_state.state == 'delete_user':
    st.title('Benutzer löschen')

    username_to_delete = st.text_input('Benutzername des zu löschenden Benutzers')
    
    if st.button('Benutzer löschen', key='delete_user_action_button'):
        if User.benutzer_existiert(username_to_delete):
            User.benutzer_loeschen(username_to_delete)
            st.success(f'Benutzer {username_to_delete} erfolgreich gelöscht!')
        else:
            st.error('Benutzer existiert nicht.')

if st.session_state.state == 'about':
    st.header('About')
    st.write('Hier findest du eine kurze Beschreibung zur App.')
    st.write('Die App wurde im Rahmen des Abschlussprojekts der Lehrveranstaltung "Softwaredesign" am MCI entwickelt.')
    st.write('Die App ermöglicht es, dass sich Nutzer registrieren, anmelden oder als Gast fortfahren können.')
    st.write('Schritt 1: Fahre als Gast fort oder melde dich an. Wenn du noch keinen Account hast, registriere dich.')
    st.write('Schritt 2: Wähle aus ob du ein Lied hochladen möchtest oder ein Lied erkennen möchtest.')
    st.write('Schritt 3: Um ein Lied hochzuladen, klicke auf "Lied hochladen" und wähle das Lied aus.')
    st.write('Schritt 4: Wenn das Lied hochgeladen wurde, gib den Titel und den Künstler ein und klicke auf "Lied registrieren".')
    st.write('Schritt 5: Um ein Lied zu erkennen, klicke auf "Lied erkennen" und wähle das Lied aus.')
    st.write('Schritt 6: Wenn das Lied erkannt wurde, wird der Titel und der Künstler angezeigt.')
    st.write('Viel Spaß beim Nutzen der App!')

if st.session_state.state == 'contact':
    st.header('Kontakt')
    st.write('Falls du Fragen hast, kontaktiere eine Person unseres Support Teams.')
    st.write('Name: Sandra Grüner | E-Mail: s.gruener@mci4me.at')
    st.write('Name: Tim Hornikel | E-Mail: t.hornikel@mci4me.at')
    st.write('Name: Oskar Klöpfer | E-Mail: o.kloepfer@mci4me.at')