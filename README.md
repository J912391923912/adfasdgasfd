# 🏝️ Åland Rabatter & Erbjudanden - Automatisk Scraper

Automatiskt system som hämtar aktuella rabatter och erbjudanden från butiker på Åland och genererar två HTML-sidor:

1. **offers_display.html** - Snygg besökssida för din webbplats
2. **offers_ai.html** - Enkel HTML-version för AI-kunskap

## 🚀 Snabbstart

### Steg 1: Skapa GitHub Repository

1. Gå till [GitHub](https://github.com) och logga in (eller skapa konto - gratis!)
2. Klicka på **"New repository"** (gröna knappen)
3. Namnge repot: `aland-offers` (eller vad du vill)
4. Välj **Public** (krävs för gratis GitHub Pages)
5. Klicka **"Create repository"**

### Steg 2: Ladda upp filerna

**Alternativ A: Via webb-gränssnittet (enklast)**
1. Klicka på **"uploading an existing file"**
2. Dra och släpp alla filer från detta projekt
3. Klicka **"Commit changes"**

**Alternativ B: Via Git (om du kan Git)**
```bash
git clone https://github.com/ditt-användarnamn/aland-offers.git
cd aland-offers
# Kopiera alla filer hit
git add .
git commit -m "Initial commit"
git push
```

### Steg 3: Aktivera GitHub Pages

1. Gå till ditt repo → **Settings** → **Pages**
2. Under **"Source"**, välj **"gh-pages"** branch
3. Klicka **"Save"**

### Steg 4: Aktivera GitHub Actions

1. Gå till **Actions**-fliken i ditt repo
2. Om det frågar om att aktivera workflows, klicka **"I understand my workflows"**
3. GitHub Actions kommer nu köra scriptet automatiskt varje dag kl 06:00 UTC (08:00 svensk tid)

### Steg 5: Första körningen (manuell)

1. Gå till **Actions** → **Update Åland Offers**
2. Klicka **"Run workflow"** → **"Run workflow"**
3. Vänta 1-2 minuter
4. ✅ Klart! HTML-filerna är nu genererade

## 📋 Använda HTML-filerna

Efter första körningen finns filerna på:

### **Besökssida:**
```
https://ditt-användarnamn.github.io/aland-offers/offers_display.html
```

### **AI-version:**
```
https://ditt-användarnamn.github.io/aland-offers/offers_ai.html
```

## 🔗 Integrera med WordPress

### Metod 1: Iframe (enklast)
Lägg till i Elementor HTML-widget:
```html
<iframe 
  src="https://ditt-användarnamn.github.io/aland-offers/offers_display.html" 
  width="100%" 
  height="2000" 
  frameborder="0">
</iframe>
```

### Metod 2: Fetch med JavaScript
```html
<div id="offers-container"></div>
<script>
fetch('https://ditt-användarnamn.github.io/aland-offers/offers_display.html')
  .then(response => response.text())
  .then(html => {
    document.getElementById('offers-container').innerHTML = html;
  });
</script>
```

### Metod 3: Direkt länk
```html
<a href="https://ditt-användarnamn.github.io/aland-offers/offers_display.html" target="_blank">
  Se aktuella erbjudanden →
</a>
```

## 🤖 AI Knowledge Base

Använd **offers_ai.html** för din chatbot:

1. Lägg till URL:en i din AI-kunskapsmotor
2. Crawla/indexera sidan
3. Chatboten kan nu svara på frågor om aktuella erbjudanden!

URL att använda:
```
https://ditt-användarnamn.github.io/aland-offers/offers_ai.html
```

## ⏰ Uppdateringsschema

Scriptet körs automatiskt:
- **Varje dag kl 06:00 UTC (08:00 svensk tid)**
- Kan även köras manuellt via Actions-fliken

För att ändra schema, redigera `.github/workflows/update-offers.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'  # Ändra dessa värden
```

Cron-format: `minuter timmar dag månad veckodag`
- `0 6 * * *` = varje dag kl 06:00
- `0 */6 * * *` = var 6:e timme
- `0 6 * * 1` = varje måndag kl 06:00

## 📁 Filstruktur

```
aland-offers/
├── .github/
│   └── workflows/
│       └── update-offers.yml    # GitHub Actions workflow
├── scrape_offers.py             # Python scraper-script
├── requirements.txt             # Python dependencies
├── offers_display.html          # Genererad besökssida
├── offers_ai.html               # Genererad AI-version
└── README.md                    # Denna fil
```

## 🔧 Anpassa Scraping

För att lägga till fler källor eller förbättra scraping, redigera `scrape_offers.py`:

```python
def scrape_ny_butik(self):
    """Lägg till ny butik här"""
    try:
        url = "https://exempel.ax/erbjudanden"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Din scraping-logik här
        
        return offers
    except Exception as e:
        return []
```

## 🐛 Felsökning

### Actions misslyckas?
1. Kolla **Actions**-fliken för felmeddelanden
2. Kontrollera att Python-syntaxen är korrekt
3. Se till att requirements.txt är korrekt

### Ingen output?
1. Kör workflow manuellt första gången
2. Vänta 2-3 minuter efter körning
3. Kontrollera **gh-pages** branch för filer

### GitHub Pages visar fel sida?
1. Gå till Settings → Pages
2. Bekräfta att **gh-pages** branch är vald
3. Vänta 1-2 minuter efter ändring

## 💡 Tips

- **Testa lokalt först:** Kör `python scrape_offers.py` lokalt innan du pushar
- **Kolla logs:** Actions-fliken visar detaljerade logs för varje körning
- **Backup:** GitHub sparar all historik, du kan alltid återställa gamla versioner

## 📞 Support

Om något inte fungerar:
1. Kolla **Issues**-fliken i GitHub-repot
2. Skapa ett nytt issue med felbeskrivning
3. Inkludera logs från Actions

## 📄 Licens

Fri att använda och modifiera som du vill!

---

**Skapad för Chatbot.ax - Din guide till Åland** 🏝️
