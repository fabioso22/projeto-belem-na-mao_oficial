import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAIS_FILE = ROOT / "data" / "locais.json"


def carregar_locais():
    with LOCAIS_FILE.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def buscar_locais(locais, texto="", categoria="Todas", preco="Qualquer"):
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


def rotulo_preco(valor):
    return {1: "$ · Baixo", 2: "$$ · Médio", 3: "$$$ · Alto"}.get(valor, "Não informado")
