"""Translation service for multi-language support using free translation APIs"""

import requests
from typing import List
import unicodedata


def _is_devanagari(s: str) -> bool:
    # Basic check: characters in Devanagari block
    return any(0x0900 <= ord(ch) <= 0x097F for ch in s)


def _ascii_preview(s: str, max_len: int = 80) -> str:
    """Return an ASCII-safe preview of text to avoid Windows console encoding errors."""
    # Strip non-spacing marks to reduce risk, then encode ASCII with replacement
    try:
        nfkd = unicodedata.normalize("NFKD", s)
        ascii_text = nfkd.encode("ascii", "ignore").decode("ascii")
        ascii_text = ascii_text[:max_len]
        return ascii_text if ascii_text else "[unicode text]"
    except Exception:
        return "[text preview unavailable]"


def _try_mymemory(text: str, target_code: str, timeout: float = 6.0) -> str | None:
    resp = requests.get(
        "https://api.mymemory.translated.net/get",
        params={"q": text, "langpair": f"en|{target_code}"},
        timeout=timeout,
    )
    if resp.status_code != 200:
        print(f"[WARN] MyMemory status code: {resp.status_code} for {target_code}")
        return None
    data = resp.json()
    if data.get("responseStatus") != 200:
        print(f"[WARN] MyMemory responseStatus: {data.get('responseStatus')} for {target_code}")
        return None
    translated = data.get("responseData", {}).get("translatedText")
    return translated


def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translate English `text` to `target_language` using MyMemory (free).
    Adds fallbacks for Marathi (mr) and other codes, with light heuristics.
    """
    if not text:
        return text

    # Normalize code like 'mr-IN' -> 'mr'
    target_language = (target_language or "en").lower()
    if target_language in ("en", "en-us", "en-in"):
        return text
    if "-" in target_language:
        target_language = target_language.split("-")[0]

    # Preferred codes and fallbacks per target
    # Order matters: we'll try in sequence until one yields a translation
    preferred: dict[str, List[str]] = {
        "hi": ["hi", "hi-IN"],
        "mr": ["mr-IN", "mr"],  # try mr-IN then mr (works better on some days)
        "ta": ["ta"],
        "te": ["te"],
        "kn": ["kn"],
        "ml": ["ml"],
        "bn": ["bn"],
        "gu": ["gu"],
    }

    if target_language not in preferred:
        print(f"[WARN] Unsupported language: {target_language}. Returning original text.")
        return text

    # If already Devanagari and target is hi/mr, return as-is
    if target_language in ("hi", "mr") and _is_devanagari(text):
        return text

    for code in preferred[target_language]:
        try:
            translated = _try_mymemory(text, code)
            if translated and translated.strip():
                # Sometimes API echoes the same text back; accept only if changed or in target script
                if translated != text or _is_devanagari(translated):
                    # Avoid printing full Unicode that may break on Windows consoles
                    src_prev = _ascii_preview(text)
                    dst_prev = _ascii_preview(translated)
                    print(f"[INFO] Translated '{src_prev}' to {target_language} ({code}): '{dst_prev}'")
                    return translated
                else:
                    print(f"[WARN] Translation unchanged for {code}, trying fallback...")
        except requests.exceptions.Timeout:
            print(f"[WARN] Translation timeout for {code}, trying fallback...")
        except requests.exceptions.RequestException as e:
            print(f"[WARN] Translation API error for {code}: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected translation error for {code}: {e}")

    # All attempts failed; return original
    return text
