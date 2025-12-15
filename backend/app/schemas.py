from pydantic import BaseModel
from typing import List, Optional


class SignToTextRequest(BaseModel):
    features: List[float]
    language: Optional[str] = "en"  # Language code for translation (e.g., "en", "hi", "mr")


class SignToTextResponse(BaseModel):
    text: str
    confidence: Optional[float] = None  # Confidence score (0.0 to 1.0)


class TextToSignRequest(BaseModel):
    text: str
    # kept for compatibility; you can ignore it in backend
    sign_language: Optional[str] = "ISL"


class TextToSignResponse(BaseModel):
    sign_tokens: List[str]
    # now used to return GIF URLs (relative paths like /sign_gifs/HELLO.gif)
    avatar_animation_ids: List[str]
