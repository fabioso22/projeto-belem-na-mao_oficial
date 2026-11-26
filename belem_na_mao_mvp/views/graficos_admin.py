"""
Módulo de Visualização com Matplotlib para o Painel Admin (DataInsight) — BelémNaMão
Estilo Dashboard SaaS Dark Mode (#111827 / #0F172A) com suporte a Modo Claro,
anotações de pico sazonal e seletor de visualização (Ambos, Evolução Mensal ou Ranking).
"""
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd


MESES_ABREV = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def _paleta_grafico():
    """Retorna a paleta SaaS moderna de acordo com o tema atual do CustomTkinter."""
    eh_dark = ctk.get_appearance_mode().lower() == "dark"
    if eh_dark:
        return {
            "fig_bg": "#111827",
            "ax_bg": "#0F172A",
            "texto": "#F8FAFC",
            "muted": "#94A3B8",
            "grid": "#334155",
            "linha_acessos": "#38BDF8",
            "linha_roteiros": "#818CF8",
            "borda_marker": "#FFFFFF",
            "pico_bg": "#1E293B",
            "pico_cor": "#F59E0B",
            "barras_grad": [
                "#0C4A6E", "#075985", "#0369A1", "#0284C7",
                "#0EA5E9", "#0EA5E9", "#38BDF8", "#38BDF8", "#7DD3FC",
            ],
            "barra_top": "#38BDF8",
        }
    return {
        "fig_bg": "#FFFFFF",
        "ax_bg": "#F8FAFC",
        "texto": "#0F172A",
        "muted": "#64748B",
        "grid": "#CBD5E1",
        "linha_acessos": "#0284C7",
        "linha_roteiros": "#6366F1",
        "borda_marker": "#FFFFFF",
        "pico_bg": "#FEF3C7",
        "pico_cor": "#D97706",
        "barras_grad": [
            "#BAE6FD", "#7DD3FC", "#38BDF8", "#0EA5E9",
            "#0284C7", "#0284C7", "#0369A1", "#075985", "#0C4A6E",
        ],
        "barra_top": "#0284C7",
    }


def _plotar_evolucao_mensal(ax, df: pd.DataFrame, cores: dict):
    """Plota o gráfico de linhas com preenchimento translúcido e anotações de picos."""
    mensal = (
        df.groupby("mes", as_index=False)[["acessos", "adicionados_roteiro"]]
        .sum()
        .sort_values("mes")
    )

    ax.set_facecolor(cores["ax_bg"])
    ax.plot(
        mensal["mes"],
        mensal["acessos"],
        marker="o",
        markersize=7,
        markerfacecolor=cores["linha_acessos"],
        markeredgecolor=cores["borda_marker"],
        markeredgewidth=1.4,
        linewidth=2.6,
        color=cores["linha_acessos"],
        label="Acessos",
        zorder=4,
    )
    ax.plot(
        mensal["mes"],
        mensal["adicionados_roteiro"],
        marker="o",
        markersize=6,
        markerfacecolor=cores["linha_roteiros"],
        markeredgecolor=cores["borda_marker"],
        markeredgewidth=1.2,
        linewidth=2.2,
        color=cores["linha_roteiros"],
        label="Interações / Roteiros",
        zorder=4,
    )
    ax.fill_between(mensal["mes"], mensal["acessos"], alpha=0.20, color=cores["linha_acessos"], zorder=2)
    ax.fill_between(mensal["mes"], mensal["adicionados_roteiro"], alpha=0.14, color=cores["linha_roteiros"], zorder=2)

    # Anotações elegantes nos picos sazonais (Julho e Outubro)
    mapa_acessos = dict(zip(mensal["mes"], mensal["acessos"]))
    y_max = float(mensal["acessos"].max()) if not mensal.empty else 1.0
    for mes_pico, rotulo in ((7, "Verão (Jul)"), (10, "Círio (Out)")):
        if mes_pico in mapa_acessos:
            val = mapa_acessos[mes_pico]
            ax.annotate(
                f"{rotulo}\n{int(val):,}".replace(",", "."),
                xy=(mes_pico, val),
                xytext=(mes_pico, val + y_max * 0.10),
                ha="center",
                va="bottom",
                fontsize=7.8,
                fontweight="bold",
                color=cores["pico_cor"],
                bbox=dict(
                    boxstyle="round,pad=0.3",
                    facecolor=cores["pico_bg"],
                    edgecolor=cores["pico_cor"],
                    linewidth=0.9,
                ),
                arrowprops=dict(arrowstyle="-|>", color=cores["pico_cor"], lw=1.0),
                zorder=5,
            )

    anos = sorted(df["ano"].unique().tolist()) if "ano" in df.columns else []
    periodo_txt = f"{anos[0]}–{anos[-1]}" if len(anos) > 1 else (str(anos[0]) if anos else "MySQL Aiven")
    ax.set_title(
        f"Evolução Mensal: Acessos vs. Interações ({periodo_txt})",
        fontsize=11,
        fontweight="bold",
        color=cores["texto"],
        loc="left",
        pad=12,
    )
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(MESES_ABREV, fontsize=8.5, color=cores["muted"])
    ax.tick_params(axis="y", labelsize=8.5, colors=cores["muted"])
    ax.set_ylim(0, y_max * 1.30)
    ax.set_ylabel("Quantidade", fontsize=9, color=cores["muted"])
    ax.grid(True, linestyle="--", alpha=0.15, color=cores["grid"], zorder=1)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("bottom", "left"):
        ax.spines[spine].set_color(cores["grid"])
        ax.spines[spine].set_alpha(0.5)

    leg = ax.legend(
        frameon=True,
        facecolor=cores["fig_bg"],
        edgecolor=cores["grid"],
        fontsize=8.5,
        loc="upper left",
    )
    for txt in leg.get_texts():
        txt.set_color(cores["texto"])


def _plotar_ranking_barras(ax, df: pd.DataFrame, cores: dict):
    """Plota o gráfico de barras horizontais em degradê azul ciano destacando o #1."""
    ranking = (
        df.groupby("local")["adicionados_roteiro"]
        .sum()
        .sort_values(ascending=True)
    )

    ax.set_facecolor(cores["ax_bg"])
    n = len(ranking)
    grad = cores["barras_grad"]
    bar_colors = []
    for i in range(n):
        if i == n - 1:
            bar_colors.append(cores["barra_top"])
        else:
            idx_cor = int(i / max(1, n - 1) * (len(grad) - 1))
            bar_colors.append(grad[idx_cor])

    barras = ax.barh(
        ranking.index,
        ranking.values,
        color=bar_colors,
        height=0.62,
        edgecolor="none",
        zorder=3,
    )

    ax.set_title(
        "Ranking: Locais Mais Procurados e Adicionados",
        fontsize=11,
        fontweight="bold",
        color=cores["texto"],
        loc="left",
        pad=12,
    )
    ax.set_xlabel("Total de Interações / Roteiros", fontsize=9, color=cores["muted"])
    ax.tick_params(axis="x", labelsize=8.5, colors=cores["muted"])
    ax.tick_params(axis="y", labelsize=8.8, colors=cores["texto"])
    ax.grid(axis="x", linestyle="--", alpha=0.15, color=cores["grid"], zorder=1)
    max_val = float(ranking.max()) if not ranking.empty else 1.0
    ax.set_xlim(0, max_val * 1.20)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("bottom", "left"):
        ax.spines[spine].set_color(cores["grid"])
        ax.spines[spine].set_alpha(0.5)

    for i, barra in enumerate(barras):
        largura = barra.get_width()
        eh_top = i == n - 1
        rotulo = f"★ {int(largura):,}".replace(",", ".") if eh_top else f"{int(largura):,}".replace(",", ".")
        ax.text(
            largura + max_val * 0.018,
            barra.get_y() + barra.get_height() / 2,
            rotulo,
            va="center",
            ha="left",
            fontsize=8.5 if eh_top else 8.0,
            fontweight="bold",
            color=cores["pico_cor"] if eh_top else cores["texto"],
        )


def _criar_figura(df: pd.DataFrame, figsize=(6.8, 6.0), modo: str = "ambos"):
    """
    Constrói a figura Matplotlib conforme o modo selecionado:
    'ambos' (2 gráficos), 'evolucao' (apenas linhas) ou 'ranking' (apenas barras).
    """
    cores = _paleta_grafico()
    modo_norm = str(modo or "ambos").strip().lower()

    if modo_norm == "evolucao":
        figura = Figure(figsize=figsize, dpi=100)
        ax = figura.add_subplot(1, 1, 1)
        figura.patch.set_facecolor(cores["fig_bg"])
        _plotar_evolucao_mensal(ax, df, cores)
        figura.tight_layout(pad=2.0)
        return figura

    if modo_norm == "ranking":
        figura = Figure(figsize=figsize, dpi=100)
        ax = figura.add_subplot(1, 1, 1)
        figura.patch.set_facecolor(cores["fig_bg"])
        _plotar_ranking_barras(ax, df, cores)
        figura.tight_layout(pad=2.0)
        return figura

    figura = Figure(figsize=figsize, dpi=100)
    eixos = figura.subplots(2, 1)
    figura.patch.set_facecolor(cores["fig_bg"])
    _plotar_evolucao_mensal(eixos[0], df, cores)
    _plotar_ranking_barras(eixos[1], df, cores)
    figura.tight_layout(pad=2.2, h_pad=2.6)
    return figura


def desenhar_graficos_painel(container, df: pd.DataFrame, modo: str = "ambos"):
    """Renderiza os gráficos Matplotlib embutidos dentro de um frame CustomTkinter."""
    for widget in container.winfo_children():
        widget.destroy()

    fig_anterior = getattr(container, "_fig_atual", None)
    if fig_anterior is not None:
        plt.close(fig_anterior)

    figura = _criar_figura(df, figsize=(6.8, 5.8), modo=modo)
    container._fig_atual = figura

    canvas = FigureCanvasTkAgg(figura, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
    return figura


def mostrar_graficos_modal(pai, df: pd.DataFrame, modo: str = "ambos"):
    """Abre uma janela dedicada ampliada com os gráficos do Painel Admin."""
    cores = _paleta_grafico()
    janela = ctk.CTkToplevel(pai)
    janela.title("BelémNaMão • Gráficos DataInsight")
    janela.geometry("980x740")
    janela.configure(fg_color=cores["fig_bg"])
    janela.grab_set()

    figura = _criar_figura(df, figsize=(9.4, 7.0), modo=modo)

    canvas = FigureCanvasTkAgg(figura, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=14, pady=14)

    def fechar():
        plt.close(figura)
        janela.destroy()

    janela.protocol("WM_DELETE_WINDOW", fechar)
    return janela
