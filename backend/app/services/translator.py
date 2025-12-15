"""Translation service for multi-language support using free translation APIs"""

import requests

def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translate text to target language dynamically using MyMemory API (free).
    
    Args:
        text: Text to translate (in English)
        target_language: Target language code ("en", "hi", "mr", etc.)
    
    Returns:
        Translated text
    """
    # Normalize target language
    target_language = target_language.lower()
    
    # If English, return as-is
    if target_language == "en" or target_language == "en-us":
        return text
    
    # Map language codes: hi-IN -> hi, mr-IN -> mr
    if "-" in target_language:
        target_language = target_language.split("-")[0]
    
    # Language code mapping for MyMemory API
    lang_map = {
        "hi": "hi",              # Hindi
        "mr": "mr-IN",           # Marathi
        "ta": "ta",              # Tamil
        "te": "te",              # Telugu
        "kn": "kn",              # Kannada
        "ml": "ml",              # Malayalam
        "bn": "bn",              # Bengali
        "gu": "gu",              # Gujarati
    }
    
    if target_language not in lang_map:
        print(f"[WARN] Unsupported language: {target_language}. Returning original text.")
        return text
    
    try:
        target_code = lang_map[target_language]
        
        # Use MyMemory API (free, no API key needed)
        response = requests.get(
            'https://api.mymemory.translated.net/get',
            params={
                'q': text,
                'langpair': f'en|{target_code}',
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('responseStatus') == 200 and 'translatedText' in data['responseData']:
                translated = data['responseData']['translatedText']
                print(f"[INFO] Translated '{text}' to {target_language}: '{translated}'")
                return translated
            else:
                print(f"[WARN] MyMemory API returned status: {data.get('responseStatus')}")
                return text
        else:
            print(f"[WARN] MyMemory API returned status code: {response.status_code}")
            return text
            
    except requests.exceptions.Timeout:
        print(f"[WARN] Translation request timed out for '{text}'")
        return text
    except requests.exceptions.RequestException as e:
        print(f"[WARN] Translation API error: {e}")
        return text
    except Exception as e:
        print(f"[ERROR] Unexpected translation error: {e}")
        return text
