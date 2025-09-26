from __future__ import annotations

import base64
from typing import List, Optional

try:
    from PIL import Image as PILImage
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


_PROMPT = """
Please identify all food ingredients visible in this image.
Focus only on raw ingredients, produce, and food items.
Ignore any containers, utensils, packaging, or non-food objects.
List each ingredient on a separate line. Do not include numbering or bullets.
""".strip()


def _guess_mime(image_bytes: bytes) -> str:
    """Tiny mime sniffer. Prefer JPEG if unsure."""
    if image_bytes.startswith(b"\xff\xd8"):
        return "image/jpeg"
    if image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    return "image/jpeg"


def _normalize_lines(text: str) -> List[str]:
    out: List[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        low = line.lower()
        if low.startswith(("okay", "here are", "ingredients:", "ingredient list")):
            continue

        while line and (line[0] in "-•*0123456789. "):
            line = line[1:].lstrip()
        if line and line not in out:
            out.append(line)
    return out


def identify_ingredients_from_image(client, image_bytes: bytes) -> List[str]:
    """
    Use Gemini to extract ingredient names from an image.
    Returns [] if client is None (offline) or on model error.
    """
    if not image_bytes:
        return []
    if client is None:
        return []

    # Pick mime
    mime = _guess_mime(image_bytes)
    if PIL_AVAILABLE:
        try:

            im = PILImage.open(io.BytesIO(image_bytes)) 
            fmt = (im.format or "").upper()
            if fmt == "PNG":
                mime = "image/png"
            elif fmt == "JPEG" or fmt == "JPG":
                mime = "image/jpeg"
        except Exception:
            pass

    image_part = {
        "inline_data": {
            "mime_type": mime,
            "data": base64.b64encode(image_bytes).decode("utf-8"),
        }
    }

    try:
        resp = client.generate_content(
            contents=[{"parts": [{"text": _PROMPT}, image_part]}]
        )
        return _normalize_lines(resp.text or "")
    except Exception:
        return []


def identify_ingredients_from_path(client, path: str) -> List[str]:
    """Convenience: read file and call identify_ingredients_from_image."""
    with open(path, "rb") as f:
        data = f.read()
    return identify_ingredients_from_image(client, data)