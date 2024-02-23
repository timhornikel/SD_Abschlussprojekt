import streamlit as st
from user.users import User

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
        st.sidebar.success(message)
    elif type == 'error':
        st.sidebar.error(message)

# Hinweis nach Anmeldung
def display_login_message():
    st.sidebar.info("Bitte wählen Sie in der Sidebar nun 'Musik hochladen' oder 'Musik erkennen'.")

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
            st.success('Musikdatei erfolgreich hochgeladen!')
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
                st.success('Musikdatei erfolgreich hochgeladen!')
        elif recognition_option == "Über Mikrofon erkennen":
            st.write("Hier kann die Musik über das Mikrofon erkannt werden.")
    else:
        st.warning("Bitte melden Sie sich zuerst an.")

# About und Kontakt
elif option == 'About':
    st.title('About')
    st.write('Hier finden Sie eine kurze Beschreibung zur App.')
    st.write('Die App wurde im Rahmen des Abschlussprojekts der Lehrveranstaltung "Softwaredesign" am MCI entwickelt.')
    st.write('Die App ermöglicht es, dass sich Nutzer registrieren, anmelden oder als Gast fortsetzen können.')
    st.write('Schritt 1: Fahren Sie als Gast fort oder melden Sie sich an. Wenn Sie noch keinen Account haben, registrieren Sie sich.')
    st.write('Schritt 2: Wählen Sie aus, ob Sie ein Lied hochladen möchten oder ein Lied erkennen möchten.')
    st.write('Schritt 3: Um ein Lied hochzuladen, klicken Sie auf "Lied hochladen" und wählen Sie das Lied aus.')
    st.write('Schritt 4: Wenn das Lied hochgeladen wurde, geben Sie den Titel und den Künstler ein und klicken Sie auf "Lied registrieren".')
    st.write('Schritt 5: Um ein Lied zu erkennen, klicken Sie auf "Lied erkennen" und wählen Sie das Lied aus.')
    st.write('Schritt 6: Wenn das Lied erkannt wurde, wird der Titel und der Künstler angezeigt.')

elif option == 'Kontakt':
    st.title('Kontakt')
    st.write('Wenn Sie Fragen haben, kontaktieren Sie bitte eine Person aus unserem Support-Team.')
    st.write('Name: Sandra Grüner | E-Mail: s.gruener@mci4me.at')
    st.write('Name: Tim Hornikel | E-Mail: t.hornikel@mci4me.at')
    st.write('Name: Oskar Klöpfer | E-Mail: o.kloepfer@mci4me.at')

elif option == 'Abmelden':
    logout()