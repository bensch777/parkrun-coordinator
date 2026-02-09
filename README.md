# Parkrun Roster Coordinator 🌳🏃

Automatisierter Helfer-Check für den [Krupunder See parkrun](https://www.parkrun.com.de/krupundersee/).

Dieses Projekt prüft wöchentlich den aktuellen Helferplan ("Roster") und generiert eine fertige WhatsApp-Nachricht mit den offenen Positionen.

## Funktionsweise

1.  **GitHub Action**: Mo-Do (ca. 08:00 Uhr) läuft ein Skript in der Cloud.
2.  **Scraping**: Es prüft `parkrun.com.de` auf freie Plätze für den nächsten Samstag.
3.  **Output**: Das Ergebnis wird in die Datei [`latest_message.txt`](latest_message.txt) geschrieben.
4.  **iOS Shortcut**: Dein iPhone holt sich diesen Text und sendet ihn via WhatsApp.

## Einrichtung

### 1. Repository (Public)

Damit dein iPhone den Text einfach lesen kann, muss dieses Repository **Public** sein.
*(Keine Sorge: Deine Secrets sind trotzdem sicher!)*

### 2. GitHub Secrets

Damit der Scraper nicht geblockt wird, nutzen wir einen Proxy. Hinterlege diesen unter `Settings` -> `Secrets and variables` -> `Actions`:

*   **Name**: `ROSTER_PROXY`
*   **Value**: Dein Proxy-String (z.B. `gw-eu.lemonclub.io:5555:...`)

### 3. iPhone / iOS Kurzbefehl

Erstelle einen Kurzbefehl mit folgenden Schritten:

1.  **Inhalte von URL abrufen**:
    *   URL: `https://raw.githubusercontent.com/bensch777/parkrun-coordinator/main/latest_message.txt`
2.  **(Optional) Apple Intelligence / ChatGPT**:
    *   "Mache diesen Text lustiger: [Inhalte von URL]"
3.  **Nachricht senden (WhatsApp)**:
    *   Empfänger: Deine Parkrun-Gruppe.

## Manuelle Nutzung (Lokal)

Du kannst das Skript auch auf deinem PC ausführen:

```bash
pip install -r requirements.txt
python check_roster.py
```

Es öffnet dann direkt WhatsApp Web mit dem Text.
