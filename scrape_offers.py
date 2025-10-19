#!/usr/bin/env python3
"""
Automatisk rabatt-scraper för Åland
Hämtar erbjudanden från olika källor och genererar två HTML-filer:
1. Snygg besökssida (offers_display.html)
2. Enkel AI-läsbar version (offers_ai.html)
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

class OffersScraper:
    def __init__(self):
        self.offers = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_kantarellen(self):
        """Scrape K-Supermarket Kantarellen erbjudanden"""
        try:
            url = "https://www.kantarellen.ax/erbjudanden"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Hitta erbjudanden (anpassa efter faktisk struktur)
            offers = []
            
            # Exempel på parsing - måste anpassas till faktisk HTML-struktur
            offer_items = soup.find_all(['div', 'article'], class_=re.compile('offer|product|campaign', re.I))
            
            for item in offer_items[:5]:  # Max 5 erbjudanden
                try:
                    # Försök hitta produktnamn
                    name_elem = item.find(['h2', 'h3', 'h4', 'strong'])
                    name = name_elem.get_text(strip=True) if name_elem else None
                    
                    # Försök hitta pris
                    price_elem = item.find(class_=re.compile('price|pris', re.I))
                    price = price_elem.get_text(strip=True) if price_elem else None
                    
                    if name:
                        offers.append({
                            'store': 'K-Supermarket Kantarellen',
                            'category': 'Matvaror',
                            'icon': '🏪',
                            'product': name,
                            'price': price or 'Se butiken',
                            'valid': 'Giltigt v.' + str(datetime.now().isocalendar()[1]),
                            'url': url
                        })
                except Exception as e:
                    continue
            
            return offers
        except Exception as e:
            print(f"Error scraping Kantarellen: {e}")
            return []
    
    def scrape_varuboden(self):
        """Scrape Varuboden kampanjer"""
        try:
            url = "https://varuboden.ax/kampanjer/"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            offers = []
            
            # Försök hitta kampanjbilder eller innehåll
            campaign_items = soup.find_all(['div', 'article'], class_=re.compile('campaign|kampanj', re.I))
            
            for item in campaign_items[:5]:
                try:
                    name_elem = item.find(['h2', 'h3', 'h4'])
                    name = name_elem.get_text(strip=True) if name_elem else None
                    
                    desc_elem = item.find(['p', 'span'])
                    desc = desc_elem.get_text(strip=True) if desc_elem else None
                    
                    if name or desc:
                        offers.append({
                            'store': 'Varuboden (S-market)',
                            'category': 'Matvaror',
                            'icon': '🛒',
                            'product': name or desc[:50],
                            'price': 'Ägarkund-bonus upp till 5%',
                            'valid': 'Löpande',
                            'url': url
                        })
                except Exception as e:
                    continue
            
            return offers
        except Exception as e:
            print(f"Error scraping Varuboden: {e}")
            return []
    
    def get_mock_offers(self):
        """Generera exempel-erbjudanden när scraping inte fungerar"""
        return [
            {
                'store': 'K-Supermarket Kantarellen',
                'category': 'Matvaror',
                'icon': '🏪',
                'product': 'Plussakort - Spara upp till 5%',
                'price': 'Gratis kort',
                'valid': 'Löpande',
                'url': 'https://www.kantarellen.ax/erbjudanden'
            },
            {
                'store': 'K-Supermarket Kantarellen',
                'category': 'Matvaror',
                'icon': '🏪',
                'product': 'Veckans erbjudanden',
                'price': 'Se aktuella priser i butik',
                'valid': f'Vecka {datetime.now().isocalendar()[1]}',
                'url': 'https://www.kantarellen.ax/erbjudanden'
            },
            {
                'store': 'Varuboden (S-market)',
                'category': 'Matvaror',
                'icon': '🛒',
                'product': 'S-Förmånskort Bonus',
                'price': 'Upp till 5% bonus på inköp',
                'valid': 'Löpande',
                'url': 'https://varuboden.ax/kampanjer/'
            },
            {
                'store': 'Varuboden (S-market)',
                'category': 'Matvaror',
                'icon': '🛒',
                'product': 'Ägarens Lönedag',
                'price': 'Extra erbjudanden',
                'valid': 'Den 10:e varje månad',
                'url': 'https://varuboden.ax/kampanjer/'
            },
            {
                'store': 'Varuboden (S-market)',
                'category': 'Matvaror',
                'icon': '🛒',
                'product': 'Röda Lappar - Dubbelrabatt',
                'price': 'Dubbel rabatt under sista öppethålningstiden',
                'valid': 'Dagligen',
                'url': 'https://varuboden.ax/kampanjer/'
            },
            {
                'store': 'ÅlandsRabatten',
                'category': 'Blandat',
                'icon': '🎟️',
                'product': '~350 kuponger',
                'price': 'Mat, kläder, restauranger m.m.',
                'valid': 'Årskupongbok',
                'url': 'https://www.eckerolinjen.ax/alandsrabatten'
            },
            {
                'store': 'Kupongfesten (Ålandskortet)',
                'category': 'Blandat',
                'icon': '🎉',
                'product': 'Bio Savoy',
                'price': '2 för 1 biobiljetter',
                'valid': 'Se aktuella kuponger',
                'url': 'https://alandskortet.alandstidningen.ax/kupongfesten'
            },
            {
                'store': 'Maxinge Center',
                'category': 'Köpcentrum',
                'icon': '🏬',
                'product': 'Se Maxingebladet',
                'price': 'Specialerbjudanden från olika butiker',
                'valid': 'Enligt Maxingebladet',
                'url': 'https://www.maxinge.ax'
            }
        ]
    
    def scrape_all(self):
        """Scrape alla källor"""
        print("Scraping Kantarellen...")
        kantarellen_offers = self.scrape_kantarellen()
        
        print("Scraping Varuboden...")
        varuboden_offers = self.scrape_varuboden()
        
        # Kombinera alla erbjudanden
        all_offers = kantarellen_offers + varuboden_offers
        
        # Om inga riktiga erbjudanden hittades, använd mock data
        if len(all_offers) < 3:
            print("Använder exempel-erbjudanden...")
            all_offers = self.get_mock_offers()
        
        self.offers = all_offers
        return all_offers
    
    def generate_display_html(self, output_file='offers_display.html'):
        """Generera snygg besökssida"""
        
        # Gruppera efter kategori
        categories = {}
        for offer in self.offers:
            cat = offer.get('category', 'Övrigt')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(offer)
        
        html = f'''<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aktuella Rabatter & Erbjudanden - Chatbot.ax</title>
<style>
  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #fff;
    line-height: 1.6;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
  }}

  .container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 40px 5%;
  }}

  .header {{
    text-align: center;
    margin-bottom: 50px;
  }}

  .badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.1);
    padding: 10px 20px;
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 1em;
    font-size: 0.9em;
    font-weight: 600;
  }}

  h1 {{
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 800;
    margin-bottom: 0.5em;
  }}

  .gradient-text {{
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }}

  .subtitle {{
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 1em;
  }}

  .update-time {{
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.6);
  }}

  .category-section {{
    margin-bottom: 50px;
  }}

  .category-title {{
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 1.5em;
    padding-bottom: 0.5em;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  }}

  .offers-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 25px;
  }}

  .offer-card {{
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 25px;
    transition: all 0.3s ease;
    text-decoration: none;
    color: #fff;
    display: block;
  }}

  .offer-card:hover {{
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  }}

  .offer-header {{
    display: flex;
    align-items: flex-start;
    gap: 15px;
    margin-bottom: 15px;
  }}

  .offer-icon {{
    font-size: 2.5em;
    flex-shrink: 0;
  }}

  .offer-info {{
    flex: 1;
  }}

  .offer-store {{
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 0.5em;
  }}

  .offer-product {{
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 0.8em;
  }}

  .offer-details {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 1em;
  }}

  .offer-price {{
    font-size: 1.5rem;
    font-weight: 700;
    color: #10b981;
  }}

  .offer-valid {{
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.6);
  }}

  .offer-link {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #60a5fa;
    font-size: 0.9em;
    font-weight: 600;
    text-decoration: none;
  }}

  .footer {{
    text-align: center;
    margin-top: 60px;
    padding: 30px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }}

  @media (max-width: 768px) {{
    .offers-grid {{
      grid-template-columns: 1fr;
    }}
  }}
</style>
</head>
<body>

<div class="container">
  
  <div class="header">
    <div class="badge">
      💰 Uppdateras automatiskt
    </div>
    <h1>
      Aktuella Rabatter & <span class="gradient-text">Erbjudanden</span>
    </h1>
    <p class="subtitle">
      De bästa erbjudandena från lokala butiker på Åland
    </p>
    <p class="update-time">
      Senast uppdaterad: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    </p>
  </div>
'''
        
        # Lägg till kategorier
        for category, offers in categories.items():
            html += f'''
  <div class="category-section">
    <h2 class="category-title">{category}</h2>
    <div class="offers-grid">
'''
            
            for offer in offers:
                html += f'''
      <a href="{offer['url']}" target="_blank" class="offer-card">
        <div class="offer-header">
          <div class="offer-icon">{offer['icon']}</div>
          <div class="offer-info">
            <h3 class="offer-store">{offer['store']}</h3>
          </div>
        </div>
        <p class="offer-product">{offer['product']}</p>
        <div class="offer-details">
          <div class="offer-price">{offer['price']}</div>
          <div class="offer-valid">⏰ {offer['valid']}</div>
        </div>
        <span class="offer-link">
          Se mer →
        </span>
      </a>
'''
            
            html += '''
    </div>
  </div>
'''
        
        html += f'''
  <div class="footer">
    <p>
      💡 <strong>Tips:</strong> Fråga vår AI-guide om specifika rabatter eller erbjudanden!
    </p>
    <p style="margin-top: 1em; font-size: 0.9em; color: rgba(255, 255, 255, 0.6);">
      Chatbot.ax - Din guide till Åland
    </p>
  </div>

</div>

</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Besökssida skapad: {output_file}")
    
    def generate_ai_html(self, output_file='offers_ai.html'):
        """Generera enkel AI-läsbar HTML"""
        
        html = f'''<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<title>Rabatter och Erbjudanden - Åland</title>
</head>
<body>

<h1>Aktuella Rabatter och Erbjudanden på Åland</h1>
<p>Senast uppdaterad: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

'''
        
        # Gruppera efter butik
        stores = {}
        for offer in self.offers:
            store = offer['store']
            if store not in stores:
                stores[store] = []
            stores[store].append(offer)
        
        for store, offers in stores.items():
            html += f'''
<h2>{store}</h2>
<ul>
'''
            for offer in offers:
                html += f'''  <li>
    <strong>{offer['product']}</strong>
    <br>Pris: {offer['price']}
    <br>Giltigt: {offer['valid']}
    <br>Kategori: {offer['category']}
    <br>Länk: <a href="{offer['url']}">{offer['url']}</a>
  </li>
'''
            html += '</ul>\n\n'
        
        html += '''
<h2>Övriga Rabattkällor</h2>
<ul>
  <li><strong>ÅlandsRabatten</strong> - ~350 kuponger för olika butiker (mat, kläder, restauranger). <a href="https://www.eckerolinjen.ax/alandsrabatten">https://www.eckerolinjen.ax/alandsrabatten</a></li>
  <li><strong>Kupongfesten (Ålandskortet)</strong> - Lokala kuponger och deals. <a href="https://alandskortet.alandstidningen.ax/kupongfesten">https://alandskortet.alandstidningen.ax/kupongfesten</a></li>
  <li><strong>Maxinge Center</strong> - Specialerbjudanden från olika butiker. <a href="https://www.maxinge.ax">https://www.maxinge.ax</a></li>
  <li><strong>Loppisar På Åland (Facebook)</strong> - Second-hand försäljning. <a href="https://www.facebook.com/groups/1159640120797248">https://www.facebook.com/groups/1159640120797248</a></li>
</ul>

</body>
</html>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"AI-läsbar sida skapad: {output_file}")


if __name__ == "__main__":
    print("Startar automatisk rabatt-scraper...")
    print("=" * 50)
    
    scraper = OffersScraper()
    offers = scraper.scrape_all()
    
    print(f"\nHittade {len(offers)} erbjudanden")
    print("=" * 50)
    
    # Generera båda HTML-filerna
    scraper.generate_display_html('offers_display.html')
    scraper.generate_ai_html('offers_ai.html')
    
    print("\n✅ Klart! Två filer skapade:")
    print("   1. offers_display.html - Snygg besökssida")
    print("   2. offers_ai.html - Enkel AI-läsbar version")
