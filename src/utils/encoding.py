import base64
import binascii


def decode_base64(encoded_text: str) -> str:
    """Decodes a base64 encoded string back to plain text. Returns empty string on error."""
    try:
        return base64.b64decode(encoded_text).decode('utf-8', errors='replace')
    except (binascii.Error, ValueError):
        return ""
