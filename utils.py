from rapidfuzz import fuzz

from config import WAKE_WORD, MIN_SIMILARITY


def is_wake_word(text: str) -> bool:
    similarity = fuzz.ratio(WAKE_WORD.lower(), text.lower())
    return WAKE_WORD.lower() in text.lower() or similarity > MIN_SIMILARITY
