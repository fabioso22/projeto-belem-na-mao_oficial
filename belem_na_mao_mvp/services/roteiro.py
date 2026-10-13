import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROTEIRO_FILE = ROOT / "data" / "roteiro.json"


def carregar_roteiro():
    if not ROTEIRO_FILE.exists():
        return []
    try:
        with ROTEIRO_FILE.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        return []


def salvar_roteiro(roteiro):
    ROTEIRO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with ROTEIRO_FILE.open("w", encoding="utf-8") as arquivo:
        json.dump(roteiro, arquivo, ensure_ascii=False, indent=2)


def adicionar(roteiro, local):
    if not any(item.get("id") == local.get("id") for item in roteiro):
        roteiro.append(local)
    salvar_roteiro(roteiro)
    return roteiro


def remover(roteiro, local_id):
    atualizado = [item for item in roteiro if item.get("id") != local_id]
    salvar_roteiro(atualizado)
    return atualizado
