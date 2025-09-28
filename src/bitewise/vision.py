from __future__ import annotations
from typing import List
import io, base64
import json as _json

try:
    from PIL import Image as PILImage  # optional
except Exception:
    PILImage = None  # gracefully fall back to inline_data

_PROMPT_JSON = (
    "Identify edible grocery/food items visible in this photo. "
    "Return ONLY a JSON array of strings (unique, capitalized common names). "
    "No commentary."
)

_PROMPT_LINES = (
    "List all visible food ingredients (one per line, no numbers or bullets). "
    "Ignore packaging/utensils."
)

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

def _dedup_clamp(items: List[str], max_items: int) -> List[str]:
    seen, out = set(), []
    for it in (str(x).strip() for x in items):
        if it and it not in seen:
            seen.add(it)
            out.append(it)
        if len(out) >= max_items:
            break
    return out

def detect_ingredients(image_path: str, client, max_items: int = 20) -> List[str]:
    """
    Use Gemini Vision to detect edible grocery/food items in an image.
    Returns: list[str] of unique, capitalized common names (max max_items).
    Requires a configured client (see create_client in recipes.py).
    """
    if client is None:
        raise RuntimeError("Online detection requires GOOGLE_API_KEY. See .env setup.")

    with open(image_path, "rb") as f:
        data = f.read()
    mime = _guess_mime(data)

    # Prefer JSON array response for clean parsing
    try:
        from google.generativeai.types import GenerationConfig
        if PILImage:
            img = PILImage.open(io.BytesIO(data))
            resp = client.generate_content(
                [img, {"text": _PROMPT_JSON}],
                generation_config=GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )
        else:
            image_part = {
                "inline_data": {
                    "mime_type": mime,
                    "data": base64.b64encode(data).decode("utf-8"),
                }
            }
            resp = client.generate_content(
                [image_part, {"text": _PROMPT_JSON}],
                generation_config=GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )

        try:
            parsed = _json.loads(resp.text)
        except Exception:
            parsed = resp.text

        if isinstance(parsed, list):
            items = [str(x).strip() for x in parsed if str(x).strip()]
        elif isinstance(parsed, dict) and "ingredients" in parsed:
            items = [str(x).strip() for x in parsed["ingredients"] if str(x).strip()]
        elif isinstance(parsed, str):
            items = _normalize_lines(parsed)
        else:
            items = []
    except Exception:
        # Fallback: let the model return plain lines
        if PILImage:
            img = PILImage.open(io.BytesIO(data))
            resp2 = client.generate_content([img, {"text": _PROMPT_LINES}])
        else:
            image_part = {
                "inline_data": {
                    "mime_type": mime,
                    "data": base64.b64encode(data).decode("utf-8"),
                }
            }
            resp2 = client.generate_content([image_part, {"text": _PROMPT_LINES}])
        items = _normalize_lines(getattr(resp2, "text", "") or "")

    return _dedup_clamp(items, max_items)
