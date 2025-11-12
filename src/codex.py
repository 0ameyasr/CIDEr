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


def assemble_codex(code_objects: list):
    codex = f"Use `.{code_objects[0]['raw'].split(':')[1].strip()}`\n"
    for i in range(1, len(code_objects)):
        block = code_objects[i]
        buid = block["uid"]
        raw = block["raw"]
        sln, eln = block["span"]
        codex += f"Block #{buid}, Lines <{sln},{eln}>& {raw}\n"
    return codex


def compile(codex: str):
    payload = get_prompt("compile", codex=codex)
    response = generate(payload)
    return response
