import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from services.database import (
    adicionar_ao_roteiro_db,
    limpar_roteiro_db,
    obter_roteiro_db,
    remover_do_roteiro_db,
)

ROOT = Path(__file__).resolve().parents[1]
ROTEIRO_FILE = ROOT / "data" / "roteiro.json"


def carregar_roteiro(usuario_id: Optional[int] = 1) -> List[Dict[str, Any]]:
    """Carrega o roteiro salvo no banco SQLite para o usuário."""
    try:
        return obter_roteiro_db(usuario_id=usuario_id)
    except Exception as e:
        print(f"[Aviso] Erro ao carregar roteiro do SQLite: {e}")

    # Fallback para JSON
    if not ROTEIRO_FILE.exists():
        return []
    try:
        with ROTEIRO_FILE.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        return []


def salvar_roteiro(roteiro: List[Dict[str, Any]]) -> None:
    """Salva o roteiro em arquivo JSON para compatibilidade e backup."""
    try:
        ROTEIRO_FILE.parent.mkdir(parents=True, exist_ok=True)
        with ROTEIRO_FILE.open("w", encoding="utf-8") as arquivo:
            json.dump(roteiro, arquivo, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Aviso] Erro ao sincronizar roteiro.json: {e}")


def adicionar(
    roteiro: List[Dict[str, Any]],
    local: Dict[str, Any],
    usuario_id: Optional[int] = 1,
) -> List[Dict[str, Any]]:
    """Adiciona um local ao roteiro no SQLite e atualiza a lista em memória."""
    local_id = local.get("id")
    if local_id:
        adicionar_ao_roteiro_db(local_id, usuario_id=usuario_id)

    # Atualiza lista em memória se não estiver presente
    if not any(item.get("id") == local.get("id") for item in roteiro):
        roteiro.append(local)

    salvar_roteiro(roteiro)
    return roteiro


def remover(
    roteiro: List[Dict[str, Any]],
    local_id: str,
    usuario_id: Optional[int] = 1,
) -> List[Dict[str, Any]]:
    """Remove um local do roteiro no SQLite e na lista em memória."""
    remover_do_roteiro_db(local_id, usuario_id=usuario_id)
    atualizado = [item for item in roteiro if item.get("id") != local_id]
    salvar_roteiro(atualizado)
    return atualizado


def limpar(usuario_id: Optional[int] = 1) -> List[Dict[str, Any]]:
    """Limpa todo o roteiro do usuário no SQLite e em disco."""
    limpar_roteiro_db(usuario_id=usuario_id)
    salvar_roteiro([])
    return []
