import json
from pathlib import Path
from typing import Any, Dict, List

from services.database import buscar_locais_db, inicializar_banco, listar_todos_locais

ROOT = Path(__file__).resolve().parents[1]
LOCAIS_FILE = ROOT / "data" / "locais.json"


def carregar_locais() -> List[Dict[str, Any]]:
    """Carrega os locais a partir do banco SQLite, com fallback para JSON se necessário."""
    try:
        locais = listar_todos_locais()
        if locais:
            return locais
    except Exception as e:
        print(f"[Aviso] Erro ao carregar locais do SQLite: {e}")

    # Fallback seguro para locais.json
    if LOCAIS_FILE.exists():
        with LOCAIS_FILE.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return []


def buscar_locais(
    locais: List[Dict[str, Any]],
    texto: str = "",
    categoria: str = "Todas",
    preco: str = "Qualquer",
) -> List[Dict[str, Any]]:
    """Filtra locais por termo de busca, categoria e faixa de preço."""
    termo = texto.strip().casefold()
    resultado = []

    mapa_preco = {"Baixo": 1, "Médio": 2, "Alto": 3}
    limite_preco = mapa_preco.get(preco)

    for local in locais:
        texto_local = " ".join([
            local.get("nome", ""),
            local.get("bairro", ""),
            local.get("descricao", ""),
            " ".join(local.get("tags", [])),
        ]).casefold()

        if termo and termo not in texto_local:
            continue
        if categoria != "Todas" and categoria not in local.get("categoria", []):
            continue
        if limite_preco is not None and local.get("preco", 2) > limite_preco:
            continue

        resultado.append(local)

    return resultado


def rotulo_preco(valor: Any) -> str:
    """Converte o valor numérico de preço para texto legível."""
    return {1: "$ · Baixo", 2: "$$ · Médio", 3: "$$$ · Alto"}.get(valor, "Não informado")

# fim