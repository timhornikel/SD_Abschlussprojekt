import streamlit as st

# Startseite
st.title('Willkommen zu')
logo = st.image('Abschlussprojekt_Logo.png', width=500)  # Ändere die width nach Bedarf)

# Buttons für Registrieren, Anmelden, Als Gast fortfahren, About und Kontakt
register_button = st.button('Registrieren')
login_button = st.button('Anmelden')
guest_button = st.button('Als Gast fortfahren')
about_button = st.button('About')
contact_button = st.button('Kontakt')

# Überprüfe, welcher Button geklickt wurde
if register_button:
    st.title('Registrierung')

    if register_button:
        username = st.text_input('Benutzername')
        email = st.text_input('E-Mail')
        password = st.text_input('Passwort', type='password')
        
        if st.button('Registrieren'):
            # Füge den Code für die Registrierung hier ein
            st.success(f'Benutzer {username} erfolgreich registriert!')

        # Leite zu neuer Seite weiter
        st.empty()
        if st.button('Musik hochladen und registrieren'):
            st.title('Lied hochladen und registrieren')
            # Füge den Code für das Hochladen und Registrieren hier ein

elif login_button:
    st.title('Anmeldung')

    if login_button:
        username = st.text_input('Benutzername')
        password = st.text_input('Passwort', type='password')
        
        if st.button('Anmelden'):
            # Füge den Code für die Anmeldung hier ein
            # Beispiel: Überprüfe die Anmeldeinformationen und leite den Benutzer weiter
            if username == 'demo' and password == 'demo':
                st.success(f'Erfolgreich als {username} angemeldet!')
            else:
                st.error('Ungültige Anmeldeinformationen. Bitte versuche es erneut.')
        # Leite zu neuer Seite weiter
        st.empty()
        if st.button('Musik hochladen und registrieren'):
            st.title('Lied hochladen und registrieren')

elif guest_button:
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

elif about_button:
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

elif contact_button:
    st.header('Kontakt')
    st.write('Falls du Fragen hast, kontaktiere eine Person unseres Support Teams.')
    st.write('Name: Sandra Grüner | E-Mail: s.gruener@mci4me.at')
    st.write('Name: Tim Hornikel | E-Mail: t.hornikel@mci4me.at')
    st.write('Name: Oskar Klöpfer | E-Mail: o.kloepfer@mci4me.at')