import base64
import json
import requests

from config import API_KEY, API_TYPE


GEMINI_MODELS_TO_TRY = [     
    "gemini-2.5-flash",         
]

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def clean_json_string(content):
    content = content.strip()
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0].strip()
    elif '```' in content:
        content = content.split('```')[1].split('```')[0].strip()
    return content

def detect_sudoku_with_gemini(image_path):
    base64_image = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json"
    }
    prompt = """Analyze this Sudoku image.
Return ONLY a JSON object representing the 9x9 grid.
Use 0 for empty cells.
Format: {"grid": [[0, 5, ...], [2, 0, ...], ...]}
DO NOT write any other text, just the JSON."""

    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": base64_image
                    }
                }
            ]
        }]
    }
    
    last_error = None

    print("\n--- Gemini Modelleri Deneniyor ---")
    for model_name in GEMINI_MODELS_TO_TRY:
        print(f"Denenen Model: {model_name}...", end=" ")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 404:
                print(" BULUNAMADI 404")
                last_error = f"{model_name}: 404 Not Found"
                continue
            
            if response.status_code != 200:
                print(f" HATA ({response.status_code})")
                last_error = f"{model_name}: {response.text}"
                continue

            result = response.json()
            
            try:
                if 'candidates' in result and result['candidates']:
                    parts = result['candidates'][0]['content']['parts']
                    content = parts[0]['text']
                    
                    print("BAŞARILI!")
                    
                    content = clean_json_string(content)
                    data = json.loads(content)
                    return data.get('grid')
                else:
                    print("BOŞ YANIT")
                    last_error = f"{model_name}: Yanıt boş veya engellendi"
                    continue
                
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                print("JSON AYRIŞTIRMA HATASI")
                last_error = f"Yanıt işleme hatası: {e}"
                continue
                
        except Exception as e:
            print(f"BAĞLANTI HATASI")
            last_error = str(e)
            continue

    print("\n--- TÜM MODELLER BAŞARISIZ OLDU ---")
    if last_error:
        print(f"Son Hata: {last_error}")
    return None

def detect_sudoku_with_openai(image_path):
    print("OpenAI modu pasif.")
    return None

def parse_sudoku_grid(image_path):
    return detect_sudoku_with_gemini(image_path)