# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys
import webbrowser
import argparse

# Set stdout to handle UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def get_roster_page(url, proxy=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    proxies = None
    if proxy:
        proxies = {"http": proxy, "https": proxy}
        print(f"Using proxy: {proxy}")
        
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        sys.exit(1)

def parse_roster(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', id='rosterTable')
    
    if not table:
        print("Error: Could not find roster table.")
        sys.exit(1)

    # Get dates from header
    headers = table.find('thead').find_all('th')
    # First header is empty/spacer, remaining are dates
    dates = [th.get_text(strip=True) for th in headers[1:]]
    
    if not dates:
        print("Error: No dates found in roster.")
        sys.exit(1)

    next_run_date = dates[0]
    print(f"Checking roster for: {next_run_date}")

    open_positions = []
    streckenposten_found = False

    # Iterate through rows
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        cells = row.find_all(['th', 'td'])
        
        if len(cells) < 1:
            continue
            
        role_cell = cells[0]
        role_name = role_cell.get_text(strip=True)
        
        # Skip excluded roles
        if role_name in ["Fotos", "Berichterstattung"]:
            continue
            
        # Handle Streckenposten (only the first one, rename it)
        if role_name == "Streckenposten":
            if streckenposten_found:
                continue
            role_name = "Streckenposten (Seegrabenweg)"
            streckenposten_found = True
        
        # Check the cell corresponding to the next run date (index 1)
        if len(cells) > 1:
            volunteer_cell = cells[1]
            volunteer_name = volunteer_cell.get_text(strip=True)
            
            # If volunteer name is empty, position is open
            if not volunteer_name:
                open_positions.append(role_name)

    return next_run_date, open_positions

def generate_whatsapp_link(date, open_positions):
    if not open_positions:
        return f"Alle Positionen für den {date} sind besetzt! \U0001F389", None

    # Construct the message
    lines = [
        f"Hallo zusammen \U0001F44B,",
        f"",
        f"für den kommenden parkrun am {date} suchen wir noch Helfer! \U0001F333\U0001F3C3",
        f"",
        f"Folgende Positionen sind noch offen:"
    ]
    
    for role in open_positions:
        lines.append(f"- {role}")
    
    lines.append("")
    lines.append("Wer hat Zeit und Lust uns zu unterstützen? \U0001F64C")
    lines.append("")
    lines.append("Den kompletten Plan findest du hier: https://www.parkrun.com.de/krupundersee/futureroster/")

    message = "\n".join(lines)
    
    encoded_message = urllib.parse.quote(message)
    link = f"https://api.whatsapp.com/send?text={encoded_message}"
    
    return message, link

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outfile", help="Write the message and link to this file instead of opening browser")
    parser.add_argument("--plain", action="store_true", help="Write ONLY the message text to the outfile (no markdown headers)")
    parser.add_argument("--proxy", help="Proxy URL to use for the request")
    args = parser.parse_args()

    url = "https://www.parkrun.com.de/krupundersee/futureroster/"
    print(f"Fetching roster from {url}...")
    
    html = get_roster_page(url, proxy=args.proxy)
    date, open_positions = parse_roster(html)
    
    message, link = generate_whatsapp_link(date, open_positions)
    
    if args.outfile:
        with open(args.outfile, "w", encoding="utf-8") as f:
            if args.plain:
                # Just the raw message for iOS Shortcuts or other automation
                f.write(message)
            else:
                # Markdown format for Issues/Email
                f.write(f"# Parkrun Roster Check: {date}\n\n")
                f.write(message)
                f.write("\n\n")
                f.write(f"**WhatsApp Quick Link**: [Klick mich]({link})\n\n")
                f.write(f"Raw Link: `{link}`")
        print(f"Output written to {args.outfile}")
    
    print("\n" + "="*40)
    print("GENERATED MESSAGE:")
    print("="*40)
    print(message)
    print("="*40)
    
    # Pass outfile arg to handle browser behavior (None if not set)
    if not args.outfile and link:
         print("\nWhatsApp Quick Link (wird geöffnet...):")
         print(link)
         webbrowser.open(link)

if __name__ == "__main__":
    main()
