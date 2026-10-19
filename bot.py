import os
import requests
import random

# Konfiguracja Discord Webhook ze zmiennej środowiskowej
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Pula meczów do symulacji analizy
MOCK_MATCHES = [
    {"teams": "Real Madryt - Barcelona", "pick": "Real Madryt (Wygrana)", "odds": 1.85, "link": "https://betclic.pl"},
    {"teams": "Manchester City - Arsenal", "pick": "Powyżej 2.5 goli", "odds": 1.70, "link": "https://betclic.pl"},
    {"teams": "Bayern Monachium - Borussia Dortmund", "pick": "Bayern (Wygrana)", "odds": 1.55, "link": "https://betclic.pl"},
    {"teams": "Juventus - Inter Mediolan", "pick": "Obie drużyny strzelą", "odds": 1.90, "link": "https://betclic.pl"},
    {"teams": "PSG - Marsylia", "pick": "PSG (Wygrana)", "odds": 1.45, "link": "https://betclic.pl"}
]

def send_to_discord(message):
    """Wysyła powiadomienie na kanał Discord przez Webhook."""
    if not DISCORD_WEBHOOK_URL:
        print("Błąd: Brak zdefiniowanej zmiennej DISCORD_WEBHOOK_URL w Secrets!")
        return
    
    data = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("Pomyślnie wysłano wiadomość na Discorda.")
        else:
            print(f"Błąd wysyłania na Discorda: {response.status_code}")
    except Exception as e:
        print(f"Wyjątek podczas wysyłania wiadomości: {e}")

def analyze_and_bet():
    """Analiza statystyczna i wybór typu SOLO."""
    print("Skanowanie oferty Betclic w poszukiwaniu wartościowych typów...")
    
    match = random.choice(MOCK_MATCHES)
    
    stake = 5.0
    odds = match["odds"]
    potential_win = round(stake * odds * 0.88, 2) # Uwzględnienie podatku 12%
    
    message = (
        f"🎯 *NOWY TYP SOLO (Betclic)* 🎯\n"
        f"⚽ *Mecz:* {match['teams']}\n"
        f"💡 *Typ:* {match['pick']}\n"
        f"📊 *Kurs:* {odds}\n"
        f"💰 *Stawka:* {stake} zł\n"
        f"💵 *Przewidywana wygrana:* {potential_win} zł\n"
        f"🔗 [Postaw zakład w Betclic]({match['link']})"
    )
    
    send_to_discord(message)

if _name_ == "_main_":
    analyze_and_bet()
