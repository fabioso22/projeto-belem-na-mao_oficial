"""
Módulo de Geração de Dados Simulados e Análise Exploratória (Pandas) — BelémNaMão
Baseado no modelo DataInsight: transforma registros de interações turísticas
em indicadores mensais, rankings de procura e insights baseados em regras.
"""
import random
from datetime import date
from typing import List, Optional

import pandas as pd


NOMES_MESES_PT = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}

LOCAIS_TURISTICOS = [
    {"nome": "Mercado Ver-o-Peso", "categoria": "Gastronomia", "base": 420, "taxa_roteiro": 0.38},
    {"nome": "Estação das Docas", "categoria": "Gastronomia", "base": 390, "taxa_roteiro": 0.42},
    {"nome": "Complexo Feliz Lusitânia", "categoria": "História", "base": 310, "taxa_roteiro": 0.35},
    {"nome": "Mangal das Garças", "categoria": "Natureza", "base": 280, "taxa_roteiro": 0.36},
    {"nome": "Theatro da Paz", "categoria": "Cultura", "base": 260, "taxa_roteiro": 0.34},
    {"nome": "Ilha do Combu", "categoria": "Passeio", "base": 240, "taxa_roteiro": 0.40},
    {"nome": "Basílica de Nazaré", "categoria": "Cultura", "base": 290, "taxa_roteiro": 0.37},
]

# Fatores sazonais gerais de turismo em Belém (Julho = Férias/Verão Amazônico, Outubro = Círio, Dezembro = Festas)
FATORES_MES = {
    1: 1.00,
    2: 0.90,
    3: 0.85,
    4: 0.80,
    5: 0.90,
    6: 1.00,
    7: 1.45,
    8: 1.05,
    9: 1.00,
    10: 1.55,
    11: 1.10,
    12: 1.35,
}

# Fatores específicos por atração e mês (evidenciando sazonalidades para fins didáticos)
FATORES_LOCAIS = {
    "Mercado Ver-o-Peso": {7: 1.25, 10: 1.40},
    "Estação das Docas": {7: 1.40, 12: 1.30},
    "Complexo Feliz Lusitânia": {10: 1.35, 12: 1.20},
    "Mangal das Garças": {7: 1.45, 8: 1.15},
    "Theatro da Paz": {10: 1.25, 12: 1.45},
    "Ilha do Combu": {7: 1.60, 1: 1.25},
    "Basílica de Nazaré": {10: 1.85, 5: 1.15},
}

OCASIOES_BELEM = {
    1: "Férias de Verão / Início de Ano",
    7: "Férias Escolares e Verão Amazônico",
    10: "Círio de Nazaré (Alta Temporada Religiosa e Cultural)",
    12: "Festas e Programação de Fim de Ano",
}


def gerar_base_simulada() -> pd.DataFrame:
    """
    Gera automaticamente um DataFrame fictício de 12 meses (2025)
    com interações de turistas nos pontos turísticos de Belém.
    Usa random.seed(42) para reprodutibilidade nos testes e apresentações.
    """
    random.seed(42)
    registros = []

    for local in LOCAIS_TURISTICOS:
        nome = local["nome"]
        categoria = local["categoria"]
        base_acessos = local["base"]
        taxa_base = local["taxa_roteiro"]

        for mes in range(1, 13):
            fator_mes = FATORES_MES[mes]
            fator_local = FATORES_LOCAIS.get(nome, {}).get(mes, 1.0)
            acessos_esperados = base_acessos * fator_mes * fator_local

            for dia in (5, 15, 25):
                variacao_acessos = random.randint(-20, 20)
                acessos = max(30, int(round(acessos_esperados + variacao_acessos)))

                variacao_taxa = random.uniform(-0.03, 0.03)
                taxa_efetiva = max(0.15, min(0.75, taxa_base + variacao_taxa))
                adicionados_roteiro = max(5, int(round(acessos * taxa_efetiva)) + random.randint(-4, 4))
                adicionados_roteiro = min(adicionados_roteiro, acessos)

                registros.append(
                    {
                        "data": date(2025, mes, dia).isoformat(),
                        "mes": mes,
                        "nome_mes": NOMES_MESES_PT[mes],
                        "local": nome,
                        "categoria": categoria,
                        "acessos": acessos,
                        "adicionados_roteiro": adicionados_roteiro,
                    }
                )

    df = pd.DataFrame(registros)
    df["data"] = pd.to_datetime(df["data"])
    df["taxa_conversao"] = (df["adicionados_roteiro"] / df["acessos"] * 100).round(1)
    return df


def carregar_dados() -> pd.DataFrame:
    """Carrega a base simulada de 12 meses tipada e ordenada cronologicamente."""
    df = gerar_base_simulada()
    if df.empty:
        return df

    df["data"] = pd.to_datetime(df["data"])
    df = df.sort_values("data").reset_index(drop=True)
    return df


def _garantir_df(df: Optional[pd.DataFrame]) -> pd.DataFrame:
    return df if df is not None and not df.empty else carregar_dados()


def locais_mais_procurados(df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Agrupa por local e categoria, somando acessos e adições ao roteiro em ordem decrescente."""
    base = _garantir_df(df)
    ranking = (
        base.groupby(["local", "categoria"], as_index=False)[["acessos", "adicionados_roteiro"]]
        .sum()
        .sort_values("adicionados_roteiro", ascending=False)
        .reset_index(drop=True)
    )
    ranking["taxa_conversao"] = (ranking["adicionados_roteiro"] / ranking["acessos"] * 100).round(1)
    return ranking


def resumo_mensal(df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Resume acessos, adições ao roteiro e variação percentual mês a mês (Janeiro a Dezembro)."""
    base = _garantir_df(df)
    mensal = (
        base.groupby(["mes", "nome_mes"], as_index=False)[["acessos", "adicionados_roteiro"]]
        .sum()
        .sort_values("mes")
        .reset_index(drop=True)
    )
    mensal["crescimento_%"] = (mensal["acessos"].pct_change() * 100).round(1)
    mensal["taxa_conversao"] = (mensal["adicionados_roteiro"] / mensal["acessos"] * 100).round(1)
    return mensal


def gerar_insights(df: Optional[pd.DataFrame] = None) -> List[str]:
    """
    Motor de Insights baseado em regras simples (regra de > 130% da média mensal):
    Identifica locais e meses com procura acima de 130% da média histórica.
    """
    base = _garantir_df(df)
    insights: List[str] = []

    agrupado = (
        base.groupby(["local", "mes", "nome_mes"], as_index=False)[["acessos", "adicionados_roteiro"]]
        .sum()
    )

    # 1. Regra de > 130% da média por ponto turístico
    for nome_local in agrupado["local"].unique():
        dados_local = agrupado[agrupado["local"] == nome_local]
        media_roteiros = dados_local["adicionados_roteiro"].mean()
        idx_pico = dados_local["adicionados_roteiro"].idxmax()
        linha_pico = dados_local.loc[idx_pico]

        qtd_pico = int(linha_pico["adicionados_roteiro"])
        acessos_pico = int(linha_pico["acessos"])
        mes_pico = int(linha_pico["mes"])
        nome_mes_pico = str(linha_pico["nome_mes"])

        if qtd_pico > media_roteiros * 1.3:
            percentual_acima = ((qtd_pico - media_roteiros) / media_roteiros) * 100
            ocasiao = OCASIOES_BELEM.get(mes_pico, "Período de Alta Demanda Local")
            insights.append(
                f"🔥 PICO POR LOCAL — {nome_local} ({nome_mes_pico}): "
                f"{qtd_pico:,} adições ao roteiro ({acessos_pico:,} acessos), "
                f"{percentual_acima:.0f}% acima da média mensal ({media_roteiros:.1f}).\n"
                f"   ↳ Contexto: {ocasiao}. Recomendação: destacar guias rápidos, horários alternativos e rotas próximas na aba Explorar."
            )

    # 2. Regra de > 130% da média geral mensal da plataforma
    totais_mes = (
        base.groupby(["mes", "nome_mes"], as_index=False)[["acessos", "adicionados_roteiro"]]
        .sum()
        .sort_values("mes")
    )
    media_geral_acessos = totais_mes["acessos"].mean()
    for _, linha in totais_mes.iterrows():
        acessos_m = int(linha["acessos"])
        roteiros_m = int(linha["adicionados_roteiro"])
        mes_m = int(linha["mes"])
        nome_m = str(linha["nome_mes"])
        if acessos_m > media_geral_acessos * 1.3:
            pct = ((acessos_m - media_geral_acessos) / media_geral_acessos) * 100
            ocasiao = OCASIOES_BELEM.get(mes_m, "Pico Geral de Visitação")
            insights.append(
                f"📈 ALTA GERAL EM {nome_m.upper()}: "
                f"{acessos_m:,} acessos e {roteiros_m:,} inclusões em roteiros "
                f"({pct:.0f}% acima da média anual de {media_geral_acessos:.0f} acessos/mês).\n"
                f"   ↳ Contexto: {ocasiao}. Recomendação: reforçar infraestrutura turística, alertas de chuva/maré e sugestões de deslocamento."
            )

    if not insights:
        insights.append("Nenhum local ou mês ultrapassou o limite de 130% da média na base atual.")

    return insights
