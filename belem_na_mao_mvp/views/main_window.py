"""
Visual Principal do BelémNaMão — Guia Inteligente
Design Moderno, Clean, Profissional e Atrativo baseado no Design System oficial.
Suporte completo a i18n (PT-BR, EN, ES), Modo Claro/Escuro, Ranking Dinâmico e MySQL.
"""
import webbrowser
from typing import Any, Dict, List, Optional

import customtkinter as ctk

from services.catalogo import buscar_locais, carregar_locais, rotulo_preco
from services.database import obter_top3_por_categoria_db
from services.i18n import (
    IDIOMAS_DISPONIVEIS,
    ROTULOS_IDIOMA,
    chave_preco_por_rotulo,
    get_idioma,
    lista_meses,
    set_idioma,
    t,
    traduzir_categoria,
    traduzir_categoria_desc,
    traduzir_local,
    traduzir_mes,
    traduzir_preco_filtro,
)
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
    PANEL,
    PANEL_SUBTLE,
    PRIMARY,
    PRIMARY_BTN,
    PRIMARY_CONTAINER,
    PRIMARY_HOVER,
    SECONDARY,
    SECONDARY_FIXED,
    SECONDARY_HOVER,
    SEG_SELECTED_BG,
    SUCCESS,
    TAG_BG,
    TAG_BORDER,
    TAG_TEXT,
    TERTIARY,
    TERTIARY_CONTAINER,
    TERTIARY_FIXED,
    ON_TERTIARY_FIXED,
    TEXT,
    TEXT_BRAND,
    TEXT_EXPLORAR,
    TEXT_KPI,
    TEXT_LIGHT,
    TEXT_MUTED,
    TEXT_TITLE,
    fonte,
    obter_imagem_processada,
)

# Metadados e notas editoriais em PT-BR (traduzidos dinamicamente via i18n)
METADADOS_LOCAIS: Dict[str, Dict[str, Any]] = {
    "ver-o-peso": {
        "rating": 4.8,
        "avaliacoes": "2.4k",
        "subtitulo": "A maior feira a céu aberto da América Latina • Foz do Guamá",
        "horario": "05h00 às 18h00 (Setor de peixes a partir das 03h00)",
        "melhor_horario": "Manhã cedo (07h às 09h30)",
        "preco_tag": "$ • Acessível / Entrada Gratuita",
        "destaque_tag": "Cultura & Gastronomia",
        "distancia": "0,5 km",
        "destaques_cards": [
            ("🥭", "Sabores Amazônicos", "Prove açaí fresco com peixe frito, tacacá, cupuaçu e queijos do Marajó."),
            ("🌿", "Bancas de Ervas e Cheiros", "Ervas medicinais tradicionais, banhos aromáticos e especiarias regionais."),
            ("⚓", "Mercado de Ferro (1901)", "Arquitetura histórica em ferro inglês ao lado dos barcos ribeirinhos."),
            ("📸", "Patrimônio Vivo", "Torres icônicas e feira vibrante às margens da Baía do Guajará."),
        ],
    },
    "estacao-das-docas": {
        "rating": 4.9,
        "avaliacoes": "3.1k",
        "subtitulo": "Galpões iluminados • Pôr do Sol, Bares e Vida Noturna no Guajará",
        "horario": "10h00 às 00h00 • Destaque Noturno a partir das 18h (Sex/Sáb até 01h00)",
        "melhor_horario": "Fim de tarde e Noite (17h30 às 23h30)",
        "preco_tag": "$$$ • Alto",
        "destaque_tag": "Vida Noturna & Gastronomia",
        "distancia": "0,9 km",
        "destaques_cards": [
            ("🌙", "Noite na Orla Iluminada", "Guindastes históricos iluminados, brisa da baía e música ao vivo à noite."),
            ("🍺", "Cervejaria Amazônica", "Chopes artesanais regionais com sabores como bacuri, priprioca e açaí."),
            ("🍽️", "Jantares na Baía", "Restaurantes renomados com pato no tucupi, filhote e frutos do mar."),
            ("🎶", "Anfiteatro & Lazer", "Programação cultural noturna, sorveterias regionais e passeio seguro."),
        ],
    },
    "bistro-guajara-noturno": {
        "rating": 4.9,
        "avaliacoes": "1.1k",
        "subtitulo": "Alta gastronomia amazônica noturna e coquetelaria autoral • Umarizal",
        "horario": "18h30 às 00h30 (Terça a Domingo — Exclusivo Noturno)",
        "melhor_horario": "Jantar & Música ao Vivo (20h00 às 23h00)",
        "preco_tag": "$$$ • Alto",
        "destaque_tag": "Gastronomia Noturna",
        "distancia": "2,3 km",
        "destaques_cards": [
            ("🍷", "Menu Noturno Amazônico", "Filhote na brasa, pato no tucupi, croquetes de maniçoba e sobremesas de cupuaçu."),
            ("🍸", "Bar de Jambu & Taperebá", "Carta autoral de drinques noturnos com cachaça de jambu e botânicos da floresta."),
            ("🎸", "Música Paraense ao Vivo", "Apresentações acústicas noturnas de carimbó contemporâneo e MPB amazônica."),
            ("✨", "Polo Gastronômico da Doca", "Localizado no Umarizal, coração da vida noturna gastronômica de Belém."),
        ],
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
        "destaques_cards": [
            ("🌅", "Mirante 360° da Baía", "Panorama deslumbrante das embarcações ribeirinhas e o pôr do sol amazônico."),
            ("🏺", "Acervo e Memória Viva", "Cerâmicas marajoaras e vestígios de mais de 2.000 anos preservados."),
            ("🛡️", "Artilharia e Muralhas", "Baterias de canhões históricos voltados para a entrada do estuário."),
            ("🍲", "Cultura & Sabores", "Jardins e restaurante contíguo com o melhor da gastronomia regional."),
        ],
    },
    "mangal": {
        "rating": 4.8,
        "avaliacoes": "2.7k",
        "subtitulo": "Parque ecológico com borboletário gigante, farol e guarás",
        "horario": "08h00 às 18h00 (Fecha às segundas)",
        "melhor_horario": "Alimentação dos guarás às 11h15 e 15h00",
        "preco_tag": "$$ • Parque Grátis (Espaços R$ 5)",
        "destaque_tag": "Natureza & Fauna",
        "distancia": "2,8 km",
        "destaques_cards": [
            ("🦩", "Guarás Vermelhos", "Aves amazônicas soltas entre lagos e passarelas ecológicas."),
            ("🦋", "Borboletário & Orquidário", "Um dos maiores borboletários do Norte rodeado de espécies nativas."),
            ("🗼", "Farol Mirante de 47m", "Vista panorâmica elevada do Rio Guamá e do centro histórico."),
            ("🌿", "Flora Amazônica", "Trilhas sombreadas, vitórias-régias e espelhos d'água relaxantes."),
        ],
    },
    "teatro-da-paz": {
        "rating": 4.9,
        "avaliacoes": "1.4k",
        "subtitulo": "Joia neoclássica do Ciclo da Borracha na Praça da República",
        "horario": "Visitas guiadas: Terça a Domingo de hora em hora",
        "melhor_horario": "Tarde (15h00 — climatizado durante a chuva)",
        "preco_tag": "$$ (R$ 10 inteira / R$ 5 meia)",
        "destaque_tag": "Arquitetura Imperial",
        "distancia": "1,8 km",
        "destaques_cards": [
            ("🎭", "Nobreza Neoclássica", "Escadarias em mármore de Carrara, lustres franceses e folhas de ouro."),
            ("🎶", "Acústica de Ópera", "Salão histórico em ferradura com programação sinfônica e lírica."),
            ("🎨", "Afrescos Amazônicos", "Pinturas no teto exaltando a mitologia e a natureza da Amazônia."),
            ("🏛️", "Visitas Guiadas", "Imersão na história da Belle Époque paraense do século XIX."),
        ],
    },
    "praca-republica": {
        "rating": 4.7,
        "avaliacoes": "950",
        "subtitulo": "Coração arborizado com mangueiras centenárias e feira aos domingos",
        "horario": "Acesso livre 24 horas",
        "melhor_horario": "Domingo de manhã (Feirinha de artesanato)",
        "preco_tag": "$ • Gratuito",
        "destaque_tag": "Caminhada & Lazer",
        "distancia": "1,7 km",
        "destaques_cards": [
            ("🌳", "Túnel de Mangueiras", "Sombra fresca sob árvores centenárias no coração de Belém."),
            ("🛍️", "Feirinha de Domingo", "Artesanato paraense, cerâmica marajoara e comidas típicas."),
            ("🗿", "Monumento à República", "Esculturas históricas em mármore cercadas por jardins."),
            ("☕", "Vida Urbana & Cultura", "Em frente ao Theatro da Paz e próxima a cafés tradicionais."),
        ],
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
        "destaques_cards": [
            ("🍫", "Chocolate da Floresta", "Visite produções familiares de cacau orgânico nativo do Combu."),
            ("🚤", "Travessia de 15 min", "Navegação cênica pelo Rio Guamá observando palafitas e igarapés."),
            ("🐟", "Decks sobre o Rio", "Restaurantes ribeirinhos com peixe fresco, caranguejo e açaí puro."),
            ("🌴", "Trilhas de Várzea", "Contato com samaúmas gigantes e vegetação típica da várzea amazônica."),
        ],
    },
    "basilica-nazare": {
        "rating": 4.9,
        "avaliacoes": "2.1k",
        "subtitulo": "Santuário de Nossa Senhora de Nazaré e ápice do Círio",
        "horario": "06h00 às 20h00 diariamente",
        "melhor_horario": "Início da manhã ou final da tarde",
        "preco_tag": "$ • Gratuito",
        "destaque_tag": "Fé & Tradição",
        "distancia": "3,1 km",
        "destaques_cards": [
            ("⛪", "Arquitetura Romana", "Mármores policromados, mosaicos venezianos e vitrais europeus."),
            ("🕯️", "Berço do Círio de Nazaré", "Centro espiritual da maior procissão mariana do Brasil."),
            ("🏛️", "Praça Santuário", "Espaço arborizado com exposições e centro cultural anexo."),
            ("🎵", "Acústica e Contemplação", "Órgão monumental e ambiente de serenidade durante todo o dia."),
        ],
    },
}


class BelemNaMaoApp(ctk.CTk):
    LARGURA = 1220
    ALTURA = 800

    def __init__(self, usuario: Optional[Dict[str, Any]] = None, on_logout: Optional[Any] = None):
        super().__init__()
        self.usuario = usuario or {"id": 1, "nome": "Turista", "usuario": "turista"}
        self.usuario_id = self.usuario.get("id", 1)
        self.on_logout = on_logout

        self.title(t("app_title"))
        self.geometry(f"{self.LARGURA}x{self.ALTURA}")
        self.minsize(1060, 660)
        self.configure(fg_color=BG)

        # Estado da Aplicação (chaves canônicas independentes de idioma)
        self.locais = carregar_locais()
        self.roteiro = carregar_roteiro(usuario_id=self.usuario_id)
        self.aba_atual = "inicio"
        self._local_detalhe_atual: Optional[Dict[str, Any]] = None
        self._voltar_detalhe_atual = None

        # Filtros de Catálogo (chaves canônicas)
        self.f_texto = ""
        self.f_categoria = "Todas"
        self.f_preco = "Qualquer"
        self.f_bairro = "Todos"

        # Filtros da Tela "Mais Visitados" (Top 3 por Categoria)
        self.ranking_categoria = "Todas"

        # Estado persistente do Checklist em "Meu Roteiro"
        self._checklist_estado: List[bool] = [True, True, True, False]

        # Cache de telas para navegação instantânea entre abas
        self._telas_cache: Dict[str, ctk.CTkFrame] = {}

        self._centralizar()
        self._configurar_grid()
        self._criar_topo_navbar()

        # Container Principal com Troca Dinâmica de Telas
        self.conteudo = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.conteudo.grid(row=1, column=0, sticky="nsew")

        # Rodapé Discreto com Seletor de Idioma (PT-BR, EN, ES)
        self._criar_rodape_idiomas()

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
        self.grid_rowconfigure(2, weight=0)  # Rodapé Discreto (Idiomas)

    # ==================================================================
    # 1. Barra de Navegação Superior e Rodapé de Idiomas
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
        clima_pill.pack(side="left", padx=(14, 0), pady=16)

        self.lbl_clima = ctk.CTkLabel(
            clima_pill,
            text=t("clima_pill"),
            font=fonte(11, "bold"),
            text_color=TEXT_BRAND,
            padx=12,
            pady=4,
        )
        self.lbl_clima.pack()

        # Centro: Menu Pill de Navegação (substitui "Sobre Belém" por "Mais Visitados")
        centro = ctk.CTkFrame(inner, fg_color="transparent")
        centro.pack(side="left", expand=True)

        self.nav_botoes: Dict[str, ctk.CTkButton] = {}
        itens_nav = [
            ("inicio", "nav_inicio", self.mostrar_inicio),
            ("explorar", "nav_explorar", self.mostrar_explorar),
            ("roteiro", "nav_roteiro", self.mostrar_roteiro),
            ("ranking", "nav_ranking", self.mostrar_mais_visitados),
        ]

        nav_pill_container = ctk.CTkFrame(centro, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        nav_pill_container.pack(pady=16)

        for chave, i18n_key, cmd in itens_nav:
            btn = ctk.CTkButton(
                nav_pill_container,
                text=t(i18n_key),
                font=fonte(13, "bold"),
                height=34,
                corner_radius=8,
                fg_color="transparent",
                text_color=TEXT_MUTED,
                hover_color=PANEL_SUBTLE,
                command=cmd,
            )
            btn.pack(side="left", padx=3, pady=3)
            self.nav_botoes[chave] = btn

        # Direita: Botões Rápidos + Perfil
        direita = ctk.CTkFrame(inner, fg_color="transparent")
        direita.pack(side="right", fill="y", pady=16)

        self.btn_busca_nav = ctk.CTkButton(
            direita,
            text=t("btn_buscar_nav"),
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
        self.btn_busca_nav.pack(side="left", padx=(0, 8))

        self.btn_salvos_pill = ctk.CTkButton(
            direita,
            text=t("btn_salvos_nav", n=len(self.roteiro)),
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

        modo_atual = ctk.get_appearance_mode().lower()
        texto_tema = t("tema_claro") if modo_atual == "dark" else t("tema_escuro")
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

        perfil_box = ctk.CTkFrame(direita, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        perfil_box.pack(side="left", padx=(0, 8))

        avatar = ctk.CTkFrame(perfil_box, width=28, height=28, corner_radius=6, fg_color=PRIMARY_BTN)
        avatar.pack(side="left", padx=(4, 6), pady=3)
        avatar.pack_propagate(False)
        ctk.CTkLabel(avatar, text="👤", font=fonte(11), text_color="#FFFFFF").pack(expand=True)

        nome_user = self.usuario.get("nome", "Turista").split()[0]
        self.lbl_ola_user = ctk.CTkLabel(
            perfil_box,
            text=t("ola_usuario", nome=nome_user),
            font=fonte(12, "bold"),
            text_color=TEXT_TITLE,
        )
        self.lbl_ola_user.pack(side="left", padx=(0, 10))

        self.btn_sair_nav = ctk.CTkButton(
            direita,
            text=t("btn_sair"),
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
        self.btn_sair_nav.pack(side="left")

    def _criar_rodape_idiomas(self):
        """Cria um rodapé discreto e acessível com seletor de idioma (PT-BR, EN, ES)."""
        self.footer = ctk.CTkFrame(self, fg_color=PANEL, height=40, corner_radius=0, border_width=1, border_color=LINE)
        self.footer.grid(row=2, column=0, sticky="ew")
        self.footer.grid_propagate(False)

        inner = ctk.CTkFrame(self.footer, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=24)

        self.lbl_rodape_info = ctk.CTkLabel(
            inner,
            text=t("rodape_texto"),
            font=fonte(11),
            text_color=TEXT_MUTED,
        )
        self.lbl_rodape_info.pack(side="left")

        lang_box = ctk.CTkFrame(inner, fg_color="transparent")
        lang_box.pack(side="right", pady=5)

        self.lbl_idioma_rodape = ctk.CTkLabel(
            lang_box,
            text=f"🌐 {t('idioma_label')}",
            font=fonte(11, "bold"),
            text_color=TEXT_MUTED,
        )
        self.lbl_idioma_rodape.pack(side="left", padx=(0, 8))

        self.lang_botoes: Dict[str, ctk.CTkButton] = {}
        idioma_ativo = get_idioma()
        for codigo in IDIOMAS_DISPONIVEIS:
            ativo = codigo == idioma_ativo
            btn = ctk.CTkButton(
                lang_box,
                text=ROTULOS_IDIOMA[codigo],
                width=52,
                height=26,
                corner_radius=6,
                fg_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BG,
                hover_color=PRIMARY_HOVER if ativo else BTN_SECONDARY_HOVER,
                border_width=1,
                border_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BORDER,
                text_color="#FFFFFF" if ativo else BTN_SECONDARY_TEXT,
                font=fonte(11, "bold"),
                command=lambda c=codigo: self._alterar_idioma(c),
            )
            btn.pack(side="left", padx=2)
            self.lang_botoes[codigo] = btn

    def _atualizar_textos_fixos(self):
        """Atualiza imediatamente todos os textos da barra superior e rodapé após troca de idioma."""
        self.title(t("app_title"))
        self.lbl_clima.configure(text=t("clima_pill"))

        mapa_nav = {
            "inicio": "nav_inicio",
            "explorar": "nav_explorar",
            "roteiro": "nav_roteiro",
            "ranking": "nav_ranking",
        }
        for chave, i18n_key in mapa_nav.items():
            if chave in self.nav_botoes:
                self.nav_botoes[chave].configure(text=t(i18n_key))

        self.btn_busca_nav.configure(text=t("btn_buscar_nav"))
        self.btn_salvos_pill.configure(text=t("btn_salvos_nav", n=len(self.roteiro)))

        modo_atual = ctk.get_appearance_mode().lower()
        self.btn_tema.configure(text=t("tema_claro") if modo_atual == "dark" else t("tema_escuro"))

        nome_user = self.usuario.get("nome", "Turista").split()[0]
        self.lbl_ola_user.configure(text=t("ola_usuario", nome=nome_user))
        self.btn_sair_nav.configure(text=t("btn_sair"))

        self.lbl_rodape_info.configure(text=t("rodape_texto"))
        self.lbl_idioma_rodape.configure(text=f"🌐 {t('idioma_label')}")

        idioma_ativo = get_idioma()
        for codigo, btn in self.lang_botoes.items():
            ativo = codigo == idioma_ativo
            btn.configure(
                fg_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BG,
                hover_color=PRIMARY_HOVER if ativo else BTN_SECONDARY_HOVER,
                border_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BORDER,
                text_color="#FFFFFF" if ativo else BTN_SECONDARY_TEXT,
            )

    def _alterar_idioma(self, codigo: str):
        """Alterna o idioma em tempo real mantendo estado, tela atual e dados."""
        if get_idioma() == codigo:
            return
        set_idioma(codigo)
        self._invalidar_cache_telas()
        self._atualizar_textos_fixos()

        if self.aba_atual == "inicio":
            self.mostrar_inicio()
        elif self.aba_atual == "explorar":
            self.mostrar_explorar()
        elif self.aba_atual == "roteiro":
            self.mostrar_roteiro()
        elif self.aba_atual == "ranking":
            self.mostrar_mais_visitados()
        elif self.aba_atual == "detalhes" and self._local_detalhe_atual is not None:
            self.mostrar_detalhes(self._local_detalhe_atual, voltar=self._voltar_detalhe_atual)
        else:
            self.mostrar_inicio()

        self._toast(t("toast_idioma"), cor_bg=PRIMARY)

    def _alternar_modo_escuro(self):
        """Alterna reativamente entre Modo Claro e Modo Escuro."""
        modo_atual = ctk.get_appearance_mode().lower()
        if modo_atual == "dark":
            ctk.set_appearance_mode("light")
            self.btn_tema.configure(text=t("tema_escuro"))
            self._toast(t("toast_tema_claro"))
        else:
            ctk.set_appearance_mode("dark")
            self.btn_tema.configure(text=t("tema_claro"))
            self._toast(t("toast_tema_escuro"), cor_bg=TERTIARY_CONTAINER)

    def _fazer_logout(self):
        """Encerra a sessão e retorna à tela de login."""
        if self.on_logout:
            self.on_logout()
        else:
            self.destroy()

    def _marcar_aba_ativa(self, chave_aba: str):
        """Atualiza a aparência dos botões de navegação para a aba selecionada."""
        self.aba_atual = chave_aba
        for chave, btn in self.nav_botoes.items():
            ativo = chave == chave_aba
            btn.configure(
                fg_color=PRIMARY_CONTAINER if ativo else "transparent",
                text_color="#FFFFFF" if ativo else TEXT_MUTED,
            )
        if hasattr(self, "btn_salvos_pill"):
            self.btn_salvos_pill.configure(text=t("btn_salvos_nav", n=len(self.roteiro)))

    def _invalidar_cache_telas(self):
        """Remove telas em cache quando o idioma ou o roteiro é alterado."""
        for frame in self._telas_cache.values():
            if frame.winfo_exists():
                frame.destroy()
        self._telas_cache.clear()

    def _exibir_frame_tela(self, frame: ctk.CTkFrame):
        """Oculta os outros frames filhos e exibe apenas o frame desejado sem recriar widgets."""
        for child in self.conteudo.winfo_children():
            if child is not frame:
                child.pack_forget()
        frame.pack(fill="both", expand=True)

    def _limpar_conteudo(self):
        """Remove apenas widgets temporários (fora do cache de abas) do container principal."""
        cached = set(self._telas_cache.values())
        for w in self.conteudo.winfo_children():
            if w in cached:
                w.pack_forget()
            else:
                w.destroy()

    def _toast(self, mensagem: str, cor_bg: str = PRIMARY):
        """Exibe uma notificação flutuante elegante no canto inferior."""
        toast = ctk.CTkFrame(self, fg_color=cor_bg, corner_radius=16, border_width=1, border_color="#314868")
        toast.place(relx=0.98, rely=0.92, anchor="se")

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
    # 2. Tela Início (Clean + Cache de Frame para troca instantânea)
    # ==================================================================
    def mostrar_inicio(self):
        self._marcar_aba_ativa("inicio")
        if "inicio" in self._telas_cache and self._telas_cache["inicio"].winfo_exists():
            self._exibir_frame_tela(self._telas_cache["inicio"])
            return

        self._limpar_conteudo()
        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        self._telas_cache["inicio"] = rolagem
        self._exibir_frame_tela(rolagem)

        inner = ctk.CTkFrame(rolagem, fg_color="transparent")
        inner.pack(fill="x", padx=32, pady=(20, 40))

        # --- A. Card Azul Minimalista e Elegante ---
        hero = ctk.CTkFrame(inner, fg_color=PRIMARY_CONTAINER, corner_radius=12, border_width=1, border_color=LINE)
        hero.pack(fill="x", pady=(0, 24))

        hero_content = ctk.CTkFrame(hero, fg_color="transparent")
        hero_content.pack(fill="both", expand=True, padx=36, pady=32)

        ctk.CTkLabel(
            hero_content,
            text=t("hero_titulo"),
            font=fonte(32, "bold"),
            text_color="#FFFFFF",
            justify="left",
            anchor="w",
        ).pack(anchor="w", pady=(0, 4))

        ctk.CTkLabel(
            hero_content,
            text=t("hero_subtitulo"),
            font=fonte(14),
            text_color="#D5E3FF",
            justify="left",
            anchor="w",
        ).pack(anchor="w", pady=(0, 18))

        hero_actions = ctk.CTkFrame(hero_content, fg_color="transparent")
        hero_actions.pack(anchor="w")

        ctk.CTkButton(
            hero_actions,
            text=t("hero_btn_explorar"),
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
            text=t("hero_btn_roteiro"),
            height=40,
            corner_radius=8,
            fg_color=SECONDARY,
            text_color="#FFFFFF",
            hover_color=SECONDARY_HOVER,
            font=fonte(13, "bold"),
            command=self.mostrar_roteiro,
        ).pack(side="left")

        # --- B. Categorias Bento ---
        ctk.CTkLabel(inner, text=t("inicio_cats_titulo"), font=fonte(22, "bold"), text_color=TEXT_TITLE).pack(
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

            ctk.CTkLabel(
                c_box,
                text=traduzir_categoria(nome_cat),
                font=fonte(16, "bold"),
                text_color=TEXT_TITLE,
            ).pack(anchor="w")
            ctk.CTkLabel(
                c_box,
                text=traduzir_categoria_desc(nome_cat) or info["desc"],
                font=fonte(12),
                text_color=TEXT_MUTED,
                wraplength=175,
                justify="left",
            ).pack(anchor="w", pady=(4, 0))

            for w in (c_card, c_box, *c_box.winfo_children(), tile_emoji, *tile_emoji.winfo_children()):
                w.bind("<Button-1>", lambda _e, cat=nome_cat: self._filtrar_por_categoria(cat))

        # --- C. Destaques Imperdíveis ---
        topo_destaques = ctk.CTkFrame(inner, fg_color="transparent")
        topo_destaques.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(topo_destaques, text=t("inicio_destaques_titulo"), font=fonte(22, "bold"), text_color=TEXT_TITLE).pack(
            side="left"
        )
        ctk.CTkButton(
            topo_destaques,
            text=t("inicio_destaques_ver_todas"),
            fg_color="transparent",
            text_color=TEXT_BRAND,
            hover_color=PANEL_SUBTLE,
            font=fonte(13, "bold"),
            command=self.mostrar_explorar,
        ).pack(side="right")

        grade_destaques = ctk.CTkFrame(inner, fg_color="transparent")
        grade_destaques.pack(fill="x", pady=(0, 28))
        grade_destaques.grid_columnconfigure((0, 1, 2), weight=1, uniform="destaque_col")

        destaques_cards = [l for l in self.locais if l.get("id") in ["ver-o-peso", "estacao-das-docas", "bistro-guajara-noturno"]]
        if len(destaques_cards) < 3:
            destaques_cards = [l for l in self.locais if l.get("id") in ["ver-o-peso", "feliz-lusitania", "estacao-das-docas"]][:3]
        for i, loc in enumerate(destaques_cards[:3]):
            self._criar_card_destaque(grade_destaques, loc, coluna=i)

    def _criar_card_destaque(self, master, local: Dict[str, Any], coluna: int):
        meta = METADADOS_LOCAIS.get(local.get("id", ""), {})
        loc_t = traduzir_local(local, meta)

        card = ctk.CTkFrame(master, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE, cursor="hand2")
        card.grid(row=0, column=coluna, padx=6, sticky="nsew")

        img_ctk = obter_imagem_processada(local.get("id", ""), 360, 202, raio=12, apenas_topo=True)
        lbl_img = ctk.CTkLabel(card, text="", image=img_ctk)
        lbl_img.pack(side="top", fill="x", padx=0, pady=0)

        corpo = ctk.CTkFrame(card, fg_color="transparent")
        corpo.pack(side="top", fill="both", expand=True, padx=18, pady=16)

        meta_row = ctk.CTkFrame(corpo, fg_color="transparent")
        meta_row.pack(fill="x", pady=(0, 8))

        tag_cat = ctk.CTkFrame(meta_row, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
        tag_cat.pack(side="left")
        tag_txt = traduzir_categoria(local.get("categoria", ["Passeio"])[0])
        ctk.CTkLabel(
            tag_cat,
            text=tag_txt,
            font=fonte(10, "bold"),
            text_color=TAG_TEXT,
            padx=8,
            pady=2,
        ).pack()

        ctk.CTkLabel(
            meta_row,
            text=f"★ {meta.get('rating', 4.8)}",
            font=fonte(12, "bold"),
            text_color=AMBER,
        ).pack(side="right")

        ctk.CTkLabel(corpo, text=local["nome"], font=fonte(16, "bold"), text_color=TEXT_TITLE).pack(anchor="w", pady=(0, 4))

        preco = rotulo_preco(local.get("preco"))
        ctk.CTkLabel(
            corpo,
            text=preco,
            font=fonte(12, "bold"),
            text_color=TEXT_BRAND,
        ).pack(anchor="w", pady=(0, 14))

        botoes = ctk.CTkFrame(corpo, fg_color="transparent")
        botoes.pack(side="bottom", fill="x")

        presente = self._no_roteiro(local)
        btn_it = ctk.CTkButton(
            botoes,
            text=t("btn_no_roteiro") if presente else t("btn_add_roteiro"),
            height=36,
            corner_radius=8,
            fg_color=TERTIARY_CONTAINER if presente else PRIMARY_BTN,
            hover_color=TERTIARY if presente else PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(12, "bold"),
        )
        btn_it.configure(command=lambda l=local, b=btn_it: self.alternar_roteiro_btn(l, b, estilo="card"))
        btn_it.pack(side="left", fill="x", expand=True, padx=(0, 6))

        ctk.CTkButton(
            botoes,
            text=t("btn_detalhes"),
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

        for w in (card, lbl_img, corpo):
            w.bind("<Button-1>", lambda _e, l=local: self.mostrar_detalhes(l, voltar=self.mostrar_inicio))

    def _filtrar_por_categoria(self, categoria: str):
        self.f_categoria = categoria
        self.mostrar_explorar()

    # ==================================================================
    # 3. Tela Explorar (Alto Contraste #FFFFFF em Tema Escuro + Filtros)
    # ==================================================================
    def mostrar_explorar(self):
        self._limpar_conteudo()
        self._marcar_aba_ativa("explorar")

        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(rolagem, fg_color="transparent")
        inner.pack(fill="x", padx=32, pady=(20, 40))

        # Cabeçalho da Aba
        topo = ctk.CTkFrame(inner, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 14))

        topo_esq = ctk.CTkFrame(topo, fg_color="transparent")
        topo_esq.pack(side="left")

        ctk.CTkLabel(topo_esq, text=t("explorar_eyebrow"), font=fonte(11, "bold"), text_color=SECONDARY).pack(anchor="w")
        ctk.CTkLabel(topo_esq, text=t("explorar_titulo"), font=fonte(28, "bold"), text_color=TEXT_EXPLORAR).pack(anchor="w")
        ctk.CTkLabel(
            topo_esq,
            text=t("explorar_subtitulo"),
            font=fonte(13),
            text_color=TEXT_EXPLORAR,
        ).pack(anchor="w")

        # Barra de Pesquisa Flutuante
        barra_busca = ctk.CTkFrame(inner, fg_color=PANEL, corner_radius=8, border_width=1, border_color=LINE)
        barra_busca.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(barra_busca, text="🔍", font=fonte(16), text_color=TEXT_EXPLORAR).pack(side="left", padx=(16, 6), pady=12)

        self.entry_busca = ctk.CTkEntry(
            barra_busca,
            height=44,
            corner_radius=0,
            fg_color="transparent",
            border_width=0,
            text_color=TEXT_EXPLORAR,
            placeholder_text=t("explorar_busca_placeholder"),
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
            text_color=TEXT_EXPLORAR,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(12, "bold"),
            command=self._limpar_campo_busca,
        )
        btn_limpar_busca.pack(side="right", padx=(6, 12))

        # Carrossel de Categorias
        chips_frame = ctk.CTkFrame(inner, fg_color="transparent")
        chips_frame.pack(fill="x", pady=(0, 12))

        self.chips_botoes: Dict[str, ctk.CTkButton] = {}
        for chave_c in ["Todas", *CATEGORIAS_INFO.keys()]:
            ativo = chave_c == self.f_categoria
            btn_c = ctk.CTkButton(
                chips_frame,
                text=traduzir_categoria(chave_c),
                height=34,
                corner_radius=8,
                fg_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BG,
                text_color="#FFFFFF" if ativo else TEXT_EXPLORAR,
                border_width=1,
                border_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BORDER,
                hover_color=PRIMARY_HOVER if ativo else BTN_SECONDARY_HOVER,
                font=fonte(12, "bold"),
                command=lambda n=chave_c: self._selecionar_categoria_chip(n),
            )
            btn_c.pack(side="left", padx=(0, 8))
            self.chips_botoes[chave_c] = btn_c

        # Barra Secundária de Filtros (Preço, Bairro e Contador)
        barra_filtros = ctk.CTkFrame(inner, fg_color=PANEL_SUBTLE, corner_radius=12, border_width=1, border_color=LINE)
        barra_filtros.pack(fill="x", pady=(0, 18))

        bf_inner = ctk.CTkFrame(barra_filtros, fg_color="transparent")
        bf_inner.pack(fill="both", expand=True, padx=16, pady=10)

        ctk.CTkLabel(bf_inner, text=t("explorar_preco_label"), font=fonte(12, "bold"), text_color=TEXT_EXPLORAR).pack(
            side="left", padx=(0, 8)
        )
        opcoes_preco = [traduzir_preco_filtro(k) for k in ("Qualquer", "Baixo", "Médio", "Alto")]
        self.seg_preco = ctk.CTkSegmentedButton(
            bf_inner,
            values=opcoes_preco,
            height=32,
            corner_radius=8,
            fg_color=PANEL,
            selected_color=SEG_SELECTED_BG,
            selected_hover_color=PRIMARY_HOVER,
            unselected_color=PANEL,
            unselected_hover_color=PANEL_SUBTLE,
            text_color=TEXT_EXPLORAR,
            font=fonte(11, "bold"),
            command=self._filtrar_preco,
        )
        self.seg_preco.set(traduzir_preco_filtro(self.f_preco))
        self.seg_preco.pack(side="left", padx=(0, 16))

        # Filtro de Bairros (inclui Umarizal)
        todos_bairros_label = t("filtro_todos_bairros")
        self._bairros_mapa_display = {
            todos_bairros_label: "Todos",
            "Cidade Velha": "Cidade Velha",
            "Campina": "Campina",
            "Nazaré": "Nazaré",
            "Umarizal": "Umarizal",
            "Região insular": "Região insular",
        }
        bairros_exibidos = list(self._bairros_mapa_display.keys())
        self.menu_bairro = ctk.CTkOptionMenu(
            bf_inner,
            values=bairros_exibidos,
            height=32,
            corner_radius=8,
            fg_color=PANEL,
            button_color=PANEL_SUBTLE,
            button_hover_color=LINE,
            text_color=TEXT_EXPLORAR,
            font=fonte(12),
            command=self._filtrar_bairro,
        )
        display_bairro_atual = todos_bairros_label if self.f_bairro == "Todos" else self.f_bairro
        self.menu_bairro.set(display_bairro_atual)
        self.menu_bairro.pack(side="left")

        # Indicador de Resultados
        self.lbl_contagem = ctk.CTkLabel(bf_inner, text="", font=fonte(12, "bold"), text_color=TEXT_EXPLORAR)
        self.lbl_contagem.pack(side="right")

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
                text_color="#FFFFFF" if ativo else TEXT_EXPLORAR,
                border_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BORDER,
            )
        self._renderizar_catalogo()

    def _filtrar_preco(self, rotulo: str):
        self.f_preco = chave_preco_por_rotulo(rotulo)
        self._renderizar_catalogo()

    def _filtrar_bairro(self, valor_exibido: str):
        self.f_bairro = self._bairros_mapa_display.get(valor_exibido, valor_exibido)
        self._renderizar_catalogo()

    def _renderizar_catalogo(self):
        for w in self.container_cards.winfo_children():
            w.destroy()

        self.f_texto = self.entry_busca.get().strip()
        encontrados = buscar_locais(self.locais, self.f_texto, self.f_categoria, self.f_preco)

        if self.f_bairro != "Todos":
            encontrados = [l for l in encontrados if l.get("bairro", "").casefold() == self.f_bairro.casefold()]

        self.lbl_contagem.configure(text=t("explorar_contagem", n=len(encontrados), total=len(self.locais)))

        if not encontrados:
            self._criar_estado_vazio(self.container_cards)
            return

        grid = ctk.CTkFrame(self.container_cards, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="grid_locais")

        for idx, local in enumerate(encontrados):
            row = idx // 3
            col = idx % 3
            self._criar_card_catalogo(grid, local, row, col)

    def _criar_card_catalogo(self, master, local: Dict[str, Any], row: int, col: int):
        meta = METADADOS_LOCAIS.get(local.get("id", ""), {})
        loc_t = traduzir_local(local, meta)

        card = ctk.CTkFrame(master, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE, cursor="hand2")
        card.grid(row=row, column=col, padx=6, pady=8, sticky="nsew")

        img_ctk = obter_imagem_processada(local.get("id", ""), 360, 202, raio=12, apenas_topo=True)
        lbl_img = ctk.CTkLabel(card, text="", image=img_ctk)
        lbl_img.pack(side="top", fill="x", padx=0, pady=0)

        corpo = ctk.CTkFrame(card, fg_color="transparent")
        corpo.pack(side="top", fill="both", expand=True, padx=18, pady=16)

        meta_row = ctk.CTkFrame(corpo, fg_color="transparent")
        meta_row.pack(fill="x", pady=(0, 8))

        tag_cat = ctk.CTkFrame(meta_row, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
        tag_cat.pack(side="left", padx=(0, 6))
        tag_txt = traduzir_categoria(local.get("categoria", ["Passeio"])[0])
        ctk.CTkLabel(
            tag_cat,
            text=tag_txt,
            font=fonte(10, "bold"),
            text_color=TEXT_EXPLORAR,
            padx=8,
            pady=2,
        ).pack()

        ctk.CTkLabel(
            meta_row,
            text=f"★ {meta.get('rating', 4.8)}",
            font=fonte(12, "bold"),
            text_color=AMBER,
        ).pack(side="right")

        ctk.CTkLabel(corpo, text=local["nome"], font=fonte(16, "bold"), text_color=TEXT_EXPLORAR).pack(anchor="w", pady=(0, 4))

        preco = rotulo_preco(local.get("preco"))
        ctk.CTkLabel(
            corpo,
            text=preco,
            font=fonte(12, "bold"),
            text_color=TEXT_EXPLORAR,
        ).pack(anchor="w", pady=(0, 14))

        botoes = ctk.CTkFrame(corpo, fg_color="transparent")
        botoes.pack(side="bottom", fill="x")

        presente = self._no_roteiro(local)
        btn_it = ctk.CTkButton(
            botoes,
            text=t("btn_no_roteiro") if presente else t("btn_add_roteiro"),
            height=36,
            corner_radius=8,
            fg_color=TERTIARY_CONTAINER if presente else PRIMARY_BTN,
            hover_color=TERTIARY if presente else PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(12, "bold"),
        )
        btn_it.configure(command=lambda l=local, b=btn_it: self.alternar_roteiro_btn(l, b, estilo="card"))
        btn_it.pack(side="left", fill="x", expand=True, padx=(0, 6))

        ctk.CTkButton(
            botoes,
            text=t("btn_detalhes"),
            height=36,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            hover_color=BTN_SECONDARY_HOVER,
            text_color=TEXT_EXPLORAR,
            font=fonte(12, "bold"),
            command=lambda l=local: self.mostrar_detalhes(l, voltar=self.mostrar_explorar),
        ).pack(side="right")

        for w in (card, lbl_img, corpo):
            w.bind("<Button-1>", lambda _e, l=local: self.mostrar_detalhes(l, voltar=self.mostrar_explorar))

    def _criar_estado_vazio(self, master):
        vazio = ctk.CTkFrame(master, fg_color="transparent")
        vazio.pack(pady=60)
        ctk.CTkLabel(vazio, text="🔎", font=fonte(42), text_color=TEXT_EXPLORAR).pack(pady=(0, 6))
        ctk.CTkLabel(vazio, text=t("vazio_titulo"), font=fonte(18, "bold"), text_color=TEXT_EXPLORAR).pack(pady=(0, 4))
        ctk.CTkLabel(
            vazio,
            text=t("vazio_subtitulo"),
            font=fonte(13),
            text_color=TEXT_EXPLORAR,
        ).pack()
        ctk.CTkButton(
            vazio,
            text=t("vazio_btn_limpar"),
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
        self.f_bairro = "Todos"
        self.seg_preco.set(traduzir_preco_filtro("Qualquer"))
        self.menu_bairro.set(t("filtro_todos_bairros"))
        self._selecionar_categoria_chip("Todas")

    # ==================================================================
    # 4. Tela Detalhes da Atração
    # ==================================================================
    def mostrar_detalhes(self, local: Dict[str, Any], voltar=None):
        voltar = voltar or self.mostrar_explorar
        self._local_detalhe_atual = local
        self._voltar_detalhe_atual = voltar

        self._limpar_conteudo()
        self._marcar_aba_ativa("detalhes")
        meta = METADADOS_LOCAIS.get(local.get("id", ""), {})
        loc_t = traduzir_local(local, meta)

        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(rolagem, fg_color="transparent")
        inner.pack(fill="x", padx=32, pady=(16, 40))

        # 1. Breadcrumb & Top Bar de Ações
        top_bar = ctk.CTkFrame(inner, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 14))

        bc_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        bc_frame.pack(side="left")

        ctk.CTkButton(
            bc_frame,
            text=t("btn_voltar"),
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
            text=f"{t('breadcrumb_inicio')}  /  {t('breadcrumb_explorar')}  /  {local.get('bairro', 'Belém')}  /  ",
            font=fonte(12),
            text_color=TEXT_MUTED,
        ).pack(side="left")
        ctk.CTkLabel(bc_frame, text=local["nome"], font=fonte(12, "bold"), text_color=TEXT_TITLE).pack(side="left")

        acoes_topo = ctk.CTkFrame(top_bar, fg_color="transparent")
        acoes_topo.pack(side="right")

        ctk.CTkButton(
            acoes_topo,
            text=t("btn_compartilhar"),
            height=32,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            font=fonte(12),
            command=lambda: self._toast(t("toast_compartilhar")),
        ).pack(side="left", padx=(0, 8))

        presente = self._no_roteiro(local)
        btn_fav = ctk.CTkButton(
            acoes_topo,
            text=t("btn_salvo_roteiro") if presente else t("btn_salvar_fav"),
            height=32,
            corner_radius=8,
            fg_color=TERTIARY_FIXED if presente else BTN_SECONDARY_BG,
            text_color=ON_TERTIARY_FIXED if presente else BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            font=fonte(12, "bold"),
        )
        btn_fav.configure(command=lambda l=local, b=btn_fav: self.alternar_roteiro_btn(l, b, estilo="fav"))
        btn_fav.pack(side="left")

        # 2. Bento Visual Gallery
        galeria = ctk.CTkFrame(inner, fg_color="transparent")
        galeria.pack(fill="x", pady=(0, 18))
        galeria.grid_columnconfigure(0, weight=7, uniform="gal")
        galeria.grid_columnconfigure(1, weight=4, uniform="gal")

        img_principal = obter_imagem_processada(local.get("id", ""), 680, 360, raio=12)
        lbl_p = ctk.CTkLabel(galeria, text="", image=img_principal)
        lbl_p.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        sec_box = ctk.CTkFrame(galeria, fg_color="transparent")
        sec_box.grid(row=0, column=1, sticky="nsew")

        id_sec_1 = "feliz-lusitania-2" if local.get("id") == "feliz-lusitania" else (
            "bistro-guajara-noturno" if local.get("id") == "estacao-das-docas" else "estacao-das-docas"
        )
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

        tag1 = ctk.CTkFrame(tags_line, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
        tag1.pack(side="left", padx=(0, 6))
        ctk.CTkLabel(
            tag1,
            text=loc_t.get("destaque_tag") or "Belém",
            font=fonte(11, "bold"),
            text_color=TAG_TEXT,
            padx=10,
            pady=3,
        ).pack()

        tag2 = ctk.CTkFrame(tags_line, fg_color=PANEL_SUBTLE, corner_radius=6, border_width=1, border_color=LINE)
        tag2.pack(side="left", padx=(0, 6))
        ctk.CTkLabel(
            tag2,
            text=f"★ {meta.get('rating', 4.9)} ({meta.get('avaliacoes', '1.8k')} {t('avaliacoes_suffix')})",
            font=fonte(11, "bold"),
            text_color=AMBER,
            padx=10,
            pady=3,
        ).pack()

        ctk.CTkLabel(cab_detalhes, text=local["nome"], font=fonte(28, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(
            cab_detalhes,
            text=f"📍 {loc_t.get('endereco', local.get('endereco', 'Belém, Pará'))}",
            font=fonte(13),
            text_color=TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 6))

        # 4. Grid de Conteúdo Principal
        grid_conteudo = ctk.CTkFrame(inner, fg_color="transparent")
        grid_conteudo.pack(fill="x")
        grid_conteudo.grid_columnconfigure(0, weight=65, uniform="detalhes_cols")
        grid_conteudo.grid_columnconfigure(1, weight=35, uniform="detalhes_cols")

        # === COLUNA ESQUERDA ===
        col_esq = ctk.CTkFrame(grid_conteudo, fg_color="transparent")
        col_esq.grid(row=0, column=0, padx=(0, 16), sticky="nsew")

        bloco_sobre = ctk.CTkFrame(col_esq, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        bloco_sobre.pack(fill="x", pady=(0, 16))

        bs_inner = ctk.CTkFrame(bloco_sobre, fg_color="transparent")
        bs_inner.pack(fill="both", expand=True, padx=22, pady=18)

        ctk.CTkLabel(bs_inner, text=t("detalhes_sobre_titulo"), font=fonte(18, "bold"), text_color=TEXT_TITLE).pack(
            anchor="w", pady=(0, 8)
        )
        ctk.CTkLabel(
            bs_inner,
            text=loc_t.get("descricao", local["descricao"]),
            font=fonte(13),
            text_color=TEXT,
            justify="left",
            wraplength=640,
        ).pack(anchor="w", pady=(0, 8))

        ctk.CTkLabel(
            bs_inner,
            text=f"{t('detalhes_importancia')} {loc_t.get('por_que_visitar', local.get('por_que_visitar', ''))}",
            font=fonte(13),
            text_color=TEXT_MUTED,
            justify="left",
            wraplength=640,
        ).pack(anchor="w")

        ctk.CTkLabel(col_esq, text=t("detalhes_destaques_titulo"), font=fonte(18, "bold"), text_color=TEXT_TITLE).pack(
            anchor="w", pady=(6, 10)
        )

        grid_destaques_detalhe = ctk.CTkFrame(col_esq, fg_color="transparent")
        grid_destaques_detalhe.pack(fill="x", pady=(0, 16))
        grid_destaques_detalhe.grid_columnconfigure((0, 1), weight=1, uniform="pq_visitar")

        itens_pq = loc_t.get("destaques_cards", [])
        for i, (ic, tit, desc) in enumerate(itens_pq[:4]):
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

        # === COLUNA DIREITA ===
        col_dir = ctk.CTkFrame(grid_conteudo, fg_color="transparent")
        col_dir.grid(row=0, column=1, sticky="nsew")

        card_planejamento = ctk.CTkFrame(col_dir, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        card_planejamento.pack(fill="x", pady=(0, 16))

        cp_inner = ctk.CTkFrame(card_planejamento, fg_color="transparent")
        cp_inner.pack(fill="both", expand=True, padx=22, pady=20)

        cp_topo = ctk.CTkFrame(cp_inner, fg_color="transparent")
        cp_topo.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(cp_topo, text=t("detalhes_ingresso"), font=fonte(10, "bold"), text_color=TEXT_MUTED).pack(anchor="w")
        preco_val = loc_t.get("preco_tag", rotulo_preco(local.get("preco")))
        ctk.CTkLabel(cp_topo, text=preco_val, font=fonte(20, "bold"), text_color=TEXT_TITLE).pack(anchor="w")

        status_box = ctk.CTkFrame(cp_inner, fg_color=TERTIARY_FIXED, corner_radius=8)
        status_box.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(
            status_box,
            text=f"{t('detalhes_aberto_agora')}  •  {loc_t.get('horario', '09h às 18h')}",
            font=fonte(11, "bold"),
            text_color=ON_TERTIARY_FIXED,
            padx=12,
            pady=6,
            wraplength=290,
            justify="left",
        ).pack(anchor="w")

        clima_box = ctk.CTkFrame(cp_inner, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        clima_box.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(
            clima_box,
            text=t("detalhes_clima"),
            font=fonte(11),
            text_color=TEXT_TITLE,
            padx=12,
            pady=8,
            wraplength=280,
            justify="left",
        ).pack(anchor="w")

        presente = self._no_roteiro(local)
        self.btn_acao_detalhe = ctk.CTkButton(
            cp_inner,
            text=t("detalhes_salvo_roteiro") if presente else t("detalhes_add_roteiro"),
            height=44,
            corner_radius=8,
            fg_color=TERTIARY_CONTAINER if presente else PRIMARY_BTN,
            hover_color=TERTIARY if presente else PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(14, "bold"),
        )
        self.btn_acao_detalhe.configure(
            command=lambda l=local: self.alternar_roteiro_btn(l, self.btn_acao_detalhe, estilo="detalhe")
        )
        self.btn_acao_detalhe.pack(fill="x", pady=(0, 10))

        ctk.CTkButton(
            cp_inner,
            text=t("detalhes_maps"),
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

        ctk.CTkFrame(cp_inner, height=1, fg_color=LINE).pack(fill="x", pady=(0, 12))

        praticas = [
            ("⏱️", t("detalhes_tempo_sugerido", duracao=loc_t.get("duracao", local.get("duracao", "1h30 a 2h")))),
            ("❄️", t("detalhes_clima_ar")),
            ("📷", t("detalhes_fotos")),
            ("♿", t("detalhes_acessibilidade")),
        ]
        for ic, txt in praticas:
            r = ctk.CTkFrame(cp_inner, fg_color="transparent")
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=ic, font=fonte(12)).pack(side="left", padx=(0, 6))
            ctk.CTkLabel(r, text=txt, font=fonte(11), text_color=TEXT_MUTED).pack(side="left")

    # ==================================================================
    # 5. Tela Meu Roteiro (Redesign Clean, 3 KPIs, Timeline Conectada e Mapa)
    # ==================================================================
    def mostrar_roteiro(self):
        self._limpar_conteudo()
        self._marcar_aba_ativa("roteiro")

        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(rolagem, fg_color="transparent")
        inner.pack(fill="x", padx=32, pady=(20, 44))

        # Cabeçalho + Ações
        topo_roteiro = ctk.CTkFrame(inner, fg_color="transparent")
        topo_roteiro.pack(fill="x", pady=(0, 18))

        esq_r = ctk.CTkFrame(topo_roteiro, fg_color="transparent")
        esq_r.pack(side="left")

        tag_r = ctk.CTkFrame(esq_r, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
        tag_r.pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(tag_r, text=t("roteiro_tag"), font=fonte(10, "bold"), text_color=TAG_TEXT, padx=8, pady=2).pack()

        ctk.CTkLabel(esq_r, text=t("roteiro_titulo"), font=fonte(28, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(
            esq_r,
            text=t("roteiro_subtitulo"),
            font=fonte(13),
            text_color=TEXT_MUTED,
        ).pack(anchor="w")

        acoes_r = ctk.CTkFrame(topo_roteiro, fg_color="transparent")
        acoes_r.pack(side="right", pady=8)

        ctk.CTkButton(
            acoes_r,
            text=t("btn_otimizar_ia"),
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
            text=t("btn_salvar"),
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
            text=t("btn_limpar"),
            height=38,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            hover_color=("#FEE2E2", "#4C0519"),
            text_color=ERROR,
            font=fonte(12, "bold"),
            command=self._confirmar_limpar_roteiro,
        ).pack(side="left")

        # --- 1. Três Cards Superiores (Grid de 3 Colunas Equilibradas) ---
        strip_metricas = ctk.CTkFrame(inner, fg_color="transparent")
        strip_metricas.pack(fill="x", pady=(0, 24))
        strip_metricas.grid_columnconfigure((0, 1, 2), weight=1, uniform="met_r")

        total_paradas = len(self.roteiro)
        if total_paradas == 0:
            metricas = [
                ("⏱️", t("kpi_duracao"), "0h", ("#E0F2FE", "#0C4A6E")),
                ("📍", t("kpi_paradas"), t("kpi_paradas_zero"), ("#E0E7FF", "#1E1B4B")),
                ("💰", t("kpi_gasto"), "R$ 0", ("#D1FAE5", "#064E3B")),
            ]
        else:
            metricas = [
                ("⏱️", t("kpi_duracao"), t("kpi_duracao_val", h=total_paradas * 2), ("#E0F2FE", "#0C4A6E")),
                ("📍", t("kpi_paradas"), t("kpi_paradas_val", n=total_paradas), ("#E0E7FF", "#1E1B4B")),
                ("💰", t("kpi_gasto"), t("kpi_gasto_val", v=total_paradas * 15), ("#D1FAE5", "#064E3B")),
            ]

        borda_kpi = ("#E2E8F0", "#1E293B")
        for i, (ic, tit, val, badge_bg) in enumerate(metricas):
            c_m = ctk.CTkFrame(strip_metricas, fg_color=PANEL, corner_radius=12, border_width=1, border_color=borda_kpi)
            c_m.grid(row=0, column=i, padx=(0 if i == 0 else 7, 0 if i == 2 else 7), sticky="nsew")

            cm_in = ctk.CTkFrame(c_m, fg_color="transparent")
            cm_in.pack(fill="both", expand=True, padx=18, pady=16)

            t_row = ctk.CTkFrame(cm_in, fg_color="transparent")
            t_row.pack(fill="x")
            ctk.CTkLabel(t_row, text=tit.upper(), font=fonte(11, "bold"), text_color=TEXT_MUTED).pack(
                side="left", anchor="n", pady=(4, 0)
            )

            ic_badge = ctk.CTkFrame(t_row, width=36, height=36, corner_radius=10, fg_color=badge_bg)
            ic_badge.pack(side="right")
            ic_badge.pack_propagate(False)
            ctk.CTkLabel(ic_badge, text=ic, font=fonte(16)).pack(expand=True)

            ctk.CTkLabel(cm_in, text=val, font=fonte(21, "bold"), text_color=TEXT_TITLE).pack(anchor="w", pady=(8, 0))

        if not self.roteiro:
            self._criar_roteiro_vazio(inner)
            return

        # --- 2. Grid Principal: Timeline Clean (Esquerda) + Painel Interativo (Direita) ---
        grid_rot = ctk.CTkFrame(inner, fg_color="transparent")
        grid_rot.pack(fill="both", expand=True)
        grid_rot.grid_columnconfigure(0, weight=63, uniform="rot_cols")
        grid_rot.grid_columnconfigure(1, weight=37, uniform="rot_cols")

        col_timeline = ctk.CTkFrame(grid_rot, fg_color="transparent")
        col_timeline.grid(row=0, column=0, padx=(0, 18), sticky="nsew")

        self._criar_divisor_periodo(col_timeline, t("turno_manha_titulo"), t("turno_manha_sub"))

        paradas_manha = self.roteiro[:2]
        paradas_tarde = self.roteiro[2:]
        for idx, local in enumerate(paradas_manha, start=1):
            eh_ultimo_geral = (idx == total_paradas) and not paradas_tarde
            self._criar_card_timeline_parada(
                col_timeline,
                local,
                idx,
                horario="08:00 – 10:30" if idx == 1 else "10:45 – 12:30",
                mostrar_linha_abaixo=not eh_ultimo_geral,
            )
            if idx == 1 and len(paradas_manha) > 1:
                self._criar_conector_deslocamento(col_timeline, t("conector_manha"))

        self._criar_card_almoco(col_timeline, mostrar_linha_abaixo=bool(paradas_tarde))

        if paradas_tarde:
            self._criar_divisor_periodo(col_timeline, t("turno_tarde_titulo"), t("turno_tarde_sub"))
            self._criar_conector_deslocamento(col_timeline, t("conector_carro"))

            for idx, local in enumerate(paradas_tarde, start=3):
                eh_ultimo = idx == total_paradas
                horario_tarde = "14:30 – 17:30" if idx == 3 else ("18:30 – 22:00" if idx == 4 else "20:00 – 23:30")
                self._criar_card_timeline_parada(
                    col_timeline,
                    local,
                    idx,
                    horario=horario_tarde,
                    mostrar_linha_abaixo=not eh_ultimo,
                )
                if not eh_ultimo:
                    self._criar_conector_deslocamento(col_timeline, t("conector_tarde"))

        # --- 3. Coluna da Direita: Traçado da Rota, Checklist com Contador e Sugestões ---
        col_planejamento = ctk.CTkFrame(grid_rot, fg_color="transparent")
        col_planejamento.grid(row=0, column=1, sticky="nsew")

        # A. Card Traçado da Rota
        mapa_box = ctk.CTkFrame(col_planejamento, fg_color=PANEL, corner_radius=12, border_width=1, border_color=borda_kpi)
        mapa_box.pack(fill="x", pady=(0, 16))

        mb_in = ctk.CTkFrame(mapa_box, fg_color="transparent")
        mb_in.pack(fill="both", expand=True, padx=18, pady=18)

        topo_mapa = ctk.CTkFrame(mb_in, fg_color="transparent")
        topo_mapa.pack(fill="x")
        ctk.CTkLabel(topo_mapa, text=t("rota_titulo"), font=fonte(16, "bold"), text_color=TEXT_TITLE).pack(side="left")

        pill_paradas = ctk.CTkFrame(topo_mapa, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
        pill_paradas.pack(side="right")
        ctk.CTkLabel(
            pill_paradas,
            text=t("rota_subtitulo", n=total_paradas),
            font=fonte(10, "bold"),
            text_color=TAG_TEXT,
            padx=8,
            pady=2,
        ).pack()

        id_capa_rota = self.roteiro[0].get("id", "estacao-das-docas")
        img_map_route = obter_imagem_processada(id_capa_rota, 360, 168, raio=10)
        lbl_img_rota = ctk.CTkLabel(mb_in, text="", image=img_map_route)
        lbl_img_rota.pack(fill="x", pady=(12, 10))

        # Badge mostrando os pontos conectados em sequência
        nomes_curtos = [loc.get("nome", "").replace("Mercado ", "").replace("Complexo ", "") for loc in self.roteiro]
        texto_sequencia = "  →  ".join(nomes_curtos[:4])
        if len(nomes_curtos) > 4:
            texto_sequencia += f"  (+{len(nomes_curtos) - 4})"

        box_seq = ctk.CTkFrame(mb_in, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        box_seq.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(
            box_seq,
            text=f"🧭 {texto_sequencia}",
            font=fonte(11, "bold"),
            text_color=TEXT_BRAND,
            wraplength=320,
            justify="left",
            padx=12,
            pady=8,
        ).pack(anchor="w")

        rota_query = "/".join(f"{loc['nome']}+Belem+PA".replace(" ", "+") for loc in self.roteiro[:5])
        url_maps = f"https://www.google.com/maps/dir/{rota_query}" if len(self.roteiro) > 1 else f"https://maps.google.com/?q={self.roteiro[0]['nome']}+Belem"

        ctk.CTkButton(
            mb_in,
            text=t("btn_maps_rota"),
            height=40,
            corner_radius=8,
            fg_color=("#0284C7", "#0EA5E9"),
            hover_color="#0369A1",
            text_color="#FFFFFF",
            font=fonte(12, "bold"),
            command=lambda u=url_maps: webbrowser.open(u),
        ).pack(fill="x")

        # B. Card Checklist "O que levar no dia" com Contador Dinâmico
        card_check = ctk.CTkFrame(col_planejamento, fg_color=PANEL, corner_radius=12, border_width=1, border_color=borda_kpi)
        card_check.pack(fill="x", pady=(0, 16))

        cc_in = ctk.CTkFrame(card_check, fg_color="transparent")
        cc_in.pack(fill="both", expand=True, padx=18, pady=18)

        topo_chk = ctk.CTkFrame(cc_in, fg_color="transparent")
        topo_chk.pack(fill="x")
        ctk.CTkLabel(topo_chk, text=t("checklist_titulo"), font=fonte(16, "bold"), text_color=TEXT_TITLE).pack(side="left")

        prontos_ini = sum(1 for v in self._checklist_estado if v)
        pill_prog = ctk.CTkFrame(topo_chk, fg_color=TERTIARY_FIXED, corner_radius=6)
        pill_prog.pack(side="right")
        self.lbl_progresso_check = ctk.CTkLabel(
            pill_prog,
            text=t("checklist_progresso", prontos=prontos_ini, total=len(self._checklist_estado)),
            font=fonte(10, "bold"),
            text_color=ON_TERTIARY_FIXED,
            padx=8,
            pady=2,
        )
        self.lbl_progresso_check.pack()

        ctk.CTkLabel(cc_in, text=t("checklist_sub"), font=fonte(12), text_color=TEXT_MUTED).pack(anchor="w", pady=(2, 10))

        textos_mochila = [t("check_1"), t("check_2"), t("check_3"), t("check_4")]
        self._checkbox_widgets: List[ctk.CTkCheckBox] = []
        for idx_c, txt in enumerate(textos_mochila):
            chk = ctk.CTkCheckBox(
                cc_in,
                text=txt,
                font=fonte(12),
                text_color=TEXT,
                fg_color=PRIMARY_BTN,
                hover_color=PRIMARY_HOVER,
                border_color=BTN_SECONDARY_BORDER,
                corner_radius=5,
                command=lambda i=idx_c: self._ao_alternar_checklist(i),
            )
            if self._checklist_estado[idx_c]:
                chk.select()
            chk.pack(anchor="w", pady=6)
            self._checkbox_widgets.append(chk)

        # C. Bloco "Adicionar Paradas Sugeridas"
        sugestoes_disponiveis = [
            loc for loc in self.locais if not self._no_roteiro(loc)
        ][:4]

        if sugestoes_disponiveis:
            card_quick = ctk.CTkFrame(col_planejamento, fg_color=PANEL, corner_radius=12, border_width=1, border_color=borda_kpi)
            card_quick.pack(fill="x")

            cq_in = ctk.CTkFrame(card_quick, fg_color="transparent")
            cq_in.pack(fill="both", expand=True, padx=18, pady=18)

            ctk.CTkLabel(cq_in, text=t("sugestoes_titulo"), font=fonte(15, "bold"), text_color=TEXT_TITLE).pack(
                anchor="w", pady=(0, 10)
            )

            for loc_sug in sugestoes_disponiveis:
                item_sug = ctk.CTkFrame(cq_in, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
                item_sug.pack(fill="x", pady=4)

                is_in = ctk.CTkFrame(item_sug, fg_color="transparent")
                is_in.pack(fill="x", padx=12, pady=8)

                txt_box = ctk.CTkFrame(is_in, fg_color="transparent")
                txt_box.pack(side="left", fill="x", expand=True)
                ctk.CTkLabel(txt_box, text=loc_sug["nome"], font=fonte(12, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
                ctk.CTkLabel(txt_box, text=f"📍 {loc_sug.get('bairro', 'Belém')}", font=fonte(11), text_color=TEXT_MUTED).pack(anchor="w")

                ctk.CTkButton(
                    is_in,
                    text=t("btn_adicionar_curto"),
                    width=92,
                    height=30,
                    corner_radius=7,
                    fg_color=PRIMARY_BTN,
                    hover_color=PRIMARY_HOVER,
                    text_color="#FFFFFF",
                    font=fonte(11, "bold"),
                    command=lambda ls=loc_sug: self._adicionar_sugestao_rapida(ls),
                ).pack(side="right", padx=(8, 0))

    def _ao_alternar_checklist(self, indice: int):
        if 0 <= indice < len(self._checkbox_widgets):
            self._checklist_estado[indice] = bool(self._checkbox_widgets[indice].get())
            prontos = sum(1 for v in self._checklist_estado if v)
            if hasattr(self, "lbl_progresso_check") and self.lbl_progresso_check.winfo_exists():
                self.lbl_progresso_check.configure(
                    text=t("checklist_progresso", prontos=prontos, total=len(self._checklist_estado))
                )

    def _criar_divisor_periodo(self, master, titulo: str, subtitulo: str):
        divisor = ctk.CTkFrame(master, fg_color="transparent")
        divisor.pack(fill="x", pady=(10, 8))
        ctk.CTkLabel(divisor, text=titulo, font=fonte(16, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(divisor, text=subtitulo, font=fonte(12), text_color=TEXT_MUTED).pack(anchor="w")

    def _criar_conector_deslocamento(self, master, texto: str):
        """Conector intermediário discreto alinhado à linha vertical da timeline."""
        wrap = ctk.CTkFrame(master, fg_color="transparent")
        wrap.pack(fill="x", pady=0)

        rail = ctk.CTkFrame(wrap, width=42, height=28, fg_color="transparent")
        rail.pack(side="left", padx=(0, 12))
        rail.pack_propagate(False)
        ctk.CTkFrame(rail, width=2, fg_color=("#CBD5E1", "#334155")).pack(expand=True, fill="y")

        ctk.CTkLabel(
            wrap,
            text=texto,
            font=fonte(11),
            text_color=TEXT_MUTED,
        ).pack(side="left", pady=4)

    def _criar_card_almoco(self, master, mostrar_linha_abaixo: bool = True):
        """Card diferenciado em tom âmbar/dourado sutil para pausa sugerida de almoço."""
        wrap = ctk.CTkFrame(master, fg_color="transparent")
        wrap.pack(fill="x", pady=4)

        rail = ctk.CTkFrame(wrap, width=42, fg_color="transparent")
        rail.pack(side="left", fill="y", padx=(0, 12))
        rail.pack_propagate(False)

        ctk.CTkFrame(rail, width=2, height=10, fg_color=("#CBD5E1", "#334155")).pack()
        icone_almoco = ctk.CTkFrame(
            rail,
            width=32,
            height=32,
            corner_radius=16,
            fg_color=("#FEF3C7", "#3B2506"),
            border_width=1,
            border_color=("#F59E0B", "#D97706"),
        )
        icone_almoco.pack()
        icone_almoco.pack_propagate(False)
        ctk.CTkLabel(icone_almoco, text="🍽️", font=fonte(13)).pack(expand=True)
        if mostrar_linha_abaixo:
            ctk.CTkFrame(rail, width=2, fg_color=("#CBD5E1", "#334155")).pack(expand=True, fill="y")

        card = ctk.CTkFrame(
            wrap,
            fg_color=("#FFFBEB", "#1F1A10"),
            corner_radius=12,
            border_width=1,
            border_color=("#FDE68A", "#92400E"),
        )
        card.pack(side="left", fill="both", expand=True, pady=4)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=18, pady=14)

        tag = ctk.CTkFrame(inner, fg_color=("#FEF3C7", "#3B2506"), corner_radius=6)
        tag.pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(
            tag,
            text=f"✦  {t('almoco_tag')}",
            font=fonte(10, "bold"),
            text_color=("#B45309", "#FBBF24"),
            padx=8,
            pady=2,
        ).pack()

        ctk.CTkLabel(inner, text=t("almoco_titulo"), font=fonte(14, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(
            inner,
            text=t("almoco_desc"),
            font=fonte(12),
            text_color=TEXT_MUTED,
            wraplength=500,
            justify="left",
        ).pack(anchor="w", pady=(2, 0))

    def _criar_card_timeline_parada(
        self,
        master,
        local: Dict[str, Any],
        indice: int,
        horario: str,
        mostrar_linha_abaixo: bool = True,
    ):
        """Item da timeline conectado por linha vertical com foto maior e layout limpo."""
        meta = METADADOS_LOCAIS.get(local.get("id", ""), {})
        loc_t = traduzir_local(local, meta)

        wrap = ctk.CTkFrame(master, fg_color="transparent")
        wrap.pack(fill="x", pady=2)

        # Trilha vertical esquerda conectando os números 1 -> 2 -> 3...
        rail = ctk.CTkFrame(wrap, width=42, fg_color="transparent")
        rail.pack(side="left", fill="y", padx=(0, 12))
        rail.pack_propagate(False)

        if indice > 1:
            ctk.CTkFrame(rail, width=2, height=12, fg_color=("#CBD5E1", "#334155")).pack()
        else:
            ctk.CTkFrame(rail, width=2, height=12, fg_color="transparent").pack()

        num = ctk.CTkFrame(rail, width=34, height=34, corner_radius=10, fg_color=PRIMARY_BTN)
        num.pack()
        num.pack_propagate(False)
        ctk.CTkLabel(num, text=str(indice), font=fonte(13, "bold"), text_color="#FFFFFF").pack(expand=True)

        if mostrar_linha_abaixo:
            ctk.CTkFrame(rail, width=2, fg_color=("#CBD5E1", "#334155")).pack(expand=True, fill="y")

        # Card Clean da Parada
        card = ctk.CTkFrame(wrap, fg_color=PANEL, corner_radius=12, border_width=1, border_color=("#E2E8F0", "#1E293B"))
        card.pack(side="left", fill="both", expand=True, pady=4)

        c_in = ctk.CTkFrame(card, fg_color="transparent")
        c_in.pack(fill="both", expand=True, padx=16, pady=14)

        # Foto miniatura mais alta e expressiva
        img_thumb = obter_imagem_processada(local.get("id", ""), 132, 92, raio=10)
        lbl_thumb = ctk.CTkLabel(c_in, text="", image=img_thumb)
        lbl_thumb.pack(side="left", padx=(0, 16))

        info = ctk.CTkFrame(c_in, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)

        topo_info = ctk.CTkFrame(info, fg_color="transparent")
        topo_info.pack(fill="x")
        ctk.CTkLabel(topo_info, text=local["nome"], font=fonte(16, "bold"), text_color=TEXT_TITLE).pack(
            side="left", padx=(0, 8)
        )

        pill_hora = ctk.CTkFrame(topo_info, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
        pill_hora.pack(side="left")
        ctk.CTkLabel(pill_hora, text=horario, font=fonte(10, "bold"), text_color=TAG_TEXT, padx=8, pady=2).pack()

        ctk.CTkLabel(
            info,
            text=f"📍 {local['bairro']}  •  {loc_t.get('duracao', local.get('duracao', '2h'))}",
            font=fonte(12),
            text_color=TEXT_MUTED,
        ).pack(anchor="w", pady=(3, 4))

        desc_curta = loc_t.get("subtitulo") or loc_t.get("descricao", local["descricao"])
        if len(desc_curta) > 84:
            desc_curta = desc_curta[:81].rstrip() + "..."
        ctk.CTkLabel(
            info,
            text=desc_curta,
            font=fonte(12),
            text_color=TEXT,
            wraplength=330,
            justify="left",
        ).pack(anchor="w")

        acoes = ctk.CTkFrame(c_in, fg_color="transparent")
        acoes.pack(side="right", padx=(12, 0))

        ctk.CTkButton(
            acoes,
            text=t("btn_ver_guia"),
            height=34,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            hover_color=BTN_SECONDARY_HOVER,
            text_color=BTN_SECONDARY_TEXT,
            font=fonte(11, "bold"),
            command=lambda l=local: self.mostrar_detalhes(l, voltar=self.mostrar_roteiro),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            acoes,
            text="✕",
            width=34,
            height=34,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            hover_color=("#FEE2E2", "#4C0519"),
            text_color=ERROR,
            font=fonte(12, "bold"),
            command=lambda lid=local["id"]: self._remover_item_roteiro(lid),
        ).pack(side="left")

    def _adicionar_sugestao_rapida(self, local: Dict[str, Any]):
        self.roteiro = adicionar(self.roteiro, local, usuario_id=self.usuario_id)
        self._invalidar_cache_telas()
        self.mostrar_roteiro()
        self._toast(t("toast_add_roteiro", nome=local["nome"]))

    def _remover_item_roteiro(self, local_id: str):
        self.roteiro = remover(self.roteiro, local_id, usuario_id=self.usuario_id)
        self._invalidar_cache_telas()
        self.mostrar_roteiro()
        self._toast(t("toast_rem_generico"))

    def _otimizar_roteiro_ia(self):
        """Reordena o roteiro em fluxo geográfico e cronológico ideal (diurno -> noturno)."""
        ordem_ideal = [
            "ver-o-peso",
            "feliz-lusitania",
            "teatro-da-paz",
            "praca-republica",
            "mangal",
            "basilica-nazare",
            "ilha-combu",
            "estacao-das-docas",
            "bistro-guajara-noturno",
        ]
        self.roteiro.sort(key=lambda x: ordem_ideal.index(x.get("id")) if x.get("id") in ordem_ideal else 99)
        salvar_roteiro(self.roteiro)
        self.mostrar_roteiro()
        self._toast(t("toast_ia_otimizado"), cor_bg=TERTIARY_CONTAINER)

    def _confirmar_salvamento_banco(self):
        salvar_roteiro(self.roteiro)
        self._toast(t("toast_roteiro_salvo", n=len(self.roteiro)), cor_bg=TERTIARY_CONTAINER)

    def _confirmar_limpar_roteiro(self):
        self.roteiro = limpar(usuario_id=self.usuario_id)
        self._invalidar_cache_telas()
        self.mostrar_roteiro()
        self._toast(t("toast_roteiro_limpo"))

    def _criar_roteiro_vazio(self, master):
        vazio = ctk.CTkFrame(master, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        vazio.pack(fill="x", pady=24)

        vi = ctk.CTkFrame(vazio, fg_color="transparent")
        vi.pack(pady=48, padx=24)

        ctk.CTkLabel(vi, text="🗺️", font=fonte(48)).pack(pady=(0, 10))
        ctk.CTkLabel(vi, text=t("roteiro_vazio_titulo"), font=fonte(20, "bold"), text_color=TEXT_TITLE).pack(pady=(0, 6))
        ctk.CTkLabel(
            vi,
            text=t("roteiro_vazio_desc"),
            font=fonte(13),
            text_color=TEXT_MUTED,
            justify="center",
        ).pack(pady=(0, 20))

        ctk.CTkButton(
            vi,
            text=t("roteiro_vazio_btn"),
            height=40,
            corner_radius=8,
            fg_color=PRIMARY_BTN,
            hover_color=PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(13, "bold"),
            command=self.mostrar_explorar,
        ).pack()

    # ==================================================================
    # 6. Tela "Mais Visitados" (Top 3 por Categoria)
    # ==================================================================
    def mostrar_mais_visitados(self):
        self._marcar_aba_ativa("ranking")
        if "ranking" in self._telas_cache and self._telas_cache["ranking"].winfo_exists():
            self._exibir_frame_tela(self._telas_cache["ranking"])
            return

        self._limpar_conteudo()
        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        self._telas_cache["ranking"] = rolagem
        self._exibir_frame_tela(rolagem)

        inner = ctk.CTkFrame(rolagem, fg_color="transparent")
        inner.pack(fill="x", padx=32, pady=(20, 40))

        # Cabeçalho
        topo = ctk.CTkFrame(inner, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 18))

        topo_esq = ctk.CTkFrame(topo, fg_color="transparent")
        topo_esq.pack(side="left")

        ctk.CTkLabel(topo_esq, text=t("ranking_eyebrow"), font=fonte(11, "bold"), text_color=SECONDARY).pack(anchor="w")
        ctk.CTkLabel(topo_esq, text=t("ranking_titulo"), font=fonte(28, "bold"), text_color=TEXT_TITLE).pack(anchor="w")
        ctk.CTkLabel(topo_esq, text=t("ranking_subtitulo"), font=fonte(13), text_color=TEXT_MUTED).pack(anchor="w")

        self.badge_fonte_ranking = ctk.CTkFrame(topo, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        self.badge_fonte_ranking.pack(side="right", pady=8)
        self.lbl_fonte_ranking = ctk.CTkLabel(
            self.badge_fonte_ranking,
            text="",
            font=fonte(11, "bold"),
            text_color=TEXT_BRAND,
            padx=12,
            pady=6,
        )
        self.lbl_fonte_ranking.pack()

        # Barra de Botões por Categoria (Todas + 5 Categorias)
        barra_cats = ctk.CTkFrame(inner, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        barra_cats.pack(fill="x", pady=(0, 18))

        bc_in = ctk.CTkFrame(barra_cats, fg_color="transparent")
        bc_in.pack(fill="x", padx=18, pady=12)

        ctk.CTkLabel(bc_in, text=t("ranking_cat_label"), font=fonte(12, "bold"), text_color=TEXT_TITLE).pack(
            side="left", padx=(0, 12)
        )

        self.ranking_cat_botoes: Dict[str, ctk.CTkButton] = {}
        categorias_ordem = ["Todas", "Gastronomia", "Cultura", "História", "Passeio", "Natureza"]
        for chave_c in categorias_ordem:
            ativo = chave_c == self.ranking_categoria
            btn = ctk.CTkButton(
                bc_in,
                text=traduzir_categoria(chave_c),
                height=34,
                corner_radius=8,
                fg_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BG,
                hover_color=PRIMARY_HOVER if ativo else BTN_SECONDARY_HOVER,
                border_width=1,
                border_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BORDER,
                text_color="#FFFFFF" if ativo else BTN_SECONDARY_TEXT,
                font=fonte(12, "bold"),
                command=lambda c=chave_c: self._selecionar_categoria_ranking(c),
            )
            btn.pack(side="left", padx=(0, 8))
            self.ranking_cat_botoes[chave_c] = btn

        self.lbl_subtitulo_top3 = ctk.CTkLabel(inner, text="", font=fonte(18, "bold"), text_color=TEXT_TITLE)
        self.lbl_subtitulo_top3.pack(anchor="w", pady=(4, 12))

        self.container_ranking = ctk.CTkFrame(inner, fg_color="transparent")
        self.container_ranking.pack(fill="both", expand=True)

        self._renderizar_ranking()

    def _selecionar_categoria_ranking(self, categoria: str):
        self.ranking_categoria = categoria
        for chave_c, btn in self.ranking_cat_botoes.items():
            ativo = chave_c == categoria
            btn.configure(
                fg_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BG,
                hover_color=PRIMARY_HOVER if ativo else BTN_SECONDARY_HOVER,
                border_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BORDER,
                text_color="#FFFFFF" if ativo else BTN_SECONDARY_TEXT,
            )
        self._renderizar_ranking()

    def _renderizar_ranking(self):
        for w in self.container_ranking.winfo_children():
            w.destroy()

        top3, conectado_mysql = obter_top3_por_categoria_db(self.ranking_categoria)

        self.lbl_fonte_ranking.configure(
            text=t("ranking_fonte_mysql") if conectado_mysql else t("ranking_fonte_local"),
            text_color=ON_TERTIARY_FIXED if conectado_mysql else TEXT_BRAND,
        )

        if self.ranking_categoria == "Todas":
            self.lbl_subtitulo_top3.configure(text=t("ranking_top3_todas"))
        else:
            self.lbl_subtitulo_top3.configure(
                text=t("ranking_top3_titulo", cat=traduzir_categoria(self.ranking_categoria))
            )

        if not top3:
            vazio = ctk.CTkFrame(self.container_ranking, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
            vazio.pack(fill="x", pady=16)
            ctk.CTkLabel(vazio, text=t("ranking_vazio"), font=fonte(14), text_color=TEXT_MUTED, pady=36).pack()
            return

        max_visitas = max(item["visitas"] for item in top3) or 1
        locais_por_id = {l["id"]: l for l in self.locais}

        for item in top3:
            pos = item["posicao"]
            loc_obj = locais_por_id.get(item["local_id"])

            card = ctk.CTkFrame(
                self.container_ranking,
                fg_color=PANEL,
                corner_radius=12,
                border_width=1,
                border_color=AMBER if pos == 1 else LINE,
            )
            card.pack(fill="x", pady=8)

            row_in = ctk.CTkFrame(card, fg_color="transparent")
            row_in.pack(fill="x", padx=20, pady=16)

            if pos == 1:
                medalha_bg, medalha_txt, medalha_fg = "#F59E0B", f"🥇 {t('ranking_pos_1')}", "#0F172A"
            elif pos == 2:
                medalha_bg, medalha_txt, medalha_fg = "#CBD5E1", f"🥈 {t('ranking_pos_2')}", "#0F172A"
            else:
                medalha_bg, medalha_txt, medalha_fg = "#D97706", f"🥉 {t('ranking_pos_3')}", "#FFFFFF"

            pos_box = ctk.CTkFrame(row_in, width=72, height=52, corner_radius=10, fg_color=medalha_bg)
            pos_box.pack(side="left", padx=(0, 14))
            pos_box.pack_propagate(False)
            ctk.CTkLabel(pos_box, text=medalha_txt, font=fonte(15, "bold"), text_color=medalha_fg).pack(expand=True)

            img_thumb = obter_imagem_processada(item["local_id"], 108, 70, raio=10)
            ctk.CTkLabel(row_in, text="", image=img_thumb).pack(side="left", padx=(0, 16))

            info_box = ctk.CTkFrame(row_in, fg_color="transparent")
            info_box.pack(side="left", fill="both", expand=True, padx=(0, 14))

            titulo_row = ctk.CTkFrame(info_box, fg_color="transparent")
            titulo_row.pack(fill="x")
            ctk.CTkLabel(titulo_row, text=item["nome"], font=fonte(17, "bold"), text_color=TEXT_TITLE).pack(
                side="left", padx=(0, 10)
            )

            for c_nome in [traduzir_categoria(c) for c in item.get("categoria", [])[:2]]:
                badge = ctk.CTkFrame(titulo_row, fg_color=TAG_BG, corner_radius=6, border_width=1, border_color=TAG_BORDER)
                badge.pack(side="left", padx=(0, 6))
                ctk.CTkLabel(badge, text=c_nome, font=fonte(10, "bold"), text_color=TAG_TEXT, padx=8, pady=2).pack()

            barra = ctk.CTkProgressBar(
                info_box,
                height=8,
                corner_radius=4,
                fg_color=PANEL_SUBTLE,
                progress_color=AMBER if pos == 1 else PRIMARY_BTN,
            )
            barra.set(item["visitas"] / max_visitas)
            barra.pack(fill="x", padx=(0, 24), pady=(10, 0))

            metrics_box = ctk.CTkFrame(row_in, fg_color="transparent", width=170)
            metrics_box.pack(side="left", padx=(0, 14))

            vis_fmt = f"{item['visitas']:,}".replace(",", ".")
            ctk.CTkLabel(
                metrics_box,
                text=t("ranking_visitas_qtd", n=vis_fmt),
                font=fonte(16, "bold"),
                text_color=TEXT_KPI,
            ).pack(anchor="e")
            ctk.CTkLabel(
                metrics_box,
                text=f"★ {item['nota_media']:.2f}",
                font=fonte(13, "bold"),
                text_color=AMBER,
            ).pack(anchor="e", pady=(2, 0))

            if loc_obj is not None:
                acoes = ctk.CTkFrame(row_in, fg_color="transparent")
                acoes.pack(side="right")

                presente = self._no_roteiro(loc_obj)
                btn_rot = ctk.CTkButton(
                    acoes,
                    text=t("btn_no_roteiro") if presente else t("btn_add_roteiro"),
                    width=105,
                    height=36,
                    corner_radius=8,
                    fg_color=TERTIARY_CONTAINER if presente else PRIMARY_BTN,
                    hover_color=TERTIARY if presente else PRIMARY_HOVER,
                    text_color="#FFFFFF",
                    font=fonte(12, "bold"),
                )
                btn_rot.configure(command=lambda l=loc_obj, b=btn_rot: self.alternar_roteiro_btn(l, b, estilo="card"))
                btn_rot.pack(side="left", padx=(0, 8))

                ctk.CTkButton(
                    acoes,
                    text=t("btn_detalhes"),
                    width=88,
                    height=36,
                    corner_radius=8,
                    fg_color=BTN_SECONDARY_BG,
                    border_width=1,
                    border_color=BTN_SECONDARY_BORDER,
                    hover_color=BTN_SECONDARY_HOVER,
                    text_color=BTN_SECONDARY_TEXT,
                    font=fonte(12, "bold"),
                    command=lambda l=loc_obj: self.mostrar_detalhes(l, voltar=self.mostrar_mais_visitados),
                ).pack(side="left")

    # ==================================================================
    # 7. Helper Geral de Alternância de Roteiro (compatível com i18n)
    # ==================================================================
    def alternar_roteiro_btn(
        self,
        local: Dict[str, Any],
        botao: Optional[ctk.CTkButton] = None,
        estilo: str = "card",
    ):
        """Adiciona ou remove do roteiro de forma reativa com feedback multilíngue."""
        presente = self._no_roteiro(local)
        if presente:
            self.roteiro = remover(self.roteiro, local["id"], usuario_id=self.usuario_id)
            self._toast(t("toast_rem_roteiro", nome=local["nome"]))
            if botao:
                if estilo == "fav":
                    botao.configure(
                        text=t("btn_salvar_fav"),
                        fg_color=BTN_SECONDARY_BG,
                        hover_color=BTN_SECONDARY_HOVER,
                        text_color=BTN_SECONDARY_TEXT,
                    )
                elif estilo == "detalhe":
                    botao.configure(
                        text=t("detalhes_add_roteiro"),
                        fg_color=PRIMARY_BTN,
                        hover_color=PRIMARY_HOVER,
                        text_color="#FFFFFF",
                    )
                else:
                    botao.configure(
                        text=t("btn_add_roteiro"),
                        fg_color=PRIMARY_BTN,
                        hover_color=PRIMARY_HOVER,
                        text_color="#FFFFFF",
                    )
        else:
            self.roteiro = adicionar(self.roteiro, local, usuario_id=self.usuario_id)
            self._toast(t("toast_add_roteiro", nome=local["nome"]), cor_bg=TERTIARY_CONTAINER)
            if botao:
                if estilo == "fav":
                    botao.configure(
                        text=t("btn_salvo_roteiro"),
                        fg_color=TERTIARY_FIXED,
                        hover_color=SECONDARY_FIXED,
                        text_color=ON_TERTIARY_FIXED,
                    )
                elif estilo == "detalhe":
                    botao.configure(
                        text=t("detalhes_salvo_roteiro"),
                        fg_color=TERTIARY_CONTAINER,
                        hover_color=TERTIARY,
                        text_color="#FFFFFF",
                    )
                else:
                    botao.configure(
                        text=t("btn_no_roteiro"),
                        fg_color=TERTIARY_CONTAINER,
                        hover_color=TERTIARY,
                        text_color="#FFFFFF",
                    )

        if hasattr(self, "btn_salvos_pill"):
            self.btn_salvos_pill.configure(text=t("btn_salvos_nav", n=len(self.roteiro)))
        self._invalidar_cache_telas()


if __name__ == "__main__":
    app = BelemNaMaoApp()
    app.mainloop()
