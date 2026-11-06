import json


def bytes_to_unicode() -> dict[int, str]:
    """checks for special characters: every
    byte (0-255) -> visible character."""
    bs = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return dict(zip(bs, (chr(c) for c in cs)))


BYTE_DECODER: dict[str, int] = {
    c: b for b, c in bytes_to_unicode().items()
}


def token_to_text(token: str) -> str:
    """Token from vocab -> real text. Returns "" if not usable."""
    try:
        return bytes(BYTE_DECODER[c] for c in token).decode("utf-8")
    except (KeyError, UnicodeDecodeError):
        return ""


def load_id_to_text(vocab_path: str) -> dict[int, str]:
    """Reads vocab.json (token -> id) and returns id -> real text."""
    with open(vocab_path, encoding="utf-8") as f:
        vocab: dict[str, int] = json.load(f)
    return {i: token_to_text(t) for t, i in vocab.items()}
