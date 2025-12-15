import google.generativeai as genai
import json
import datetime
import os
import time

# --- MODIFICARE: CITIM CHEIA DIN SEIFUL GITHUB ---
# Daca nu gaseste cheia in seif (pe server), o foloseste pe cea de test (local)
API_KEY = os.environ.get("GEMINI_API_KEY")

# Configureaza AI-ul
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("❌ EROARE: Nu am gasit cheia API! Robotul nu poate functiona.")
    exit()

model = genai.GenerativeModel('gemini-1.5-flash')

ZODII = [
    "berbec", "taur", "gemini", "rac", "leu", "fecioara", 
    "balanta", "scorpion", "sagetator", "capricorn", "varsator", "pesti"
]

def get_date_string():
    return datetime.date.today().strftime("%d-%m-%Y")

def generate_zodiac_content(zodia, data_curenta):
    print(f"🔮 Vorbesc cu astrele pentru {zodia}...")
    
    prompt = f"""
    Esti un astrolog mistic. Scrie horoscopul pentru zodia {zodia} pe data de {data_curenta}.
    Returneaza DOAR un JSON valid cu acest format exact:
    {{
        "general": "Text mistic scurt (2 fraze).",
        "dragoste": "Predictie sentimentala.",
        "bani": "Predictie financiara.",
        "noroc_nr": "Un numar 1-99",
        "noroc_culoare": "O culoare",
        "stare": "Un cuvant (ex: Energic)"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"❌ Eroare la {zodia}: {e}")
        return None

def main():
    print("--- 🚀 PORNIRE GENERATOR AUTOMAT ---")
    data_afisata = get_date_string()
    
    final_data = { "meta": { "data_valabilitate": data_afisata } }

    for zodia in ZODII:
        content = generate_zodiac_content(zodia, data_afisata)
        if content:
            final_data[zodia] = content
        time.sleep(1) 

    # Salvare
    cale_json = os.path.join(os.path.dirname(__file__), "..", "content", "daily_data.json")
    
    with open(cale_json, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"✅ GATA! Fisierul daily_data.json a fost actualizat.")

if __name__ == "__main__":
    main()