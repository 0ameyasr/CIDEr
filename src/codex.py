"""Turns CIDEr script code blocks into object notation (JSON-only conversation)."""

from google import genai
from src.utils import get_prompt

GEMINI_MODEL_NAME = "gemini-2.0-flash"


def generate(request: str):
    client = genai.Client()
    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=request,
        config={
            "response_mime_type": "application/json",
        },
    ).text
    return response


def inline_block(target: str, block: str):
    payload = get_prompt("inline_block", ext=target, block=block)
    response = generate(payload)
    return response