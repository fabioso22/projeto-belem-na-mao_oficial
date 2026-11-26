"""
Módulo de Autenticação e Telas de Login e Cadastro do BelémNaMão
Interface moderna, limpa e profissional com layout split-panel e suporte a demonstração rápida.
"""
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import customtkinter as ctk
from PIL import Image, ImageDraw

from services.database import autenticar_usuario, cadastrar_usuario, inicializar_banco
from services.i18n import IDIOMAS_DISPONIVEIS, ROTULOS_IDIOMA, get_idioma, set_idioma, t
from views.theme import (
    AMBER,
    BG,
    BTN_SECONDARY_BG,
    BTN_SECONDARY_BORDER,
    BTN_SECONDARY_HOVER,
    BTN_SECONDARY_TEXT,
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
    SECONDARY_FIXED,
    SUCCESS,
    TERTIARY_CONTAINER,
    TERTIARY_FIXED,
    ON_TERTIARY_FIXED,
    TEXT,
    TEXT_BRAND,
    TEXT_LIGHT,
    TEXT_MUTED,
    TEXT_TITLE,
    fonte,
)


def obter_caminho_imagem_login() -> Path:
    """Busca a foto de alta resolução de Belém para o painel de showcase."""
    diretorio_script = Path(__file__).resolve().parent
    pasta_assets = diretorio_script.parent / "assets" / "images"

    candidatos = [
        pasta_assets / "login_showcase.jpg",
        pasta_assets / "imagem_login.jpg",
        pasta_assets / "imagem_login.png",
    ]
    for c in candidatos:
        if c.is_file():
            return c
    return pasta_assets / "login_showcase.jpg"


# ======================================================================
# Janela Modal de Cadastro
# ======================================================================
class JanelaCadastro(ctk.CTkToplevel):
    def __init__(self, parent, on_cadastro_sucesso: Optional[Callable[[str], None]] = None):
        super().__init__(parent)
        self.on_cadastro_sucesso = on_cadastro_sucesso
        self.title(t("cad_window_title"))
        self.geometry("440x650")
        self.minsize(400, 580)
        self.configure(fg_color=BG)
        self.transient(parent)
        self.grab_set()

        self._criar_ui()
        self._centralizar()

    def _centralizar(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - w) // 2)
        y = max(0, (sh - h) // 2)
        self.geometry(f"+{x}+{y}")

    def _criar_ui(self):
        container = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=12, border_width=1, border_color=LINE)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        rolagem = ctk.CTkScrollableFrame(container, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True, padx=16, pady=16)

        # Cabeçalho
        ctk.CTkLabel(rolagem, text=t("cad_titulo"), font=fonte(22, "bold"), text_color=TEXT_TITLE).pack(
            anchor="w", pady=(8, 2)
        )
        ctk.CTkLabel(
            rolagem,
            text=t("cad_subtitulo"),
            font=fonte(12),
            text_color=TEXT_MUTED,
            wraplength=340,
            justify="left",
        ).pack(anchor="w", pady=(0, 12))

        self.lbl_msg = ctk.CTkLabel(rolagem, text="", font=fonte(12, "bold"), wraplength=340)
        self.lbl_msg.pack(fill="x", pady=(0, 6))

        self.entry_nome = self._campo(rolagem, t("cad_nome"), t("cad_nome_ph"))
        self.entry_usuario = self._campo(rolagem, t("cad_usuario"), t("cad_usuario_ph"))
        self.entry_email = self._campo(rolagem, t("cad_email"), t("cad_email_ph"))
        self.entry_senha = self._campo(rolagem, t("cad_senha"), t("cad_senha_ph"), mostrar="•")
        self.entry_confirma = self._campo(rolagem, t("cad_confirma"), t("cad_confirma_ph"), mostrar="•")

        btn_cadastrar = ctk.CTkButton(
            rolagem,
            text=t("cad_btn_criar"),
            height=44,
            corner_radius=8,
            fg_color=PRIMARY_BTN,
            hover_color=PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(14, "bold"),
            command=self._salvar_cadastro,
        )
        btn_cadastrar.pack(fill="x", pady=(18, 8))

        ctk.CTkButton(
            rolagem,
            text=t("cad_btn_voltar"),
            height=36,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(13, "bold"),
            command=self.destroy,
        ).pack(fill="x", pady=(0, 10))

    def _campo(self, master, rotulo, placeholder="", mostrar=None):
        ctk.CTkLabel(master, text=rotulo, font=fonte(12, "bold"), text_color=TEXT_TITLE).pack(
            anchor="w", padx=4, pady=(8, 3)
        )
        entry = ctk.CTkEntry(
            master,
            height=42,
            corner_radius=8,
            fg_color=PANEL_SUBTLE,
            border_width=1,
            border_color=LINE,
            text_color=TEXT,
            placeholder_text=placeholder,
            placeholder_text_color=TEXT_LIGHT,
            font=fonte(13),
            show=mostrar or "",
        )
        entry.pack(fill="x")
        entry.bind("<FocusIn>", lambda _e: entry.configure(border_color=PRIMARY_BTN, fg_color=PANEL))
        entry.bind("<FocusOut>", lambda _e: entry.configure(border_color=LINE, fg_color=PANEL_SUBTLE))
        return entry

    def _salvar_cadastro(self):
        nome = self.entry_nome.get().strip()
        usuario = self.entry_usuario.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get()
        confirma = self.entry_confirma.get()

        if not nome or not usuario or not senha:
            self.lbl_msg.configure(text=t("cad_erro_campos"), text_color=ERROR)
            return

        if len(senha) < 4:
            self.lbl_msg.configure(text=t("cad_erro_senha_curta"), text_color=ERROR)
            return

        if senha != confirma:
            self.lbl_msg.configure(text=t("cad_erro_confirma"), text_color=ERROR)
            return

        sucesso, msg = cadastrar_usuario(nome, usuario, email, senha)
        if sucesso:
            if self.on_cadastro_sucesso:
                self.on_cadastro_sucesso(usuario)
            self.destroy()
        else:
            self.lbl_msg.configure(text=msg, text_color=ERROR)


# ======================================================================
# Janela de Login Principal (Split-Screen Moderno)
# ======================================================================
class JanelaLogin(ctk.CTk):
    LARGURA = 1020
    ALTURA = 660

    def __init__(
        self,
        on_login_success: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_admin_login: Optional[Callable[[Dict[str, Any]], None]] = None,
    ):
        super().__init__()
        self.on_login_success = on_login_success
        self.on_admin_login = on_admin_login
        self.title(t("login_window_title"))
        self.geometry(f"{self.LARGURA}x{self.ALTURA}")
        self.minsize(860, 580)
        self.configure(fg_color=BG)

        # Garante inicialização do banco ao abrir sem travar em caso de falha de rede
        try:
            inicializar_banco()
        except Exception as e:
            print(f"[Aviso] Falha ao inicializar banco: {e}")

        self._centralizar()
        self._configurar_grid()
        self._criar_lado_esquerdo()
        self._criar_lado_direito()

        self.bind("<Return>", lambda _e: self.fazer_login())
        self.after(150, self.entry_user.focus_set)

    def _alterar_idioma_login(self, codigo: str):
        """Alterna o idioma da tela de login em tempo real preservando campos digitados."""
        if get_idioma() == codigo:
            return
        usuario_digitado = self.entry_user.get() if hasattr(self, "entry_user") else ""
        senha_digitada = self.entry_pass.get() if hasattr(self, "entry_pass") else ""
        set_idioma(codigo)
        self.title(t("login_window_title"))
        for w in self.winfo_children():
            w.destroy()
        self._criar_lado_esquerdo()
        self._criar_lado_direito()
        if usuario_digitado:
            self.entry_user.insert(0, usuario_digitado)
        if senha_digitada:
            self.entry_pass.insert(0, senha_digitada)

    def _centralizar(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - self.LARGURA) // 2)
        y = max(0, (sh - self.ALTURA) // 2)
        self.geometry(f"{self.LARGURA}x{self.ALTURA}+{x}+{y}")

    def _alternar_modo_escuro_login(self):
        """Alterna o tema entre Claro e Escuro na tela de login."""
        modo_atual = ctk.get_appearance_mode().lower()
        if modo_atual == "dark":
            ctk.set_appearance_mode("light")
            if hasattr(self, "btn_tema_login"):
                self.btn_tema_login.configure(text="🌙")
        else:
            ctk.set_appearance_mode("dark")
            if hasattr(self, "btn_tema_login"):
                self.btn_tema_login.configure(text="☀️")

    def _configurar_grid(self):
        self.grid_columnconfigure(0, weight=4, uniform="login_split")
        self.grid_columnconfigure(1, weight=5, uniform="login_split")
        self.grid_rowconfigure(0, weight=1)

    # ------------------------------------------------------------------
    # Painel Esquerdo: Formulário de Autenticação
    # ------------------------------------------------------------------
    def _criar_lado_esquerdo(self):
        painel_esquerdo = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=0)
        painel_esquerdo.grid(row=0, column=0, sticky="nsew")

        rolagem = ctk.CTkScrollableFrame(painel_esquerdo, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True, padx=32, pady=24)

        # 1. Top Bar com Logo e Selo Regional
        topo = ctk.CTkFrame(rolagem, fg_color="transparent")
        topo.pack(fill="x", pady=(0, 20))

        logo_frame = ctk.CTkFrame(topo, fg_color="transparent")
        logo_frame.pack(side="left")

        # Ícone distintivo
        icone_box = ctk.CTkFrame(logo_frame, width=42, height=42, corner_radius=8, fg_color=PRIMARY_BTN)
        icone_box.pack(side="left", padx=(0, 10))
        icone_box.pack_propagate(False)
        ctk.CTkLabel(icone_box, text="≋", font=fonte(22, "bold"), text_color=SECONDARY_FIXED).pack(expand=True)

        txt_logo = ctk.CTkFrame(logo_frame, fg_color="transparent")
        txt_logo.pack(side="left")
        ctk.CTkLabel(txt_logo, text="Belém", font=fonte(20, "bold"), text_color=TEXT_TITLE).pack(side="left")
        ctk.CTkLabel(txt_logo, text="NaMão", font=fonte(20, "bold"), text_color=SECONDARY).pack(side="left")

        # Selo Pará, Amazônia + Seletor de Idiomas discreto
        selo = ctk.CTkFrame(topo, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        selo.pack(side="right", pady=4)
        ctk.CTkLabel(
            selo,
            text=t("login_selo"),
            font=fonte(11, "bold"),
            text_color=ON_TERTIARY_FIXED,
            padx=8,
            pady=4,
        ).pack()

        # Botão Modo Escuro
        modo_atual = ctk.get_appearance_mode().lower()
        texto_tema = "☀️" if modo_atual == "dark" else "🌙"
        self.btn_tema_login = ctk.CTkButton(
            topo,
            text=texto_tema,
            width=34,
            height=30,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(13),
            command=self._alternar_modo_escuro_login,
        )
        self.btn_tema_login.pack(side="right", padx=(0, 6))

        # Barra discreta de Idiomas (PT-BR / EN / ES)
        barra_lang = ctk.CTkFrame(rolagem, fg_color="transparent")
        barra_lang.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(
            barra_lang,
            text=f"🌐 {t('idioma_label')}",
            font=fonte(11, "bold"),
            text_color=TEXT_MUTED,
        ).pack(side="left", padx=(0, 6))
        idioma_atual = get_idioma()
        for codigo in IDIOMAS_DISPONIVEIS:
            ativo = codigo == idioma_atual
            ctk.CTkButton(
                barra_lang,
                text=ROTULOS_IDIOMA[codigo],
                width=48,
                height=24,
                corner_radius=6,
                fg_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BG,
                hover_color=PRIMARY_HOVER if ativo else BTN_SECONDARY_HOVER,
                border_width=1,
                border_color=PRIMARY_BTN if ativo else BTN_SECONDARY_BORDER,
                text_color="#FFFFFF" if ativo else BTN_SECONDARY_TEXT,
                font=fonte(10, "bold"),
                command=lambda c=codigo: self._alterar_idioma_login(c),
            ).pack(side="left", padx=2)

        # 2. Título de Boas-Vindas
        ctk.CTkLabel(
            rolagem,
            text=t("login_boas_vindas"),
            font=fonte(26, "bold"),
            text_color=TEXT_TITLE,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(4, 2))

        ctk.CTkLabel(
            rolagem,
            text=t("login_subtitulo"),
            font=fonte(13),
            text_color=TEXT_MUTED,
            justify="left",
            anchor="w",
            wraplength=380,
        ).pack(fill="x", pady=(0, 14))

        # 3. Card Interativo de Credenciais Demo
        demo_card = ctk.CTkFrame(rolagem, fg_color=PANEL_SUBTLE, corner_radius=8, border_width=1, border_color=LINE)
        demo_card.pack(fill="x", pady=(0, 16))

        demo_inner = ctk.CTkFrame(demo_card, fg_color="transparent")
        demo_inner.pack(fill="x", padx=12, pady=10)

        ctk.CTkLabel(
            demo_inner,
            text=t("login_demo_label"),
            font=fonte(12, "bold"),
            text_color=TEXT_BRAND,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkLabel(
            demo_inner,
            text="turista / 123456  |  Admin: admin",
            font=fonte(11),
            text_color=TEXT_MUTED,
        ).pack(side="left")

        self.btn_preencher_demo = ctk.CTkButton(
            demo_inner,
            text=t("login_btn_preencher"),
            width=76,
            height=28,
            corner_radius=8,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(11, "bold"),
            command=self._preencher_credenciais_demo,
        )
        self.btn_preencher_demo.pack(side="right")

        # Feedback de erro ou sucesso
        self.lbl_feedback = ctk.CTkLabel(
            rolagem,
            text="",
            font=fonte(12, "bold"),
            text_color=ERROR,
            wraplength=380,
            justify="left",
            anchor="w",
        )
        self.lbl_feedback.pack(fill="x", pady=(0, 4))

        # 4. Campos do Formulário
        ctk.CTkLabel(rolagem, text=t("login_user_label"), font=fonte(11, "bold"), text_color=TEXT_TITLE).pack(
            anchor="w", padx=4, pady=(6, 4)
        )
        self.entry_user = ctk.CTkEntry(
            rolagem,
            height=44,
            corner_radius=8,
            fg_color=PANEL_SUBTLE,
            border_width=1,
            border_color=LINE,
            text_color=TEXT,
            placeholder_text=t("login_user_placeholder"),
            placeholder_text_color=TEXT_LIGHT,
            font=fonte(14),
        )
        self.entry_user.pack(fill="x", pady=(0, 10))
        self.entry_user.bind("<FocusIn>", lambda _e: self.entry_user.configure(border_color=PRIMARY_BTN, fg_color=PANEL))
        self.entry_user.bind("<FocusOut>", lambda _e: self.entry_user.configure(border_color=LINE, fg_color=PANEL_SUBTLE))

        ctk.CTkLabel(rolagem, text=t("login_pass_label"), font=fonte(11, "bold"), text_color=TEXT_TITLE).pack(
            anchor="w", padx=4, pady=(4, 4)
        )
        senha_container = ctk.CTkFrame(rolagem, fg_color="transparent")
        senha_container.pack(fill="x", pady=(0, 12))

        self.entry_pass = ctk.CTkEntry(
            senha_container,
            height=44,
            corner_radius=8,
            fg_color=PANEL_SUBTLE,
            border_width=1,
            border_color=LINE,
            text_color=TEXT,
            placeholder_text=t("login_pass_placeholder"),
            placeholder_text_color=TEXT_LIGHT,
            font=fonte(14),
            show="•",
        )
        self.entry_pass.pack(fill="x")
        self.entry_pass.bind("<FocusIn>", lambda _e: self.entry_pass.configure(border_color=PRIMARY_BTN, fg_color=PANEL))
        self.entry_pass.bind("<FocusOut>", lambda _e: self.entry_pass.configure(border_color=LINE, fg_color=PANEL_SUBTLE))

        # Botão Mostrar/Ocultar Senha
        self._senha_visivel = False
        self.btn_olho = ctk.CTkButton(
            self.entry_pass,
            text=t("login_mostrar"),
            width=62,
            height=28,
            corner_radius=6,
            fg_color=BTN_SECONDARY_BG,
            border_width=1,
            border_color=BTN_SECONDARY_BORDER,
            text_color=BTN_SECONDARY_TEXT,
            hover_color=BTN_SECONDARY_HOVER,
            font=fonte(11, "bold"),
            command=self._alternar_senha,
        )
        self.btn_olho.place(relx=1.0, rely=0.5, x=-8, anchor="e")

        # Opção Lembrar de mim
        self.check_lembrar = ctk.CTkCheckBox(
            rolagem,
            text=t("login_lembrar"),
            font=fonte(12),
            text_color=TEXT_MUTED,
            fg_color=PRIMARY_BTN,
            hover_color=PRIMARY_HOVER,
            corner_radius=4,
            border_width=1,
            border_color=LINE,
        )
        self.check_lembrar.select()
        self.check_lembrar.pack(anchor="w", padx=4, pady=(0, 16))

        # Botão Principal de Login
        self.btn_login = ctk.CTkButton(
            rolagem,
            text=t("login_entrar"),
            height=44,
            corner_radius=8,
            fg_color=PRIMARY_BTN,
            hover_color=PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=fonte(15, "bold"),
            command=self.fazer_login,
        )
        self.btn_login.pack(fill="x", pady=(0, 8))

        # Continuar como Convidado
        ctk.CTkButton(
            rolagem,
            text=t("login_convidado"),
            fg_color="transparent",
            text_color=TEXT_MUTED,
            hover_color=PANEL_SUBTLE,
            font=fonte(12),
            height=34,
            corner_radius=8,
            command=self._login_visitante,
        ).pack(fill="x", pady=(0, 10))

        # Separador e Cadastro
        ctk.CTkFrame(rolagem, height=1, fg_color=LINE).pack(fill="x", pady=6)

        rodape = ctk.CTkFrame(rolagem, fg_color="transparent")
        rodape.pack(pady=4)
        ctk.CTkLabel(rodape, text=t("login_sem_conta"), text_color=TEXT_MUTED, font=fonte(13)).pack(side="left")
        ctk.CTkButton(
            rodape,
            text=t("login_cadastre_se"),
            fg_color="transparent",
            text_color=TEXT_BRAND,
            hover_color=PANEL_SUBTLE,
            font=fonte(13, "bold"),
            width=90,
            cursor="hand2",
            command=self._abrir_cadastro,
        ).pack(side="left", padx=2)

        # Assinatura discreta
        ctk.CTkLabel(
            rolagem,
            text=t("login_rodape"),
            font=fonte(11),
            text_color=TEXT_LIGHT,
        ).pack(pady=(12, 0))

    # ------------------------------------------------------------------
    # Painel Direito: Showcase Fotográfico de Belém
    # ------------------------------------------------------------------
    def _criar_lado_direito(self):
        painel_direito = ctk.CTkFrame(self, fg_color=PRIMARY_CONTAINER, corner_radius=0)
        painel_direito.grid(row=0, column=1, sticky="nsew")

        # Tentar carregar a foto panorâmica de Belém
        caminho_foto = obter_caminho_imagem_login()
        if caminho_foto and caminho_foto.is_file():
            try:
                # Dimensão proporcional para o showcase
                w, h = 580, 660
                img = Image.open(caminho_foto).convert("RGBA")
                target_ratio = w / h
                img_ratio = img.width / img.height
                if img_ratio > target_ratio:
                    new_w = int(img.height * target_ratio)
                    left = (img.width - new_w) // 2
                    img = img.crop((left, 0, left + new_w, img.height))
                else:
                    new_h = int(img.width / target_ratio)
                    top = (img.height - new_h) // 2
                    img = img.crop((0, top, img.width, top + new_h))
                img = img.resize((w, h), Image.LANCZOS)

                # Aplicar gradiente escuro na base para leitura perfeita
                overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
                draw = ImageDraw.Draw(overlay)
                for y in range(h):
                    progresso = y / h
                    # Escurecimento elegante do centro para o rodapé
                    if progresso > 0.4:
                        alpha = int((progresso - 0.4) / 0.6 * 200)
                        draw.line([(0, y), (w, y)], fill=(11, 28, 48, alpha))
                img = Image.alpha_composite(img, overlay)

                self._img_showcase = ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
                lbl_bg = ctk.CTkLabel(painel_direito, text="", image=self._img_showcase)
                lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print(f"[Aviso] Erro ao renderizar showcase do login: {e}")

        # Badge Flutuante Superior
        topo_pill = ctk.CTkFrame(painel_direito, fg_color="#0F2847", corner_radius=16)
        topo_pill.place(relx=0.94, rely=0.06, anchor="ne")
        ctk.CTkLabel(
            topo_pill,
            text=t("login_showcase_pill"),
            font=fonte(12, "bold"),
            text_color="#FFFFFF",
            padx=14,
            pady=6,
        ).pack()

        # Card Glassmorphism Inferior de Destaque
        card_glass = ctk.CTkFrame(painel_direito, fg_color="#0F2847", corner_radius=24, border_width=1, border_color="#314868")
        card_glass.place(relx=0.08, rely=0.92, relwidth=0.84, anchor="sw")

        card_conteudo = ctk.CTkFrame(card_glass, fg_color="transparent")
        card_conteudo.pack(fill="both", expand=True, padx=22, pady=18)

        # Pill Categoria
        pill_cat = ctk.CTkFrame(card_conteudo, fg_color=SECONDARY, corner_radius=10)
        pill_cat.pack(anchor="w", pady=(0, 8))
        ctk.CTkLabel(
            pill_cat,
            text=t("login_showcase_tag"),
            font=fonte(10, "bold"),
            text_color="#FFFFFF",
            padx=10,
            pady=3,
        ).pack()

        ctk.CTkLabel(
            card_conteudo,
            text=t("login_showcase_titulo"),
            font=fonte(19, "bold"),
            text_color="#FFFFFF",
            justify="left",
            anchor="w",
            wraplength=420,
        ).pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(
            card_conteudo,
            text=t("login_showcase_desc"),
            font=fonte(12),
            text_color="#CADDEE",
            justify="left",
            anchor="w",
            wraplength=420,
        ).pack(fill="x", pady=(0, 12))

        # Destaques Rápidos
        pills_box = ctk.CTkFrame(card_conteudo, fg_color="transparent")
        pills_box.pack(fill="x")
        for tag in ["✦ Ver-o-Peso", "✦ Estação das Docas", "✦ Feliz Lusitânia", "✦ Ilha do Combu"]:
            p = ctk.CTkFrame(pills_box, fg_color="#173860", corner_radius=10)
            p.pack(side="left", padx=(0, 6))
            ctk.CTkLabel(p, text=tag, font=fonte(11, "bold"), text_color="#E3EAF5", padx=8, pady=3).pack()

    # ------------------------------------------------------------------
    # Interações
    # ------------------------------------------------------------------
    def _preencher_credenciais_demo(self):
        """Preenche automaticamente os dados de demonstração com feedback visual."""
        self.entry_user.delete(0, "end")
        self.entry_user.insert(0, "turista")
        self.entry_pass.delete(0, "end")
        self.entry_pass.insert(0, "123456")

        self.btn_preencher_demo.configure(text=t("login_btn_pronto"), fg_color=TERTIARY_FIXED, text_color=ON_TERTIARY_FIXED)
        self.lbl_feedback.configure(text=t("login_demo_msg"), text_color=SUCCESS)
        self.after(
            1600,
            lambda: self.btn_preencher_demo.configure(
                text=t("login_btn_preencher"), fg_color=BTN_SECONDARY_BG, text_color=BTN_SECONDARY_TEXT
            ),
        )

    def _alternar_senha(self):
        self._senha_visivel = not self._senha_visivel
        self.entry_pass.configure(show="" if self._senha_visivel else "•")
        self.btn_olho.configure(text=t("login_ocultar") if self._senha_visivel else t("login_mostrar"))

    def _abrir_cadastro(self):
        def apos_cadastro(novo_usuario: str):
            self.entry_user.delete(0, "end")
            self.entry_user.insert(0, novo_usuario)
            self.entry_pass.delete(0, "end")
            self.lbl_feedback.configure(
                text=t("login_cadastro_ok", user=novo_usuario),
                text_color=SUCCESS,
            )
            self.entry_pass.focus_set()

        JanelaCadastro(self, on_cadastro_sucesso=apos_cadastro)

    def _login_visitante(self):
        visitante = {"id": 1, "nome": "Visitante", "usuario": "visitante"}
        if self.on_login_success:
            self.destroy()
            try:
                self.on_login_success(visitante)
            except TypeError:
                self.on_login_success()

    def fazer_login(self):
        usuario = self.entry_user.get().strip()
        senha = self.entry_pass.get().strip()

        # Roteamento de Administrador (Painel DataInsight) pela senha "admin"
        if senha.lower() == "admin":
            admin_user = {
                "id": 0,
                "nome": "Administrador",
                "usuario": usuario or "admin",
                "is_admin": True,
            }
            self.destroy()
            if self.on_admin_login:
                try:
                    self.on_admin_login(admin_user)
                except TypeError:
                    self.on_admin_login()
            elif self.on_login_success:
                try:
                    self.on_login_success(admin_user)
                except TypeError:
                    self.on_login_success()
            return

        if not usuario or not senha:
            self.lbl_feedback.configure(
                text=t("login_erro_vazio"),
                text_color=ERROR,
            )
            return

        usuario_autenticado = autenticar_usuario(usuario, senha)
        if usuario_autenticado:
            if self.on_login_success:
                self.destroy()
                try:
                    self.on_login_success(usuario_autenticado)
                except TypeError:
                    self.on_login_success()
        else:
            self.lbl_feedback.configure(
                text=t("login_erro_invalido"),
                text_color=ERROR,
            )


if __name__ == "__main__":
    app = JanelaLogin()
    app.mainloop()
