"""Translates CIDEr object code notation to target languages."""
import json

def emit(codex_blocks: list):
    for obj in codex_blocks:
        codex = json.loads(obj['codex'])
        response = codex['response']
        if codex['status'] == "OK":
            print(response)
        else:
            print(obj, response)
            break