from pathlib import Path
from typing import Any, Callable, Dict, Optional

import customtkinter as ctk
from PIL import Image, ImageDraw

from services.database import autenticar_usuario, cadastrar_usuario, inicializar_banco

# ---------- Paleta Visual ----------
BG = "#F3F5F9"
PANEL = "#FFFFFF"
PRIMARY = "#062454"
PRIMARY_HOVER = "#0B3277"
PRIMARY_SOFT = "#E3EAF5"
TEXT = "#161D27"
MUTED = "#6B7686"
LINE = "#E4E8EF"
ERROR = "#B3261E"
SUCCESS = "#1E7E34"

FONT = "Segoe UI"


def fonte(size=14, weight="normal"):
    return ctk.CTkFont(family=FONT, size=size, weight=weight)


def obter_caminho_imagem() -> Path:
    """Busca o arquivo de imagem de login em diferentes caminhos possíveis."""
    diretorio_script = Path(__file__).resolve().parent

    possiveis_caminhos = [
        diretorio_script.parent / "assets" / "images" / "imagem_login.jpg",
        diretorio_script.parent / "assets" / "images" / "imagem_login.png",
        diretorio_script / "belem_na_mao_mvp" / "assets" / "images" / "imagem_login.jpg",
        diretorio_script / "assets" / "images" / "imagem_login.jpg",
        diretorio_script.parent.parent / "belem_na_mao_mvp" / "assets" / "images" / "imagem_login.jpg",
    ]

    for caminho in possiveis_caminhos:
        if caminho.is_file():
            return caminho

    return possiveis_caminhos[0]


def imagem_arredondada(caminho: Path, tamanho: int, raio: int) -> Image.Image:
    """Abre a imagem, recorta em quadrado e arredonda os cantos."""
    img = Image.open(caminho).convert("RGBA")
    lado = min(img.size)
    esq = (img.width - lado) // 2
    topo = (img.height - lado) // 2
    img = img.crop((esq, topo, esq + lado, topo + lado)).resize((tamanho, tamanho), Image.LANCZOS)

    mascara = Image.new("L", (tamanho, tamanho), 0)
    ImageDraw.Draw(mascara).rounded_rectangle((0, 0, tamanho, tamanho), radius=raio, fill=255)
    img.putalpha(mascara)
    return img


# ======================================================================
# Janela Modal de Cadastro
# ======================================================================
class JanelaCadastro(ctk.CTkToplevel):
    def __init__(self, parent, on_cadastro_sucesso: Optional[Callable[[str], None]] = None):
        super().__init__(parent)
        self.on_cadastro_sucesso = on_cadastro_sucesso
        self.title("Criar Conta — BelémNaMão")
        self.geometry("400x620")
        self.minsize(360, 560)
        self.configure(fg_color=BG)
        self.transient(parent)
        self.grab_set()

        self._criar_ui()

    def _criar_ui(self):
        rolagem = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        rolagem.pack(fill="both", expand=True, padx=20, pady=16)

        ctk.CTkLabel(rolagem, text="Criar Conta", font=fonte(22, "bold"), text_color=PRIMARY).pack(
            anchor="w", pady=(8, 2)
        )
        ctk.CTkLabel(
            rolagem,
            text="Cadastre-se para salvar seus roteiros personalizados.",
            font=fonte(12),
            text_color=MUTED,
            wraplength=340,
            justify="left",
        ).pack(anchor="w", pady=(0, 14))

        self.lbl_msg = ctk.CTkLabel(rolagem, text="", font=fonte(12, "bold"), wraplength=340)
        self.lbl_msg.pack(fill="x", pady=(0, 8))

        self.entry_nome = self._campo(rolagem, "Nome completo")
        self.entry_usuario = self._campo(rolagem, "Nome de usuário (login)")
        self.entry_email = self._campo(rolagem, "E-mail")
        self.entry_senha = self._campo(rolagem, "Senha (mínimo 4 dígitos)", mostrar="•")
        self.entry_confirma = self._campo(rolagem, "Confirmar senha", mostrar="•")

        btn_cadastrar = ctk.CTkButton(
            rolagem,
            text="Criar minha conta",
            height=48,
            corner_radius=24,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=fonte(15, "bold"),
            command=self._salvar_cadastro,
        )
        btn_cadastrar.pack(fill="x", pady=(20, 8))

        ctk.CTkButton(
            rolagem,
            text="Voltar ao login",
            height=38,
            corner_radius=19,
            fg_color=PRIMARY_SOFT,
            text_color=PRIMARY,
            hover_color="#D3DEEE",
            font=fonte(13, "bold"),
            command=self.destroy,
        ).pack(fill="x")

    def _campo(self, master, rotulo, mostrar=None):
        ctk.CTkLabel(master, text=rotulo, font=fonte(12, "bold"), text_color=TEXT).pack(
            anchor="w", padx=4, pady=(10, 4)
        )
        entry = ctk.CTkEntry(
            master,
            height=44,
            corner_radius=22,
            fg_color=PANEL,
            border_width=1,
            border_color=LINE,
            text_color=TEXT,
            font=fonte(13),
            show=mostrar or "",
        )
        entry.pack(fill="x")
        return entry

    def _salvar_cadastro(self):
        nome = self.entry_nome.get().strip()
        usuario = self.entry_usuario.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get()
        confirma = self.entry_confirma.get()

        if not nome or not usuario or not senha:
            self.lbl_msg.configure(text="Preencha nome, usuário e senha.", text_color=ERROR)
            return

        if senha != confirma:
            self.lbl_msg.configure(text="As senhas digitadas não coincidem.", text_color=ERROR)
            return

        sucesso, msg = cadastrar_usuario(nome, usuario, email, senha)
        if sucesso:
            if self.on_cadastro_sucesso:
                self.on_cadastro_sucesso(usuario)
            self.destroy()
        else:
            self.lbl_msg.configure(text=msg, text_color=ERROR)


# ======================================================================
# Janela de Login Principal
# ======================================================================
class JanelaLogin(ctk.CTk):
    LARGURA = 430
    ALTURA = 860

    def __init__(self, on_login_success: Optional[Callable[[Dict[str, Any]], None]] = None):
        super().__init__()
        self.on_login_success = on_login_success
        self.title("BelémNaMão — Login")
        self.geometry(f"{self.LARGURA}x{self.ALTURA}")
        self.minsize(380, 700)
        self.configure(fg_color=BG)

        # Garante inicialização do banco SQLite ao abrir a tela de login
        inicializar_banco()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        rolagem = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        rolagem.grid(row=0, column=0, sticky="nsew")
        self.corpo = ctk.CTkFrame(rolagem, fg_color="transparent")
        self.corpo.pack(fill="both", expand=True, padx=22)

        self._criar_topo()
        self._criar_formulario()
        self._criar_rodape()

        self.bind("<Return>", lambda _e: self.fazer_login())
        self.after(100, self.entry_user.focus_set)

    def _criar_topo(self):
        topo = ctk.CTkFrame(
            self.corpo,
            fg_color=PANEL,
            corner_radius=30,
            border_width=1,
            border_color=LINE,
        )
        topo.pack(fill="x", pady=(24, 0))

        caminho = obter_caminho_imagem()
        try:
            img = imagem_arredondada(caminho, 520, 70)
            self._imagem = ctk.CTkImage(light_image=img, size=(240, 240))
            ctk.CTkLabel(topo, text="", image=self._imagem).pack(pady=(22, 4))
        except Exception as e:
            ctk.CTkLabel(
                topo,
                text=f"Belém na Mão\n{e}",
                text_color=PRIMARY,
                font=fonte(18, "bold"),
            ).pack(padx=16, pady=24)

        ctk.CTkLabel(topo, text="Bem-vindo a Belém", font=fonte(26, "bold"), text_color=PRIMARY).pack(
            pady=(8, 2)
        )
        ctk.CTkLabel(
            topo,
            text="Entre para montar seu roteiro do seu jeito.",
            font=fonte(13),
            text_color=MUTED,
        ).pack(pady=(0, 22))

    def _campo(self, rotulo, mostrar=None):
        ctk.CTkLabel(self.corpo, text=rotulo, font=fonte(13, "bold"), text_color=TEXT).pack(
            anchor="w", padx=6, pady=(16, 6)
        )
        entry = ctk.CTkEntry(
            self.corpo,
            height=50,
            corner_radius=25,
            fg_color=PANEL,
            border_width=1,
            border_color=LINE,
            text_color=TEXT,
            font=fonte(14),
            show=mostrar or "",
        )
        entry.pack(fill="x")
        entry.bind("<FocusIn>", lambda _e: entry.configure(border_color=PRIMARY, border_width=2))
        entry.bind("<FocusOut>", lambda _e: entry.configure(border_color=LINE, border_width=1))
        return entry

    def _criar_formulario(self):
        self.lbl_feedback = ctk.CTkLabel(
            self.corpo,
            text="",
            font=fonte(12, "bold"),
            text_color=ERROR,
            wraplength=self.LARGURA - 60,
        )
        self.lbl_feedback.pack(fill="x", pady=(12, 0))

        self.entry_user = self._campo("Usuário ou E-mail")
        self.entry_pass = self._campo("Senha", mostrar="•")

        # Botão para alternar visualização da senha
        self._senha_visivel = False
        self.btn_olho = ctk.CTkButton(
            self.entry_pass,
            text="Mostrar",
            width=64,
            height=32,
            corner_radius=16,
            fg_color=PRIMARY_SOFT,
            text_color=PRIMARY,
            hover_color="#D3DEEE",
            font=fonte(12, "bold"),
            command=self._alternar_senha,
        )
        self.btn_olho.place(relx=1.0, rely=0.5, x=-12, anchor="e")

        # Dica rápida de teste para conveniência
        dica_box = ctk.CTkFrame(self.corpo, fg_color=PRIMARY_SOFT, corner_radius=12)
        dica_box.pack(fill="x", pady=(12, 0), padx=2)
        ctk.CTkLabel(
            dica_box,
            text="💡 Login de demonstração: usuário turista / senha 123456",
            font=fonte(11, "bold"),
            text_color=PRIMARY,
        ).pack(pady=6, padx=8)

        self.btn_login = ctk.CTkButton(
            self.corpo,
            text="Entrar",
            height=52,
            corner_radius=26,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=fonte(16, "bold"),
            command=self.fazer_login,
        )
        self.btn_login.pack(fill="x", pady=(18, 0))

        # Opção rápida para continuar como convidado
        ctk.CTkButton(
            self.corpo,
            text="Continuar sem login (Convidado)",
            fg_color="transparent",
            text_color=MUTED,
            hover_color=BG,
            font=fonte(12),
            height=32,
            command=self._login_visitante,
        ).pack(pady=(6, 0))

    def _criar_rodape(self):
        rodape = ctk.CTkFrame(self.corpo, fg_color="transparent")
        rodape.pack(pady=(18, 24))
        ctk.CTkLabel(rodape, text="Ainda não tem conta?", text_color=MUTED, font=fonte(13)).pack(
            side="left"
        )
        ctk.CTkButton(
            rodape,
            text="Cadastre-se",
            fg_color="transparent",
            text_color=PRIMARY,
            hover_color=BG,
            font=fonte(13, "bold"),
            width=80,
            cursor="hand2",
            command=self._abrir_cadastro,
        ).pack(side="left", padx=2)

    def _alternar_senha(self):
        self._senha_visivel = not self._senha_visivel
        self.entry_pass.configure(show="" if self._senha_visivel else "•")
        self.btn_olho.configure(text="Ocultar" if self._senha_visivel else "Mostrar")

    def _abrir_cadastro(self):
        def apos_cadastro(novo_usuario: str):
            self.entry_user.delete(0, "end")
            self.entry_user.insert(0, novo_usuario)
            self.entry_pass.delete(0, "end")
            self.lbl_feedback.configure(
                text=f"Conta '{novo_usuario}' cadastrada com sucesso! Digite sua senha para entrar.",
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
        senha = self.entry_pass.get()

        if not usuario or not senha:
            self.lbl_feedback.configure(
                text="Por favor, preencha o usuário e a senha.",
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
                text="Usuário ou senha incorretos. Verifique suas credenciais.",
                text_color=ERROR,
            )


if __name__ == "__main__":
    app = JanelaLogin()
    app.mainloop()