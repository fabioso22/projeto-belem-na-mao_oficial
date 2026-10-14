import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from services.catalogo import carregar_locais, buscar_locais, rotulo_preco
from services.roteiro import carregar_roteiro, adicionar, remover

BG = "#F5F6F8"
PANEL = "#FFFFFF"
PRIMARY = "#062454"
PRIMARY_HOVER = "#041838"
ACCENT_BLUE = "#587CA8"
TEXT = "#161D27"
MUTED = "#606B7A"
ACCENT = "#8F151B"
ACCENT_HOVER = "#6D1014"


class BelemNaMaoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BelémNaMão")
        self.geometry("1180x760")
        self.minsize(960, 620)
        self.configure(fg_color=BG)

        self.locais = carregar_locais()
        self.roteiro = carregar_roteiro()
        self.tela_atual = "Início"
        self.local_selecionado = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._criar_menu()
        self.conteudo = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.conteudo.grid(row=0, column=1, sticky="nsew", padx=26, pady=24)
        self.mostrar_inicio()

    def _criar_menu(self):
        menu = ctk.CTkFrame(self, width=220, fg_color=PRIMARY, corner_radius=0)
        menu.grid(row=0, column=0, sticky="nsew")
        menu.grid_propagate(False)

        logo = ctk.CTkLabel(
            menu,
            text="◉  Belém\n    na Mão",
            font=ctk.CTkFont(size=27, weight="bold"),
            text_color="#FFFFFF",
            justify="left",
        )
        logo.pack(anchor="w", padx=24, pady=(35, 8))
        ctk.CTkLabel(
            menu,
            text="DESCUBRA DO SEU JEITO",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#CCDBEB",
        ).pack(anchor="w", padx=25, pady=(0, 32))

        for texto, comando in [
            ("⌂   Início", self.mostrar_inicio),
            ("⌕   Explorar locais", self.mostrar_explorar),
            ("♡   Meu roteiro", self.mostrar_roteiro),
        ]:
            ctk.CTkButton(
                menu,
                text=texto,
                anchor="w",
                height=44,
                corner_radius=10,
                fg_color="transparent",
                hover_color=PRIMARY_HOVER,
                font=ctk.CTkFont(size=15),
                command=comando,
            ).pack(fill="x", padx=14, pady=4)

        menu_spacer = ctk.CTkFrame(menu, fg_color="transparent")
        menu_spacer.pack(expand=True, fill="both")
        ctk.CTkLabel(
            menu,
            text="MVP demonstrativo\nBelém, Pará",
            text_color="#CCDBEB",
            font=ctk.CTkFont(size=11),
            justify="left",
        ).pack(anchor="w", padx=24, pady=22)

    def _limpar(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def _titulo(self, titulo, subtitulo=None):
        ctk.CTkLabel(
            self.conteudo,
            text=titulo,
            text_color=TEXT,
            font=ctk.CTkFont(size=29, weight="bold"),
        ).pack(anchor="w", pady=(3, 4))
        if subtitulo:
            ctk.CTkLabel(
                self.conteudo,
                text=subtitulo,
                text_color=MUTED,
                font=ctk.CTkFont(size=14),
            ).pack(anchor="w", pady=(0, 18))

    def _botao(self, master, texto, comando, width=140, fg_color=None, hover_color=None):
        cor_fundo = fg_color or PRIMARY
        cor_hover = hover_color or PRIMARY_HOVER
        return ctk.CTkButton(
            master,
            text=texto,
            command=comando,
            width=width,
            height=38,
            corner_radius=10,
            fg_color=cor_fundo,
            hover_color=cor_hover,
        )

    def mostrar_inicio(self):
        self._limpar()
        self.tela_atual = "Início"
        self._titulo(
            "Descubra Belém do seu jeito",
            "Encontre lugares, sabores e experiências para montar seu passeio.",
        )
        hero = ctk.CTkFrame(self.conteudo, fg_color=PRIMARY, corner_radius=18)
        hero.pack(fill="x", pady=(0, 22))
        ctk.CTkLabel(
            hero,
            text="Belém na Mão",
            text_color="white",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(anchor="w", padx=24, pady=(22, 3))
        ctk.CTkLabel(
            hero,
            text="Menos tempo procurando. Mais tempo vivendo Belém.",
            text_color="#CCDBEB",
            font=ctk.CTkFont(size=15),
        ).pack(anchor="w", padx=24, pady=(0, 20))

        ctk.CTkLabel(
            self.conteudo,
            text="O que você quer fazer?",
            text_color=TEXT,
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", pady=(0, 12))
        grid = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        grid.pack(fill="x")
        categories = [
            ("🍴", "Gastronomia", "Sabores paraenses"),
            ("🏛", "Cultura", "História e patrimônio"),
            ("🌿", "Natureza", "Verde e ar livre"),
            ("🧭", "Passeio", "Conheça a cidade"),
        ]
        for i, (emoji, cat, desc) in enumerate(categories):
            card = ctk.CTkFrame(
                grid,
                fg_color=PANEL,
                corner_radius=14,
                border_width=1,
                border_color="#CCDBEB",
            )
            card.grid(row=i // 2, column=i % 2, sticky="nsew", padx=(0, 12), pady=(0, 12))
            ctk.CTkLabel(card, text=emoji, font=ctk.CTkFont(size=28)).pack(anchor="w", padx=17, pady=(14, 2))
            ctk.CTkLabel(card, text=cat, text_color=TEXT, font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", padx=17)
            ctk.CTkLabel(card, text=desc, text_color=MUTED, font=ctk.CTkFont(size=12)).pack(anchor="w", padx=17, pady=(1, 12))
            self._botao(card, "Explorar", lambda c=cat: self.mostrar_explorar(c)).pack(anchor="w", padx=17, pady=(0, 15))
        grid.grid_columnconfigure((0, 1), weight=1)

        self._botao(self.conteudo, "Ver todos os locais  →", self.mostrar_explorar, width=220).pack(anchor="w", pady=(4, 0))

    def mostrar_explorar(self, categoria_inicial="Todas"):
        self._limpar()
        self.tela_atual = "Explorar"
        self._titulo(
            "Explorar locais",
            "Filtre o catálogo de demonstração para encontrar sua próxima experiência.",
        )

        filtros = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        filtros.pack(fill="x", pady=(0, 14))
        busca = ctk.CTkEntry(filtros, placeholder_text="Buscar por nome, bairro ou palavra-chave", height=40)
        busca.pack(side="left", fill="x", expand=True, padx=(0, 8))
        categoria = ctk.CTkOptionMenu(
            filtros,
            values=["Todas", "Gastronomia", "Cultura", "História", "Natureza", "Passeio"],
            width=150,
            height=40,
            fg_color=PRIMARY,
            button_color=PRIMARY_HOVER,
        )
        categoria.set(categoria_inicial)
        categoria.pack(side="left", padx=(0, 8))
        preco = ctk.CTkOptionMenu(
            filtros,
            values=["Qualquer", "Baixo", "Médio", "Alto"],
            width=120,
            height=40,
            fg_color=PRIMARY,
            button_color=PRIMARY_HOVER,
        )
        preco.pack(side="left", padx=(0, 8))
        resultado_frame = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        resultado_frame.pack(fill="both", expand=True)

        def renderizar():
            for child in resultado_frame.winfo_children():
                child.destroy()
            encontrados = buscar_locais(self.locais, busca.get(), categoria.get(), preco.get())
            if not encontrados:
                ctk.CTkLabel(
                    resultado_frame,
                    text="Nenhum local encontrado. Tente outros filtros.",
                    text_color=MUTED,
                ).pack(anchor="w", padx=8, pady=20)
                return
            for local in encontrados:
                card = ctk.CTkFrame(
                    resultado_frame,
                    fg_color=PANEL,
                    corner_radius=14,
                    border_width=1,
                    border_color="#CADDEE",
                )
                card.pack(fill="x", pady=6)
                left = ctk.CTkFrame(card, fg_color="#CCDBEB", corner_radius=10, width=82, height=82)
                left.pack(side="left", padx=14, pady=14)
                left.pack_propagate(False)
                ctk.CTkLabel(left, text="✦", font=ctk.CTkFont(size=30), text_color=PRIMARY).pack(expand=True)
                info = ctk.CTkFrame(card, fg_color="transparent")
                info.pack(side="left", fill="both", expand=True, pady=14)
                ctk.CTkLabel(
                    info,
                    text=local["nome"],
                    text_color=TEXT,
                    font=ctk.CTkFont(size=17, weight="bold"),
                ).pack(anchor="w")
                ctk.CTkLabel(
                    info,
                    text=f'{local["bairro"]}  •  {", ".join(local["categoria"])}',
                    text_color=MUTED,
                    font=ctk.CTkFont(size=12),
                ).pack(anchor="w", pady=2)
                ctk.CTkLabel(
                    info,
                    text=local["descricao"],
                    text_color=TEXT,
                    wraplength=460,
                    justify="left",
                    font=ctk.CTkFont(size=12),
                ).pack(anchor="w", pady=(2, 0))
                actions = ctk.CTkFrame(card, fg_color="transparent")
                actions.pack(side="right", padx=14)
                ctk.CTkLabel(actions, text=rotulo_preco(local.get("preco")), text_color=MUTED).pack(pady=(0, 8))
                self._botao(
                    actions,
                    "Ver detalhes",
                    lambda item=local: self.mostrar_detalhes(item),
                    width=120,
                ).pack(pady=3)
                self._botao(
                    actions,
                    "+ Roteiro",
                    lambda item=local: self.adicionar_roteiro(item),
                    width=120,
                    fg_color=ACCENT,
                    hover_color=ACCENT_HOVER,
                ).pack(pady=3)

        self._botao(filtros, "Filtrar", renderizar, width=85).pack(side="left")
        busca.bind("<Return>", lambda _event: renderizar())
        categoria.configure(command=lambda _value: renderizar())
        preco.configure(command=lambda _value: renderizar())
        renderizar()

    def mostrar_detalhes(self, local):
        janela = ctk.CTkToplevel(self)
        janela.title(local["nome"])
        janela.geometry("580x570")
        janela.minsize(500, 480)
        janela.configure(fg_color=BG)
        janela.transient(self)
        ctk.CTkLabel(
            janela,
            text=local["nome"],
            text_color=TEXT,
            font=ctk.CTkFont(size=26, weight="bold"),
            wraplength=520,
        ).pack(anchor="w", padx=24, pady=(24, 6))
        ctk.CTkLabel(
            janela,
            text=f'{local["bairro"]}  •  {", ".join(local["categoria"])}  •  {rotulo_preco(local.get("preco"))}',
            text_color=MUTED,
            font=ctk.CTkFont(size=13),
        ).pack(anchor="w", padx=24, pady=(0, 18))
        box = ctk.CTkFrame(janela, fg_color=PANEL, corner_radius=14)
        box.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        for titulo, texto in [
            ("Sobre o lugar", local["descricao"]),
            ("Por que visitar?", local["por_que_visitar"]),
            ("Tempo sugerido", local["duracao"]),
            ("Localização / observações", local["endereco"]),
        ]:
            ctk.CTkLabel(
                box,
                text=titulo,
                text_color=PRIMARY,
                font=ctk.CTkFont(size=14, weight="bold"),
            ).pack(anchor="w", padx=16, pady=(13, 2))
            ctk.CTkLabel(
                box,
                text=texto,
                text_color=TEXT,
                font=ctk.CTkFont(size=13),
                justify="left",
                wraplength=475,
            ).pack(anchor="w", padx=16)
        self._botao(
            janela,
            "Adicionar ao meu roteiro",
            lambda: (self.adicionar_roteiro(local), janela.destroy()),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
        ).pack(anchor="e", padx=24, pady=(0, 20))

    def adicionar_roteiro(self, local):
        ja_existe = any(item.get("id") == local.get("id") for item in self.roteiro)
        self.roteiro = adicionar(self.roteiro, local)
        if ja_existe:
            messagebox.showinfo("Meu roteiro", "Esse local já está no seu roteiro.")
        else:
            messagebox.showinfo("Meu roteiro", f'{local["nome"]} foi adicionado ao roteiro.')

    def mostrar_roteiro(self):
        self._limpar()
        self.tela_atual = "Meu roteiro"
        self._titulo(
            "Meu roteiro",
            "Organize os lugares que deseja conhecer. As alterações ficam salvas neste computador.",
        )
        if not self.roteiro:
            ctk.CTkLabel(
                self.conteudo,
                text="Seu roteiro ainda está vazio.",
                text_color=TEXT,
                font=ctk.CTkFont(size=18, weight="bold"),
            ).pack(anchor="w", pady=(20, 6))
            ctk.CTkLabel(
                self.conteudo,
                text="Explore os locais e adicione os que chamarem sua atenção.",
                text_color=MUTED,
            ).pack(anchor="w", pady=(0, 16))
            self._botao(self.conteudo, "Explorar locais", self.mostrar_explorar, width=180).pack(anchor="w")
            return

        lista = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent", corner_radius=0)
        lista.pack(fill="both", expand=True)
        for indice, local in enumerate(self.roteiro, start=1):
            card = ctk.CTkFrame(
                lista,
                fg_color=PANEL,
                corner_radius=12,
                border_width=1,
                border_color="#CDDEF8",
            )
            card.pack(fill="x", pady=6)
            ctk.CTkLabel(
                card,
                text=f"{indice:02d}",
                text_color=PRIMARY,
                font=ctk.CTkFont(size=22, weight="bold"),
                width=55,
            ).pack(side="left", padx=12, pady=16)
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, pady=14)
            ctk.CTkLabel(
                info,
                text=local["nome"],
                text_color=TEXT,
                font=ctk.CTkFont(size=16, weight="bold"),
            ).pack(anchor="w")
            ctk.CTkLabel(
                info,
                text=f'{local["bairro"]}  •  {local["duracao"]}',
                text_color=MUTED,
                font=ctk.CTkFont(size=12),
            ).pack(anchor="w", pady=(3, 0))
            self._botao(
                card,
                "Ver detalhes",
                lambda item=local: self.mostrar_detalhes(item),
                width=110,
            ).pack(side="right", padx=8)
            self._botao(
                card,
                "Remover",
                lambda item_id=local["id"]: self._remover_e_atualizar(item_id),
                width=90,
            ).pack(side="right", padx=(0, 14))

        bottom = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        bottom.pack(fill="x", pady=(12, 0))
        ctk.CTkLabel(
            bottom,
            text=f"{len(self.roteiro)} local(is) no roteiro",
            text_color=MUTED,
        ).pack(side="left")
        self._botao(bottom, "Limpar roteiro", self.limpar_roteiro, width=130).pack(side="right")

    def _remover_e_atualizar(self, local_id):
        self.roteiro = remover(self.roteiro, local_id)
        self.mostrar_roteiro()

    def limpar_roteiro(self):
        if messagebox.askyesno("Limpar roteiro", "Deseja remover todos os locais do roteiro?"):
            self.roteiro = []
            from services.roteiro import salvar_roteiro

            salvar_roteiro(self.roteiro)
            self.mostrar_roteiro()