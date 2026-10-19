import os
import time
import random
import requests

# Konfiguracja Discord Webhook z zmiennej środowiskowej
DISCORD_WEBHOOK_URL = os.environ.get("https://discord.com/api/webhooks/1561825475901390980/xj3pdlT-qPSQMjUPYR3QlIxQjroaPA-w4IHInoBVp5yOOX5kcFXq2Q72AK4TCmhPmy-T")

# Historia wysłanych meczów (system anty-spamowy - brak powtórzeń)
sent_matches = set()

def send_to_discord(message):
    """Wysyła powiadomienie na kanał Discord przez Webhook."""
    if not DISCORD_WEBHOOK_URL:
        print("Błąd: Brak zdefiniowanej zmiennej DISCORD_WEBHOOK_URL!")
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
    """Symulacja analizy statystycznej i wyszukiwania kuponów SOLO w Betclic."""
    print("Skanowanie oferty Betclic w poszukiwaniu wartościowych typów...")
    
    # Przykładowa pula meczów do symulacji analizy
    mock_matches = [
        {"teams": "Real Madryt - Barcelona", "pick": "Real Madryt (Wygrana)", "odds": 1.85, "link": "https://betclic.pl"},
        {"teams": "Manchester City - Arsenal", "pick": "Powyżej 2.5 goli", "odds": 1.70, "link": "https://betclic.pl"},
        {"teams": "Bayern Monachium - Borussia Dortmund", "pick": "Bayern (Wygrana)", "odds": 1.55, "link": "https://betclic.pl"},
        {"teams": "Juventus - Inter Mediolan", "pick": "Obie drużyny strzelą", "odds": 1.90, "link": "https://betclic.pl"},
        {"teams": "PSG - Marsylia", "pick": "PSG (Wygrana)", "odds": 1.45, "link": "https://betclic.pl"}
    ]
    
    # Filtrowanie i wybór typu
    for match in mock_matches:
        match_name = match["teams"]
        
        # Sprawdzenie systemu anty-spamowego (czy mecz był już wysyłany)
        if match_name in sent_matches:
            continue
            
        # Dodanie do historii, aby się nie powtórzył
        sent_matches.add(match_name)
        
        # Formatowanie wiadomości SOLO (stawka 5 zł)
        stake = 5.0
        odds = match["odds"]
        potential_win = round(stake * odds * 0.88, 2) # Uwzględnienie podatku 12%
        
        message = (
            f"🎯 *NOWY TYP SOLO (Betclic)* 🎯\n"
            f"⚽ *Mecz:* {match_name}\n"
            f"💡 *Typ:* {match['pick']}\n"
            f"📊 *Kurs:* {odds}\n"
            f"💰 *Stawka:* {stake} zł\n"
            f"💵 *Przewidywana wygrana:* {potential_win} zł\n"
            f"🔗 [Postaw zakład w Betclic]({match['link']})"
        )
        
        # Wysłanie na Discorda
        send_to_discord(message)
        break # Wysyłamy jeden kupon na cykl, żeby nie spamować

if _name_ == "_main_":
    print("Bot bukmacherski Betclic został uruchomiony i działa 24/7...")
    while True:
        try:
            analyze_and_bet()
        except Exception as e:
            print(f"Wystąpił błąd w pętli głównej: {e}")
        
        # Odczekaj np. 10 minut przed kolejnym skanowaniem (600 sekund)
        time.sleep(600)
