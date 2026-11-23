"""Core Base64 encode/decode helpers (standard library only).

The URL-safe alphabet replaces ``+`` with ``-`` and ``/`` with ``_``,
so the output is safe to use in URLs and filenames.
"""

import base64
import binascii


def encode_bytes(data: bytes, urlsafe: bool = False) -> str:
    """Encode bytes to a Base64 string."""
    encoder = base64.urlsafe_b64encode if urlsafe else base64.b64encode
    return encoder(data).decode("ascii")


def encode_text(text: str, urlsafe: bool = False) -> str:
    """Encode a text string (UTF-8) to a Base64 string."""
    return encode_bytes(text.encode("utf-8"), urlsafe=urlsafe)


def decode_bytes(encoded: str, urlsafe: bool = False) -> bytes:
    """Decode a Base64 string back to bytes.

    Raises ValueError on invalid Base64 input (bad characters or
    bad padding) instead of silently returning garbage.
    """
    text = "".join(encoded.split())
    if urlsafe:
        # urlsafe_b64decode takes no validate flag, so translate the
        # URL-safe alphabet back to the standard one and validate there.
        text = text.translate(str.maketrans("-_", "+/"))
    try:
        return base64.b64decode(text, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError(f"invalid Base64 input: {exc}") from exc


def decode_text(encoded: str, urlsafe: bool = False) -> str:
    """Decode a Base64 string back to a text string (UTF-8)."""
    return decode_bytes(encoded, urlsafe=urlsafe).decode("utf-8")


def wrap_text(text: str, width: int) -> str:
    """Wrap text at ``width`` columns (like the ``base64`` command).

    A width of 0 or less disables wrapping and returns the text unchanged.
    """
    if width <= 0:
        return text
    return "\n".join(text[i : i + width] for i in range(0, len(text), width))
