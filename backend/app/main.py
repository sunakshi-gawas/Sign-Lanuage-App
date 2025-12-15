from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import re

import cv2
import numpy as np
import mediapipe as mp

from .schemas import (
    SignToTextRequest,
    SignToTextResponse,
    TextToSignRequest,
    TextToSignResponse,
)
from .services.sign_classifier import SignClassifier
from .services.translator import translate_text

# ====================== PATHS & STATIC ======================

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/

app = FastAPI(title="SignVerse AI Backend")

# Folder that stores your GIFs, e.g. backend/sign_gifs/HELLO.gif
GIF_DIR = BASE_DIR / "sign_gifs"
GIF_URL_PREFIX = "/sign_gifs"

if GIF_DIR.exists():
    app.mount(
        GIF_URL_PREFIX,
        StaticFiles(directory=GIF_DIR, html=False),
        name="sign_gifs",
    )
    print(f"[INFO] Serving GIFs from: {GIF_DIR} at {GIF_URL_PREFIX}/...")
else:
    print(f"[WARN] GIF directory not found: {GIF_DIR}. Text→Sign GIFs will not work.")

# ====================== CORS ======================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for dev, you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================== SERVICES ======================

classifier = SignClassifier()

# ====================== MEDIAPIPE (Sign → Text) ======================

mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5,
)

# ====================== HELPERS ======================


def label_to_text(label: str) -> str:
    """
    'HELLO' -> 'Hello'
    'THANK_YOU' -> 'Thank You'
    UNKNOWN/empty -> polite error.
    """
    if not label or label.upper() == "UNKNOWN":
        return "I did not understand the sign."
    return label.replace("_", " ").title()


def text_to_tokens(raw: str) -> list[str]:
    """
    Very simple tokenizer:
    - uppercase
    - keep only A–Z and spaces
    - split on spaces
    Example: "Hello, please help!" -> ["HELLO", "PLEASE", "HELP"]
    """
    cleaned = re.sub(r"[^A-Za-z ]+", " ", raw.upper())
    tokens = [t for t in cleaned.split() if t]
    return tokens


def token_to_gif_url(token: str) -> str | None:
    """
    For token 'HELLO' it checks:
      backend/sign_gifs/HELLO.gif
    If exists -> returns '/sign_gifs/HELLO.gif'
    Else -> None
    """
    fname = f"{token}.gif"
    fpath = GIF_DIR / fname
    if fpath.exists():
        return f"{GIF_URL_PREFIX}/{fname}"
    return None


# ====================== ROUTES ======================

@app.get("/")
def root():
    return {"status": "ok", "message": "SignVerse AI backend running"}


# --------------- HEALTH CHECK (for auto-discovery) ----------------

@app.get("/api/health")
def health_check():
    """
    Health check endpoint used by mobile app for server auto-discovery.
    Returns quickly to verify server is running without loading heavy models.
    """
    return {"status": "healthy", "service": "SignVerse AI"}


# ---------------- SIGN → TEXT (features) ----------------

@app.post("/api/sign-to-text", response_model=SignToTextResponse)
def sign_to_text(req: SignToTextRequest):
    """
    Old feature-based sign→text endpoint.
    Kept as-is to avoid breaking your working sign pipeline.
    Supports language parameter for translation.
    """
    try:
        label, confidence = classifier.predict(req.features)
        text = label_to_text(label)
        
        # Translate if requested
        if req.language and req.language != "en":
            text = translate_text(text, req.language)
        
        return SignToTextResponse(text=text, confidence=float(confidence))
    except Exception as e:
        print("[ERROR] sign_to_text:", e)
        return SignToTextResponse(text=f"ML error: {e}", confidence=0.0)


# ---------------- SIGN → TEXT (camera image) ----------------

@app.post("/api/sign-to-text-image", response_model=SignToTextResponse)
async def sign_to_text_image(request: Request):
    """
    Sign recognition from camera image.
    Supports language query parameter for translation.
    Usage: POST /api/sign-to-text-image?language=hi
    """
    # Get language from query parameters, default to English
    language = request.query_params.get("language", "en")
    
    raw = await request.body()
    np_arr = np.frombuffer(raw, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return SignToTextResponse(text="Invalid image received.")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = cv2.flip(img_rgb, 1)

    results = hands_detector.process(img_rgb)

    if not results.multi_hand_landmarks:
        text = "No hand detected. Show your hand clearly."
        if language and language != "en":
            text = translate_text(text, language)
        return SignToTextResponse(text=text)

    hand_landmarks = results.multi_hand_landmarks[0].landmark
    landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks]

    try:
        label, confidence = classifier.predict_from_landmarks(landmarks)
        text = label_to_text(label)
        
        # Translate if requested
        if language and language != "en":
            text = translate_text(text, language)
        
        return SignToTextResponse(text=text, confidence=float(confidence))
    except Exception as e:
        print("[ERROR] sign_to_text_image:", e)
        return SignToTextResponse(text=f"Recognition error: {e}", confidence=0.0)


# ---------------- TEXT → SIGN (dynamic GIFs) ----------------

@app.post("/api/text-to-sign", response_model=TextToSignResponse)
def text_to_sign(req: TextToSignRequest):
    """
    New dynamic GIF-based text→sign endpoint.

    - Tokenize input text into words: ["HELLO", "PLEASE", "HELP"]
    - For each word, look for a GIF: sign_gifs/HELLO.gif, PLEASE.gif, HELP.gif
    - Return:
        sign_tokens = ["HELLO", "PLEASE", "HELP"]
        avatar_animation_ids = ["/sign_gifs/HELLO.gif", "/sign_gifs/PLEASE.gif", ...]
    """
    try:
        tokens = text_to_tokens(req.text)
        print("[INFO] TextToSign tokens:", tokens)

        gif_urls: list[str] = []
        for t in tokens:
            url = token_to_gif_url(t)
            if url:
                gif_urls.append(url)
            else:
                print(f"[WARN] No GIF found for token '{t}'")

        # Fallback: if no GIFs matched at all, try UNKNOWN.gif
        if not gif_urls:
            unknown_url = token_to_gif_url("UNKNOWN")
            if unknown_url:
                gif_urls.append(unknown_url)

        return TextToSignResponse(
            sign_tokens=tokens,
            avatar_animation_ids=gif_urls,
        )
    except Exception as e:
        print("[ERROR] text_to_sign:", e)
        return TextToSignResponse(
            sign_tokens=["ERROR"],
            avatar_animation_ids=[],
        )


# ====================== END OF FILE ======================