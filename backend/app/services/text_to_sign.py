from .gloss_ai import GlossAI
from .sign_avatar_mapper import AvatarMapper

class TextToSignService:
    def __init__(self):
        self.avatar = AvatarMapper()

    def text_to_sign_tokens(self, text, sign_language="ISL"):
        return GlossAI.text_to_gloss(text)

    def tokens_to_avatar_ids(self, tokens):
        return [self.avatar.token_to_animation(t) for t in tokens]
