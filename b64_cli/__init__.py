"""base64-cli: Base64 encode/decode from the command line.

Encode text or files to Base64 (standard or URL-safe alphabet) and decode
them back, from a file or from standard input.
"""

from .codec import (
    decode_bytes,
    decode_text,
    encode_bytes,
    encode_text,
    wrap_text,
)

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "decode_bytes",
    "decode_text",
    "encode_bytes",
    "encode_text",
    "wrap_text",
]
