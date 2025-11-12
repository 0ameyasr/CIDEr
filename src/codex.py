"""Turns CIDEr script code blocks into object notation (JSON-only conversation)."""

import os

from google import genai
from ollama import chat
from dotenv import load_dotenv

from src.utils import get_prompt

load_dotenv()
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")


def generate_gemini(request: str):
    """Generate a response for `request` using a Gemini model."""
    client = genai.Client()
    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=request,
        config={
            "response_mime_type": "application/json",
        },
    ).text
    return response


def generate_ollama(request: str):
    """Generate a response for `request` using an Ollama model."""
    response = chat(
        model=OLLAMA_MODEL_NAME,
        format="json",
        messages=[{"role": "user", "content": request}],
    )
    return response.message.content


def assemble_codex(code_objects: list):
    """Assemble the codex representation for a list of code-objects."""
    codex = f"Use `.{code_objects[0]['raw'].split(':')[1].strip()}`\n"
    for i in range(1, len(code_objects)):
        block = code_objects[i]
        buid = block["uid"]
        raw = block["raw"]
        sln, eln = block["span"]
        codex += f"Block #{buid}, Lines <{sln},{eln}>& {raw}\n"
    return codex


def compile(codex: str, ollama: bool = False):
    """Compile the codex object using the configured model."""
    payload = get_prompt("compile", codex=codex)
    response = generate_ollama(payload) if ollama else generate_gemini(payload)
    return response

def optimize(code: str, ollama: bool = False):
    """Optimize the 1st norm compiled code into a 2nd norm form."""
    payload = get_prompt("optimize", code=code)
    response = generate_ollama(payload) if ollama else generate_gemini(payload)
    return response