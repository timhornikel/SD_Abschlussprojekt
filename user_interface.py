import streamlit as st
from users import User

# Initialisierung des session_state-Objekts
if 'state' not in st.session_state:
    st.session_state.state = 'start'
    st.session_state.username = ''
    st.session_state.email = ''
    st.session_state.password = ''
    st.session_state.logged_in_user = 'Kein Nutzer'


# Funktion zum Zurückkehren zum Zustand 'start'
def main_button():
    if st.button('Zurück zum Start'):
        st.session_state.state = 'start'    


# Startseite
st.title('Willkommen zu')
logo = st.image('Abschlussprojekt_Logo.png', width=500)  # Ändere die width nach Bedarf)

if st.session_state.logged_in_user:
    st.write(f'Eingeloggt als: {st.session_state.logged_in_user}')


tabs = ['Musik erkennen', 'Nutzermanagement', 'About']

# Session states für die einzelnen Tabs
if st.session_state.state == 'start':
    selected_tab = st.sidebar.selectbox('Wähle deine Option aus', tabs)

    if selected_tab == 'Musik erkennen':
        st.session_state.state = 'musik_erkennen'
    elif selected_tab == 'Nutzermanagement':
        st.session_state.state = 'nutzermanagement'
    elif selected_tab == 'About':
        st.session_state.state = 'about'

#Musik erkennen
if st.session_state.state == 'musik_erkennen':
    st.divider()
    st.title('Musik erkennen')
    if st.session_state.logged_in_user != 'Kein Nutzer':
        st.text(f'Sie sind als {st.session_state.logged_in_user} angemeldet')
    else:
        st.text('melden sie sich erst im Nutzermanagement an')
    st.divider()




#Nutzermanagement
elif st.session_state.state == 'nutzermanagement':

    st.divider()
    auswahl_nutzer = st.radio('Wähle deine Optione aus:', ['Registrieren', 'Anmelden','Abmelden' , 'Nutzer löschen', 'Als Gast anmelden'])
    st.divider()

    # Registrieren eines neuen Nutzers
    if auswahl_nutzer == 'Registrieren':
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
                st.session_state.username = ''
                st.session_state.email = ''
                st.session_state.password = ''
        st.divider()

    # Anmelden eines Nutzers
    elif auswahl_nutzer == 'Anmelden':
        st.title('Anmeldung')

        st.session_state.username = st.text_input('Benutzername', st.session_state.username)
        st.session_state.password = st.text_input('Passwort', type='password', value=st.session_state.password)
        
        if st.button('Anmelden', key='login_action_button'):
            if User.anmelden(st.session_state.username, st.session_state.password):
                st.success(f'Erfolgreich als {st.session_state.username} angemeldet!')
                st.session_state.logged_in_user = st.session_state.username  # Den angemeldeten Benutzer festhalten
                st.session_state.username = ''
                st.session_state.password = ''
            else:
                st.error('Falscher Benutzername oder Passwort. Bitte versuche es erneut.')
        st.divider()
    
    #Nutzer abmelden
    elif auswahl_nutzer =='Abmelden':
        st.title('Abmelden')
        
        if st.button('Jetzt abmelden'):
            st.session_state.logged_in_user = 'Kein Nutzer'
            st.success('Sie haben sich erfolgreich abgemeldet')
        st.divider()

    # Einen Benutzer löschen
    elif auswahl_nutzer == 'Nutzer löschen':
        st.title('Benutzer löschen')

        username_to_delete = st.text_input('Benutzername des zu löschenden Benutzers')
        
        if st.button('Benutzer löschen', key='delete_user_action_button'):
            if User.benutzer_existiert(username_to_delete):
                User.benutzer_loeschen(username_to_delete)
                st.success(f'Benutzer {username_to_delete} erfolgreich gelöscht!')
            else:
                st.error('Benutzer existiert nicht.')
        st.divider()

    # Als Gast anmelden
    elif auswahl_nutzer == 'Als Gast anmelden':
        st.header('Hier können sie sich als Gast anmelden')
        if st.button('Jetzt als Gast anmelden'):
            st.session_state.logged_in_user = 'Gast'
            st.success('Erfolgreich als Gast angemeldet!')
        st.divider()



elif st.session_state.state == 'about':

    st.divider()

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

    st.divider()

    st.header('Kontakt')
    st.write('Falls du Fragen hast, kontaktiere eine Person unseres Support Teams.')
    st.write('Name: Sandra Grüner | E-Mail: s.gruener@mci4me.at')
    st.write('Name: Tim Hornikel | E-Mail: t.hornikel@mci4me.at')
    st.write('Name: Oskar Klöpfer | E-Mail: o.kloepfer@mci4me.at')

    st.divider()




main_button()
