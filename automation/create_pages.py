import os

# Configurare
TEMPLATE_FILE = "berbec.html" # Fisierul sursa (sablonul)
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content")

# Datele pentru fiecare zodie (Nume si Iconita)
ZODII_DATA = {
    "berbec": {"nume": "BERBEC", "icon": "♈"},
    "taur": {"nume": "TAUR", "icon": "♉"},
    "gemini": {"nume": "GEMENI", "icon": "♊"},
    "rac": {"nume": "RAC", "icon": "♋"},
    "leu": {"nume": "LEU", "icon": "♌"},
    "fecioara": {"nume": "FECIOARĂ", "icon": "♍"},
    "balanta": {"nume": "BALANȚĂ", "icon": "♎"},
    "scorpion": {"nume": "SCORPION", "icon": "♏"},
    "sagetator": {"nume": "SĂGETĂTOR", "icon": "♐"},
    "capricorn": {"nume": "CAPRICORN", "icon": "♑"},
    "varsator": {"nume": "VĂRSĂTOR", "icon": "♒"},
    "pesti": {"nume": "PEȘTI", "icon": "♓"}
}

def create_pages():
    # Citim continutul din berbec.html
    path_template = os.path.join(CONTENT_DIR, TEMPLATE_FILE)
    
    if not os.path.exists(path_template):
        print(f"❌ Eroare: Nu gasesc fisierul {TEMPLATE_FILE} in {CONTENT_DIR}")
        return

    with open(path_template, "r", encoding="utf-8") as f:
        html_template = f.read()

    print("--- 🚀 INCEP CREAREA PAGINILOR ---")

    for key, data in ZODII_DATA.items():
        if key == "berbec":
            continue # Sarim peste berbec ca exista deja

        nume_fisier = f"{key}.html"
        cale_fisier = os.path.join(CONTENT_DIR, nume_fisier)

        # Inlocuim datele specifice in HTML
        # 1. Inlocuim functia JS loadZodiacData('berbec') cu loadZodiacData('noua_zodie')
        nou_html = html_template.replace("loadZodiacData('berbec')", f"loadZodiacData('{key}')")
        
        # 2. Inlocuim Titlul (BERBEC -> TAUR)
        nou_html = nou_html.replace("<h2>BERBEC</h2>", f"<h2>{data['nume']}</h2>")
        
        # 3. Inlocuim Titlul din tab-ul browserului
        nou_html = nou_html.replace("<title>Horoscop Berbec", f"<title>Horoscop {data['nume'].title()}")
        
        # 4. Inlocuim Iconita
        nou_html = nou_html.replace('style="font-size: 5rem; margin-bottom:0; text-shadow:0 0 30px rgba(157, 78, 221, 0.5)">♈', 
                                    f'style="font-size: 5rem; margin-bottom:0; text-shadow:0 0 30px rgba(157, 78, 221, 0.5)">{data["icon"]}')

        # Scriem fisierul nou
        with open(cale_fisier, "w", encoding="utf-8") as f:
            f.write(nou_html)
        
        print(f"✅ Creat pagina: {nume_fisier}")

    print("🎉 GATA! Toate paginiile au fost generate.")

if __name__ == "__main__":
    create_pages()