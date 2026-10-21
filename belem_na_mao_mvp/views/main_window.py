# import tkinter as tk
# from tkinter import messagebox
# import customtkinter as ctk

# from services.catalogo import carregar_locais, buscar_locais, rotulo_preco
# from services.roteiro import carregar_roteiro, adicionar, remover

# BG = "#F5F6F8"
# PANEL = "#FFFFFF"
# PRIMARY = "#062454"
# PRIMARY_HOVER = "#041838"
# ACCENT_BLUE = "#587CA8"
# TEXT = "#161D27"
# MUTED = "#606B7A"
# ACCENT = "#8F151B"
# ACCENT_HOVER = "#6D1014"


# class BelemNaMaoApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("BelémNaMão")
#         self.geometry("1180x760")
#         self.minsize(960, 620)
#         self.configure(fg_color=BG)

#         self.locais = carregar_locais()
#         self.roteiro = carregar_roteiro()
#         self.tela_atual = "Início"
#         self.local_selecionado = None

#         self.grid_columnconfigure(1, weight=1)
#         self.grid_rowconfigure(0, weight=1)

#         self._criar_menu()
#         self.conteudo = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
#         self.conteudo.grid(row=0, column=1, sticky="nsew", padx=26, pady=24)
#         self.mostrar_inicio()

#     def _criar_menu(self):
#         menu = ctk.CTkFrame(self, width=220, fg_color=PRIMARY, corner_radius=0)
#         menu.grid(row=0, column=0, sticky="nsew")
#         menu.grid_propagate(False)

#         logo = ctk.CTkLabel(
#             menu,
#             text="◉  Belém\n    na Mão",
#             font=ctk.CTkFont(size=27, weight="bold"),
#             text_color="#FFFFFF",
#             justify="left",
#         )
#         logo.pack(anchor="w", padx=24, pady=(35, 8))
#         ctk.CTkLabel(
#             menu,
#             text="DESCUBRA DO SEU JEITO",
#             font=ctk.CTkFont(size=10, weight="bold"),
#             text_color="#CCDBEB",
#         ).pack(anchor="w", padx=25, pady=(0, 32))

#         for texto, comando in [
#             ("⌂   Início", self.mostrar_inicio),
#             ("⌕   Explorar locais", self.mostrar_explorar),
#             ("♡   Meu roteiro", self.mostrar_roteiro),
#         ]:
#             ctk.CTkButton(
#                 menu,
#                 text=texto,
#                 anchor="w",
#                 height=44,
#                 corner_radius=10,
#                 fg_color="transparent",
#                 hover_color=PRIMARY_HOVER,
#                 font=ctk.CTkFont(size=15),
#                 command=comando,
#             ).pack(fill="x", padx=14, pady=4)

#         menu_spacer = ctk.CTkFrame(menu, fg_color="transparent")
#         menu_spacer.pack(expand=True, fill="both")
#         ctk.CTkLabel(
#             menu,
#             text="MVP demonstrativo\nBelém, Pará",
#             text_color="#CCDBEB",
#             font=ctk.CTkFont(size=11),
#             justify="left",
#         ).pack(anchor="w", padx=24, pady=22)

#     def _limpar(self):
#         for widget in self.conteudo.winfo_children():
#             widget.destroy()

#     def _titulo(self, titulo, subtitulo=None):
#         ctk.CTkLabel(
#             self.conteudo,
#             text=titulo,
#             text_color=TEXT,
#             font=ctk.CTkFont(size=29, weight="bold"),
#         ).pack(anchor="w", pady=(3, 4))
#         if subtitulo:
#             ctk.CTkLabel(
#                 self.conteudo,
#                 text=subtitulo,
#                 text_color=MUTED,
#                 font=ctk.CTkFont(size=14),
#             ).pack(anchor="w", pady=(0, 18))

#     def _botao(self, master, texto, comando, width=140, fg_color=None, hover_color=None):
#         cor_fundo = fg_color or PRIMARY
#         cor_hover = hover_color or PRIMARY_HOVER
#         return ctk.CTkButton(
#             master,
#             text=texto,
#             command=comando,
#             width=width,
#             height=38,
#             corner_radius=10,
#             fg_color=cor_fundo,
#             hover_color=cor_hover,
#         )

#     def mostrar_inicio(self):
#         self._limpar()
#         self.tela_atual = "Início"
#         self._titulo(
#             "Descubra Belém do seu jeito",
#             "Encontre lugares, sabores e experiências para montar seu passeio.",
#         )
#         hero = ctk.CTkFrame(self.conteudo, fg_color=PRIMARY, corner_radius=18)
#         hero.pack(fill="x", pady=(0, 22))
#         ctk.CTkLabel(
#             hero,
#             text="Belém na Mão",
#             text_color="white",
#             font=ctk.CTkFont(size=28, weight="bold"),
#         ).pack(anchor="w", padx=24, pady=(22, 3))
#         ctk.CTkLabel(
#             hero,
#             text="Menos tempo procurando. Mais tempo vivendo Belém.",
#             text_color="#CCDBEB",
#             font=ctk.CTkFont(size=15),
#         ).pack(anchor="w", padx=24, pady=(0, 20))

#         ctk.CTkLabel(
#             self.conteudo,
#             text="O que você quer fazer?",
#             text_color=TEXT,
#             font=ctk.CTkFont(size=20, weight="bold"),
#         ).pack(anchor="w", pady=(0, 12))
#         grid = ctk.CTkFrame(self.conteudo, fg_color="transparent")
#         grid.pack(fill="x")
#         categories = [
#             ("🍴", "Gastronomia", "Sabores paraenses"),
#             ("🏛", "Cultura", "História e patrimônio"),
#             ("🌿", "Natureza", "Verde e ar livre"),
#             ("🧭", "Passeio", "Conheça a cidade"),
#         ]
#         for i, (emoji, cat, desc) in enumerate(categories):
#             card = ctk.CTkFrame(
#                 grid,
#                 fg_color=PANEL,
#                 corner_radius=14,
#                 border_width=1,
#                 border_color="#CCDBEB",
#             )
#             card.grid(row=i // 2, column=i % 2, sticky="nsew", padx=(0, 12), pady=(0, 12))
#             ctk.CTkLabel(card, text=emoji, font=ctk.CTkFont(size=28)).pack(anchor="w", padx=17, pady=(14, 2))
#             ctk.CTkLabel(card, text=cat, text_color=TEXT, font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", padx=17)
#             ctk.CTkLabel(card, text=desc, text_color=MUTED, font=ctk.CTkFont(size=12)).pack(anchor="w", padx=17, pady=(1, 12))
#             self._botao(card, "Explorar", lambda c=cat: self.mostrar_explorar(c)).pack(anchor="w", padx=17, pady=(0, 15))
#         grid.grid_columnconfigure((0, 1), weight=1)

#         self._botao(self.conteudo, "Ver todos os locais  →", self.mostrar_explorar, width=220).pack(anchor="w", pady=(4, 0))

#     def mostrar_explorar(self, categoria_inicial="Todas"):
#         self._limpar()
#         self.tela_atual = "Explorar"
#         self._titulo(
#             "Explorar locais",
#             "Filtre o catálogo de demonstração para encontrar sua próxima experiência.",
#         )

#         filtros = ctk.CTkFrame(self.conteudo, fg_color="transparent")
#         filtros.pack(fill="x", pady=(0, 14))
#         busca = ctk.CTkEntry(filtros, placeholder_text="Buscar por nome, bairro ou palavra-chave", height=40)
#         busca.pack(side="left", fill="x", expand=True, padx=(0, 8))
#         categoria = ctk.CTkOptionMenu(
#             filtros,
#             values=["Todas", "Gastronomia", "Cultura", "História", "Natureza", "Passeio"],
#             width=150,
#             height=40,
#             fg_color=PRIMARY,
#             button_color=PRIMARY_HOVER,
#         )
#         categoria.set(categoria_inicial)
#         categoria.pack(side="left", padx=(0, 8))
#         preco = ctk.CTkOptionMenu(
#             filtros,
#             values=["Qualquer", "Baixo", "Médio", "Alto"],
#             width=120,
#             height=40,
#             fg_color=PRIMARY,
#             button_color=PRIMARY_HOVER,
#         )
#         preco.pack(side="left", padx=(0, 8))
#         resultado_frame = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
#         resultado_frame.pack(fill="both", expand=True)

#         def renderizar():
#             for child in resultado_frame.winfo_children():
#                 child.destroy()
#             encontrados = buscar_locais(self.locais, busca.get(), categoria.get(), preco.get())
#             if not encontrados:
#                 ctk.CTkLabel(
#                     resultado_frame,
#                     text="Nenhum local encontrado. Tente outros filtros.",
#                     text_color=MUTED,
#                 ).pack(anchor="w", padx=8, pady=20)
#                 return
#             for local in encontrados:
#                 card = ctk.CTkFrame(
#                     resultado_frame,
#                     fg_color=PANEL,
#                     corner_radius=14,
#                     border_width=1,
#                     border_color="#CADDEE",
#                 )
#                 card.pack(fill="x", pady=6)
#                 left = ctk.CTkFrame(card, fg_color="#CCDBEB", corner_radius=10, width=82, height=82)
#                 left.pack(side="left", padx=14, pady=14)
#                 left.pack_propagate(False)
#                 ctk.CTkLabel(left, text="✦", font=ctk.CTkFont(size=30), text_color=PRIMARY).pack(expand=True)
#                 info = ctk.CTkFrame(card, fg_color="transparent")
#                 info.pack(side="left", fill="both", expand=True, pady=14)
#                 ctk.CTkLabel(
#                     info,
#                     text=local["nome"],
#                     text_color=TEXT,
#                     font=ctk.CTkFont(size=17, weight="bold"),
#                 ).pack(anchor="w")
#                 ctk.CTkLabel(
#                     info,
#                     text=f'{local["bairro"]}  •  {", ".join(local["categoria"])}',
#                     text_color=MUTED,
#                     font=ctk.CTkFont(size=12),
#                 ).pack(anchor="w", pady=2)
#                 ctk.CTkLabel(
#                     info,
#                     text=local["descricao"],
#                     text_color=TEXT,
#                     wraplength=460,
#                     justify="left",
#                     font=ctk.CTkFont(size=12),
#                 ).pack(anchor="w", pady=(2, 0))
#                 actions = ctk.CTkFrame(card, fg_color="transparent")
#                 actions.pack(side="right", padx=14)
#                 ctk.CTkLabel(actions, text=rotulo_preco(local.get("preco")), text_color=MUTED).pack(pady=(0, 8))
#                 self._botao(
#                     actions,
#                     "Ver detalhes",
#                     lambda item=local: self.mostrar_detalhes(item),
#                     width=120,
#                 ).pack(pady=3)
#                 self._botao(
#                     actions,
#                     "+ Roteiro",
#                     lambda item=local: self.adicionar_roteiro(item),
#                     width=120,
#                     fg_color=ACCENT,
#                     hover_color=ACCENT_HOVER,
#                 ).pack(pady=3)

#         self._botao(filtros, "Filtrar", renderizar, width=85).pack(side="left")
#         busca.bind("<Return>", lambda _event: renderizar())
#         categoria.configure(command=lambda _value: renderizar())
#         preco.configure(command=lambda _value: renderizar())
#         renderizar()

#     def mostrar_detalhes(self, local):
#         janela = ctk.CTkToplevel(self)
#         janela.title(local["nome"])
#         janela.geometry("580x570")
#         janela.minsize(500, 480)
#         janela.configure(fg_color=BG)
#         janela.transient(self)
#         ctk.CTkLabel(
#             janela,
#             text=local["nome"],
#             text_color=TEXT,
#             font=ctk.CTkFont(size=26, weight="bold"),
#             wraplength=520,
#         ).pack(anchor="w", padx=24, pady=(24, 6))
#         ctk.CTkLabel(
#             janela,
#             text=f'{local["bairro"]}  •  {", ".join(local["categoria"])}  •  {rotulo_preco(local.get("preco"))}',
#             text_color=MUTED,
#             font=ctk.CTkFont(size=13),
#         ).pack(anchor="w", padx=24, pady=(0, 18))
#         box = ctk.CTkFrame(janela, fg_color=PANEL, corner_radius=14)
#         box.pack(fill="both", expand=True, padx=24, pady=(0, 16))
#         for titulo, texto in [
#             ("Sobre o lugar", local["descricao"]),
#             ("Por que visitar?", local["por_que_visitar"]),
#             ("Tempo sugerido", local["duracao"]),
#             ("Localização / observações", local["endereco"]),
#         ]:
#             ctk.CTkLabel(
#                 box,
#                 text=titulo,
#                 text_color=PRIMARY,
#                 font=ctk.CTkFont(size=14, weight="bold"),
#             ).pack(anchor="w", padx=16, pady=(13, 2))
#             ctk.CTkLabel(
#                 box,
#                 text=texto,
#                 text_color=TEXT,
#                 font=ctk.CTkFont(size=13),
#                 justify="left",
#                 wraplength=475,
#             ).pack(anchor="w", padx=16)
#         self._botao(
#             janela,
#             "Adicionar ao meu roteiro",
#             lambda: (self.adicionar_roteiro(local), janela.destroy()),
#             fg_color=ACCENT,
#             hover_color=ACCENT_HOVER,
#         ).pack(anchor="e", padx=24, pady=(0, 20))

#     def adicionar_roteiro(self, local):
#         ja_existe = any(item.get("id") == local.get("id") for item in self.roteiro)
#         self.roteiro = adicionar(self.roteiro, local)
#         if ja_existe:
#             messagebox.showinfo("Meu roteiro", "Esse local já está no seu roteiro.")
#         else:
#             messagebox.showinfo("Meu roteiro", f'{local["nome"]} foi adicionado ao roteiro.')

#     def mostrar_roteiro(self):
#         self._limpar()
#         self.tela_atual = "Meu roteiro"
#         self._titulo(
#             "Meu roteiro",
#             "Organize os lugares que deseja conhecer. As alterações ficam salvas neste computador.",
#         )
#         if not self.roteiro:
#             ctk.CTkLabel(
#                 self.conteudo,
#                 text="Seu roteiro ainda está vazio.",
#                 text_color=TEXT,
#                 font=ctk.CTkFont(size=18, weight="bold"),
#             ).pack(anchor="w", pady=(20, 6))
#             ctk.CTkLabel(
#                 self.conteudo,
#                 text="Explore os locais e adicione os que chamarem sua atenção.",
#                 text_color=MUTED,
#             ).pack(anchor="w", pady=(0, 16))
#             self._botao(self.conteudo, "Explorar locais", self.mostrar_explorar, width=180).pack(anchor="w")
#             return

#         lista = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
#         lista.pack(fill="both", expand=True)
#         for indice, local in enumerate(self.roteiro, start=1):
#             card = ctk.CTkFrame(
#                 lista,
#                 fg_color=PANEL,
#                 corner_radius=12,
#                 border_width=1,
#                 border_color="#CDDEF8",
#             )
#             card.pack(fill="x", pady=6)
#             ctk.CTkLabel(
#                 card,
#                 text=f"{indice:02d}",
#                 text_color=PRIMARY,
#                 font=ctk.CTkFont(size=22, weight="bold"),
#                 width=55,
#             ).pack(side="left", padx=12, pady=16)
#             info = ctk.CTkFrame(card, fg_color="transparent")
#             info.pack(side="left", fill="x", expand=True, pady=14)
#             ctk.CTkLabel(
#                 info,
#                 text=local["nome"],
#                 text_color=TEXT,
#                 font=ctk.CTkFont(size=16, weight="bold"),
#             ).pack(anchor="w")
#             ctk.CTkLabel(
#                 info,
#                 text=f'{local["bairro"]}  •  {local["duracao"]}',
#                 text_color=MUTED,
#                 font=ctk.CTkFont(size=12),
#             ).pack(anchor="w", pady=(3, 0))
#             self._botao(
#                 card,
#                 "Ver detalhes",
#                 lambda item=local: self.mostrar_detalhes(item),
#                 width=110,
#             ).pack(side="right", padx=8)
#             self._botao(
#                 card,
#                 "Remover",
#                 lambda item_id=local["id"]: self._remover_e_atualizar(item_id),
#                 width=90,
#             ).pack(side="right", padx=(0, 14))

#         bottom = ctk.CTkFrame(self.conteudo, fg_color="transparent")
#         bottom.pack(fill="x", pady=(12, 0))
#         ctk.CTkLabel(
#             bottom,
#             text=f"{len(self.roteiro)} local(is) no roteiro",
#             text_color=MUTED,
#         ).pack(side="left")
#         self._botao(bottom, "Limpar roteiro", self.limpar_roteiro, width=130).pack(side="right")

#     def _remover_e_atualizar(self, local_id):
#         self.roteiro = remover(self.roteiro, local_id)
#         self.mostrar_roteiro()

#     def limpar_roteiro(self):
#         if messagebox.askyesno("Limpar roteiro", "Deseja remover todos os locais do roteiro?"):
#             self.roteiro = []
#             from services.roteiro import salvar_roteiro

#             salvar_roteiro(self.roteiro)
#             self.mostrar_roteiro()

import customtkinter as ctk

from services.catalogo import carregar_locais, buscar_locais, rotulo_preco
from services.roteiro import carregar_roteiro, adicionar, remover, salvar_roteiro, limpar

# ---------- Paleta ----------
BG = "#F3F5F9"
PANEL = "#FFFFFF"
PRIMARY = "#062454"
PRIMARY_HOVER = "#0B3277"
PRIMARY_SOFT = "#E3EAF5"
ACCENT = "#8F151B"
ACCENT_HOVER = "#6D1014"
ACCENT_SOFT = "#F8E6E7"
TEXT = "#161D27"
MUTED = "#6B7686"
LINE = "#E4E8EF"
ON_PRIMARY_MUTED = "#B9C8E0"

FONT = "Segoe UI"

# Emoji e cor de destaque por categoria
CATEGORIAS = {
    "Gastronomia": ("🍴", "#FBE9D9"),
    "Cultura": ("🏛", "#E6E9F8"),
    "História": ("📜", "#F3EAD7"),
    "Natureza": ("🌿", "#DFF1E3"),
    "Passeio": ("🧭", "#DDEEF6"),
}
DESCRICOES = {
    "Gastronomia": "Sabores paraenses",
    "Cultura": "Arte e patrimônio",
    "História": "Memória da cidade",
    "Natureza": "Verde e ar livre",
    "Passeio": "Conheça a cidade",
}


def estilo_local(local):
    cats = local.get("categoria") or []
    for c in cats:
        if c in CATEGORIAS:
            return CATEGORIAS[c]
    return ("✦", PRIMARY_SOFT)


def fonte(size=14, weight="normal"):
    return ctk.CTkFont(family=FONT, size=size, weight=weight)


class BelemNaMaoApp(ctk.CTk):
    LARGURA = 430
    ALTURA = 860

    def __init__(self, usuario=None):
        super().__init__()
        self.usuario = usuario or {"id": 1, "nome": "Visitante", "usuario": "visitante"}
        self.usuario_id = self.usuario.get("id", 1)
        self.title("BelémNaMão")
        self.geometry(f"{self.LARGURA}x{self.ALTURA}")
        self.minsize(380, 680)
        self.configure(fg_color=BG)

        self.locais = carregar_locais()
        self.roteiro = carregar_roteiro(usuario_id=self.usuario_id)
        self.aba_atual = "Início"

        # Estado dos filtros (mantido ao navegar)
        self.f_texto = ""
        self.f_categoria = "Todas"
        self.f_preco = "Qualquer"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.conteudo = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.conteudo.grid(row=0, column=0, sticky="nsew")
        self._criar_navegacao()
        self.mostrar_inicio()

    # ------------------------------------------------------------------
    # Estrutura comum
    # ------------------------------------------------------------------
    def _criar_navegacao(self):
        barra = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=0, height=74,
                             border_width=1, border_color=LINE)
        barra.grid(row=1, column=0, sticky="ew")
        barra.grid_propagate(False)
        barra.grid_rowconfigure(0, weight=1)
        self.abas = {}
        itens = [
            ("Início", "⌂", self.mostrar_inicio),
            ("Explorar", "⌕", self.mostrar_explorar),
            ("Roteiro", "♡", self.mostrar_roteiro),
        ]
        for i, (nome, icone, cmd) in enumerate(itens):
            barra.grid_columnconfigure(i, weight=1, uniform="aba")
            btn = ctk.CTkButton(
                barra, text=f"{icone}\n{nome}", font=fonte(12, "bold"),
                height=56, corner_radius=18, fg_color="transparent",
                text_color=MUTED, hover_color=PRIMARY_SOFT, command=cmd,
            )
            btn.grid(row=0, column=i, padx=8, pady=9, sticky="ew")
            self.abas[nome] = btn

    def _marcar_aba(self, nome):
        self.aba_atual = nome
        for n, btn in self.abas.items():
            ativo = n == nome
            btn.configure(
                fg_color=PRIMARY_SOFT if ativo else "transparent",
                text_color=PRIMARY if ativo else MUTED,
            )

    def _limpar(self):
        for w in self.conteudo.winfo_children():
            w.destroy()

    def _cabecalho(self, titulo, subtitulo=None, voltar=None):
        topo = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        topo.pack(fill="x", padx=20, pady=(22, 10))
        if voltar:
            ctk.CTkButton(
                topo, text="‹", width=40, height=40, corner_radius=20,
                font=fonte(24, "bold"), fg_color=PANEL, text_color=PRIMARY,
                hover_color=PRIMARY_SOFT, border_width=1, border_color=LINE,
                command=voltar,
            ).pack(anchor="w", pady=(0, 10))
        ctk.CTkLabel(topo, text=titulo, font=fonte(28, "bold"), text_color=TEXT,
                     justify="left", anchor="w", wraplength=self.LARGURA - 60).pack(anchor="w")
        if subtitulo:
            ctk.CTkLabel(topo, text=subtitulo, font=fonte(13), text_color=MUTED,
                         justify="left", anchor="w", wraplength=self.LARGURA - 60
                         ).pack(anchor="w", pady=(3, 0))

    def _botao(self, master, texto, comando, largura=140, altura=44,
               cor=PRIMARY, hover=PRIMARY_HOVER, texto_cor="#FFFFFF"):
        return ctk.CTkButton(
            master, text=texto, command=comando, width=largura, height=altura,
            corner_radius=altura // 2, fg_color=cor, hover_color=hover,
            text_color=texto_cor, font=fonte(14, "bold"),
        )

    def _toast(self, mensagem):
        toast = ctk.CTkLabel(
            self, text=mensagem, fg_color=TEXT, text_color="#FFFFFF",
            corner_radius=18, font=fonte(13, "bold"), height=40,
            padx=20, wraplength=self.LARGURA - 90,
        )
        toast.place(relx=0.5, rely=1.0, y=-92, anchor="s")
        self.after(2200, toast.destroy)

    def _no_roteiro(self, local):
        return any(i.get("id") == local.get("id") for i in self.roteiro)

    # ------------------------------------------------------------------
    # Início
    # ------------------------------------------------------------------
    def mostrar_inicio(self):
        self._limpar()
        self._marcar_aba("Início")
        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True)

        hero = ctk.CTkFrame(rolagem, fg_color=PRIMARY, corner_radius=28)
        hero.pack(fill="x", padx=16, pady=(16, 8))
        nome_usuario = self.usuario.get("nome", "Visitante")
        ctk.CTkLabel(hero, text=f"◉ Belém na Mão  •  Olá, {nome_usuario}", font=fonte(13, "bold"),
                     text_color=ON_PRIMARY_MUTED).pack(anchor="w", padx=22, pady=(22, 0))
        ctk.CTkLabel(hero, text="Descubra Belém\ndo seu jeito", font=fonte(30, "bold"),
                     text_color="#FFFFFF", justify="left").pack(anchor="w", padx=22, pady=(6, 4))
        ctk.CTkLabel(hero, text="Menos tempo procurando.\nMais tempo vivendo a cidade.",
                     font=fonte(13), text_color=ON_PRIMARY_MUTED, justify="left"
                     ).pack(anchor="w", padx=22)
        self._botao(hero, "Explorar locais", self.mostrar_explorar, largura=170,
                    cor="#FFFFFF", hover=PRIMARY_SOFT, texto_cor=PRIMARY
                    ).pack(anchor="w", padx=22, pady=(18, 22))

        self._secao(rolagem, "O que você quer fazer?")
        grade = ctk.CTkFrame(rolagem, fg_color="transparent")
        grade.pack(fill="x", padx=16)
        grade.grid_columnconfigure((0, 1), weight=1, uniform="cat")
        for i, (nome, (emoji, cor)) in enumerate(CATEGORIAS.items()):
            if i == 4:  # 5ª categoria ocupa a linha inteira
                span, col = 2, 0
            else:
                span, col = 1, i % 2
            card = ctk.CTkFrame(grade, fg_color=cor, corner_radius=22, cursor="hand2")
            card.grid(row=i // 2, column=col, columnspan=span, sticky="nsew",
                      padx=4, pady=4)
            ctk.CTkLabel(card, text=emoji, font=fonte(30)).pack(anchor="w", padx=16, pady=(14, 0))
            ctk.CTkLabel(card, text=nome, font=fonte(16, "bold"),
                         text_color=TEXT).pack(anchor="w", padx=16)
            ctk.CTkLabel(card, text=DESCRICOES[nome], font=fonte(12),
                         text_color=MUTED).pack(anchor="w", padx=16, pady=(0, 14))
            for w in (card, *card.winfo_children()):
                w.bind("<Button-1>", lambda _e, c=nome: self._ir_para_categoria(c))

        destaques = self.locais[:6]
        if destaques:
            self._secao(rolagem, "Para começar")
            carrossel = ctk.CTkScrollableFrame(rolagem, orientation="horizontal", height=170,
                                               fg_color="transparent", corner_radius=0)
            carrossel.pack(fill="x", padx=10)
            for local in destaques:
                self._card_destaque(carrossel, local)

    def _secao(self, master, texto):
        ctk.CTkLabel(master, text=texto, font=fonte(19, "bold"), text_color=TEXT
                     ).pack(anchor="w", padx=20, pady=(22, 8))

    def _card_destaque(self, master, local):
        emoji, cor = estilo_local(local)
        card = ctk.CTkFrame(master, fg_color=PANEL, corner_radius=22, width=200, height=150,
                            border_width=1, border_color=LINE, cursor="hand2")
        card.pack(side="left", padx=6, pady=4)
        card.pack_propagate(False)
        topo = ctk.CTkFrame(card, fg_color=cor, corner_radius=16, height=62)
        topo.pack(fill="x", padx=8, pady=(8, 0))
        topo.pack_propagate(False)
        ctk.CTkLabel(topo, text=emoji, font=fonte(28)).pack(expand=True)
        ctk.CTkLabel(card, text=local["nome"], font=fonte(14, "bold"), text_color=TEXT,
                     wraplength=170, justify="left", anchor="w").pack(anchor="w", padx=14, pady=(8, 0))
        ctk.CTkLabel(card, text=local["bairro"], font=fonte(12), text_color=MUTED
                     ).pack(anchor="w", padx=14)
        for w in (card, *card.winfo_children()):
            w.bind("<Button-1>", lambda _e, l=local: self.mostrar_detalhes(l, self.mostrar_inicio))

    def _ir_para_categoria(self, categoria):
        self.f_categoria = categoria
        self.f_texto = ""
        self.f_preco = "Qualquer"
        self.mostrar_explorar()

    # ------------------------------------------------------------------
    # Explorar
    # ------------------------------------------------------------------
    def mostrar_explorar(self):
        self._limpar()
        self._marcar_aba("Explorar")
        self._cabecalho("Explorar", "Lugares, sabores e experiências em Belém")

        busca = ctk.CTkEntry(
            self.conteudo, placeholder_text="🔍  Buscar por nome, bairro ou palavra-chave",
            height=48, corner_radius=24, fg_color=PANEL, border_color=LINE,
            border_width=1, text_color=TEXT, font=fonte(13),
        )
        busca.pack(fill="x", padx=20, pady=(0, 10))
        if self.f_texto:
            busca.insert(0, self.f_texto)

        chips = ctk.CTkScrollableFrame(self.conteudo, orientation="horizontal", height=44,
                                       fg_color="transparent", corner_radius=0)
        chips.pack(fill="x", padx=14)
        botoes_chip = {}

        def pintar_chips():
            for nome, b in botoes_chip.items():
                ativo = nome == self.f_categoria
                b.configure(fg_color=PRIMARY if ativo else PANEL,
                            text_color="#FFFFFF" if ativo else TEXT,
                            border_color=PRIMARY if ativo else LINE)

        def escolher(nome):
            self.f_categoria = nome
            pintar_chips()
            renderizar()

        for nome in ["Todas", *CATEGORIAS.keys()]:
            b = ctk.CTkButton(chips, text=nome, height=34, corner_radius=17, border_width=1,
                              font=fonte(13, "bold"), hover_color=PRIMARY_SOFT,
                              width=len(nome) * 8 + 34, command=lambda n=nome: escolher(n))
            b.pack(side="left", padx=4)
            botoes_chip[nome] = b
        pintar_chips()

        preco = ctk.CTkSegmentedButton(
            self.conteudo, values=["Qualquer", "Baixo", "Médio", "Alto"], height=34,
            corner_radius=17, fg_color=PRIMARY_SOFT, selected_color=PRIMARY,
            selected_hover_color=PRIMARY_HOVER, unselected_color=PRIMARY_SOFT,
            unselected_hover_color="#D3DEEE", text_color=TEXT, font=fonte(12, "bold"),
            command=lambda v: (setattr(self, "f_preco", v), renderizar()),
        )
        preco.set(self.f_preco)
        preco.pack(fill="x", padx=20, pady=(8, 6))

        resultado = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        resultado.pack(fill="both", expand=True, padx=8)

        def renderizar(_evt=None):
            self.f_texto = busca.get().strip()
            for c in resultado.winfo_children():
                c.destroy()
            achados = buscar_locais(self.locais, self.f_texto, self.f_categoria, self.f_preco)
            if not achados:
                self._vazio(resultado, "🔎", "Nenhum local encontrado",
                            "Tente outro termo ou remova algum filtro.")
                return
            for local in achados:
                self._card_local(resultado, local)

        busca.bind("<KeyRelease>", renderizar)
        renderizar()

    def _vazio(self, master, emoji, titulo, texto):
        caixa = ctk.CTkFrame(master, fg_color="transparent")
        caixa.pack(pady=50)
        ctk.CTkLabel(caixa, text=emoji, font=fonte(44)).pack()
        ctk.CTkLabel(caixa, text=titulo, font=fonte(18, "bold"), text_color=TEXT).pack(pady=(8, 2))
        ctk.CTkLabel(caixa, text=texto, font=fonte(13), text_color=MUTED,
                     wraplength=300).pack()
        return caixa

    def _card_local(self, master, local):
        emoji, cor = estilo_local(local)
        card = ctk.CTkFrame(master, fg_color=PANEL, corner_radius=22, border_width=1,
                            border_color=LINE, cursor="hand2")
        card.pack(fill="x", padx=8, pady=6)

        tile = ctk.CTkFrame(card, fg_color=cor, corner_radius=18, width=72, height=72)
        tile.pack(side="left", padx=12, pady=12)
        tile.pack_propagate(False)
        ctk.CTkLabel(tile, text=emoji, font=fonte(30)).pack(expand=True)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=12)
        ctk.CTkLabel(info, text=local["nome"], font=fonte(15, "bold"), text_color=TEXT,
                     wraplength=190, justify="left", anchor="w").pack(anchor="w")
        ctk.CTkLabel(info, text=f'{local["bairro"]}  •  {rotulo_preco(local.get("preco"))}',
                     font=fonte(12), text_color=MUTED, anchor="w").pack(anchor="w", pady=(1, 3))
        ctk.CTkLabel(info, text="  ".join(local["categoria"]), font=fonte(11, "bold"),
                     text_color=PRIMARY, fg_color=PRIMARY_SOFT, corner_radius=10,
                     padx=8).pack(anchor="w")

        presente = self._no_roteiro(local)
        btn = ctk.CTkButton(
            card, text="✓" if presente else "+", width=40, height=40, corner_radius=20,
            font=fonte(20, "bold"),
            fg_color=PRIMARY_SOFT if presente else ACCENT,
            text_color=PRIMARY if presente else "#FFFFFF",
            hover_color="#D3DEEE" if presente else ACCENT_HOVER,
        )
        btn.configure(command=lambda l=local, b=btn: self.adicionar_roteiro(l, b))
        btn.pack(side="right", padx=12)

        for w in (card, tile, info, *info.winfo_children()):
            w.bind("<Button-1>", lambda _e, l=local: self.mostrar_detalhes(l, self.mostrar_explorar))

    # ------------------------------------------------------------------
    # Detalhes (tela cheia, com botão voltar)
    # ------------------------------------------------------------------
    def mostrar_detalhes(self, local, voltar=None):
        voltar = voltar or self.mostrar_explorar
        self._limpar()
        emoji, cor = estilo_local(local)

        rolagem = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True)

        topo = ctk.CTkFrame(rolagem, fg_color=cor, corner_radius=28, height=180)
        topo.pack(fill="x", padx=16, pady=(16, 0))
        topo.pack_propagate(False)
        ctk.CTkButton(topo, text="‹", width=40, height=40, corner_radius=20, font=fonte(24, "bold"),
                      fg_color=PANEL, text_color=PRIMARY, hover_color=PRIMARY_SOFT,
                      command=voltar).place(x=14, y=14)
        ctk.CTkLabel(topo, text=emoji, font=fonte(64)).place(relx=0.5, rely=0.55, anchor="center")

        ctk.CTkLabel(rolagem, text=local["nome"], font=fonte(26, "bold"), text_color=TEXT,
                     wraplength=self.LARGURA - 70, justify="left", anchor="w"
                     ).pack(anchor="w", padx=22, pady=(16, 2))
        ctk.CTkLabel(rolagem, text=local["bairro"], font=fonte(14), text_color=MUTED
                     ).pack(anchor="w", padx=22)

        linha = ctk.CTkFrame(rolagem, fg_color="transparent")
        linha.pack(anchor="w", padx=18, pady=(10, 4))
        for texto in [*local["categoria"], rotulo_preco(local.get("preco")), local["duracao"]]:
            ctk.CTkLabel(linha, text=str(texto), font=fonte(12, "bold"), text_color=PRIMARY,
                         fg_color=PRIMARY_SOFT, corner_radius=12, padx=10, height=26
                         ).pack(side="left", padx=4)

        for titulo, texto in [
            ("Sobre o lugar", local["descricao"]),
            ("Por que visitar", local["por_que_visitar"]),
            ("Tempo sugerido", local["duracao"]),
            ("Localização e observações", local["endereco"]),
        ]:
            bloco = ctk.CTkFrame(rolagem, fg_color=PANEL, corner_radius=20,
                                 border_width=1, border_color=LINE)
            bloco.pack(fill="x", padx=16, pady=6)
            ctk.CTkLabel(bloco, text=titulo, font=fonte(14, "bold"), text_color=PRIMARY
                         ).pack(anchor="w", padx=16, pady=(14, 2))
            ctk.CTkLabel(bloco, text=texto, font=fonte(13), text_color=TEXT, justify="left",
                         wraplength=self.LARGURA - 100, anchor="w"
                         ).pack(anchor="w", padx=16, pady=(0, 14))

        # Barra de ação fixa
        barra = ctk.CTkFrame(self.conteudo, fg_color=PANEL, corner_radius=0,
                             border_width=1, border_color=LINE)
        barra.pack(fill="x", side="bottom")
        presente = self._no_roteiro(local)
        botao = self._botao(
            barra, "✓  No seu roteiro" if presente else "+  Adicionar ao roteiro",
            None, largura=300, altura=50,
            cor=PRIMARY_SOFT if presente else ACCENT,
            hover="#D3DEEE" if presente else ACCENT_HOVER,
            texto_cor=PRIMARY if presente else "#FFFFFF",
        )
        botao.configure(command=lambda: self._adicionar_na_tela(local, botao))
        botao.pack(fill="x", padx=18, pady=12)

    def _adicionar_na_tela(self, local, botao):
        self.adicionar_roteiro(local, botao=botao)

    # ------------------------------------------------------------------
    # Roteiro
    # ------------------------------------------------------------------
    def adicionar_roteiro(self, local, botao=None):
        """Adiciona diretamente o local ao roteiro sem modal de confirmação."""
        if self._no_roteiro(local):
            self._toast("Esse local já está no seu roteiro")
        else:
            self.roteiro = adicionar(self.roteiro, local, usuario_id=self.usuario_id)
            self._toast(f"✓ {local['nome']} adicionado ao roteiro")
        if botao is not None:
            texto_atual = str(botao.cget("text"))
            if "roteiro" in texto_atual.lower():
                botao.configure(text="✓  No seu roteiro", fg_color=PRIMARY_SOFT,
                                text_color=PRIMARY, hover_color="#D3DEEE")
            else:
                botao.configure(text="✓", fg_color=PRIMARY_SOFT,
                                text_color=PRIMARY, hover_color="#D3DEEE")

    def confirmar_remover_item(self, local):
        """Janela de confirmação para remover um item específico do roteiro."""
        fundo = ctk.CTkFrame(self, fg_color="#0A1020", corner_radius=0)
        fundo.place(relx=0, rely=0, relwidth=1, relheight=1)
        painel = ctk.CTkFrame(fundo, fg_color=PANEL, corner_radius=26)
        painel.place(relx=0.5, rely=0.5, anchor="center")

        emoji, cor = estilo_local(local)
        tile = ctk.CTkFrame(painel, fg_color=cor, corner_radius=18, width=64, height=64)
        tile.pack(pady=(22, 10))
        tile.pack_propagate(False)
        ctk.CTkLabel(tile, text=emoji, font=fonte(28)).pack(expand=True)

        ctk.CTkLabel(painel, text="Remover do roteiro?", font=fonte(20, "bold"), text_color=TEXT
                     ).pack(padx=28, pady=(0, 4))
        ctk.CTkLabel(painel, text=local["nome"], font=fonte(15, "bold"), text_color=ACCENT,
                     wraplength=280).pack(padx=24)
        ctk.CTkLabel(painel, text=f"{local['bairro']}  •  {local.get('duracao', '')}",
                     font=fonte(12), text_color=MUTED).pack(padx=24, pady=(2, 10))

        ctk.CTkLabel(painel, text="Tem certeza que deseja remover este local do seu roteiro?",
                     font=fonte(13), text_color=TEXT, justify="center", wraplength=280).pack(padx=28, pady=(0, 18))

        def confirmar():
            fundo.destroy()
            self._remover_e_atualizar(local["id"])

        botoes = ctk.CTkFrame(painel, fg_color="transparent")
        botoes.pack(padx=22, pady=(0, 22))
        self._botao(botoes, "Cancelar", fundo.destroy, largura=115, cor=PRIMARY_SOFT,
                    hover="#D3DEEE", texto_cor=PRIMARY).pack(side="left", padx=5)
        self._botao(botoes, "Remover", confirmar, largura=115, cor=ACCENT,
                    hover=ACCENT_HOVER).pack(side="left", padx=5)

    def confirmar_salvar_roteiro(self):
        """Menu de confirmação para salvar e consolidar o roteiro no banco de dados SQLite."""
        if not self.roteiro:
            self._toast("Seu roteiro ainda não tem locais para salvar")
            return

        fundo = ctk.CTkFrame(self, fg_color="#0A1020", corner_radius=0)
        fundo.place(relx=0, rely=0, relwidth=1, relheight=1)
        painel = ctk.CTkFrame(fundo, fg_color=PANEL, corner_radius=26)
        painel.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(painel, text="💾", font=fonte(38)).pack(pady=(22, 6))
        ctk.CTkLabel(painel, text="Salvar Roteiro?", font=fonte(20, "bold"), text_color=TEXT
                     ).pack(padx=28, pady=(0, 4))

        total = len(self.roteiro)
        usuario_nome = self.usuario.get("nome", "Visitante")
        ctk.CTkLabel(painel, text=f"Deseja confirmar o salvamento de {total} local(is)\nno perfil de {usuario_nome} no banco de dados?",
                     font=fonte(13), text_color=MUTED, justify="center").pack(padx=24, pady=(4, 18))

        def confirmar():
            salvar_roteiro(self.roteiro)
            fundo.destroy()
            self._toast(f"✓ Roteiro salvo com sucesso ({total} locais)!")

        botoes = ctk.CTkFrame(painel, fg_color="transparent")
        botoes.pack(padx=22, pady=(0, 22))
        self._botao(botoes, "Cancelar", fundo.destroy, largura=115, cor=PRIMARY_SOFT,
                    hover="#D3DEEE", texto_cor=PRIMARY).pack(side="left", padx=5)
        self._botao(botoes, "Confirmar", confirmar, largura=125, cor=PRIMARY,
                    hover=PRIMARY_HOVER).pack(side="left", padx=5)

    def mostrar_roteiro(self):
        self._limpar()
        self._marcar_aba("Roteiro")
        total = len(self.roteiro)
        sub = (f"{total} local(is) salvo(s) no seu roteiro" if total
               else "Os lugares que você salvar aparecem aqui")
        self._cabecalho("Meu roteiro", sub)

        if not self.roteiro:
            caixa = self._vazio(self.conteudo, "🗺", "Seu roteiro está vazio",
                                "Explore os locais e toque em + para salvar os que chamarem sua atenção.")
            self._botao(caixa, "Explorar locais", self.mostrar_explorar, largura=190
                        ).pack(pady=(18, 0))
            return

        lista = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        lista.pack(fill="both", expand=True, padx=8)

        for indice, local in enumerate(self.roteiro, start=1):
            emoji, cor = estilo_local(local)
            card = ctk.CTkFrame(lista, fg_color=PANEL, corner_radius=22,
                                border_width=1, border_color=LINE, cursor="hand2")
            card.pack(fill="x", padx=8, pady=6)
            ctk.CTkLabel(card, text=str(indice), width=34, height=34, corner_radius=17,
                         fg_color=PRIMARY, text_color="#FFFFFF", font=fonte(14, "bold")
                         ).pack(side="left", padx=(14, 6), pady=14)
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, pady=12, padx=(4, 0))
            ctk.CTkLabel(info, text=f'{emoji}  {local["nome"]}', font=fonte(15, "bold"),
                         text_color=TEXT, wraplength=210, justify="left", anchor="w"
                         ).pack(anchor="w")
            ctk.CTkLabel(info, text=f'{local["bairro"]}  •  {local["duracao"]}', font=fonte(12),
                         text_color=MUTED, wraplength=210, justify="left", anchor="w"
                         ).pack(anchor="w", pady=(2, 0))
            ctk.CTkButton(
                card, text="✕", width=36, height=36, corner_radius=18, font=fonte(14, "bold"),
                fg_color=ACCENT_SOFT, text_color=ACCENT, hover_color="#F0CDD0",
                command=lambda l=local: self.confirmar_remover_item(l),
            ).pack(side="right", padx=12)
            for w in (card, info, *info.winfo_children()):
                w.bind("<Button-1>", lambda _e, l=local: self.mostrar_detalhes(l, self.mostrar_roteiro))

        rodape = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        rodape.pack(fill="x", padx=16, pady=(6, 12))
        self._botao(rodape, "Limpar", self.limpar_roteiro, largura=110, altura=40,
                    cor=ACCENT_SOFT, hover="#F0CDD0", texto_cor=ACCENT).pack(side="left", padx=4)
        self._botao(rodape, "💾 Salvar roteiro", self.confirmar_salvar_roteiro, largura=150, altura=40,
                    cor=PRIMARY, hover=PRIMARY_HOVER, texto_cor="#FFFFFF").pack(side="right", padx=4)

    def _remover_e_atualizar(self, local_id):
        self.roteiro = remover(self.roteiro, local_id, usuario_id=self.usuario_id)
        self.mostrar_roteiro()
        self._toast("Local removido do roteiro")

    def limpar_roteiro(self):
        """Confirmação em painel próprio (no lugar do messagebox)."""
        fundo = ctk.CTkFrame(self, fg_color="#0A1020", corner_radius=0)
        fundo.place(relx=0, rely=0, relwidth=1, relheight=1)
        painel = ctk.CTkFrame(fundo, fg_color=PANEL, corner_radius=26)
        painel.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(painel, text="Limpar roteiro?", font=fonte(20, "bold"), text_color=TEXT
                     ).pack(padx=28, pady=(26, 4))
        ctk.CTkLabel(painel, text="Todos os locais salvos serão removidos.",
                     font=fonte(13), text_color=MUTED).pack(padx=28)

        def confirmar():
            self.roteiro = limpar(usuario_id=self.usuario_id)
            fundo.destroy()
            self.mostrar_roteiro()
            self._toast("Roteiro limpo")

        botoes = ctk.CTkFrame(painel, fg_color="transparent")
        botoes.pack(padx=22, pady=22)
        self._botao(botoes, "Cancelar", fundo.destroy, largura=120, cor=PRIMARY_SOFT,
                    hover="#D3DEEE", texto_cor=PRIMARY).pack(side="left", padx=5)
        self._botao(botoes, "Limpar", confirmar, largura=120, cor=ACCENT,
                    hover=ACCENT_HOVER).pack(side="left", padx=5)

# fim