"""
Módulo de Visualização com Matplotlib para o Painel Admin (DataInsight) — BelémNaMão
Integra gráficos de linhas (evolução mensal) e barras (ranking de locais) ao CustomTkinter.
"""
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


MESES_ABREV = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def _paleta_grafico():
    """Retorna as cores do gráfico de acordo com o tema atual do CustomTkinter."""
    eh_dark = ctk.get_appearance_mode().lower() == "dark"
    if eh_dark:
        return {
            "fig_bg": "#0E1A2B",
            "ax_bg": "#1E293B",
            "texto": "#F8FAFC",
            "muted": "#94A3B8",
            "grid": "#334155",
            "linha_acessos": "#38BDF8",
            "linha_roteiros": "#C24B68",
            "barras": "#0284C7",
            "barras_top": "#38BDF8",
        }
    return {
        "fig_bg": "#FFFFFF",
        "ax_bg": "#F8F9FF",
        "texto": "#00132C",
        "muted": "#475569",
        "grid": "#E2E8F0",
        "linha_acessos": "#0284C7",
        "linha_roteiros": "#A13A53",
        "barras": "#0F2847",
        "barras_top": "#0284C7",
    }


def _criar_figura(df: pd.DataFrame, figsize=(6.6, 5.8)):
    """Constrói a figura Matplotlib com os 2 gráficos solicitados."""
    cores = _paleta_grafico()
    figura, eixos = plt.subplots(2, 1, figsize=figsize, dpi=100)
    figura.patch.set_facecolor(cores["fig_bg"])

    # --- Gráfico 1: Linhas — Evolução Mensal de Acessos e Roteiros ---
    mensal = (
        df.groupby("mes", as_index=False)[["acessos", "adicionados_roteiro"]]
        .sum()
        .sort_values("mes")
    )

    ax_linha = eixos[0]
    ax_linha.set_facecolor(cores["ax_bg"])
    ax_linha.plot(
        mensal["mes"],
        mensal["acessos"],
        marker="o",
        linewidth=2.4,
        color=cores["linha_acessos"],
        label="Acessos",
    )
    ax_linha.plot(
        mensal["mes"],
        mensal["adicionados_roteiro"],
        marker="s",
        linewidth=2.2,
        color=cores["linha_roteiros"],
        label="Adicionados ao Roteiro",
    )
    ax_linha.fill_between(mensal["mes"], mensal["acessos"], alpha=0.08, color=cores["linha_acessos"])

    ax_linha.set_title(
        "Evolução Mensal: Acessos vs. Adicionados ao Roteiro (2025)",
        fontsize=11,
        fontweight="bold",
        color=cores["texto"],
        pad=10,
    )
    ax_linha.set_xticks(range(1, 13))
    ax_linha.set_xticklabels(MESES_ABREV, fontsize=8.5, color=cores["muted"])
    ax_linha.tick_params(axis="y", labelsize=8.5, colors=cores["muted"])
    ax_linha.set_ylabel("Quantidade", fontsize=9, color=cores["muted"])
    ax_linha.grid(True, linestyle="--", alpha=0.45, color=cores["grid"])
    for spine in ("top", "right"):
        ax_linha.spines[spine].set_visible(False)
    for spine in ("bottom", "left"):
        ax_linha.spines[spine].set_color(cores["grid"])

    leg = ax_linha.legend(frameon=True, facecolor=cores["fig_bg"], edgecolor=cores["grid"], fontsize=8.5)
    for txt in leg.get_texts():
        txt.set_color(cores["texto"])

    # --- Gráfico 2: Barras Horizontais — Ranking dos Locais Mais Adicionados ---
    ranking = (
        df.groupby("local")["adicionados_roteiro"]
        .sum()
        .sort_values(ascending=True)
    )

    ax_bar = eixos[1]
    ax_bar.set_facecolor(cores["ax_bg"])
    bar_colors = [
        cores["barras_top"] if i == len(ranking) - 1 else cores["barras"]
        for i in range(len(ranking))
    ]
    barras = ax_bar.barh(ranking.index, ranking.values, color=bar_colors, height=0.62)

    ax_bar.set_title(
        "Ranking: Locais Mais Adicionados aos Roteiros",
        fontsize=11,
        fontweight="bold",
        color=cores["texto"],
        pad=10,
    )
    ax_bar.set_xlabel("Total de Adições ao Roteiro", fontsize=9, color=cores["muted"])
    ax_bar.tick_params(axis="x", labelsize=8.5, colors=cores["muted"])
    ax_bar.tick_params(axis="y", labelsize=8.5, colors=cores["texto"])
    ax_bar.grid(axis="x", linestyle="--", alpha=0.45, color=cores["grid"])
    ax_bar.set_xlim(0, ranking.max() * 1.16)

    for spine in ("top", "right"):
        ax_bar.spines[spine].set_visible(False)
    for spine in ("bottom", "left"):
        ax_bar.spines[spine].set_color(cores["grid"])

    # Rótulos numéricos ao lado das barras
    for barra in barras:
        largura = barra.get_width()
        ax_bar.text(
            largura + ranking.max() * 0.015,
            barra.get_y() + barra.get_height() / 2,
            f"{int(largura):,}",
            va="center",
            ha="left",
            fontsize=8,
            fontweight="bold",
            color=cores["texto"],
        )

    figura.tight_layout(pad=1.8)
    return figura


def desenhar_graficos_painel(container, df: pd.DataFrame):
    """Renderiza os 2 gráficos Matplotlib embutidos dentro de um frame CustomTkinter."""
    for widget in container.winfo_children():
        widget.destroy()

    fig_anterior = getattr(container, "_fig_atual", None)
    if fig_anterior is not None:
        plt.close(fig_anterior)

    figura = _criar_figura(df, figsize=(6.5, 5.6))
    container._fig_atual = figura

    canvas = FigureCanvasTkAgg(figura, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
    return figura


def mostrar_graficos_modal(pai, df: pd.DataFrame):
    """Abre uma janela dedicada ampliada com os gráficos do Painel Admin."""
    cores = _paleta_grafico()
    janela = ctk.CTkToplevel(pai)
    janela.title("BelémNaMão • Gráficos DataInsight")
    janela.geometry("960x720")
    janela.configure(fg_color=cores["fig_bg"])
    janela.grab_set()

    figura = _criar_figura(df, figsize=(9.2, 6.8))

    canvas = FigureCanvasTkAgg(figura, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)

    def fechar():
        plt.close(figura)
        janela.destroy()

    janela.protocol("WM_DELETE_WINDOW", fechar)
    return janela
