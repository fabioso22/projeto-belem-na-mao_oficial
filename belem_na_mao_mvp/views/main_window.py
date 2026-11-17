"""
Visual Principal do BelémNaMão — Guia Inteligente
Design Moderno, Clean, Profissional e Atrativo baseado no Design System oficial.
"""
import webbrowser
from typing import Any, Dict, List, Optional

import customtkinter as ctk

from services.catalogo import buscar_locais, carregar_locais, rotulo_preco
from services.roteiro import adicionar, carregar_roteiro, limpar, remover, salvar_roteiro
from views.theme import (
    AMBER,
    BG,
    BTN_SECONDARY_BG,
    BTN_SECONDARY_BORDER,
    BTN_SECONDARY_HOVER,
    BTN_SECONDARY_TEXT,
    CATEGORIAS_INFO,
    ERROR,
    LINE,
    LINE_LIGHT,
    PANEL,
    PANEL_SUBTLE,
    PRIMARY,
    PRIMARY_BTN,
    PRIMARY_CONTAINER,
    PRIMARY_HOVER,
    PRIMARY_SOFT,
    SECONDARY,
    SECONDARY_CONTAINER,
    SECONDARY_FIXED,
    SECONDARY_HOVER,
    SUCCESS,
    TAG_BG,
    TAG_BORDER,
    TAG_TEXT,
    TERTIARY,
    TERTIARY_CONTAINER,
    TERTIARY_FIXED,
    ON_TERTIARY_FIXED,
    ON_TERTIARY_VARIANT,
    TEXT,
    TEXT_BRAND,
    TEXT_KPI,
    TEXT_LIGHT,
    TEXT_MUTED,
    TEXT_TITLE,
    fonte,
    obter_imagem_processada,
)

# Metadados e notas editoriais para enriquecer a experiência visual
METADADOS_LOCAIS = {
    "ver-o-peso": {
        "rating": 4.8,
        "avaliacoes": "2.4k",
        "subtitulo": "A maior feira a céu aberto da América Latina • Foz do Guamá",
        "horario": "05h00 às 18h00 (Setor de peixes a partir das 03h00)",
        "melhor_horario": "Manhã cedo (07h às 09h30)",
        "preco_tag": "$ • Acessível",
        "destaque_tag": "Cultura & Gastronomia",
        "distancia": "0,5 km",
    },
    "estacao-das-docas": {
        "rating": 4.9,
        "avaliacoes": "3.1k",
        "subtitulo": "Galpões portuários de ferro inglês restaurados de frente para o Guajará",
        "horario": "10h00 às 00h00 (Sexta e Sábado até 01h00)",
        "melhor_horario": "Fim de tarde / Pôr do sol (17h00)",
        "preco_tag": "$$$ • Médio/Alto",
        "destaque_tag": "Gastronomia & Lazer",
        "distancia": "0,9 km",
    },
    "feliz-lusitania": {
        "rating": 4.9,
        "avaliacoes": "1.8k",
        "subtitulo": "Marco zero de fundação de Belém em 1616 • Fortaleza e Museus",
        "horario": "09h00 às 18h00 (Fecha às segundas)",
        "melhor_horario": "Tarde (16h30 para contemplar o pôr do sol)",
        "preco_tag": "$ (R$ 6 / Terça Grátis)",
        "destaque_tag": "Patrimônio IPHAN",
        "distancia": "1,4 km",
    },
    "mangal": {
        "rating": 4.8,
        "avaliacoes": "2.7k",
        "subtitulo": "Parque ecológico com borboletário gigante, farol e guarás",
        "horario": "08h00 às 18h00 (Fecha às segundas)",
        "melhor_horario": "Alimentação dos guarás às 11h15 e 15h00",
        "preco_tag": "Parque Grátis (Espaços R$ 5)",
        "destaque_tag": "Natureza & Fauna",
        "distancia": "2,8 km",
    },
    "teatro-da-paz": {
        "rating": 4.9,
        "avaliacoes": "1.4k",
        "subtitulo": "Joia neoclássica do Ciclo da Borracha na Praça da República",
        "horario": "Visitas guiadas: Terça a Domingo de hora em hora",
        "melhor_horario": "Tarde (15h00 — climatizado durante a chuva)",
        "preco_tag": "$ (R$ 10 inteira / R$ 5 meia)",
        "destaque_tag": "Arquitetura Imperial",
        "distancia": "1,8 km",
    },
    "praca-republica": {
        "rating": 4.7,
        "avaliacoes": "950",
        "subtitulo": "Coração arborizado com mangueiras centenárias e feira aos domingos",
        "horario": "Acesso livre 24 horas",
        "melhor_horario": "Domingo de manhã (Feirinha de artesanato)",
        "preco_tag": "Gratuito",
        "destaque_tag": "Caminhada & Lazer",
        "distancia": "1,7 km",
    },
    "ilha-combu": {
        "rating": 4.8,
        "avaliacoes": "1.9k",
        "subtitulo": "Polo gastronômico ribeirinho e cultivo artesanal de cacau nativo",
        "horario": "Barcos das 09h00 às 18h00 (Praça Princesa Isabel)",
        "melhor_horario": "Almoço de sábado ou domingo (11h às 16h)",
        "preco_tag": "$$ • Médio",
        "destaque_tag": "Ribeirinho & Cacau",
        "distancia": "4,2 km (barco)",
    },
    "basilica-nazare": {
        "rating": 4.9,
        "avaliacoes": "2.1k",
        "subtitulo": "Santuário de Nossa Senhora de Nazaré e ápice do Círio",
        "horario": "06h00 às 20h00 diariamente",
        "melhor_horario": "Início da manhã ou final da tarde",
        "preco_tag": "Gratuito",
        "destaque_tag": "Fé & Tradição",
        "distancia": "3,1 km",
    },
}


class BelemNaMaoApp(ctk.CTk):
    LARGURA = 1200
    ALTURA = 780

    def __init__(self, usuario: Optional[Dict[str, Any]] = None, on_logout: Optional[Any] = None):
        super().__init__()
        self.usuario = usuario or {"id": 1, "nome": "Turista", "usuario": "turista"}
        self.usuario_id = self.usuario.get("id", 1)
        self.on_logout = on_logout

        self.title("BelémNaMão — Guia Inteligente da Amazônia Atlântica")
        self.geometry(f"{self.LARGURA}x{self.ALTURA}")
        self.minsize(1040, 640)
        self.configure(fg_color=BG)

        # Estado da Aplicação
        self.locais = carregar_locais()
        self.roteiro = carregar_roteiro(usuario_id=self.usuario_id)
        self.aba_atual = "Início"

        # Filtros de Catálogo
        self.f_texto = ""
        self.f_categoria = "Todas"
        self.f_preco = "Qualquer"
        self.f_bairro = "Todos os Bairros"

        self._centralizar()
        self._configurar_grid()
        self._criar_topo_navbar()

        # Container Principal com Troca Dinâmica de Telas
        self.conteudo = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.conteudo.grid(row=1, column=0, sticky="nsew")

        self.mostrar_inicio()

    def _centralizar(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - self.LARGURA) // 2)
        y = max(0, (sh - self.ALTURA) // 2)
        self.geometry(f"{self.LARGURA}x{self.ALTURA}+{x}+{y}")

    def _configurar_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Navbar Superior
        self.grid_rowconfigure(1, weight=1)  # Conteúdo da Página

    # ==================================================================
    # 1. Barra de Navegação Superior (Header Fixo Moderno)
    # ==================================================================
    def _criar_topo_navbar(self):
        self.navbar = ctk.CTkFrame(self, fg_color=PANEL, height=72, corner_radius=0, border_width=1, border_color=LINE)
        self.navbar.grid(row=0, column=0, sticky="ew")
        self.navbar.grid_propagate(False)

        inner = ctk.CTkFrame(self.navbar, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=24)

        # Esquerda: Logo + Clima/Maré Intel Pill
        esquerda = ctk.CTkFrame(inner, fg_color="transparent")
        esquerda.pack(side="left", fill="y")

        # Botão/Logo Clicável
        logo_box = ctk.CTkFrame(esquerda, fg_color="transparent", cursor="hand2")
        logo_box.pack(side="left", pady=14)
        logo_box.bind("<Button-1>", lambda _e: self.mostrar_inicio())

        emblema = ctk.CTkFrame(logo_box, width=40, height=40, corner_radius=8, fg_color=PRIMARY_BTN)
        emblema.pack(side="left", padx=(0, 10))
        emblema.pack_propagate(False)
        lbl_emb = ctk.CTkLabel(emblema, text="≋", font=fonte(22, "bold"), text_color=SECONDARY_FIXED)
        lbl_emb.pack(expand=True)
        lbl_emb.bind("<Button-1>", lambda _e: self.mostrar_inicio())

        brand_text = ctk.CTkFrame(logo_box, fg_color="transparent")
        brand_text.pack(side="left")
        ctk.CTkLabel(brand_text, text="Belém", font=fonte(18, "bold"), text_color=TEXT_TITLE).pack(side="left")
        ctk.CTkLabel(brand_text, text="NaMão", font=fonte(18, "bold"), text_color=SECONDARY).pack(side="left")

        # Widget de Clima e Maré em Tempo Real
        clima_pill = ctk.CTkFrame(esquerda, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        clima_pill.pack(side="left", padx=(18, 0), pady=16)

        ctk.CTkLabel(
            clima_pill,
            text="🕒 Chuva das 16h: Provável (82%)  •  🌊 Maré: Enchendo",
            font=fonte(11, "bold"),
            text_color=TEXT_BRAND,
            padx=14,
            pady=4,
        ).pack()

        # Centro: Menu Pill de Navegação
        centro = ctk.CTkFrame(inner, fg_color="transparent")
        centro.pack(side="left", expand=True)

        self.nav_botoes = {}
        itens_nav = [
            ("Início", self.mostrar_inicio),
            ("Explorar", self.mostrar_explorar),
            ("Meu Roteiro", self.mostrar_roteiro),
            ("Sobre Belém", self.mostrar_sobre_belem),
        ]

        nav_pill_container = ctk.CTkFrame(centro, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        nav_pill_container.pack(pady=16)

        for nome, cmd in itens_nav:
            btn = ctk.CTkButton(
                nav_pill_container,
                text=nome,
                font=fonte(13, "bold"),
                height=34,
                corner_radius=8,
                fg_color="transparent",
                text_color=TEXT_MUTED,
                hover_color=PANEL_SUBTLE,
                command=cmd,
            )
            btn.pack(side="left", padx=3, pady=3)
            self.nav_botoes[nome] = btn

        # Direita: Botão Rápido de Salvos + Perfil do Usuário
        direita = ctk.CTkFrame(inner, fg_color="transparent")
        direita.pack(side="right", fill="y", pady=16)

        # Botão de Busca Rápida
        btn_busca = ctk.CTkButton(
            direita,
            text="🔍 Buscar...",
            height=34,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(12),
            command=self.mostrar_explorar,
        )
        btn_busca.pack(side="left", padx=(0, 8))

        # Indicador de Salvos
        self.btn_salvos_pill = ctk.CTkButton(
            direita,
            text=f"🔖 {len(self.roteiro)} salvos",
            height=34,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=SECONDARY,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(12, "bold"),
            command=self.mostrar_roteiro,
        )
        self.btn_salvos_pill.pack(side="left", padx=(0, 8))

        # Botão Modo Escuro / Modo Claro
        modo_atual = ctk.get_appearance_mode().lower()
        texto_tema = "☀️ Modo Claro" if modo_atual == "dark" else "🌙 Modo Escuro"
        self.btn_tema = ctk.CTkButton(
            direita,
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

        # Perfil do Visitante
        perfil_box = ctk.CTkFrame(direita, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        perfil_box.pack(side="left", padx=(0, 8))

        avatar = ctk.CTkFrame(perfil_box, width=28, height=28, corner_radius=6, fg_color=PRIMARY_BTN)
        avatar.pack(side="left", padx=(4, 6), pady=3)
        avatar.pack_propagate(False)
        ctk.CTkLabel(avatar, text="👤", font=fonte(11), text_color="#FFFFFF").pack(expand=True)

        nome_user = self.usuario.get("nome", "Turista").split()[0]
        ctk.CTkLabel(perfil_box, text=f"Olá, {nome_user}", font=fonte(12, "bold"), text_color=TEXT_TITLE).pack(
            side="left", padx=(0, 10)
        )

        # Botão Sair / Logout
        btn_sair = ctk.CTkButton(
            direita,
            text="🚪 Sair",
            width=64,
            height=34,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(11, "bold"),
            command=self._fazer_logout,
        )
        btn_sair.pack(side="left")

    def _alternar_modo_escuro(self):
        """Alterna reativamente entre Modo Claro e Modo Escuro."""
        modo_atual = ctk.get_appearance_mode().lower()
        if modo_atual == "dark":
            ctk.set_appearance_mode("light")
            self.btn_tema.configure(text="🌙 Modo Escuro")
            self._toast("Modo Claro ativado")
        else:
            ctk.set_appearance_mode("dark")
            self.btn_tema.configure(text="☀️ Modo Claro")
            self._toast("Modo Escuro ativado", cor_bg=TERTIARY_CONTAINER)

    def _fazer_logout(self):
        """Encerra a sessão e retorna à tela de login."""
        if self.on_logout:
            self.on_logout()
        else:
            self.destroy()

    def _marcar_aba_ativa(self, nome_aba: str):
        """Atualiza a aparência dos botões de navegação para a aba selecionada."""
        self.aba_atual = nome_aba
        for n, btn in self.nav_botoes.items():
            ativo = n == nome_aba
            btn.configure(
                fg_color=PRIMARY_CONTAINER if ativo else "transparent",
                text_color="#FFFFFF" if ativo else TEXT_MUTED,
            )
        # Atualiza contagem de itens salvos
        if hasattr(self, "btn_salvos_pill"):
            self.btn_salvos_pill.configure(text=f"🔖 {len(self.roteiro)} salvos")

    def _limpar_conteudo(self):
        """Remove widgets da página anterior com limpeza limpa de memória."""
        for w in self.conteudo.winfo_children():
            w.destroy()

    def _toast(self, mensagem: str, cor_bg: str = PRIMARY):
        """Exibe uma notificação flutuante elegante no canto inferior."""
        toast = ctk.CTkFrame(self, fg_color=cor_bg, corner_radius=16, border_width=1, border_color="#314868")
        toast.place(relx=0.98, rely=0.95, anchor="se")

        ctk.CTkLabel(
            toast,
            text=f"  {mensagem}  ",
            font=fonte(13, "bold"),
            text_color="#FFFFFF",
            padx=14,
            pady=10,
        ).pack()

        self.after(2800, toast.destroy)

    def _no_roteiro(self, local: Dict[str, Any]) -> bool:
        return any(i.get("id") == local.get("id") for i in self.roteiro)

    # ==================================================================
    # 2. Tela Início (Hero Showcase, Clima, Categorias e Destaques)
    # ==================================================================
    def mostrar_inicio(self):
        self._limpar_conteudo()
        self._marcar_aba_ativa("Início")

        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(rolagem, fg_color="transparent")
        inner.pack(fill="x", padx=32, pady=(20, 40))

        # --- A. Card Azul Minimalista e Elegante ---
        hero = ctk.CTkFrame(inner, fg_color=PRIMARY_CONTAINER, corner_radius=12, border_width=1, border_color=LINE)
        hero.pack(fill="x", pady=(0, 24))

        hero_content = ctk.CTkFrame(hero, fg_color="transparent")
        hero_content.pack(fill="both", expand=True, padx=36, pady=32)

        ctk.CTkLabel(
            hero_content,
            text="Descubra Belém do seu jeito",
            font=fonte(32, "bold"),
            text_color="#FFFFFF",
            justify="left",
            anchor="w",
        ).pack(anchor="w", pady=(0, 4))

        ctk.CTkLabel(
            hero_content,
            text="Menos tempo procurando. Mais tempo vivendo as feiras, docas e sabores da Amazônia Atlântica.",
            font=fonte(14),
            text_color="#D5E3FF",
            justify="left",
            anchor="w",
        ).pack(anchor="w", pady=(0, 18))

        # Botões de Ação do Hero
        hero_actions = ctk.CTkFrame(hero_content, fg_color="transparent")
        hero_actions.pack(anchor="w")

        ctk.CTkButton(
            hero_actions,
            text="Explorar Catálogo  →",
            height=40,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(13, "bold"),
            command=self.mostrar_explorar,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            hero_actions,
            text="Ver Meu Roteiro",
            height=40,
            corner_radius=8,
            fg_color=SECONDARY,
            text_color="#FFFFFF",
            hover_color=SECONDARY_HOVER,
            font=fonte(13, "bold"),
            command=self.mostrar_roteiro,
        ).pack(side="left")

        # --- B. Categorias Bento (O que você quer fazer?) ---
        ctk.CTkLabel(inner, text="O que você quer fazer?", font=fonte(22, "bold"), text_color=TEXT_TITLE).pack(
            anchor="w", pady=(4, 14)
        )

        grade_cat = ctk.CTkFrame(inner, fg_color="transparent")
        grade_cat.pack(fill="x", pady=(0, 28))
        grade_cat.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="cat_col")

        for i, (nome_cat, info) in enumerate(CATEGORIAS_INFO.items()):
            c_card = ctk.CTkFrame(
                grade_cat,
                fg_color=PANEL,
                corner_radius=12,
                border_width=1,
                border_color=LINE,
                cursor="hand2",
            )
            c_card.grid(row=0, column=i, padx=5, sticky="nsew")

            c_box = ctk.CTkFrame(c_card, fg_color="transparent")
            c_box.pack(fill="both", expand=True, padx=16, pady=16)

            tile_emoji = ctk.CTkFrame(c_box, width=44, height=44, corner_radius=10, fg_color=info["cor_bg"])
            tile_emoji.pack(anchor="w", pady=(0, 10))
            tile_emoji.pack_propagate(False)
            ctk.CTkLabel(tile_emoji, text=info["emoji"], font=fonte(22)).pack(expand=True)

            ctk.CTkLabel(c_box, text=nome_cat, font=fonte(16, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
            ctk.CTkLabel(c_box, text=info["desc"], font=fonte(12), text_color=TEXT_MUTED).pack(anchor="w", pady=(2, 6))
            ctk.CTkLabel(
                c_box,
                text=f"{info['qtd']} experiências",
                font=fonte(11, "bold"),
                text_color=SECONDARY,
            ).pack(anchor="w")

            for w in (c_card, c_box, *c_box.winfo_children(), tile_emoji, *tile_emoji.winfo_children()):
                w.bind("<Button-1>", lambda _e, cat=nome_cat: self._filtrar_por_categoria(cat))

        # --- C. Destaques Imperdíveis (Cards com Foto Real) ---
        topo_destaques = ctk.CTkFrame(inner, fg_color="transparent")
        topo_destaques.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(topo_destaques, text="Destaques de Belém", font=fonte(22, "bold"), text_color=TEXT_TITLE).pack(
            side="left"
        )
        ctk.CTkButton(
            topo_destaques,
            text="Ver todas as atrações  →",
            fg_color="transparent",
            text_color=TEXT_BRAND,
            hover_color=PANEL_SUBTLE,
            font=fonte(13, "bold"),
            command=self.mostrar_explorar,
        ).pack(side="right")

        grade_destaques = ctk.CTkFrame(inner, fg_color="transparent")
        grade_destaques.pack(fill="x", pady=(0, 28))
        grade_destaques.grid_columnconfigure((0, 1, 2), weight=1, uniform="destaque_col")

        # Selecionar os 3 principais monumentos para o card bento
        destaques_cards = [l for l in self.locais if l.get("id") in ["ver-o-peso", "feliz-lusitania", "estacao-das-docas"]][:3]
        for i, loc in enumerate(destaques_cards):
            self._criar_card_destaque(grade_destaques, loc, coluna=i)

    def _criar_card_destaque(self, master, local: Dict[str, Any], coluna: int):
        meta = METADADOS_LOCAIS.get(local.get("id", ""), {})
        card = ctk.CTkFrame(master, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE, cursor="hand2")
        card.grid(row=0, column=coluna, padx=6, sticky="nsew")

        # Foto uniforme 16:9 ocupando toda a largura útil sem sobras
        img_ctk = obter_imagem_processada(local.get("id", ""), 360, 202, raio=12, apenas_topo=True)
        lbl_img = ctk.CTkLabel(card, text="", image=img_ctk)
        lbl_img.pack(side="top", fill="x", padx=0, pady=0)

        corpo = ctk.CTkFrame(card, fg_color="transparent")
        corpo.pack(side="top", fill="both", expand=True, padx=16, pady=14)

        # Linha de Metadados (Categoria + Avaliação)
        meta_row = ctk.CTkFrame(corpo, fg_color="transparent")
        meta_row.pack(fill="x", pady=(2, 6))

        tag_cat = ctk.CTkFrame(meta_row, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
        tag_cat.pack(side="left")
        ctk.CTkLabel(
            tag_cat,
            text=meta.get("destaque_tag", local.get("categoria", ["Turismo"])[0]),
            font=fonte(10, "bold"),
            text_color=TAG_TEXT,
            padx=8,
            pady=2,
        ).pack()

        ctk.CTkLabel(
            meta_row,
            text=f"★ {meta.get('rating', 4.8)} ({meta.get('avaliacoes', '1.2k')})",
            font=fonte(11, "bold"),
            text_color=AMBER,
        ).pack(side="right")

        ctk.CTkLabel(corpo, text=local["nome"], font=fonte(16, "bold"), text_color=TEXT_TITLE).pack(anchor="w")

        dist = meta.get("distancia", "1,4 km")
        dur = local.get("duracao", "2h")
        bairro = local.get("bairro", "Belém")
        preco = meta.get("preco_tag", rotulo_preco(local.get("preco")))
        ctk.CTkLabel(
            corpo,
            text=f"📍 {bairro} • {dist} • {dur}   |   {preco}",
            font=fonte(12),
            text_color=TEXT_BRAND,
        ).pack(anchor="w", pady=(2, 6))

        desc = local.get("descricao", "")
        if len(desc) > 95:
            desc = desc[:92] + "..."
        ctk.CTkLabel(
            corpo,
            text=desc,
            font=fonte(12),
            text_color=TEXT_MUTED,
            justify="left",
            wraplength=310,
        ).pack(anchor="w", pady=(0, 10))

        # Botões de Ação fixos na base do card
        botoes = ctk.CTkFrame(corpo, fg_color="transparent")
        botoes.pack(side="bottom", fill="x")

        presente = self._no_roteiro(local)
        btn_it = ctk.CTkButton(
            botoes,
            text="✓ No Roteiro" if presente else "+ Roteiro",
            height=36,
            corner_radius=8,
            fg_color=TERTIARY_CONTAINER if presente else PRIMARY_BTN,
            hover_color=TERTIARY if presente else PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(12, "bold"),
        )
        btn_it.configure(command=lambda l=local, b=btn_it: self.alternar_roteiro_btn(l, b))
        btn_it.pack(side="left", fill="x", expand=True, padx=(0, 6))

        ctk.CTkButton(
            botoes,
            text="Detalhes",
            height=36,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            hover_color=BTN_SECONDARY_HOVER,
            text_color=BTN_SECONDARY_TEXT,
            font=fonte(12, "bold"),
            command=lambda l=local: self.mostrar_detalhes(l, voltar=self.mostrar_inicio),
        ).pack(side="right")

        # Clique no card abre detalhes
        for w in (card, lbl_img, corpo):
            w.bind("<Button-1>", lambda _e, l=local: self.mostrar_detalhes(l, voltar=self.mostrar_inicio))

    def _filtrar_por_categoria(self, categoria: str):
        self.f_categoria = categoria
        self.mostrar_explorar()

    # ==================================================================
    # 3. Tela Explorar (Catálogo em Grade, Filtros por Bairro/Preço e Busca)
    # ==================================================================
    def mostrar_explorar(self):
        self._limpar_conteudo()
        self._marcar_aba_ativa("Explorar")

        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(rolagem, fg_color="transparent")
        inner.pack(fill="x", padx=32, pady=(20, 40))

        # Cabeçalho da Aba
        topo = ctk.CTkFrame(inner, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 14))

        topo_esq = ctk.CTkFrame(topo, fg_color="transparent")
        topo_esq.pack(side="left")

        ctk.CTkLabel(topo_esq, text="EXPLORAR PARÁ", font=fonte(11, "bold"), text_color=SECONDARY).pack(anchor="w")
        ctk.CTkLabel(topo_esq, text="Explorar Belém", font=fonte(28, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(
            topo_esq,
            text="Descubra os pontos turísticos, feiras culturais, gastronomia ribeirinha e recantos históricos.",
            font=fonte(13),
            text_color=TEXT_MUTED,
        ).pack(anchor="w")

        # Barra de Pesquisa Flutuante
        barra_busca = ctk.CTkFrame(inner, fg_color=PANEL, corner_radius=8, border_width=1, border_color=LINE)
        barra_busca.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(barra_busca, text="🔍", font=fonte(16)).pack(side="left", padx=(16, 6), pady=12)

        self.entry_busca = ctk.CTkEntry(
            barra_busca,
            height=44,
            corner_radius=0,
            fg_color="transparent",
            border_width=0,
            text_color=TEXT,
            placeholder_text="Buscar por nome, bairro (ex: Cidade Velha, Campina) ou palavra-chave...",
            placeholder_text_color=TEXT_LIGHT,
            font=fonte(14),
        )
        self.entry_busca.pack(side="left", fill="x", expand=True)
        if self.f_texto:
            self.entry_busca.insert(0, self.f_texto)

        btn_limpar_busca = ctk.CTkButton(
            barra_busca,
            text="✕",
            width=32,
            height=32,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(12, "bold"),
            command=self._limpar_campo_busca,
        )
        btn_limpar_busca.pack(side="right", padx=(6, 12))

        # Carrossel de Categorias (Pills Horizontais)
        chips_frame = ctk.CTkFrame(inner, fg_color="transparent")
        chips_frame.pack(fill="x", pady=(0, 12))

        self.chips_botoes = {}
        for nome_c in ["Todas", *CATEGORIAS_INFO.keys()]:
            ativo = nome_c == self.f_categoria
            btn_c = ctk.CTkButton(
                chips_frame,
                text=nome_c,
                height=34,
                corner_radius=8,
                fg_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BG,
                text_color="#FFFFFF" if ativo else BTN_SECONDARY_TEXT,
                border_width=1,
                border_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BORDER,
                hover_color=PRIMARY_HOVER if ativo else BTN_SECONDARY_HOVER,
                font=fonte(12, "bold"),
                command=lambda n=nome_c: self._selecionar_categoria_chip(n),
            )
            btn_c.pack(side="left", padx=(0, 8))
            self.chips_botoes[nome_c] = btn_c

        # Barra Secundária de Filtros (Preço, Bairro e Contador)
        barra_filtros = ctk.CTkFrame(inner, fg_color=PANEL_SUBTLE, corner_radius=12, border_width=1, border_color=LINE)
        barra_filtros.pack(fill="x", pady=(0, 18))

        bf_inner = ctk.CTkFrame(barra_filtros, fg_color="transparent")
        bf_inner.pack(fill="both", expand=True, padx=16, pady=10)

        # Filtro de Preço
        ctk.CTkLabel(bf_inner, text="Preço:", font=fonte(12, "bold"), text_color=TEXT_MUTED).pack(side="left", padx=(0, 8))
        self.seg_preco = ctk.CTkSegmentedButton(
            bf_inner,
            values=["Qualquer", "$ Econômico", "$$ Médio", "$$$ Alto"],
            height=32,
            corner_radius=8,
            fg_color=PANEL,
            selected_color=PRIMARY_BTN,
            selected_hover_color=PRIMARY_HOVER,
            unselected_color=PANEL,
            unselected_hover_color=PANEL_SUBTLE,
            text_color=TEXT,
            font=fonte(11, "bold"),
            command=self._filtrar_preco,
        )
        self.seg_preco.set(self.f_preco)
        self.seg_preco.pack(side="left", padx=(0, 16))

        # Filtro de Bairros
        bairros = ["Todos os Bairros", "Cidade Velha", "Campina", "Nazaré", "Região insular"]
        self.menu_bairro = ctk.CTkOptionMenu(
            bf_inner,
            values=bairros,
            height=32,
            corner_radius=8,
            fg_color=PANEL,
            button_color=PANEL_SUBTLE,
            button_hover_color=LINE,
            text_color=TEXT,
            font=fonte(12),
            command=self._filtrar_bairro,
        )
        self.menu_bairro.set(self.f_bairro)
        self.menu_bairro.pack(side="left")

        # Indicador de Resultados
        self.lbl_contagem = ctk.CTkLabel(bf_inner, text="", font=fonte(12), text_color=TEXT_MUTED)
        self.lbl_contagem.pack(side="right")

        # Container onde são inseridos os cards ou o mapa
        self.container_cards = ctk.CTkFrame(inner, fg_color="transparent")
        self.container_cards.pack(fill="both", expand=True)

        self.entry_busca.bind("<KeyRelease>", lambda _e: self._renderizar_catalogo())
        self._renderizar_catalogo()

    def _limpar_campo_busca(self):
        self.entry_busca.delete(0, "end")
        self.f_texto = ""
        self._renderizar_catalogo()

    def _selecionar_categoria_chip(self, nome_c: str):
        self.f_categoria = nome_c
        for n, btn in self.chips_botoes.items():
            ativo = n == nome_c
            btn.configure(
                fg_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BG,
                text_color="#FFFFFF" if ativo else BTN_SECONDARY_TEXT,
                border_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BORDER,
            )
        self._renderizar_catalogo()

    def _filtrar_preco(self, valor: str):
        self.f_preco = valor
        self._renderizar_catalogo()

    def _filtrar_bairro(self, valor: str):
        self.f_bairro = valor
        self._renderizar_catalogo()

    def _renderizar_catalogo(self):
        for w in self.container_cards.winfo_children():
            w.destroy()

        self.f_texto = self.entry_busca.get().strip()

        # Normalizar filtro de preço para o service
        mapa_preco_filtro = {
            "Qualquer": "Qualquer",
            "$ Econômico": "Baixo",
            "$$ Médio": "Médio",
            "$$$ Alto": "Alto",
        }
        preco_norm = mapa_preco_filtro.get(self.f_preco, "Qualquer")

        encontrados = buscar_locais(self.locais, self.f_texto, self.f_categoria, preco_norm)

        # Filtro adicional de Bairro
        if self.f_bairro != "Todos os Bairros":
            encontrados = [l for l in encontrados if l.get("bairro", "").casefold() == self.f_bairro.casefold()]

        self.lbl_contagem.configure(text=f"Mostrando {len(encontrados)} de {len(self.locais)} locais")

        if not encontrados:
            self._criar_estado_vazio(self.container_cards)
            return

        # Renderizar Grade de Cards em 3 Colunas
        grid = ctk.CTkFrame(self.container_cards, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="grid_locais")

        for idx, local in enumerate(encontrados):
            row = idx // 3
            col = idx % 3
            self._criar_card_catalogo(grid, local, row, col)

    def _criar_card_catalogo(self, master, local: Dict[str, Any], row: int, col: int):
        meta = METADADOS_LOCAIS.get(local.get("id", ""), {})
        card = ctk.CTkFrame(master, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE, cursor="hand2")
        card.grid(row=row, column=col, padx=6, pady=8, sticky="nsew")

        # Imagem uniforme 16:9 ocupando toda a largura útil sem sobras
        img_ctk = obter_imagem_processada(local.get("id", ""), 360, 202, raio=12, apenas_topo=True)
        lbl_img = ctk.CTkLabel(card, text="", image=img_ctk)
        lbl_img.pack(side="top", fill="x", padx=0, pady=0)

        corpo = ctk.CTkFrame(card, fg_color="transparent")
        corpo.pack(side="top", fill="both", expand=True, padx=16, pady=14)

        # Linha de Badges (Categoria + Avaliação)
        meta_row = ctk.CTkFrame(corpo, fg_color="transparent")
        meta_row.pack(fill="x", pady=(2, 6))

        tag_cat = ctk.CTkFrame(meta_row, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
        tag_cat.pack(side="left", padx=(0, 6))
        ctk.CTkLabel(
            tag_cat,
            text=meta.get("destaque_tag", local.get("categoria", ["Turismo"])[0]),
            font=fonte(10, "bold"),
            text_color=TAG_TEXT,
            padx=8,
            pady=2,
        ).pack()

        ctk.CTkLabel(
            meta_row,
            text=f"★ {meta.get('rating', 4.8)}",
            font=fonte(11, "bold"),
            text_color=AMBER,
        ).pack(side="right")

        ctk.CTkLabel(corpo, text=local["nome"], font=fonte(16, "bold"), text_color=TEXT_TITLE).pack(anchor="w")

        dist = meta.get("distancia", "1,4 km")
        dur = local.get("duracao", "2h")
        bairro = local.get("bairro", "Belém")
        preco = meta.get("preco_tag", rotulo_preco(local.get("preco")))
        ctk.CTkLabel(
            corpo,
            text=f"📍 {bairro} • {dist} • {dur}   |   {preco}",
            font=fonte(12),
            text_color=TEXT_BRAND,
        ).pack(anchor="w", pady=(2, 6))

        desc = local.get("descricao", "")
        if len(desc) > 95:
            desc = desc[:92] + "..."
        ctk.CTkLabel(
            corpo,
            text=desc,
            font=fonte(12),
            text_color=TEXT_MUTED,
            justify="left",
            wraplength=310,
        ).pack(anchor="w", pady=(0, 10))

        # Ações fixas na base do card
        botoes = ctk.CTkFrame(corpo, fg_color="transparent")
        botoes.pack(side="bottom", fill="x")

        presente = self._no_roteiro(local)
        btn_it = ctk.CTkButton(
            botoes,
            text="✓ No Roteiro" if presente else "+ Roteiro",
            height=36,
            corner_radius=8,
            fg_color=TERTIARY_CONTAINER if presente else PRIMARY_BTN,
            hover_color=TERTIARY if presente else PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(12, "bold"),
        )
        btn_it.configure(command=lambda l=local, b=btn_it: self.alternar_roteiro_btn(l, b))
        btn_it.pack(side="left", fill="x", expand=True, padx=(0, 6))

        ctk.CTkButton(
            botoes,
            text="Detalhes",
            height=36,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            hover_color=BTN_SECONDARY_HOVER,
            text_color=BTN_SECONDARY_TEXT,
            font=fonte(12, "bold"),
            command=lambda l=local: self.mostrar_detalhes(l, voltar=self.mostrar_explorar),
        ).pack(side="right")

        for w in (card, lbl_img, corpo):
            w.bind("<Button-1>", lambda _e, l=local: self.mostrar_detalhes(l, voltar=self.mostrar_explorar))

    def _criar_estado_vazio(self, master):
        vazio = ctk.CTkFrame(master, fg_color="transparent")
        vazio.pack(pady=60)
        ctk.CTkLabel(vazio, text="🔎", font=fonte(42)).pack(pady=(0, 6))
        ctk.CTkLabel(vazio, text="Nenhum local encontrado", font=fonte(18, "bold"), text_color=TEXT_TITLE).pack(pady=(0, 4))
        ctk.CTkLabel(
            vazio,
            text="Tente outro termo na busca ou remova algum filtro de categoria/bairro.",
            font=fonte(13),
            text_color=TEXT_MUTED,
        ).pack()
        ctk.CTkButton(
            vazio,
            text="Limpar Filtros",
            height=36,
            corner_radius=8,
            fg_color=PRIMARY_BTN,
            hover_color=PRIMARY_HOVER,
            text_color="#FFFFFF",
            command=self._resetar_filtros,
        ).pack(pady=(16, 0))

    def _resetar_filtros(self):
        self.entry_busca.delete(0, "end")
        self.f_texto = ""
        self.f_categoria = "Todas"
        self.f_preco = "Qualquer"
        self.f_bairro = "Todos os Bairros"
        self.seg_preco.set("Qualquer")
        self.menu_bairro.set("Todos os Bairros")
        self._selecionar_categoria_chip("Todas")

    # ==================================================================
    # 4. Tela Detalhes da Atração (Bento Showcase, Informações Práticas, etc.)
    # ==================================================================
    def mostrar_detalhes(self, local: Dict[str, Any], voltar=None):
        voltar = voltar or self.mostrar_explorar
        self._limpar_conteudo()
        meta = METADADOS_LOCAIS.get(local.get("id", ""), {})

        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(rolagem, fg_color="transparent")
        inner.pack(fill="x", padx=32, pady=(16, 40))

        # 1. Breadcrumb & Top Bar de Ações
        top_bar = ctk.CTkFrame(inner, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 14))

        # Breadcrumbs
        bc_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        bc_frame.pack(side="left")

        ctk.CTkButton(
            bc_frame,
            text="‹ Voltar",
            width=76,
            height=32,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            font=fonte(12, "bold"),
            command=voltar,
        ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            bc_frame,
            text=f"Início  /  Explorar  /  {local.get('bairro', 'Belém')}  /  ",
            font=fonte(12),
            text_color=TEXT_MUTED,
        ).pack(side="left")
        ctk.CTkLabel(bc_frame, text=local["nome"], font=fonte(12, "bold"), text_color=TEXT_TITLE).pack(side="left")

        # Ações do Topo: Compartilhar & Salvar
        acoes_topo = ctk.CTkFrame(top_bar, fg_color="transparent")
        acoes_topo.pack(side="right")

        ctk.CTkButton(
            acoes_topo,
            text="Compartilhar",
            height=32,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            font=fonte(12),
            command=lambda: self._toast("Link copiado para a área de transferência!"),
        ).pack(side="left", padx=(0, 8))

        presente = self._no_roteiro(local)
        btn_fav = ctk.CTkButton(
            acoes_topo,
            text="✓ Salvo no Roteiro" if presente else "Salvar nos Favoritos",
            height=32,
            corner_radius=8,
            fg_color=TERTIARY_FIXED if presente else BTN_SECONDARY_BG,
            text_color=TERTIARY_CONTAINER if presente else BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            font=fonte(12, "bold"),
        )
        btn_fav.configure(command=lambda l=local, b=btn_fav: self.alternar_roteiro_btn(l, b))
        btn_fav.pack(side="left")

        # 2. Bento Visual Gallery (Showcase com foto em destaque + secundárias)
        galeria = ctk.CTkFrame(inner, fg_color="transparent")
        galeria.pack(fill="x", pady=(0, 18))
        galeria.grid_columnconfigure(0, weight=7, uniform="gal")
        galeria.grid_columnconfigure(1, weight=4, uniform="gal")

        # Foto Principal Grande (8 Colunas)
        img_principal = obter_imagem_processada(local.get("id", ""), 680, 360, raio=12)
        lbl_p = ctk.CTkLabel(galeria, text="", image=img_principal)
        lbl_p.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        # Grid Secundário Lateral (4 Colunas)
        sec_box = ctk.CTkFrame(galeria, fg_color="transparent")
        sec_box.grid(row=0, column=1, sticky="nsew")

        id_sec_1 = "feliz-lusitania-2" if local.get("id") == "feliz-lusitania" else "estacao-das-docas"
        img_sec_1 = obter_imagem_processada(id_sec_1, 380, 172, raio=12)
        lbl_s1 = ctk.CTkLabel(sec_box, text="", image=img_sec_1)
        lbl_s1.pack(fill="x", pady=(0, 8))

        id_sec_2 = "feliz-lusitania-3" if local.get("id") == "feliz-lusitania" else "ver-o-peso"
        img_sec_2 = obter_imagem_processada(id_sec_2, 380, 172, raio=12)
        lbl_s2 = ctk.CTkLabel(sec_box, text="", image=img_sec_2)
        lbl_s2.pack(fill="x")

        # 3. Cabeçalho de Título e Tags
        cab_detalhes = ctk.CTkFrame(inner, fg_color="transparent")
        cab_detalhes.pack(fill="x", pady=(4, 16))

        tags_line = ctk.CTkFrame(cab_detalhes, fg_color="transparent")
        tags_line.pack(anchor="w", pady=(0, 6))

        # Tag Categoria
        tag1 = ctk.CTkFrame(tags_line, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
        tag1.pack(side="left", padx=(0, 6))
        ctk.CTkLabel(
            tag1,
            text=meta.get("destaque_tag", "Marco de Belém"),
            font=fonte(11, "bold"),
            text_color=TAG_TEXT,
            padx=10,
            pady=3,
        ).pack()

        # Tag Avaliação
        tag2 = ctk.CTkFrame(tags_line, fg_color=PANEL_SUBTLE, corner_radius=6, border_width=1, border_color=LINE)
        tag2.pack(side="left", padx=(0, 6))
        ctk.CTkLabel(
            tag2,
            text=f"★ {meta.get('rating', 4.9)} ({meta.get('avaliacoes', '1.8k')} avaliações)",
            font=fonte(11, "bold"),
            text_color=AMBER,
            padx=10,
            pady=3,
        ).pack()

        ctk.CTkLabel(cab_detalhes, text=local["nome"], font=fonte(28, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(
            cab_detalhes,
            text=f"📍 {local.get('endereco', 'Belém, Pará')}",
            font=fonte(13),
            text_color=TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 6))

        # 4. Grid de Conteúdo Principal (Esquerda 65% / Direita 35%)
        grid_conteudo = ctk.CTkFrame(inner, fg_color="transparent")
        grid_conteudo.pack(fill="x")
        grid_conteudo.grid_columnconfigure(0, weight=65, uniform="detalhes_cols")
        grid_conteudo.grid_columnconfigure(1, weight=35, uniform="detalhes_cols")

        # === COLUNA ESQUERDA ===
        col_esq = ctk.CTkFrame(grid_conteudo, fg_color="transparent")
        col_esq.grid(row=0, column=0, padx=(0, 16), sticky="nsew")

        # Bloco "Sobre o Lugar"
        bloco_sobre = ctk.CTkFrame(col_esq, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        bloco_sobre.pack(fill="x", pady=(0, 16))

        bs_inner = ctk.CTkFrame(bloco_sobre, fg_color="transparent")
        bs_inner.pack(fill="both", expand=True, padx=22, pady=18)

        ctk.CTkLabel(bs_inner, text="Sobre o Marco Histórico", font=fonte(18, "bold"), text_color=TEXT_TITLE).pack(
            anchor="w", pady=(0, 8)
        )
        ctk.CTkLabel(
            bs_inner,
            text=local["descricao"],
            font=fonte(13),
            text_color=TEXT,
            justify="left",
            wraplength=640,
        ).pack(anchor="w", pady=(0, 8))

        ctk.CTkLabel(
            bs_inner,
            text=f"Importância e Memória: {local.get('por_que_visitar', 'Uma experiência essencial para quem deseja compreender as raízes amazônicas.')}",
            font=fonte(13),
            text_color=TEXT_MUTED,
            justify="left",
            wraplength=640,
        ).pack(anchor="w")

        # Bloco "Destaques & Por Que Visitar" (4 Cards Bento)
        ctk.CTkLabel(col_esq, text="Destaques & Por Que Visitar", font=fonte(18, "bold"), text_color=TEXT_TITLE).pack(
            anchor="w", pady=(6, 10)
        )

        grid_destaques_detalhe = ctk.CTkFrame(col_esq, fg_color="transparent")
        grid_destaques_detalhe.pack(fill="x", pady=(0, 16))
        grid_destaques_detalhe.grid_columnconfigure((0, 1), weight=1, uniform="pq_visitar")

        itens_pq = [
            ("🌅", "Mirante 360° da Baía", "Panorama deslumbrante das embarcações ribeirinhas e o pôr do sol amazônico."),
            ("🏺", "Acervo e Memória Viva", "Cerâmicas marajoaras e vestígios de mais de 2.000 anos preservados."),
            ("🛡️", "Artilharia e Muralhas", "Baterias de canhões históricos voltados para a entrada do estuário."),
            ("🍲", "Cultura & Sabores", "Restaurantes e docas contíguas com o melhor da gastronomia local."),
        ]

        for i, (ic, tit, desc) in enumerate(itens_pq):
            c_pq = ctk.CTkFrame(grid_destaques_detalhe, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
            c_pq.grid(row=i // 2, column=i % 2, padx=4, pady=4, sticky="nsew")

            cpq_inner = ctk.CTkFrame(c_pq, fg_color="transparent")
            cpq_inner.pack(fill="both", expand=True, padx=14, pady=12)

            topo_pq = ctk.CTkFrame(cpq_inner, fg_color="transparent")
            topo_pq.pack(fill="x")
            ctk.CTkLabel(topo_pq, text=ic, font=fonte(16)).pack(side="left", padx=(0, 6))
            ctk.CTkLabel(topo_pq, text=tit, font=fonte(13, "bold"), text_color=TEXT_TITLE).pack(side="left")

            ctk.CTkLabel(cpq_inner, text=desc, font=fonte(12), text_color=TEXT_MUTED, justify="left", wraplength=280).pack(
                anchor="w", pady=(4, 0)
            )

        # === COLUNA DIREITA (Sticky Planning & Booking Card) ===
        col_dir = ctk.CTkFrame(grid_conteudo, fg_color="transparent")
        col_dir.grid(row=0, column=1, sticky="nsew")

        card_planejamento = ctk.CTkFrame(col_dir, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        card_planejamento.pack(fill="x", pady=(0, 16))

        cp_inner = ctk.CTkFrame(card_planejamento, fg_color="transparent")
        cp_inner.pack(fill="both", expand=True, padx=22, pady=20)

        # Preço & Acesso
        cp_topo = ctk.CTkFrame(cp_inner, fg_color="transparent")
        cp_topo.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(cp_topo, text="INGRESSO CIRCUITO", font=fonte(10, "bold"), text_color=TEXT_MUTED).pack(anchor="w")
        preco_val = meta.get("preco_tag", rotulo_preco(local.get("preco")))
        ctk.CTkLabel(cp_topo, text=preco_val, font=fonte(22, "bold"), text_color=TEXT_TITLE).pack(anchor="w")

        # Status Aberto Agora
        status_box = ctk.CTkFrame(cp_inner, fg_color=TERTIARY_FIXED, corner_radius=8)
        status_box.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(
            status_box,
            text=f"● Aberto Agora  •  {meta.get('horario', '09h às 18h')}",
            font=fonte(11, "bold"),
            text_color=TERTIARY_CONTAINER,
            padx=12,
            pady=6,
        ).pack()

        # Previsão Climática para a Visita
        clima_box = ctk.CTkFrame(cp_inner, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        clima_box.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(
            clima_box,
            text="🌧️ Previsão: Chuva rápida às 16h; fim de tarde com brisa fresca (29°C)",
            font=fonte(11),
            text_color=TEXT_TITLE,
            padx=12,
            pady=8,
            wraplength=280,
            justify="left",
        ).pack(anchor="w")

        # Botão de Ação Primário
        presente = self._no_roteiro(local)
        self.btn_acao_detalhe = ctk.CTkButton(
            cp_inner,
            text="✓ Salvo no Meu Roteiro" if presente else "+ Adicionar ao Meu Roteiro",
            height=44,
            corner_radius=8,
            fg_color=TERTIARY_CONTAINER if presente else PRIMARY_BTN,
            hover_color=TERTIARY if presente else PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(14, "bold"),
        )
        self.btn_acao_detalhe.configure(
            command=lambda l=local: self.alternar_roteiro_btn(l, self.btn_acao_detalhe)
        )
        self.btn_acao_detalhe.pack(fill="x", pady=(0, 10))

        # Abrir no Google Maps
        ctk.CTkButton(
            cp_inner,
            text="🗺️ Abrir Rota no Google Maps",
            height=38,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            hover_color=BTN_SECONDARY_HOVER,
            text_color=BTN_SECONDARY_TEXT,
            font=fonte(12, "bold"),
            command=lambda: webbrowser.open(f"https://maps.google.com/?q={local['nome']}+Belem"),
        ).pack(fill="x", pady=(0, 14))

        # Informações Práticas Rápidas
        ctk.CTkFrame(cp_inner, height=1, fg_color=LINE).pack(fill="x", pady=(0, 12))

        praticas = [
            ("⏱️", f"Tempo sugerido: {local.get('duracao', '1h30 a 2h')}"),
            ("❄️", "Ambientes com ar condicionado"),
            ("📷", "Permitido fotos (sem flash no acervo)"),
            ("♿", "Rampas e acessibilidade total"),
        ]
        for ic, txt in praticas:
            r = ctk.CTkFrame(cp_inner, fg_color="transparent")
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=ic, font=fonte(12)).pack(side="left", padx=(0, 6))
            ctk.CTkLabel(r, text=txt, font=fonte(11), text_color=TEXT_MUTED).pack(side="left")

    # ==================================================================
    # 5. Tela Meu Roteiro (Timeline Otimizada por IA, Métricas e Mapa)
    # ==================================================================
    def mostrar_roteiro(self):
        self._limpar_conteudo()
        self._marcar_aba_ativa("Meu Roteiro")

        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(rolagem, fg_color="transparent")
        inner.pack(fill="x", padx=32, pady=(20, 40))

        # 1. Top Bar de Métricas e Ações
        topo_roteiro = ctk.CTkFrame(inner, fg_color="transparent")
        topo_roteiro.pack(fill="x", pady=(0, 16))

        esq_r = ctk.CTkFrame(topo_roteiro, fg_color="transparent")
        esq_r.pack(side="left")

        tag_r = ctk.CTkFrame(esq_r, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
        tag_r.pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(tag_r, text="ROTEIRO INTELIGENTE • PARÁ", font=fonte(10, "bold"), text_color=TAG_TEXT, padx=8, pady=2).pack()

        ctk.CTkLabel(esq_r, text="O Melhor de Belém Histórica & Baía", font=fonte(28, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(
            esq_r,
            text="Percurso com o aroma das ervas do Ver-o-Peso, a imponência barroca de 1616 e o entardecer nas Docas.",
            font=fonte(13),
            text_color=TEXT_MUTED,
        ).pack(anchor="w")

        # Botões de Ação do Roteiro
        acoes_r = ctk.CTkFrame(topo_roteiro, fg_color="transparent")
        acoes_r.pack(side="right", pady=8)

        ctk.CTkButton(
            acoes_r,
            text="✨ Otimizar Ordem (IA)",
            height=38,
            corner_radius=8,
            fg_color=PRIMARY_BTN,
            hover_color=PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(12, "bold"),
            command=self._otimizar_roteiro_ia,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            acoes_r,
            text="💾 Salvar",
            height=38,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            hover_color=BTN_SECONDARY_HOVER,
            text_color=BTN_SECONDARY_TEXT,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            font=fonte(12, "bold"),
            command=self._confirmar_salvamento_banco,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            acoes_r,
            text="Limpar",
            height=38,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            hover_color="#F8D7DA",
            text_color=ERROR,
            font=fonte(12, "bold"),
            command=self._confirmar_limpar_roteiro,
        ).pack(side="left")

        # 2. Métricas Rápidas do Roteiro (KPIs)
        strip_metricas = ctk.CTkFrame(inner, fg_color="transparent")
        strip_metricas.pack(fill="x", pady=(0, 20))
        strip_metricas.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="met_r")

        total_paradas = len(self.roteiro)
        if total_paradas == 0:
            metricas = [
                ("⏱️", "Duração Total", "0h"),
                ("📍", "Paradas Salvas", "0 locais"),
                ("💰", "Estimativa de Gasto", "R$ 0"),
                ("🚶", "Distância a Pé", "0 km"),
            ]
        else:
            metricas = [
                ("⏱️", "Duração Total", f"~{total_paradas * 2}h com pausas"),
                ("📍", "Paradas Salvas", f"{total_paradas} locais programados"),
                ("💰", "Estimativa de Gasto", f"R$ {total_paradas * 15} / pessoa"),
                ("🚶", "Distância a Pé", f"{total_paradas * 0.8:.1f} km a pé"),
            ]

        for i, (ic, tit, val) in enumerate(metricas):
            c_m = ctk.CTkFrame(strip_metricas, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
            c_m.grid(row=0, column=i, padx=5, sticky="nsew")

            cm_in = ctk.CTkFrame(c_m, fg_color="transparent")
            cm_in.pack(fill="both", expand=True, padx=14, pady=12)

            t = ctk.CTkFrame(cm_in, fg_color="transparent")
            t.pack(fill="x")
            ctk.CTkLabel(t, text=ic, font=fonte(16)).pack(side="left", padx=(0, 6))
            ctk.CTkLabel(t, text=tit, font=fonte(11, "bold"), text_color=TEXT_MUTED).pack(side="left")

            ctk.CTkLabel(cm_in, text=val, font=fonte(15, "bold"), text_color=TEXT_KPI).pack(anchor="w", pady=(4, 0))

        # 3. Estado Vazio (100% de largura alinhado aos KPIs) ou Timeline
        if not self.roteiro:
            self._criar_roteiro_vazio(inner)
            return

        # Layout de 2 Colunas (Timeline à Esquerda / Deck de Apoio à Direita)
        grid_rot = ctk.CTkFrame(inner, fg_color="transparent")
        grid_rot.pack(fill="both", expand=True)
        grid_rot.grid_columnconfigure(0, weight=65, uniform="rot_cols")
        grid_rot.grid_columnconfigure(1, weight=35, uniform="rot_cols")

        # === ESQUERDA: Timeline de Paradas ===
        col_timeline = ctk.CTkFrame(grid_rot, fg_color="transparent")
        col_timeline.grid(row=0, column=0, padx=(0, 16), sticky="nsew")

        # Turno da Manhã Header
        self._criar_divisor_periodo(col_timeline, "🌅 Turno da Manhã (08h00 às 12h30)", "Coração Histórico e Gastronômico")

        paradas_manha = self.roteiro[:2]
        for idx, local in enumerate(paradas_manha, start=1):
            self._criar_card_timeline_parada(col_timeline, local, idx, horario="08:00 – 10:30" if idx == 1 else "10:45 – 12:30")
            if idx == 1:
                self._criar_conector_deslocamento(col_timeline, "🚶 Caminhada leve de 6 min (450m) via Boulevard Castilhos França")

        # Pausa para Almoço Sugerida
        self._criar_card_almoco(col_timeline)

        # Turno da Tarde Header
        self._criar_divisor_periodo(col_timeline, "☀️ Turno da Tarde (14h30 às 19h30)", "Arquitetura da Borracha e Pôr do Sol")

        # Conector Carro
        self._criar_conector_deslocamento(col_timeline, "🚗 Deslocamento de 8 min (2.1 km) para evitar o calor do meio-dia")

        paradas_tarde = self.roteiro[2:]
        for idx, local in enumerate(paradas_tarde, start=3):
            self._criar_card_timeline_parada(col_timeline, local, idx, horario="14:30 – 16:15" if idx == 3 else "16:30 – 19:30")
            if idx == 3:
                self._criar_conector_deslocamento(col_timeline, "🚶 Caminhada arborizada de 12 min após a chuva refrescar o ar")

        # === DIREITA: Deck de Planejamento, Clima e Checklist ===
        col_planejamento = ctk.CTkFrame(grid_rot, fg_color="transparent")
        col_planejamento.grid(row=0, column=1, sticky="nsew")

        # Mini Mapa Vetorial da Rota
        mapa_box = ctk.CTkFrame(col_planejamento, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        mapa_box.pack(fill="x", pady=(0, 16))

        mb_in = ctk.CTkFrame(mapa_box, fg_color="transparent")
        mb_in.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(mb_in, text="Traçado da Rota (Dia 1)", font=fonte(15, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(mb_in, text="4 Paradas conectadas na Baía do Guajará", font=fonte(12), text_color=TEXT_MUTED).pack(anchor="w", pady=(0, 10))

        img_map_route = obter_imagem_processada("feliz-lusitania", 340, 170, raio=12)
        ctk.CTkLabel(mb_in, text="", image=img_map_route).pack(fill="x", pady=(0, 10))

        ctk.CTkButton(
            mb_in,
            text="Abrir Trajeto no Google Maps ↗",
            height=36,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            hover_color=BTN_SECONDARY_HOVER,
            text_color=BTN_SECONDARY_TEXT,
            font=fonte(12, "bold"),
            command=lambda: webbrowser.open("https://maps.google.com/?q=Mercado+Ver-o-Peso+Belem"),
        ).pack(fill="x")

        # Checklist "O que levar no dia"
        card_check = ctk.CTkFrame(col_planejamento, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        card_check.pack(fill="x", pady=(0, 16))

        cc_in = ctk.CTkFrame(card_check, fg_color="transparent")
        cc_in.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(cc_in, text="O que levar no dia", font=fonte(15, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(cc_in, text="Itens essenciais para o clima equatorial", font=fonte(12), text_color=TEXT_MUTED).pack(anchor="w", pady=(0, 10))

        itens_mochila = [
            ("Guarda-chuva compacto ou capa", True),
            ("Dinheiro em espécie (trocado para feirantes)", True),
            ("Calçado leve e antiderrapante (paralelepípedo úmido)", True),
            ("Garrafa d'água reutilizável (hidratação)", False),
        ]
        for txt, marcado in itens_mochila:
            chk = ctk.CTkCheckBox(
                cc_in,
                text=txt,
                font=fonte(12),
                text_color=TEXT,
                fg_color=PRIMARY_BTN,
                hover_color=PRIMARY_HOVER,
                corner_radius=4,
            )
            if marcado:
                chk.select()
            chk.pack(anchor="w", pady=4)

        # Atalhos de Adição Rápida
        card_quick = ctk.CTkFrame(col_planejamento, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        card_quick.pack(fill="x")

        cq_in = ctk.CTkFrame(card_quick, fg_color="transparent")
        cq_in.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(cq_in, text="Adicionar Paradas Sugeridas", font=fonte(14, "bold"), text_color=TEXT_TITLE).pack(anchor="w", pady=(0, 8))

        sugestoes = [
            ("mangal", "+ Mangal das Garças (Parque)"),
            ("basilica-nazare", "+ Basílica de Nazaré"),
            ("ilha-combu", "+ Ilha do Combu (Chocolates)"),
        ]
        for sid, stxt in sugestoes:
            loc_sug = next((l for l in self.locais if l.get("id") == sid), None)
            if loc_sug and not self._no_roteiro(loc_sug):
                ctk.CTkButton(
                    cq_in,
                    text=stxt,
                    height=32,
                    corner_radius=8,
                    fg_color=BTN_SECONDARY_BG,
                    border_width=1,
                    border_color=BTN_SECONDARY_BORDER,
                    hover_color=BTN_SECONDARY_HOVER,
                    text_color=BTN_SECONDARY_TEXT,
                    font=fonte(11, "bold"),
                    command=lambda ls=loc_sug: self._adicionar_sugestao_rapida(ls),
                ).pack(fill="x", pady=3)

    def _criar_divisor_periodo(self, master, titulo: str, subtitulo: str):
        divisor = ctk.CTkFrame(master, fg_color="transparent")
        divisor.pack(fill="x", pady=(12, 8))
        ctk.CTkLabel(divisor, text=titulo, font=fonte(16, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(divisor, text=subtitulo, font=fonte(12), text_color=TEXT_MUTED).pack(anchor="w")

    def _criar_conector_deslocamento(self, master, texto: str):
        c = ctk.CTkFrame(master, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        c.pack(fill="x", padx=16, pady=6)
        ctk.CTkLabel(c, text=f"  {texto}  ", font=fonte(11, "bold"), text_color=TEXT_BRAND, pady=6).pack()

    def _criar_card_almoco(self, master):
        card = ctk.CTkFrame(master, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        card.pack(fill="x", pady=10)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=18, pady=14)

        tag = ctk.CTkFrame(inner, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
        tag.pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(tag, text="PAUSA DE ALMOÇO SUGERIDA • 12:30 - 14:00", font=fonte(10, "bold"), text_color=TAG_TEXT, padx=8, pady=2).pack()

        ctk.CTkLabel(inner, text="Casa das Onze Janelas ou Box do Peixe Frito com Açaí", font=fonte(15, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(
            inner,
            text="Opte por almoçar com vista para a baía (pratos contemporâneos de filhote e tucupi) ou no autêntico box da feira.",
            font=fonte(12),
            text_color=TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 0))

    def _criar_card_timeline_parada(self, master, local: Dict[str, Any], indice: int, horario: str):
        meta = METADADOS_LOCAIS.get(local.get("id", ""), {})
        card = ctk.CTkFrame(master, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        card.pack(fill="x", pady=6)

        c_in = ctk.CTkFrame(card, fg_color="transparent")
        c_in.pack(fill="both", expand=True, padx=16, pady=14)

        # Indicador numérico
        num = ctk.CTkFrame(c_in, width=32, height=32, corner_radius=8, fg_color=PRIMARY_BTN)
        num.pack(side="left", padx=(0, 12))
        num.pack_propagate(False)
        ctk.CTkLabel(num, text=str(indice), font=fonte(13, "bold"), text_color="#FFFFFF").pack(expand=True)

        # Foto Miniatura
        img_thumb = obter_imagem_processada(local.get("id", ""), 120, 80, raio=8)
        lbl_thumb = ctk.CTkLabel(c_in, text="", image=img_thumb)
        lbl_thumb.pack(side="left", padx=(0, 14))

        # Informações da Parada
        info = ctk.CTkFrame(c_in, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(info, text=f"{local['nome']}  •  {horario}", font=fonte(15, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(info, text=f"📍 {local['bairro']}  •  {local.get('duracao', '2h')}", font=fonte(12), text_color=TEXT_MUTED).pack(anchor="w")
        ctk.CTkLabel(info, text=local["descricao"], font=fonte(12), text_color=TEXT, wraplength=380, justify="left").pack(anchor="w", pady=(2, 0))

        # Ações na Linha da Parada
        acoes = ctk.CTkFrame(c_in, fg_color="transparent")
        acoes.pack(side="right")

        ctk.CTkButton(
            acoes,
            text="Ver Guia",
            height=32,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            hover_color=BTN_SECONDARY_HOVER,
            text_color=BTN_SECONDARY_TEXT,
            font=fonte(11, "bold"),
            command=lambda l=local: self.mostrar_detalhes(l, voltar=self.mostrar_roteiro),
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            acoes,
            text="✕",
            width=32,
            height=32,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            hover_color="#FEE2E2",
            text_color=ERROR,
            font=fonte(12, "bold"),
            command=lambda lid=local["id"]: self._remover_item_roteiro(lid),
        ).pack(side="left")

    def _adicionar_sugestao_rapida(self, local: Dict[str, Any]):
        self.roteiro = adicionar(self.roteiro, local, usuario_id=self.usuario_id)
        self.mostrar_roteiro()
        self._toast(f"✓ {local['nome']} adicionado ao roteiro!")

    def _remover_item_roteiro(self, local_id: str):
        self.roteiro = remover(self.roteiro, local_id, usuario_id=self.usuario_id)
        self.mostrar_roteiro()
        self._toast("Local removido do roteiro")

    def _otimizar_roteiro_ia(self):
        """Reordena o roteiro em fluxo geográfico e cronológico ideal."""
        ordem_ideal = ["ver-o-peso", "feliz-lusitania", "teatro-da-paz", "estacao-das-docas", "mangal", "basilica-nazare", "ilha-combu"]
        self.roteiro.sort(key=lambda x: ordem_ideal.index(x.get("id")) if x.get("id") in ordem_ideal else 99)
        salvar_roteiro(self.roteiro)
        self.mostrar_roteiro()
        self._toast("✨ Ordem ideal recalculada e sincronizada com o clima!", cor_bg=TERTIARY_CONTAINER)

    def _confirmar_salvamento_banco(self):
        salvar_roteiro(self.roteiro)
        self._toast(f"💾 Roteiro com {len(self.roteiro)} locais salvo com sucesso no banco SQLite!", cor_bg=TERTIARY_CONTAINER)

    def _confirmar_limpar_roteiro(self):
        self.roteiro = limpar(usuario_id=self.usuario_id)
        self.mostrar_roteiro()
        self._toast("Roteiro limpo")

    def _criar_roteiro_vazio(self, master):
        vazio = ctk.CTkFrame(master, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        vazio.pack(fill="x", pady=24)

        vi = ctk.CTkFrame(vazio, fg_color="transparent")
        vi.pack(pady=48, padx=24)

        ctk.CTkLabel(vi, text="🗺️", font=fonte(48)).pack(pady=(0, 10))
        ctk.CTkLabel(vi, text="Seu roteiro ainda está vazio", font=fonte(20, "bold"), text_color=TEXT_TITLE).pack(pady=(0, 6))
        ctk.CTkLabel(
            vi,
            text="Explore as atrações de Belém e clique em '+ Roteiro' para montar seu roteiro personalizado.",
            font=fonte(13),
            text_color=TEXT_MUTED,
            justify="center",
        ).pack(pady=(0, 20))

        ctk.CTkButton(
            vi,
            text="Explorar Locais de Belém",
            height=40,
            corner_radius=8,
            fg_color=PRIMARY_BTN,
            hover_color=PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(13, "bold"),
            command=self.mostrar_explorar,
        ).pack()

    # ==================================================================
    # 6. Tela Sobre Belém (Guia Cultural, História e Clima)
    # ==================================================================
    def mostrar_sobre_belem(self):
        self._limpar_conteudo()
        self._marcar_aba_ativa("Sobre Belém")

        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(rolagem, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=32, pady=(20, 24))

        ctk.CTkLabel(inner, text="GUIA INTELIGENTE DA CIDADE", font=fonte(11, "bold"), text_color=SECONDARY).pack(anchor="w")
        ctk.CTkLabel(inner, text="Sobre Belém do Pará", font=fonte(28, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(
            inner,
            text="A metrópole da floresta, capital da Amazônia Atlântica e Cidade Criativa da Gastronomia pela UNESCO.",
            font=fonte(13),
            text_color=TEXT_MUTED,
        ).pack(anchor="w", pady=(0, 20))

        # Cards Informativos
        grid_sobre = ctk.CTkFrame(inner, fg_color="transparent")
        grid_sobre.pack(fill="x", pady=(0, 16))
        grid_sobre.grid_columnconfigure((0, 1), weight=1, uniform="sobre_col")

        blocos_info = [
            ("🌧️ A Lendária Chuva das 16h",
             "Em Belém, os encontros costumam ser marcados 'antes ou depois da chuva'. A convecção equatorial diária gera nuvens cúmulo-nimbo que se precipitam com precisão entre 14h e 16h30, refrescando a temperatura e lavando as calçadas de mangueiras."),
            ("🍲 Gastronomia Patrimônio UNESCO",
             "Com o açaí consumido tradicionalmente com peixe frito, o tacacá fervente nas esquinas, o tucupi e o jambu que adormece os lábios, Belém possui a gastronomia mais autêntica e aromática do Brasil."),
            ("⚓ O Guajará e a Foz do Rio Guamá",
             "A água dita o ritmo da vida em Belém. Dezenas de ilhas contíguas (como o Combu, Mosqueiro e Cotijuba) oferecem refúgios de ecoturismo e praias de água doce com ondas."),
            ("🛡️ Dicas de Segurança e Locomoção",
             "A Cidade Velha, o Ver-o-Peso e as Docas contam com policiamento especializado do Batalhão Turístico (DPTUR). Prefira caminhadas durante o dia pela orla e use táxi/Uber para travessias noturnas."),
        ]

        for i, (tit, desc) in enumerate(blocos_info):
            b = ctk.CTkFrame(grid_sobre, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
            b.grid(row=i // 2, column=i % 2, padx=6, pady=6, sticky="nsew")

            bi = ctk.CTkFrame(b, fg_color="transparent")
            bi.pack(fill="both", expand=True, padx=24, pady=22)

            ctk.CTkLabel(bi, text=tit, font=fonte(16, "bold"), text_color=TEXT_TITLE).pack(anchor="w", pady=(0, 6))
            ctk.CTkLabel(bi, text=desc, font=fonte(13), text_color=TEXT_MUTED, justify="left", wraplength=480).pack(anchor="w")

        # Rodapé Institucional alinhado à base
        rodape_sb = ctk.CTkFrame(inner, fg_color=PANEL_SUBTLE, corner_radius=12, border_width=1, border_color=LINE)
        rodape_sb.pack(side="bottom", fill="x", pady=(16, 0))

        rs_in = ctk.CTkFrame(rodape_sb, fg_color="transparent")
        rs_in.pack(fill="both", expand=True, padx=24, pady=18)

        ctk.CTkLabel(rs_in, text="BelémNaMão Guia Inteligente • Versão 2.5", font=fonte(13, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(
            rs_in,
            text="Desenvolvido para conectar turistas e residentes com o rico patrimônio arquitetônico, cultural e gastronômico do Pará.",
            font=fonte(12),
            text_color=TEXT_MUTED,
        ).pack(anchor="w")

    # ==================================================================
    # 7. Helper Geral de Alternância de Roteiro
    # ==================================================================
    def alternar_roteiro_btn(self, local: Dict[str, Any], botao: Optional[ctk.CTkButton] = None):
        """Adiciona ou remove do roteiro de forma reativa com feedback no botão."""
        presente = self._no_roteiro(local)
        if presente:
            self.roteiro = remover(self.roteiro, local["id"], usuario_id=self.usuario_id)
            self._toast(f"{local['nome']} removido do roteiro")
            if botao:
                eh_fav = "Favoritos" in str(botao.cget("text"))
                botao.configure(
                    text="Salvar nos Favoritos" if eh_fav else "+ Roteiro",
                    fg_color=BTN_SECONDARY_BG if eh_fav else PRIMARY_BTN,
                    hover_color=BTN_SECONDARY_HOVER if eh_fav else PRIMARY_HOVER,
                    text_color=BTN_SECONDARY_TEXT if eh_fav else "#FFFFFF",
                )
        else:
            self.roteiro = adicionar(self.roteiro, local, usuario_id=self.usuario_id)
            self._toast(f"✓ {local['nome']} adicionado ao roteiro!", cor_bg=TERTIARY_CONTAINER)
            if botao:
                eh_fav = "Favoritos" in str(botao.cget("text"))
                botao.configure(
                    text="✓ Salvo no Roteiro",
                    fg_color=TERTIARY_FIXED if eh_fav else TERTIARY_CONTAINER,
                    hover_color=SECONDARY_FIXED if eh_fav else TERTIARY,
                    text_color=TERTIARY_CONTAINER if eh_fav else "#FFFFFF",
                )

        if hasattr(self, "btn_salvos_pill"):
            self.btn_salvos_pill.configure(text=f"🔖 {len(self.roteiro)} salvos")


if __name__ == "__main__":
    app = BelemNaMaoApp()
    app.mainloop()
