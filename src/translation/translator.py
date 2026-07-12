"""Facade that dispatches encoding/decoding to the right alphabet strategy.

Adding a new alphabet is a matter of registering its functions here (open/closed).
"""
from src.translation.encoder import encode_brazilian, encode_north_american, encode_chinese
from src.translation.decoder import decode_brazilian, decode_north_american, decode_chinese


_ENCODERS = {
    "Brazilian": encode_brazilian,
    "North American": encode_north_american,
    "Chinese": encode_chinese,
}

_DECODERS = {
    "Brazilian": decode_brazilian,
    "North American": decode_north_american,
    "Chinese": decode_chinese,
}


def encode(text: str, alphabet: str = "North American") -> str:
    strategy = _ENCODERS.get(alphabet)
    if strategy is None:
        return "Alphabet not found."
    return strategy(text)


def decode(braille: str, alphabet: str = "North American") -> str:
    strategy = _DECODERS.get(alphabet)
    if strategy is None:
        return "Alphabet not found."
    return strategy(braille)
