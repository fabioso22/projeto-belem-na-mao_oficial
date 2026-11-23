"""
Painel Administrativo — Módulo DataInsight (Pandas + Matplotlib) do BelémNaMão
Permite carregar a base simulada de 12 meses, consultar rankings, resumos mensais,
gerar insights automáticos (> 130% da média) e visualizar gráficos integrados.
"""
from tkinter import messagebox
from typing import Any, Callable, Dict, Optional

import customtkinter as ctk
import matplotlib.pyplot as plt
import pandas as pd

from services.analise_dados import (
    carregar_dados,
    gerar_insights,
    locais_mais_procurados,
    resumo_mensal,
)
from views.graficos_admin import desenhar_graficos_painel, mostrar_graficos_modal
from views.theme import (
    BG,
    BTN_SECONDARY_BG,
    BTN_SECONDARY_BORDER,
    BTN_SECONDARY_HOVER,
    BTN_SECONDARY_TEXT,
    ERROR,
    LINE,
    PANEL,
    PANEL_SUBTLE,
    PRIMARY_BTN,
    PRIMARY_HOVER,
    SECONDARY,
    SECONDARY_FIXED,
    TAG_BG,
    TAG_BORDER,
    TAG_TEXT,
    TERTIARY_CONTAINER,
    TEXT,
    TEXT_BRAND,
    TEXT_KPI,
    TEXT_MUTED,
    TEXT_TITLE,
    fonte,
)


class PainelAdminApp(ctk.CTk):
    LARGURA = 1240
    ALTURA = 800

    def __init__(self, usuario: Optional[Dict[str, Any]] = None, on_logout: Optional[Callable] = None):
        super().__init__()
        self.usuario = usuario or {"id": 0, "nome": "Administrador", "usuario": "admin", "is_admin": True}
        self.on_logout = on_logout
        self.df: Optional[pd.DataFrame] = None

        self.title("BelémNaMão • Painel Admin — DataInsight (Pandas + Matplotlib)")
        self.geometry(f"{self.LARGURA}x{self.ALTURA}")
        self.minsize(1080, 680)
        self.configure(fg_color=BG)
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)

        self._centralizar()
        self._configurar_grid()
        self._criar_navbar()
        self._criar_corpo()

    def _centralizar(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - self.LARGURA) // 2)
        y = max(0, (sh - self.ALTURA) // 2)
        self.geometry(f"{self.LARGURA}x{self.ALTURA}+{x}+{y}")

    def _configurar_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    def _ao_fechar(self):
        plt.close("all")
        self.destroy()

    def _voltar_login(self):
        plt.close("all")
        if self.on_logout:
            self.on_logout()
        else:
            self.destroy()

    # ==================================================================
    # 1. Navbar Superior
    # ==================================================================
    def _criar_navbar(self):
        navbar = ctk.CTkFrame(self, fg_color=PANEL, height=70, corner_radius=0, border_width=1, border_color=LINE)
        navbar.grid(row=0, column=0, sticky="ew")
        navbar.grid_propagate(False)

        inner = ctk.CTkFrame(navbar, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=24)

        # Esquerda: Logo + Badge Admin
        esq = ctk.CTkFrame(inner, fg_color="transparent")
        esq.pack(side="left", fill="y")

        emblema = ctk.CTkFrame(esq, width=40, height=40, corner_radius=8, fg_color=PRIMARY_BTN)
        emblema.pack(side="left", padx=(0, 10), pady=15)
        emblema.pack_propagate(False)
        ctk.CTkLabel(emblema, text="≋", font=fonte(22, "bold"), text_color=SECONDARY_FIXED).pack(expand=True)

        ctk.CTkLabel(esq, text="Belém", font=fonte(18, "bold"), text_color=TEXT_TITLE).pack(side="left")
        ctk.CTkLabel(esq, text="NaMão", font=fonte(18, "bold"), text_color=SECONDARY).pack(side="left")

        badge_admin = ctk.CTkFrame(esq, fg_color=TAG_BG, corner_radius=8, border_width=1, border_color=TAG_BORDER)
        badge_admin.pack(side="left", padx=(14, 0), pady=18)
        ctk.CTkLabel(
            badge_admin,
            text="DATAINSIGHT • PAINEL ADMIN — ANÁLISE DE DADOS",
            font=fonte(11, "bold"),
            text_color=TAG_TEXT,
            padx=12,
            pady=4,
        ).pack()

        # Direita: Modo Claro/Escuro, Identificação e Voltar ao Login
        dir_box = ctk.CTkFrame(inner, fg_color="transparent")
        dir_box.pack(side="right", fill="y", pady=16)

        modo_atual = ctk.get_appearance_mode().lower()
        texto_tema = "☀️ Modo Claro" if modo_atual == "dark" else "🌙 Modo Escuro"
        self.btn_tema = ctk.CTkButton(
            dir_box,
            text=texto_tema,
            height=34,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(12, "bold"),
            command=self._alternar_modo_escuro,
        )
        self.btn_tema.pack(side="left", padx=(0, 8))

        nome_admin = self.usuario.get("nome", "Administrador")
        perfil = ctk.CTkFrame(dir_box, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        perfil.pack(side="left", padx=(0, 8))
        ctk.CTkLabel(
            perfil,
            text=f"🛡️ {nome_admin}",
            font=fonte(12, "bold"),
            text_color=TEXT_TITLE,
            padx=12,
            pady=6,
        ).pack()

        ctk.CTkButton(
            dir_box,
            text="🚪 Voltar ao Login",
            height=34,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=ERROR,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(12, "bold"),
            command=self._voltar_login,
        ).pack(side="left")

    def _alternar_modo_escuro(self):
        modo_atual = ctk.get_appearance_mode().lower()
        if modo_atual == "dark":
            ctk.set_appearance_mode("light")
            self.btn_tema.configure(text="🌙 Modo Escuro")
        else:
            ctk.set_appearance_mode("dark")
            self.btn_tema.configure(text="☀️ Modo Claro")

        # Atualiza gráficos embutidos caso já tenham sido plotados
        if self.df is not None and not self.df.empty and self._graficos_renderizados:
            desenhar_graficos_painel(self.container_graficos, self.df)

    # ==================================================================
    # 2. Corpo Principal (KPIs + Botões de Análise + Texto + Gráficos)
    # ==================================================================
    def _criar_corpo(self):
        self._graficos_renderizados = False

        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.grid(row=1, column=0, sticky="nsew", padx=24, pady=18)
        corpo.grid_columnconfigure(0, weight=1)
        corpo.grid_rowconfigure(2, weight=1)

        # --- Linha 0: Cards de KPI ---
        strip_kpi = ctk.CTkFrame(corpo, fg_color="transparent")
        strip_kpi.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        strip_kpi.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="admin_kpi")

        kpis_def = [
            ("total_acessos", "📊", "Total de Acessos (12m)", "—"),
            ("total_roteiros", "🗺️", "Adições aos Roteiros", "—"),
            ("top_local", "🏆", "Ponto Mais Procurado", "—"),
            ("taxa_media", "📈", "Conversão p/ Roteiro", "—"),
        ]
        self.kpi_labels: Dict[str, ctk.CTkLabel] = {}

        for col, (chave, icone, titulo, valor_ini) in enumerate(kpis_def):
            card = ctk.CTkFrame(strip_kpi, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
            card.grid(row=0, column=col, padx=(0 if col == 0 else 6, 0 if col == 3 else 6), sticky="nsew")

            c_in = ctk.CTkFrame(card, fg_color="transparent")
            c_in.pack(fill="both", expand=True, padx=16, pady=12)

            topo_k = ctk.CTkFrame(c_in, fg_color="transparent")
            topo_k.pack(fill="x")
            ctk.CTkLabel(topo_k, text=icone, font=fonte(15)).pack(side="left", padx=(0, 6))
            ctk.CTkLabel(topo_k, text=titulo, font=fonte(11, "bold"), text_color=TEXT_MUTED).pack(side="left")

            lbl_val = ctk.CTkLabel(c_in, text=valor_ini, font=fonte(17, "bold"), text_color=TEXT_KPI, anchor="w")
            lbl_val.pack(anchor="w", pady=(4, 0))
            self.kpi_labels[chave] = lbl_val

        # --- Linha 1: Barra de Botões de Ação ---
        barra_acoes = ctk.CTkFrame(corpo, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        barra_acoes.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        ba_in = ctk.CTkFrame(barra_acoes, fg_color="transparent")
        ba_in.pack(fill="x", padx=14, pady=12)

        ctk.CTkButton(
            ba_in,
            text="📥 Carregar Dados",
            height=38,
            corner_radius=8,
            fg_color=PRIMARY_BTN,
            hover_color=PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(12, "bold"),
            command=self.carregar,
        ).pack(side="left", padx=(0, 8))

        acoes_secundarias = [
            ("🏆 Locais Mais Procurados", self.mostrar_locais_procurados),
            ("📅 Resumo Mensal", self.mostrar_resumo_mensal),
            ("💡 Gerar Insights", self.mostrar_insights),
            ("📊 Visualizar Gráficos", self.mostrar_graficos),
        ]

        for texto_btn, func in acoes_secundarias:
            ctk.CTkButton(
                ba_in,
                text=texto_btn,
                height=38,
                corner_radius=8,
                fg_color=BTN_SECONDARY_BG,
                border_width=1,
                border_color=BTN_SECONDARY_BORDER,
                text_color=BTN_SECONDARY_TEXT,
                hover_color=BTN_SECONDARY_HOVER,
                font=fonte(12, "bold"),
                command=lambda f=func: self.executar_acao(f),
            ).pack(side="left", padx=(0, 8))

        # --- Linha 2: Área Principal Dividida (Esquerda: Texto / Direita: Gráficos) ---
        grid_main = ctk.CTkFrame(corpo, fg_color="transparent")
        grid_main.grid(row=2, column=0, sticky="nsew")
        grid_main.grid_columnconfigure(0, weight=45, uniform="admin_cols")
        grid_main.grid_columnconfigure(1, weight=55, uniform="admin_cols")
        grid_main.grid_rowconfigure(0, weight=1)

        # Painel Esquerdo: Relatório Textual
        card_texto = ctk.CTkFrame(grid_main, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        card_texto.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        header_txt = ctk.CTkFrame(card_texto, fg_color="transparent")
        header_txt.pack(fill="x", padx=16, pady=(14, 8))
        ctk.CTkLabel(header_txt, text="📋 Relatório Analítico (Pandas)", font=fonte(15, "bold"), text_color=TEXT_TITLE).pack(side="left")

        self.resultado = ctk.CTkTextbox(
            card_texto,
            font=ctk.CTkFont(family="Consolas", size=13),
            wrap="word",
            fg_color=PANEL_SUBTLE,
            text_color=TEXT,
            border_width=1,
            border_color=LINE,
            corner_radius=8,
        )
        self.resultado.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.escrever(
            "Bem-vindo ao Painel Admin — DataInsight (BelémNaMão)!\n\n"
            "Aqui você pode explorar os indicadores de visitação simulados (12 meses)\n"
            "nos principais pontos turísticos de Belém do Pará.\n\n"
            "1. Clique em '📥 Carregar Dados' para gerar e carregar o DataFrame Pandas.\n"
            "2. Utilize os botões acima para ver rankings, resumo mensal e insights (> 130%).\n"
            "3. Clique em '📊 Visualizar Gráficos' para plotar evolução mensal e barras."
        )

        # Painel Direito: Gráficos Matplotlib (FigureCanvasTkAgg)
        card_graficos = ctk.CTkFrame(grid_main, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        card_graficos.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        header_graf = ctk.CTkFrame(card_graficos, fg_color="transparent")
        header_graf.pack(fill="x", padx=16, pady=(14, 6))
        ctk.CTkLabel(
            header_graf,
            text="📈 Visualizações Matplotlib",
            font=fonte(15, "bold"),
            text_color=TEXT_TITLE,
        ).pack(side="left")

        ctk.CTkButton(
            header_graf,
            text="⛶ Ampliar",
            width=86,
            height=28,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(11, "bold"),
            command=lambda: self.executar_acao(self._abrir_modal_graficos),
        ).pack(side="right")

        self.container_graficos = ctk.CTkFrame(
            card_graficos,
            fg_color=PANEL_SUBTLE,
            corner_radius=8,
            border_width=1,
            border_color=LINE,
        )
        self.container_graficos.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        placeholder = ctk.CTkFrame(self.container_graficos, fg_color="transparent")
        placeholder.pack(expand=True)
        ctk.CTkLabel(placeholder, text="📊", font=fonte(40)).pack(pady=(0, 8))
        ctk.CTkLabel(
            placeholder,
            text="Os gráficos aparecerão aqui",
            font=fonte(15, "bold"),
            text_color=TEXT_TITLE,
        ).pack(pady=(0, 4))
        ctk.CTkLabel(
            placeholder,
            text="Carregue os dados e clique em '📊 Visualizar Gráficos'.",
            font=fonte(12),
            text_color=TEXT_MUTED,
        ).pack()

    # ==================================================================
    # 3. Helpers e Tratamento de Erros
    # ==================================================================
    def escrever(self, texto: str):
        self.resultado.delete("1.0", "end")
        self.resultado.insert("end", texto)

    def verificar_dados(self) -> bool:
        if self.df is None or self.df.empty:
            messagebox.showwarning("Atenção", "Carregue os dados primeiro clicando em '📥 Carregar Dados'!")
            return False
        return True

    def executar_acao(self, acao: Callable):
        if not self.verificar_dados():
            return
        try:
            acao()
        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível concluir a operação:\n{erro}")

    # ==================================================================
    # 4. Ações dos Botões
    # ==================================================================
    def carregar(self):
        try:
            self.df = carregar_dados()
            if self.df.empty:
                self.escrever("Nenhum registro encontrado na base simulada.")
                return

            total_acessos = int(self.df["acessos"].sum())
            total_roteiros = int(self.df["adicionados_roteiro"].sum())
            taxa_media = (total_roteiros / total_acessos * 100) if total_acessos > 0 else 0.0

            ranking = locais_mais_procurados(self.df)
            local_top = str(ranking.iloc[0]["local"]) if not ranking.empty else "—"

            # Atualiza os 4 cards de KPI
            self.kpi_labels["total_acessos"].configure(text=f"{total_acessos:,}".replace(",", "."))
            self.kpi_labels["total_roteiros"].configure(text=f"{total_roteiros:,}".replace(",", "."))
            self.kpi_labels["top_local"].configure(text=local_top)
            self.kpi_labels["taxa_media"].configure(text=f"{taxa_media:.1f}%")

            data_ini = self.df["data"].min().strftime("%d/%m/%Y")
            data_fim = self.df["data"].max().strftime("%d/%m/%Y")

            self.escrever(
                "✅ BASE DE DADOS CARREGADA COM SUCESSO!\n"
                "==================================================\n\n"
                f"• Registros gerados:    {len(self.df)} linhas (random.seed(42))\n"
                f"• Pontos analisados:    {self.df['local'].nunique()} atrações de Belém\n"
                f"• Período simulado:     {data_ini} até {data_fim} (12 meses)\n"
                f"• Total de acessos:     {total_acessos:,}\n"
                f"• Inclusões em roteiro: {total_roteiros:,} ({taxa_media:.1f}% de conversão)\n"
                f"• Destaque no período:  {local_top}\n\n"
                "Agora selecione qualquer análise ou clique em '📊 Visualizar Gráficos'."
            )
        except Exception as erro:
            self.df = None
            messagebox.showerror("Erro", f"Falha ao carregar os dados:\n{erro}")

    def mostrar_locais_procurados(self):
        ranking = locais_mais_procurados(self.df)
        linhas = [
            "🏆 RANKING — LOCAIS MAIS PROCURADOS (BELÉM)",
            "==================================================",
            "",
        ]
        for idx, row in ranking.iterrows():
            pos = idx + 1
            medalha = "🥇" if pos == 1 else ("🥈" if pos == 2 else ("🥉" if pos == 3 else f"#{pos}"))
            linhas.append(
                f"{medalha} {row['local']} [{row['categoria']}]\n"
                f"   • Adicionados ao roteiro: {int(row['adicionados_roteiro']):,}\n"
                f"   • Acessos totais:         {int(row['acessos']):,}  (Conversão: {row['taxa_conversao']:.1f}%)\n"
            )
        self.escrever("\n".join(linhas))

    def mostrar_resumo_mensal(self):
        mensal = resumo_mensal(self.df)
        linhas = [
            "📅 RESUMO MENSAL DE VISITAÇÃO (2025)",
            "==================================================",
            "",
        ]
        for _, row in mensal.iterrows():
            crescimento = row["crescimento_%"]
            cresc_str = "—" if pd.isna(crescimento) else f"{crescimento:+.1f}%"
            linhas.append(
                f"• {str(row['nome_mes']):<10} | Acessos: {int(row['acessos']):>6,} | "
                f"Roteiros: {int(row['adicionados_roteiro']):>5,} | Var: {cresc_str}"
            )

        melhor_mes = mensal.loc[mensal["acessos"].idxmax()]
        menor_mes = mensal.loc[mensal["acessos"].idxmin()]
        linhas.extend(
            [
                "",
                "--------------------------------------------------",
                f"📌 Maior movimento: {melhor_mes['nome_mes']} ({int(melhor_mes['acessos']):,} acessos)",
                f"📌 Menor movimento: {menor_mes['nome_mes']} ({int(menor_mes['acessos']):,} acessos)",
            ]
        )
        self.escrever("\n".join(linhas))

    def mostrar_insights(self):
        itens = gerar_insights(self.df)
        cabecalho = (
            "💡 MOTOR DE INSIGHTS — PROCURA > 130% DA MÉDIA\n"
            "==================================================\n\n"
        )
        self.escrever(cabecalho + "\n\n".join(itens))

    def mostrar_graficos(self):
        desenhar_graficos_painel(self.container_graficos, self.df)
        self._graficos_renderizados = True
        self.escrever(
            "📊 GRÁFICOS ATUALIZADOS NO PAINEL À DIREITA!\n"
            "==================================================\n\n"
            "1) Gráfico de Linhas: mostra a evolução mensal de acessos e\n"
            "   adições aos roteiros ao longo dos 12 meses de 2025.\n"
            "   Observe os picos sazonais em Julho (Verão Amazônico),\n"
            "   Outubro (Círio de Nazaré) e Dezembro (Festas de Fim de Ano).\n\n"
            "2) Gráfico de Barras: exibe o ranking comparativo dos locais\n"
            "   mais adicionados aos roteiros pelos visitantes.\n\n"
            "Dica: clique em '⛶ Ampliar' acima dos gráficos para abrir em tela ampla."
        )

    def _abrir_modal_graficos(self):
        mostrar_graficos_modal(self, self.df)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = PainelAdminApp()
    app.mainloop()
