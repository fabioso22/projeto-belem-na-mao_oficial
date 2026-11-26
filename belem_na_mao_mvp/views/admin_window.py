"""
Painel Administrativo — Módulo DataInsight (Pandas + Matplotlib + MySQL Aiven) do BelémNaMão
Redesign moderno estilo Dashboard SaaS / Power BI Dark Mode com cards executivos,
abas navegáveis, micro-cards visuais, tabela estilizada e gráficos Matplotlib integrados.
"""
import re
import threading
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
from services.database import MYSQL_CONFIG
from views.graficos_admin import desenhar_graficos_painel, mostrar_graficos_modal
from views.theme import fonte

# ======================================================================
# Paleta SaaS Dark Mode + Compatibilidade Modo Claro
# ======================================================================
ADMIN_BG = ("#F1F5F9", "#0B1120")            # Fundo geral da janela
ADMIN_CARD = ("#FFFFFF", "#111827")          # Containers / cards principais
ADMIN_ELEVATED = ("#F8FAFC", "#1E293B")      # Aba ativa / elementos elevados
ADMIN_INNER = ("#F1F5F9", "#0F172A")         # Micro-cards e linhas internas
ADMIN_ROW_ALT = ("#F8FAFC", "#131C2E")       # Linhas alternadas da tabela
ADMIN_BORDER = ("#E2E8F0", "#1E293B")        # Bordas sutis de containers
ADMIN_BORDER_STRONG = ("#CBD5E1", "#334155") # Bordas de inputs/botões

ADMIN_TEXT = ("#0F172A", "#F8FAFC")          # Texto principal branco puro no escuro
ADMIN_MUTED = ("#64748B", "#94A3B8")         # Títulos menores e subtítulos

ACCENT_CYAN = "#0EA5E9"
ACCENT_CYAN_BRIGHT = "#38BDF8"
ACCENT_CYAN_HOVER = "#0284C7"
ACCENT_EMERALD = "#10B981"
ACCENT_INDIGO = "#818CF8"
ACCENT_AMBER = "#F59E0B"
ACCENT_ROSE = "#F43F5E"

CATEGORIA_CORES = {
    "Gastronomia": (("#FEF3C7", "#3B2506"), ("#B45309", "#FBBF24")),
    "Cultura": (("#E0E7FF", "#1E1B4B"), ("#4338CA", "#A5B4FC")),
    "História": (("#F3E8FF", "#2E1065"), ("#7E22CE", "#D8B4FE")),
    "Natureza": (("#D1FAE5", "#064E3B"), ("#047857", "#6EE7B7")),
    "Passeio": (("#E0F2FE", "#0C4A6E"), ("#0369A1", "#7DD3FC")),
}


class PainelAdminApp(ctk.CTk):
    LARGURA = 1280
    ALTURA = 820

    def __init__(self, usuario: Optional[Dict[str, Any]] = None, on_logout: Optional[Callable] = None):
        super().__init__()
        self.usuario = usuario or {"id": 0, "nome": "Administrador", "usuario": "admin", "is_admin": True}
        self.on_logout = on_logout
        self.df: Optional[pd.DataFrame] = None
        self.aba_ativa: str = "resumo"
        self.modo_grafico: str = "ambos"
        self._graficos_renderizados: bool = False

        self.title("BelémNaMão • DataInsight — Painel Admin (MySQL Local)")
        self.geometry(f"{self.LARGURA}x{self.ALTURA}")
        self.minsize(1100, 700)
        self.configure(fg_color=ADMIN_BG)
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
        navbar = ctk.CTkFrame(
            self,
            fg_color=ADMIN_CARD,
            height=68,
            corner_radius=0,
            border_width=1,
            border_color=ADMIN_BORDER,
        )
        navbar.grid(row=0, column=0, sticky="ew")
        navbar.grid_propagate(False)

        inner = ctk.CTkFrame(navbar, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=24)

        # Esquerda: Logo + Badge DataInsight
        esq = ctk.CTkFrame(inner, fg_color="transparent")
        esq.pack(side="left", fill="y")

        emblema = ctk.CTkFrame(esq, width=38, height=38, corner_radius=10, fg_color=ACCENT_CYAN)
        emblema.pack(side="left", padx=(0, 10), pady=15)
        emblema.pack_propagate(False)
        ctk.CTkLabel(emblema, text="≋", font=fonte(20, "bold"), text_color="#FFFFFF").pack(expand=True)

        ctk.CTkLabel(esq, text="Belém", font=fonte(18, "bold"), text_color=ADMIN_TEXT).pack(side="left")
        ctk.CTkLabel(esq, text="NaMão", font=fonte(18, "bold"), text_color=ACCENT_CYAN_BRIGHT).pack(side="left")

        badge_admin = ctk.CTkFrame(
            esq,
            fg_color=ADMIN_INNER,
            corner_radius=8,
            border_width=1,
            border_color=ADMIN_BORDER_STRONG,
        )
        badge_admin.pack(side="left", padx=(14, 0), pady=18)
        ctk.CTkLabel(
            badge_admin,
            text="● DATAINSIGHT  •  PAINEL ADMIN",
            font=fonte(11, "bold"),
            text_color=ACCENT_CYAN_BRIGHT,
            padx=12,
            pady=4,
        ).pack()

        # Direita: Modo Claro/Escuro, Perfil e Voltar ao Login
        dir_box = ctk.CTkFrame(inner, fg_color="transparent")
        dir_box.pack(side="right", fill="y", pady=16)

        modo_atual = ctk.get_appearance_mode().lower()
        texto_tema = "☀️ Modo Claro" if modo_atual == "dark" else "🌙 Modo Escuro"
        self.btn_tema = ctk.CTkButton(
            dir_box,
            text=texto_tema,
            height=34,
            corner_radius=8,
            fg_color=ADMIN_ELEVATED,
            border_width=1,
            border_color=ADMIN_BORDER_STRONG,
            text_color=ADMIN_TEXT,
            hover_color=ADMIN_INNER,
            font=fonte(12, "bold"),
            command=self._alternar_modo_escuro,
        )
        self.btn_tema.pack(side="left", padx=(0, 8))

        nome_admin = self.usuario.get("nome", "Administrador")
        perfil = ctk.CTkFrame(
            dir_box,
            fg_color=ADMIN_INNER,
            corner_radius=8,
            border_width=1,
            border_color=ADMIN_BORDER_STRONG,
        )
        perfil.pack(side="left", padx=(0, 8))
        ctk.CTkLabel(
            perfil,
            text=f"🛡️ {nome_admin}",
            font=fonte(12, "bold"),
            text_color=ADMIN_TEXT,
            padx=12,
            pady=6,
        ).pack()

        ctk.CTkButton(
            dir_box,
            text="🚪 Voltar ao Login",
            height=34,
            corner_radius=8,
            fg_color=ADMIN_ELEVATED,
            border_width=1,
            border_color=ADMIN_BORDER_STRONG,
            text_color=ACCENT_ROSE,
            hover_color=ADMIN_INNER,
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

        if self.df is not None and not self.df.empty and self._graficos_renderizados:
            desenhar_graficos_painel(self.container_graficos, self.df, modo=self.modo_grafico)

    # ==================================================================
    # 2. Corpo Principal (KPIs Executivos + Barra de Abas + Split View)
    # ==================================================================
    def _criar_corpo(self):
        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.grid(row=1, column=0, sticky="nsew", padx=24, pady=18)
        corpo.grid_columnconfigure(0, weight=1)
        corpo.grid_rowconfigure(2, weight=1)

        # --- Linha 0: 4 Cards Executivos de KPI ---
        strip_kpi = ctk.CTkFrame(corpo, fg_color="transparent")
        strip_kpi.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        strip_kpi.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="admin_kpi")

        kpis_def = [
            ("total_acessos", "📊", "TOTAL DE ACESSOS", "—", "● Aguardando carga MySQL", ACCENT_CYAN, ("#E0F2FE", "#0C4A6E")),
            ("total_roteiros", "🗺️", "ADIÇÕES AOS ROTEIROS", "—", "● Interações registradas", ACCENT_INDIGO, ("#E0E7FF", "#1E1B4B")),
            ("top_local", "🏆", "PONTO MAIS PROCURADO", "—", "★ Top 1 em Belém", ACCENT_AMBER, ("#FEF3C7", "#3B2506")),
            ("taxa_media", "📈", "CONVERSÃO P/ ROTEIRO", "—", "▲ Eficiência média", ACCENT_EMERALD, ("#D1FAE5", "#064E3B")),
        ]
        self.kpi_labels: Dict[str, ctk.CTkLabel] = {}
        self.kpi_sublabels: Dict[str, ctk.CTkLabel] = {}

        for col, (chave, icone, titulo, valor_ini, sub_ini, cor_accent, cor_badge_bg) in enumerate(kpis_def):
            card = ctk.CTkFrame(
                strip_kpi,
                fg_color=ADMIN_CARD,
                corner_radius=12,
                border_width=1,
                border_color=ADMIN_BORDER,
            )
            card.grid(row=0, column=col, padx=(0 if col == 0 else 7, 0 if col == 3 else 7), sticky="nsew")

            # Barra superior colorida (accent bar 4px)
            accent_bar = ctk.CTkFrame(card, fg_color=cor_accent, height=4, corner_radius=2)
            accent_bar.pack(fill="x", padx=12, pady=(0, 0))

            c_in = ctk.CTkFrame(card, fg_color="transparent")
            c_in.pack(fill="both", expand=True, padx=16, pady=(12, 14))

            topo_k = ctk.CTkFrame(c_in, fg_color="transparent")
            topo_k.pack(fill="x")

            ctk.CTkLabel(
                topo_k,
                text=titulo,
                font=fonte(10, "bold"),
                text_color=ADMIN_MUTED,
            ).pack(side="left", anchor="n", pady=(4, 0))

            badge_ic = ctk.CTkFrame(topo_k, width=34, height=34, corner_radius=9, fg_color=cor_badge_bg)
            badge_ic.pack(side="right")
            badge_ic.pack_propagate(False)
            ctk.CTkLabel(badge_ic, text=icone, font=fonte(15)).pack(expand=True)

            tamanho_val = 20 if chave == "top_local" else 26
            lbl_val = ctk.CTkLabel(
                c_in,
                text=valor_ini,
                font=fonte(tamanho_val, "bold"),
                text_color=ADMIN_TEXT,
                anchor="w",
            )
            lbl_val.pack(anchor="w", pady=(6, 6))
            self.kpi_labels[chave] = lbl_val

            pill_sub = ctk.CTkFrame(c_in, fg_color=ADMIN_INNER, corner_radius=6)
            pill_sub.pack(anchor="w")
            lbl_sub = ctk.CTkLabel(
                pill_sub,
                text=sub_ini,
                font=fonte(10, "bold"),
                text_color=cor_accent,
                padx=8,
                pady=2,
            )
            lbl_sub.pack()
            self.kpi_sublabels[chave] = lbl_sub

        # --- Linha 1: Barra de Navegação / Ações (Primary Sync + Abas Selecionáveis) ---
        barra_acoes = ctk.CTkFrame(
            corpo,
            fg_color=ADMIN_CARD,
            corner_radius=12,
            border_width=1,
            border_color=ADMIN_BORDER,
        )
        barra_acoes.grid(row=1, column=0, sticky="ew", pady=(0, 16))

        ba_in = ctk.CTkFrame(barra_acoes, fg_color="transparent")
        ba_in.pack(fill="x", padx=14, pady=10)

        self.btn_carregar = ctk.CTkButton(
            ba_in,
            text="🔄 Carregar Dados (MySQL)",
            height=38,
            corner_radius=9,
            fg_color=ACCENT_CYAN,
            hover_color=ACCENT_CYAN_HOVER,
            text_color="#FFFFFF",
            font=fonte(12, "bold"),
            command=self.carregar,
        )
        self.btn_carregar.pack(side="left", padx=(0, 14))

        # Container de abas estilo Segmented Control
        tabs_tray = ctk.CTkFrame(
            ba_in,
            fg_color=ADMIN_INNER,
            corner_radius=10,
            border_width=1,
            border_color=ADMIN_BORDER,
        )
        tabs_tray.pack(side="left", fill="x")

        self.tab_botoes: Dict[str, ctk.CTkButton] = {}
        self.tab_indicadores: Dict[str, ctk.CTkFrame] = {}

        abas_def = [
            ("ranking", "🏆 Locais Mais Procurados", self.mostrar_locais_procurados),
            ("mensal", "📅 Resumo Mensal", self.mostrar_resumo_mensal),
            ("insights", "💡 Gerar Insights", self.mostrar_insights),
            ("graficos", "📊 Visualizar Gráficos", self.mostrar_graficos),
        ]

        for chave, texto_btn, func in abas_def:
            tab_wrap = ctk.CTkFrame(tabs_tray, fg_color="transparent")
            tab_wrap.pack(side="left", padx=3, pady=3)

            btn = ctk.CTkButton(
                tab_wrap,
                text=texto_btn,
                height=32,
                corner_radius=8,
                fg_color="transparent",
                text_color=ADMIN_MUTED,
                hover_color=ADMIN_ELEVATED,
                font=fonte(12, "bold"),
                command=lambda f=func: self.executar_acao(f),
            )
            btn.pack(fill="x")

            ind = ctk.CTkFrame(tab_wrap, height=3, corner_radius=2, fg_color="transparent")
            ind.pack(fill="x", padx=8, pady=(2, 0))

            self.tab_botoes[chave] = btn
            self.tab_indicadores[chave] = ind

        self.lbl_status_db = ctk.CTkLabel(
            ba_in,
            text=f"MySQL • {MYSQL_CONFIG['database']}.visitas_mensais",
            font=fonte(11),
            text_color=ADMIN_MUTED,
        )
        self.lbl_status_db.pack(side="right", padx=(8, 4))

        # --- Linha 2: Área Principal Dividida (Esquerda: Micro-Cards / Direita: Gráficos) ---
        grid_main = ctk.CTkFrame(corpo, fg_color="transparent")
        grid_main.grid(row=2, column=0, sticky="nsew")
        grid_main.grid_columnconfigure(0, weight=46, uniform="admin_cols")
        grid_main.grid_columnconfigure(1, weight=54, uniform="admin_cols")
        grid_main.grid_rowconfigure(0, weight=1)

        # Painel Esquerdo: Relatório Visual (CTkScrollableFrame com Micro-Cards)
        card_esq = ctk.CTkFrame(
            grid_main,
            fg_color=ADMIN_CARD,
            corner_radius=12,
            border_width=1,
            border_color=ADMIN_BORDER,
        )
        card_esq.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        header_esq = ctk.CTkFrame(card_esq, fg_color="transparent")
        header_esq.pack(fill="x", padx=18, pady=(14, 10))

        self.lbl_titulo_esq = ctk.CTkLabel(
            header_esq,
            text="📋 Visão Geral Analítica",
            font=fonte(15, "bold"),
            text_color=ADMIN_TEXT,
        )
        self.lbl_titulo_esq.pack(side="left")

        self.badge_esq = ctk.CTkLabel(
            header_esq,
            text="Aiven MySQL",
            font=fonte(10, "bold"),
            text_color=ACCENT_CYAN_BRIGHT,
            fg_color=ADMIN_INNER,
            corner_radius=6,
            padx=10,
            pady=3,
        )
        self.badge_esq.pack(side="right")

        ctk.CTkFrame(card_esq, height=1, fg_color=ADMIN_BORDER).pack(fill="x", padx=16)

        self.painel_relatorio = ctk.CTkScrollableFrame(
            card_esq,
            fg_color="transparent",
            corner_radius=0,
        )
        self.painel_relatorio.pack(fill="both", expand=True, padx=12, pady=12)

        self._renderizar_boas_vindas()

        # Painel Direito: Gráficos Matplotlib + Seletor de Modo + Ampliar
        card_dir = ctk.CTkFrame(
            grid_main,
            fg_color=ADMIN_CARD,
            corner_radius=12,
            border_width=1,
            border_color=ADMIN_BORDER,
        )
        card_dir.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        header_dir = ctk.CTkFrame(card_dir, fg_color="transparent")
        header_dir.pack(fill="x", padx=18, pady=(12, 8))

        ctk.CTkLabel(
            header_dir,
            text="📈 Visualizações Matplotlib",
            font=fonte(15, "bold"),
            text_color=ADMIN_TEXT,
        ).pack(side="left")

        controles_graf = ctk.CTkFrame(header_dir, fg_color="transparent")
        controles_graf.pack(side="right")

        self._mapa_modos_graf = {
            "Ambos": "ambos",
            "Evolução Mensal": "evolucao",
            "Ranking": "ranking",
        }
        self.seg_modo_grafico = ctk.CTkSegmentedButton(
            controles_graf,
            values=list(self._mapa_modos_graf.keys()),
            height=28,
            corner_radius=7,
            fg_color=ADMIN_INNER,
            selected_color=ACCENT_CYAN,
            selected_hover_color=ACCENT_CYAN_HOVER,
            unselected_color=ADMIN_INNER,
            unselected_hover_color=ADMIN_ELEVATED,
            text_color=ADMIN_TEXT,
            font=fonte(11, "bold"),
            command=self._ao_alterar_modo_grafico,
        )
        self.seg_modo_grafico.set("Ambos")
        self.seg_modo_grafico.pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            controles_graf,
            text="⛶ Ampliar",
            width=82,
            height=28,
            corner_radius=7,
            fg_color=ADMIN_ELEVATED,
            border_width=1,
            border_color=ADMIN_BORDER_STRONG,
            text_color=ADMIN_TEXT,
            hover_color=ADMIN_INNER,
            font=fonte(11, "bold"),
            command=lambda: self.executar_acao(self._abrir_modal_graficos),
        ).pack(side="left")

        ctk.CTkFrame(card_dir, height=1, fg_color=ADMIN_BORDER).pack(fill="x", padx=16)

        self.container_graficos = ctk.CTkFrame(
            card_dir,
            fg_color=ADMIN_INNER,
            corner_radius=10,
            border_width=1,
            border_color=ADMIN_BORDER,
        )
        self.container_graficos.pack(fill="both", expand=True, padx=16, pady=14)

        placeholder = ctk.CTkFrame(self.container_graficos, fg_color="transparent")
        placeholder.pack(expand=True)
        ctk.CTkLabel(placeholder, text="📊", font=fonte(42)).pack(pady=(0, 8))
        ctk.CTkLabel(
            placeholder,
            text="Os gráficos aparecerão aqui",
            font=fonte(15, "bold"),
            text_color=ADMIN_TEXT,
        ).pack(pady=(0, 4))
        ctk.CTkLabel(
            placeholder,
            text="Clique em '🔄 Carregar Dados (Aiven)' e depois em '📊 Visualizar Gráficos'.",
            font=fonte(12),
            text_color=ADMIN_MUTED,
        ).pack()

    # ==================================================================
    # 3. Helpers Visuais e Navegação de Abas
    # ==================================================================
    def _limpar_painel_esquerdo(self):
        for w in self.painel_relatorio.winfo_children():
            w.destroy()

    def _marcar_aba(self, chave_aba: str):
        self.aba_ativa = chave_aba
        for chave, btn in self.tab_botoes.items():
            ativo = chave == chave_aba
            btn.configure(
                fg_color=ADMIN_ELEVATED if ativo else "transparent",
                text_color=ADMIN_TEXT if ativo else ADMIN_MUTED,
            )
            self.tab_indicadores[chave].configure(
                fg_color=ACCENT_CYAN if ativo else "transparent"
            )

    def _renderizar_boas_vindas(self):
        self._limpar_painel_esquerdo()
        self.lbl_titulo_esq.configure(text="📋 Visão Geral Analítica")
        self.badge_esq.configure(text="Pronto p/ conectar", text_color=ACCENT_CYAN_BRIGHT)

        card = ctk.CTkFrame(
            self.painel_relatorio,
            fg_color=ADMIN_INNER,
            corner_radius=12,
            border_width=1,
            border_color=ADMIN_BORDER,
        )
        card.pack(fill="x", pady=6, padx=4)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(
            inner,
            text="Painel Executivo DataInsight",
            font=fonte(17, "bold"),
            text_color=ADMIN_TEXT,
        ).pack(anchor="w", pady=(0, 6))

        ctk.CTkLabel(
            inner,
            text=f"Conectado ao banco MySQL Aiven ({MYSQL_CONFIG['database']}.visitas_mensais) via pandas.read_sql().",
            font=fonte(12),
            text_color=ADMIN_MUTED,
            wraplength=440,
            justify="left",
        ).pack(anchor="w", pady=(0, 14))

        passos = [
            ("1", ACCENT_CYAN, "Clique em '🔄 Carregar Dados (Aiven)' para consultar os registros reais."),
            ("2", ACCENT_INDIGO, "Navegue pelas abas para ver rankings, tabela mensal e insights (> 130%)."),
            ("3", ACCENT_EMERALD, "Use o seletor à direita para alternar os gráficos Matplotlib."),
        ]
        for num, cor, txt in passos:
            row = ctk.CTkFrame(inner, fg_color=ADMIN_CARD, corner_radius=8, border_width=1, border_color=ADMIN_BORDER)
            row.pack(fill="x", pady=4)
            r_in = ctk.CTkFrame(row, fg_color="transparent")
            r_in.pack(fill="x", padx=12, pady=8)

            b = ctk.CTkFrame(r_in, width=24, height=24, corner_radius=6, fg_color=cor)
            b.pack(side="left", padx=(0, 10))
            b.pack_propagate(False)
            ctk.CTkLabel(b, text=num, font=fonte(11, "bold"), text_color="#FFFFFF").pack(expand=True)
            ctk.CTkLabel(r_in, text=txt, font=fonte(12), text_color=ADMIN_TEXT, wraplength=370, justify="left").pack(
                side="left", anchor="w"
            )

    def _ao_alterar_modo_grafico(self, rotulo: str):
        self.modo_grafico = self._mapa_modos_graf.get(rotulo, "ambos")
        if self.df is not None and not self.df.empty:
            desenhar_graficos_painel(self.container_graficos, self.df, modo=self.modo_grafico)
            self._graficos_renderizados = True

    def verificar_dados(self) -> bool:
        if self.df is None or self.df.empty:
            messagebox.showwarning("Atenção", "Carregue os dados primeiro clicando em '🔄 Carregar Dados (Aiven)'!")
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
    # 4. Carregamento Assíncrono do Banco Aiven
    # ==================================================================
    def carregar(self):
        """Carrega os registros reais do MySQL Aiven em background sem travar a interface."""
        self.btn_carregar.configure(state="disabled", text="⏳ Sincronizando Aiven...")
        self._limpar_painel_esquerdo()
        self.lbl_titulo_esq.configure(text="⏳ Conectando ao MySQL Aiven")
        self.badge_esq.configure(text="Carregando...", text_color=ACCENT_AMBER)

        card = ctk.CTkFrame(
            self.painel_relatorio,
            fg_color=ADMIN_INNER,
            corner_radius=12,
            border_width=1,
            border_color=ADMIN_BORDER,
        )
        card.pack(fill="x", pady=8, padx=4)
        ci = ctk.CTkFrame(card, fg_color="transparent")
        ci.pack(fill="x", padx=18, pady=18)
        ctk.CTkLabel(ci, text="Consultando banco MySQL hospedado na Aiven...", font=fonte(14, "bold"), text_color=ADMIN_TEXT).pack(anchor="w")
        ctk.CTkLabel(
            ci,
            text=f"Servidor: {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}  •  Banco: {MYSQL_CONFIG['database']}",
            font=fonte(11),
            text_color=ADMIN_MUTED,
        ).pack(anchor="w", pady=(4, 0))

        def _worker():
            try:
                df_carregado = carregar_dados()
                self.after(0, lambda: self._ao_concluir_carregamento(df_carregado, None))
            except Exception as erro:
                self.after(0, lambda e=erro: self._ao_concluir_carregamento(None, e))

        threading.Thread(target=_worker, daemon=True).start()

    def _ao_concluir_carregamento(self, df_carregado: Optional[pd.DataFrame], erro: Optional[Exception]):
        if not self.winfo_exists():
            return

        self.btn_carregar.configure(state="normal", text="🔄 Carregar Dados (MySQL)")

        if erro is not None:
            self.df = None
            self._limpar_painel_esquerdo()
            self.lbl_titulo_esq.configure(text="❌ Erro de Conexão (Aiven)")
            self.badge_esq.configure(text="Offline / Falha", text_color=ACCENT_ROSE)

            err_card = ctk.CTkFrame(
                self.painel_relatorio,
                fg_color=ADMIN_INNER,
                corner_radius=12,
                border_width=1,
                border_color=ACCENT_ROSE,
            )
            err_card.pack(fill="x", pady=8, padx=4)
            ei = ctk.CTkFrame(err_card, fg_color="transparent")
            ei.pack(fill="x", padx=16, pady=16)
            ctk.CTkLabel(ei, text="Não foi possível carregar os dados do MySQL Aiven", font=fonte(14, "bold"), text_color=ACCENT_ROSE).pack(anchor="w")
            ctk.CTkLabel(ei, text=str(erro), font=fonte(12), text_color=ADMIN_TEXT, wraplength=430, justify="left").pack(anchor="w", pady=(6, 0))
            messagebox.showerror("Erro de Conexão (Aiven)", f"Falha ao carregar os dados reais do MySQL:\n{erro}")
            return

        self.df = df_carregado
        if self.df is None or self.df.empty:
            self._limpar_painel_esquerdo()
            ctk.CTkLabel(self.painel_relatorio, text="Nenhum registro encontrado em visitas_mensais.", font=fonte(13), text_color=ADMIN_MUTED).pack(pady=24)
            return

        total_acessos = int(self.df["acessos"].sum())
        total_roteiros = int(self.df["adicionados_roteiro"].sum())
        taxa_media = (total_roteiros / total_acessos * 100) if total_acessos > 0 else 0.0

        ranking = locais_mais_procurados(self.df)
        local_top = str(ranking.iloc[0]["local"]) if not ranking.empty else "—"

        mensal = resumo_mensal(self.df)
        melhor_mes = str(mensal.loc[mensal["acessos"].idxmax()]["nome_mes"]) if not mensal.empty else "Outubro"

        # Atualiza os 4 cards executivos de KPI
        self.kpi_labels["total_acessos"].configure(text=f"{total_acessos:,}".replace(",", "."))
        self.kpi_labels["total_roteiros"].configure(text=f"{total_roteiros:,}".replace(",", "."))
        self.kpi_labels["top_local"].configure(text=local_top)
        self.kpi_labels["taxa_media"].configure(text=f"{taxa_media:.1f}%")

        self.kpi_sublabels["total_acessos"].configure(text=f"● {len(self.df)} registros • Aiven")
        self.kpi_sublabels["total_roteiros"].configure(text=f"● {self.df['local'].nunique()} locais analisados")
        self.kpi_sublabels["top_local"].configure(text="★ Top 1 em Belém")
        self.kpi_sublabels["taxa_media"].configure(text=f"▲ Alta temporada: {melhor_mes}")

        # Renderiza automaticamente Ranking à esquerda e Gráficos à direita
        self.mostrar_locais_procurados()
        desenhar_graficos_painel(self.container_graficos, self.df, modo=self.modo_grafico)
        self._graficos_renderizados = True

    # ==================================================================
    # 5. Aba 1: Locais Mais Procurados (Micro-Cards com Medalhas & Barra)
    # ==================================================================
    def mostrar_locais_procurados(self):
        self._marcar_aba("ranking")
        self._limpar_painel_esquerdo()

        ranking = locais_mais_procurados(self.df)
        self.lbl_titulo_esq.configure(text="🏆 Locais Mais Procurados")
        self.badge_esq.configure(text=f"{len(self.df)} linhas • Aiven", text_color=ACCENT_EMERALD)

        max_rot = float(ranking["adicionados_roteiro"].max()) if not ranking.empty else 1.0

        for idx, row in ranking.iterrows():
            pos = idx + 1
            nome = str(row["local"])
            cat = str(row["categoria"])
            acessos = int(row["acessos"])
            roteiros = int(row["adicionados_roteiro"])
            conv = float(row["taxa_conversao"])

            card = ctk.CTkFrame(
                self.painel_relatorio,
                fg_color=ADMIN_INNER,
                corner_radius=10,
                border_width=1,
                border_color=ACCENT_AMBER if pos == 1 else ADMIN_BORDER,
            )
            card.pack(fill="x", pady=5, padx=4)

            ci = ctk.CTkFrame(card, fg_color="transparent")
            ci.pack(fill="x", padx=14, pady=12)

            # Linha superior: Medalha + Nome + Categoria + Conversão Verde
            top = ctk.CTkFrame(ci, fg_color="transparent")
            top.pack(fill="x")

            if pos == 1:
                m_bg, m_fg = "#F59E0B", "#0B1120"
            elif pos == 2:
                m_bg, m_fg = "#CBD5E1", "#0B1120"
            elif pos == 3:
                m_bg, m_fg = "#D97706", "#FFFFFF"
            else:
                m_bg, m_fg = ADMIN_ELEVATED, ADMIN_MUTED

            pos_badge = ctk.CTkFrame(top, width=36, height=26, corner_radius=7, fg_color=m_bg)
            pos_badge.pack(side="left", padx=(0, 10))
            pos_badge.pack_propagate(False)
            ctk.CTkLabel(pos_badge, text=f"#{pos}", font=fonte(11, "bold"), text_color=m_fg).pack(expand=True)

            ctk.CTkLabel(top, text=nome, font=fonte(14, "bold"), text_color=ADMIN_TEXT).pack(side="left", padx=(0, 8))

            cat_bg, cat_fg = CATEGORIA_CORES.get(cat, (ADMIN_ELEVATED, ACCENT_CYAN_BRIGHT))
            cat_pill = ctk.CTkFrame(top, fg_color=cat_bg, corner_radius=6)
            cat_pill.pack(side="left")
            ctk.CTkLabel(cat_pill, text=cat, font=fonte(10, "bold"), text_color=cat_fg, padx=8, pady=2).pack()

            conv_pill = ctk.CTkFrame(top, fg_color=("#D1FAE5", "#064E3B"), corner_radius=6)
            conv_pill.pack(side="right")
            ctk.CTkLabel(
                conv_pill,
                text=f"▲ {conv:.1f}% conv.",
                font=fonte(10, "bold"),
                text_color=("#047857", "#34D399"),
                padx=8,
                pady=2,
            ).pack()

            # Barra de progresso proporcional
            barra = ctk.CTkProgressBar(
                ci,
                height=7,
                corner_radius=4,
                fg_color=ADMIN_ELEVATED,
                progress_color=ACCENT_AMBER if pos == 1 else ACCENT_CYAN,
            )
            barra.set(roteiros / max(1.0, max_rot))
            barra.pack(fill="x", pady=(10, 6))

            # Linha de métricas numéricas
            bot = ctk.CTkFrame(ci, fg_color="transparent")
            bot.pack(fill="x")
            ctk.CTkLabel(
                bot,
                text=f"Acessos: {acessos:,}".replace(",", "."),
                font=fonte(11),
                text_color=ADMIN_MUTED,
            ).pack(side="left")
            ctk.CTkLabel(
                bot,
                text=f"Roteiros / Interações: {roteiros:,}".replace(",", "."),
                font=fonte(11, "bold"),
                text_color=ACCENT_CYAN_BRIGHT,
            ).pack(side="right")

    # ==================================================================
    # 6. Aba 2: Resumo Mensal (Tabela Moderna com Badges de Variação)
    # ==================================================================
    def mostrar_resumo_mensal(self):
        self._marcar_aba("mensal")
        self._limpar_painel_esquerdo()

        mensal = resumo_mensal(self.df)
        anos = sorted(self.df["ano"].unique().tolist()) if "ano" in self.df.columns else []
        periodo_txt = f"{anos[0]}–{anos[-1]}" if len(anos) > 1 else (str(anos[0]) if anos else "Aiven")

        self.lbl_titulo_esq.configure(text=f"📅 Resumo Mensal ({periodo_txt})")
        self.badge_esq.configure(text="12 meses", text_color=ACCENT_INDIGO)

        melhor = mensal.loc[mensal["acessos"].idxmax()]
        menor = mensal.loc[mensal["acessos"].idxmin()]
        melhor_mes = str(melhor["nome_mes"])
        menor_mes = str(menor["nome_mes"])

        # Mini-cards de destaque (Maior vs Menor Movimento)
        destaques = ctk.CTkFrame(self.painel_relatorio, fg_color="transparent")
        destaques.pack(fill="x", padx=4, pady=(2, 10))
        destaques.grid_columnconfigure((0, 1), weight=1, uniform="mes_dest")

        for col, (tit, mes_nome, qtd, cor) in enumerate([
            ("🔥 MAIOR MOVIMENTO", melhor_mes, int(melhor["acessos"]), ACCENT_EMERALD),
            ("📉 MENOR MOVIMENTO", menor_mes, int(menor["acessos"]), ACCENT_AMBER),
        ]):
            dc = ctk.CTkFrame(destaques, fg_color=ADMIN_INNER, corner_radius=10, border_width=1, border_color=ADMIN_BORDER)
            dc.grid(row=0, column=col, padx=(0 if col == 0 else 5, 0 if col == 1 else 5), sticky="nsew")
            di = ctk.CTkFrame(dc, fg_color="transparent")
            di.pack(fill="x", padx=12, pady=10)
            ctk.CTkLabel(di, text=tit, font=fonte(10, "bold"), text_color=ADMIN_MUTED).pack(anchor="w")
            ctk.CTkLabel(di, text=f"{mes_nome} • {qtd:,}".replace(",", "."), font=fonte(14, "bold"), text_color=cor).pack(anchor="w", pady=(2, 0))

        # Cabeçalho da Tabela
        tbl = ctk.CTkFrame(self.painel_relatorio, fg_color=ADMIN_INNER, corner_radius=10, border_width=1, border_color=ADMIN_BORDER)
        tbl.pack(fill="x", padx=4, pady=(0, 8))

        hdr = ctk.CTkFrame(tbl, fg_color=ADMIN_ELEVATED, corner_radius=8)
        hdr.pack(fill="x", padx=6, pady=(6, 4))
        hdr.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="tbl_cols")

        for c_idx, h_txt in enumerate(("MÊS", "ACESSOS", "ROTEIROS", "VARIAÇÃO")):
            ctk.CTkLabel(hdr, text=h_txt, font=fonte(10, "bold"), text_color=ADMIN_MUTED, pady=6).grid(
                row=0, column=c_idx, sticky="w" if c_idx == 0 else "e", padx=10
            )

        for idx, row in mensal.iterrows():
            nome_m = str(row["nome_mes"])
            acessos = int(row["acessos"])
            roteiros = int(row["adicionados_roteiro"])
            cresc = row["crescimento_%"]

            eh_extremo = nome_m in (melhor_mes, menor_mes)
            bg_row = ADMIN_ROW_ALT if idx % 2 == 1 else ADMIN_INNER

            r_frame = ctk.CTkFrame(
                tbl,
                fg_color=bg_row,
                corner_radius=6,
                border_width=1 if eh_extremo else 0,
                border_color=ACCENT_EMERALD if nome_m == melhor_mes else ACCENT_AMBER,
            )
            r_frame.pack(fill="x", padx=6, pady=2)
            r_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="tbl_cols")

            prefixo = "★ " if nome_m == melhor_mes else ("• " if nome_m == menor_mes else "")
            ctk.CTkLabel(
                r_frame,
                text=f"{prefixo}{nome_m}",
                font=fonte(12, "bold" if eh_extremo else "normal"),
                text_color=ADMIN_TEXT,
                pady=7,
            ).grid(row=0, column=0, sticky="w", padx=10)

            ctk.CTkLabel(
                r_frame,
                text=f"{acessos:,}".replace(",", "."),
                font=fonte(12, "bold"),
                text_color=ADMIN_TEXT,
            ).grid(row=0, column=1, sticky="e", padx=10)

            ctk.CTkLabel(
                r_frame,
                text=f"{roteiros:,}".replace(",", "."),
                font=fonte(12),
                text_color=ACCENT_CYAN_BRIGHT,
            ).grid(row=0, column=2, sticky="e", padx=10)

            if pd.isna(cresc):
                var_txt, var_bg, var_fg = "—", ADMIN_ELEVATED, ADMIN_MUTED
            elif cresc >= 0:
                var_txt = f"▲ +{cresc:.1f}%"
                var_bg, var_fg = ("#D1FAE5", "#064E3B"), ("#047857", "#34D399")
            else:
                var_txt = f"▼ {cresc:.1f}%"
                var_bg, var_fg = ("#FFE4E6", "#4C0519"), ("#BE123C", "#FB7185")

            pill = ctk.CTkFrame(r_frame, fg_color=var_bg, corner_radius=6)
            pill.grid(row=0, column=3, sticky="e", padx=10, pady=4)
            ctk.CTkLabel(pill, text=var_txt, font=fonte(10, "bold"), text_color=var_fg, padx=7, pady=2).pack()

    # ==================================================================
    # 7. Aba 3: Gerar Insights (Cards de Alerta e Recomendação Prática)
    # ==================================================================
    def mostrar_insights(self):
        self._marcar_aba("insights")
        self._limpar_painel_esquerdo()

        itens = gerar_insights(self.df)
        self.lbl_titulo_esq.configure(text="💡 Motor de Insights (> 130%)")
        self.badge_esq.configure(text=f"{len(itens)} alertas", text_color=ACCENT_AMBER)

        for texto in itens:
            partes = texto.split("\n", 1)
            linha_principal = partes[0].strip()
            linha_contexto = partes[1].replace("↳", "").strip() if len(partes) > 1 else ""

            eh_pico_local = "PICO POR LOCAL" in linha_principal
            cor_borda = ACCENT_AMBER if eh_pico_local else ACCENT_CYAN

            # Extrai título e percentual acima da média para o badge
            m_pct = re.search(r"(\d+)%\s+acima", linha_principal)
            pct_badge = f"+{m_pct.group(1)}%" if m_pct else ">130%"

            if ":" in linha_principal:
                titulo_card, detalhe_card = linha_principal.split(":", 1)
            else:
                titulo_card, detalhe_card = linha_principal, ""

            card = ctk.CTkFrame(
                self.painel_relatorio,
                fg_color=ADMIN_INNER,
                corner_radius=10,
                border_width=1,
                border_color=ADMIN_BORDER,
            )
            card.pack(fill="x", pady=6, padx=4)

            # Borda lateral colorida (4px)
            wrap = ctk.CTkFrame(card, fg_color="transparent")
            wrap.pack(fill="both", expand=True)

            stripe = ctk.CTkFrame(wrap, width=4, corner_radius=2, fg_color=cor_borda)
            stripe.pack(side="left", fill="y", padx=(0, 12), pady=8)

            body = ctk.CTkFrame(wrap, fg_color="transparent")
            body.pack(side="left", fill="both", expand=True, padx=(0, 14), pady=12)

            top = ctk.CTkFrame(body, fg_color="transparent")
            top.pack(fill="x")
            ctk.CTkLabel(
                top,
                text=titulo_card.strip(),
                font=fonte(13, "bold"),
                text_color=ADMIN_TEXT,
                wraplength=330,
                justify="left",
            ).pack(side="left", anchor="w")

            pill_pct = ctk.CTkFrame(
                top,
                fg_color=("#FEF3C7", "#3B2506") if eh_pico_local else ("#E0F2FE", "#0C4A6E"),
                corner_radius=6,
            )
            pill_pct.pack(side="right", anchor="n")
            ctk.CTkLabel(
                pill_pct,
                text=pct_badge,
                font=fonte(10, "bold"),
                text_color=cor_borda,
                padx=8,
                pady=2,
            ).pack()

            if detalhe_card.strip():
                ctk.CTkLabel(
                    body,
                    text=detalhe_card.strip(),
                    font=fonte(12),
                    text_color=ADMIN_MUTED,
                    wraplength=410,
                    justify="left",
                ).pack(anchor="w", pady=(4, 8))

            if linha_contexto:
                rec_box = ctk.CTkFrame(body, fg_color=ADMIN_CARD, corner_radius=8, border_width=1, border_color=ADMIN_BORDER)
                rec_box.pack(fill="x")
                ctk.CTkLabel(
                    rec_box,
                    text=f"💡 {linha_contexto}",
                    font=fonte(11),
                    text_color=ADMIN_TEXT,
                    wraplength=395,
                    justify="left",
                    padx=10,
                    pady=7,
                ).pack(anchor="w")

    # ==================================================================
    # 8. Aba 4: Visualizar Gráficos
    # ==================================================================
    def mostrar_graficos(self):
        self._marcar_aba("graficos")
        desenhar_graficos_painel(self.container_graficos, self.df, modo=self.modo_grafico)
        self._graficos_renderizados = True

        self._limpar_painel_esquerdo()
        self.lbl_titulo_esq.configure(text="📊 Guia de Visualizações")
        self.badge_esq.configure(text="Atualizado", text_color=ACCENT_EMERALD)

        cards_info = [
            (
                ACCENT_CYAN,
                "📈 Evolução Mensal (Linhas)",
                "Mostra a curva de acessos e interações ao longo dos meses com preenchimento translúcido e marcação automática dos picos de Julho (Verão Amazônico) e Outubro (Círio de Nazaré).",
            ),
            (
                ACCENT_INDIGO,
                "🏆 Ranking Comparativo (Barras)",
                "Exibe os pontos turísticos ordenados por interações/roteiros em degradê azul ciano, com destaque para o #1 líder de Belém.",
            ),
            (
                ACCENT_EMERALD,
                "🎛️ Controles Interativos",
                "Use o seletor no topo do painel direito ('Ambos', 'Evolução Mensal' ou 'Ranking') ou clique em '⛶ Ampliar' para abrir em tela dedicada.",
            ),
        ]
        for cor, tit, desc in cards_info:
            c = ctk.CTkFrame(self.painel_relatorio, fg_color=ADMIN_INNER, corner_radius=10, border_width=1, border_color=ADMIN_BORDER)
            c.pack(fill="x", pady=6, padx=4)
            w = ctk.CTkFrame(c, fg_color="transparent")
            w.pack(fill="x")
            ctk.CTkFrame(w, width=4, corner_radius=2, fg_color=cor).pack(side="left", fill="y", padx=(0, 12), pady=8)
            b = ctk.CTkFrame(w, fg_color="transparent")
            b.pack(side="left", fill="x", expand=True, padx=(0, 14), pady=12)
            ctk.CTkLabel(b, text=tit, font=fonte(13, "bold"), text_color=ADMIN_TEXT).pack(anchor="w")
            ctk.CTkLabel(b, text=desc, font=fonte(12), text_color=ADMIN_MUTED, wraplength=400, justify="left").pack(anchor="w", pady=(4, 0))

    def _abrir_modal_graficos(self):
        mostrar_graficos_modal(self, self.df, modo=self.modo_grafico)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = PainelAdminApp()
    app.mainloop()
