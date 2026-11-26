"""
Módulo de Análise Exploratória (Pandas) conectado ao MySQL na Aiven — BelémNaMão
Consulta os registros reais da tabela `visitas_mensais` (integrada com `locais`,
`local_categorias` e `roteiro_itens`) via `pandas.read_sql()`.
"""
from typing import List, Optional
import warnings

import pandas as pd

from services.database import MYSQL_CONFIG, obter_conexao


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

OCASIOES_BELEM = {
    1: "Férias de Verão / Início de Ano",
    7: "Férias Escolares e Verão Amazônico",
    10: "Círio de Nazaré (Alta Temporada Religiosa e Cultural)",
    12: "Festas e Programação de Fim de Ano",
}

QUERY_VISITAS_AIVEN = """
SELECT
    v.id,
    v.local_id,
    v.ano,
    v.mes,
    STR_TO_DATE(CONCAT(v.ano, '-', LPAD(v.mes, 2, '0'), '-01'), '%Y-%m-%d') AS data,
    l.nome AS local,
    COALESCE(
        (
            SELECT lc.categoria
            FROM local_categorias lc
            WHERE lc.local_id = l.id
            ORDER BY lc.categoria ASC
            LIMIT 1
        ),
        'Turismo'
    ) AS categoria,
    v.visitas_mes AS acessos,
    v.visitas_semana,
    (v.avaliacoes_qtd + COALESCE(r.qtd_roteiro, 0)) AS adicionados_roteiro,
    v.nota_media
FROM visitas_mensais v
JOIN locais l ON v.local_id = l.id
LEFT JOIN (
    SELECT local_id, COUNT(*) AS qtd_roteiro
    FROM roteiro_itens
    GROUP BY local_id
) r ON r.local_id = l.id
ORDER BY v.ano ASC, v.mes ASC, l.nome ASC;
"""


def carregar_dados() -> pd.DataFrame:
    """
    Carrega os registros reais do banco MySQL hospedado na Aiven diretamente via
    `pandas.read_sql()`, reaproveitando as credenciais/SSL de `services.database`.
    """
    with obter_conexao() as conn:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, message=".*pandas only supports SQLAlchemy.*")
            df = pd.read_sql(QUERY_VISITAS_AIVEN, conn)

    if df.empty:
        return df

    df["data"] = pd.to_datetime(df["data"])
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce").fillna(0).astype(int)
    df["mes"] = pd.to_numeric(df["mes"], errors="coerce").fillna(1).astype(int)
    df["nome_mes"] = df["mes"].map(NOMES_MESES_PT).fillna("Mês")
    df["acessos"] = pd.to_numeric(df["acessos"], errors="coerce").fillna(0).astype(int)
    df["adicionados_roteiro"] = pd.to_numeric(df["adicionados_roteiro"], errors="coerce").fillna(0).astype(int)
    df["taxa_conversao"] = (
        df["adicionados_roteiro"] / df["acessos"].replace(0, pd.NA) * 100
    ).fillna(0.0).astype(float).round(1)

    df = df.sort_values(["data", "local"]).reset_index(drop=True)
    return df


def _garantir_df(df: Optional[pd.DataFrame]) -> pd.DataFrame:
    return df if df is not None and not df.empty else carregar_dados()


def locais_mais_procurados(df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Agrupa por local e categoria, somando acessos e interações/roteiros em ordem decrescente."""
    base = _garantir_df(df)
    ranking = (
        base.groupby(["local", "categoria"], as_index=False)[["acessos", "adicionados_roteiro"]]
        .sum()
        .sort_values(["adicionados_roteiro", "acessos"], ascending=False)
        .reset_index(drop=True)
    )
    ranking["taxa_conversao"] = (
        ranking["adicionados_roteiro"] / ranking["acessos"].replace(0, pd.NA) * 100
    ).fillna(0.0).astype(float).round(1)
    return ranking


def resumo_mensal(df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Resume acessos, adições/interações e variação percentual mês a mês (Janeiro a Dezembro)."""
    base = _garantir_df(df)
    mensal = (
        base.groupby(["mes", "nome_mes"], as_index=False)[["acessos", "adicionados_roteiro"]]
        .sum()
        .sort_values("mes")
        .reset_index(drop=True)
    )
    mensal["crescimento_%"] = (mensal["acessos"].pct_change() * 100).round(1)
    mensal["taxa_conversao"] = (
        mensal["adicionados_roteiro"] / mensal["acessos"].replace(0, pd.NA) * 100
    ).fillna(0.0).astype(float).round(1)
    return mensal


def gerar_insights(df: Optional[pd.DataFrame] = None) -> List[str]:
    """
    Motor de Insights baseado em regras (> 130% da média mensal):
    Identifica locais e meses com procura acima de 130% da média histórica real.
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

        if media_roteiros > 0 and qtd_pico > media_roteiros * 1.3:
            percentual_acima = ((qtd_pico - media_roteiros) / media_roteiros) * 100
            ocasiao = OCASIOES_BELEM.get(mes_pico, "Período de Alta Demanda Local")
            insights.append(
                f"🔥 PICO POR LOCAL — {nome_local} ({nome_mes_pico}): "
                f"{qtd_pico:,} interações/roteiros ({acessos_pico:,} acessos), "
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
        if media_geral_acessos > 0 and acessos_m > media_geral_acessos * 1.3:
            pct = ((acessos_m - media_geral_acessos) / media_geral_acessos) * 100
            ocasiao = OCASIOES_BELEM.get(mes_m, "Pico Geral de Visitação")
            insights.append(
                f"📈 ALTA GERAL EM {nome_m.upper()}: "
                f"{acessos_m:,} acessos e {roteiros_m:,} interações/roteiros "
                f"({pct:.0f}% acima da média anual de {media_geral_acessos:.0f} acessos/mês).\n"
                f"   ↳ Contexto: {ocasiao}. Recomendação: reforçar infraestrutura turística, alertas de chuva/maré e sugestões de deslocamento."
            )

    if not insights:
        insights.append("Nenhum local ou mês ultrapassou o limite de 130% da média na base atual.")

    return insights
