# from pathlib import Path
# from PIL import Image
# import customtkinter as ctk

# # Cores baseadas na paleta do projeto e na imagem de referência
# BG = "#FFFFFF"
# PRIMARY = "#062454"
# PRIMARY_HOVER = "#041838"
# TEXT_DARK = "#000000"
# MUTED = "#6B6B6B"

# # Função para obter o caminho da imagem de login, considerando diferentes estruturas de diretórios, até criar o banco de dados
# def obter_caminho_imagem() -> Path:
#   diretorio_script = Path(__file__).resolve().parent

#   # Lista de locais possíveis para encontrar a imagem conforme a estrutura do projeto
#   possiveis_caminhos = [
#       # Se o script está dentro de 'services/' e 'assets/' está no mesmo nível que 'services/':
#       diretorio_script.parent / "assets" / "images" / "imagem_login.png",
#       # Se o script está na raiz do projeto:
#       (
#           diretorio_script
#           / "belem_na_mao_mvp"
#           / "assets"
#           / "images"
#           / "imagem_login.png"
#       ),
#       # Se o script está diretamente dentro da pasta 'belem_na_mao_mvp':
#       diretorio_script / "assets" / "images" / "imagem_login.png",
#       # Se o script está em 'services/' e precisa subir 2 níveis:
#       (
#           diretorio_script.parent.parent
#           / "belem_na_mao_mvp"
#           / "assets"
#           / "images"
#           / "imagem_login.png"
#       ),
#   ]

#   for caminho in possiveis_caminhos:
#     if caminho.is_file():
#       return caminho

#   return possiveis_caminhos[0]
# #-----------------FIM--------------------------#

# class JanelaLogin(ctk.CTk):

#   def __init__(self, on_login_success=None):
#     super().__init__()
#     self.on_login_success = on_login_success
#     self.title("Login")

#     self.geometry("900x550")
#     self.minsize(800, 500)
#     self.configure(fg_color=BG)

#     self.grid_columnconfigure(0, weight=1)
#     self.grid_columnconfigure(1, weight=1)
#     self.grid_rowconfigure(0, weight=1)

#     self._criar_lado_esquerdo()
#     self._criar_lado_direito()

#   def _criar_lado_esquerdo(self):
#     frame_esq = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
#     frame_esq.grid(row=0, column=0, sticky="nsew")

#     caminho_imagem = obter_caminho_imagem()

#     try:
#       imagem_pil = Image.open(caminho_imagem)
#       imagem_ctk = ctk.CTkImage(light_image=imagem_pil, size=(450, 450))
#       label_img = ctk.CTkLabel(frame_esq, text="", image=imagem_ctk)
#       label_img.place(relx=0.5, rely=0.5, anchor="center")
#     except Exception as e:
#       ctk.CTkLabel(
#           frame_esq,
#           text=(
#               "Não foi possível carregar a imagem:\n"
#               f"{e}\n"
#               f"Tentando acessar: {caminho_imagem}"
#           ),
#           text_color="red",
#       ).place(relx=0.5, rely=0.5, anchor="center")

#   def _criar_lado_direito(self):
#     frame_dir = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
#     frame_dir.grid(row=0, column=1, sticky="nsew")

#     form_container = ctk.CTkFrame(frame_dir, fg_color="transparent")
#     form_container.place(relx=0.5, rely=0.5, anchor="center")

#     lbl_titulo = ctk.CTkLabel(
#         form_container,
#         text="Sign in",
#         font=ctk.CTkFont(size=36),
#         text_color=PRIMARY,
#     )
#     lbl_titulo.pack(anchor="center", pady=(0, 50))

#     lbl_user = ctk.CTkLabel(
#         form_container,
#         text="Username",
#         font=ctk.CTkFont(size=14),
#         text_color=MUTED,
#     )
#     lbl_user.pack(anchor="w")

#     self.entry_user = ctk.CTkEntry(
#         form_container,
#         width=320,
#         height=30,
#         border_width=0,
#         fg_color="transparent",
#         text_color=TEXT_DARK,
#         font=ctk.CTkFont(size=14),
#     )
#     self.entry_user.pack(anchor="w")

#     ctk.CTkFrame(
#         form_container, width=320, height=2, fg_color=TEXT_DARK
#     ).pack(anchor="w", pady=(0, 30))

#     lbl_pass = ctk.CTkLabel(
#         form_container,
#         text="Password",
#         font=ctk.CTkFont(size=14),
#         text_color=MUTED,
#     )
#     lbl_pass.pack(anchor="w")

#     self.entry_pass = ctk.CTkEntry(
#         form_container,
#         width=320,
#         height=30,
#         border_width=0,
#         fg_color="transparent",
#         show="*",
#         text_color=TEXT_DARK,
#         font=ctk.CTkFont(size=14),
#     )
#     self.entry_pass.pack(anchor="w")

#     ctk.CTkFrame(
#         form_container, width=320, height=2, fg_color=TEXT_DARK
#     ).pack(anchor="w", pady=(0, 40))

#     btn_login = ctk.CTkButton(
#         form_container,
#         text="Sign in",
#         width=320,
#         height=45,
#         fg_color=PRIMARY,
#         hover_color=PRIMARY_HOVER,
#         corner_radius=4,
#         font=ctk.CTkFont(size=15),
#         command=self.fazer_login,
#     )
#     btn_login.pack(anchor="w", pady=(0, 30))

#     signup_frame = ctk.CTkFrame(form_container, fg_color="transparent")
#     signup_frame.pack(anchor="center")

#     ctk.CTkLabel(
#         signup_frame,
#         text="Don't have an account?",
#         text_color=MUTED,
#         font=ctk.CTkFont(size=13),
#     ).pack(side="left")

#     ctk.CTkButton(
#         signup_frame,
#         text="Sign up",
#         fg_color="transparent",
#         text_color=PRIMARY,
#         hover_color=BG,
#         font=ctk.CTkFont(size=13),
#         width=50,
#         cursor="hand2",
#     ).pack(side="left", padx=2)

#   def fazer_login(self):
#     if self.on_login_success:
#       self.destroy()
#       self.on_login_success()


# if __name__ == "__main__":
#   app = JanelaLogin()
#   app.mainloop()

from pathlib import Path

import customtkinter as ctk
from PIL import Image, ImageDraw

# Mesma paleta do app principal
BG = "#F3F5F9"
PANEL = "#FFFFFF"
PRIMARY = "#062454"
PRIMARY_HOVER = "#0B3277"
PRIMARY_SOFT = "#E3EAF5"
TEXT = "#161D27"
MUTED = "#6B7686"
LINE = "#E4E8EF"

FONT = "Segoe UI"


def fonte(size=14, weight="normal"):
    return ctk.CTkFont(family=FONT, size=size, weight=weight)


# Função para obter o caminho da imagem de login, considerando diferentes estruturas de diretórios
def obter_caminho_imagem() -> Path:
    diretorio_script = Path(__file__).resolve().parent

    possiveis_caminhos = [
        # Script dentro de 'services/' e 'assets/' no mesmo nível de 'services/'
        diretorio_script.parent / "assets" / "images" / "imagem_login.jpg",
        # Script na raiz do projeto
        diretorio_script / "belem_na_mao_mvp" / "assets" / "images" / "imagem_login.jpg",
        # Script diretamente dentro de 'belem_na_mao_mvp'
        diretorio_script / "assets" / "images" / "imagem_login.jpg",
        # Script em 'services/' e precisa subir 2 níveis
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


class JanelaLogin(ctk.CTk):
    LARGURA = 430
    ALTURA = 860

    def __init__(self, on_login_success=None):
        super().__init__()
        self.on_login_success = on_login_success
        self.title("BelémNaMão")
        self.geometry(f"{self.LARGURA}x{self.ALTURA}")
        self.minsize(380, 700)
        self.configure(fg_color=BG)

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

    # ------------------------------------------------------------------
    def _criar_topo(self):
        topo = ctk.CTkFrame(self.corpo, fg_color=PANEL, corner_radius=30,
                            border_width=1, border_color=LINE)
        topo.pack(fill="x", pady=(28, 0))

        caminho = obter_caminho_imagem()
        try:
            img = imagem_arredondada(caminho, 520, 70)
            self._imagem = ctk.CTkImage(light_image=img, size=(240, 240))
            ctk.CTkLabel(topo, text="", image=self._imagem).pack(pady=(22, 4))
        except Exception as e:
            ctk.CTkLabel(
                topo, text=f"Não foi possível carregar a imagem:\n{e}\nCaminho: {caminho}",
                text_color="#B3261E", font=fonte(11), wraplength=330, justify="left",
            ).pack(padx=16, pady=24)

        ctk.CTkLabel(topo, text="Bem-vindo a Belém", font=fonte(26, "bold"),
                     text_color=PRIMARY).pack(pady=(8, 2))
        ctk.CTkLabel(topo, text="Entre para montar seu roteiro do seu jeito.",
                     font=fonte(13), text_color=MUTED).pack(pady=(0, 22))

    def _campo(self, rotulo, mostrar=None):
        ctk.CTkLabel(self.corpo, text=rotulo, font=fonte(13, "bold"), text_color=TEXT
                     ).pack(anchor="w", padx=6, pady=(18, 6))
        entry = ctk.CTkEntry(
            self.corpo, height=52, corner_radius=26, fg_color=PANEL,
            border_width=1, border_color=LINE, text_color=TEXT, font=fonte(14),
            show=mostrar or "",
        )
        entry.pack(fill="x")
        entry.bind("<FocusIn>", lambda _e: entry.configure(border_color=PRIMARY, border_width=2))
        entry.bind("<FocusOut>", lambda _e: entry.configure(border_color=LINE, border_width=1))
        return entry

    def _criar_formulario(self):
        self.entry_user = self._campo("Usuário")
        self.entry_pass = self._campo("Senha", mostrar="•")

        # Botão para mostrar/ocultar senha, sobre o campo
        self._senha_visivel = False
        self.btn_olho = ctk.CTkButton(
            self.entry_pass, text="Mostrar", width=64, height=32, corner_radius=16,
            fg_color=PRIMARY_SOFT, text_color=PRIMARY, hover_color="#D3DEEE",
            font=fonte(12, "bold"), command=self._alternar_senha,
        )
        self.btn_olho.place(relx=1.0, rely=0.5, x=-12, anchor="e")

        ctk.CTkButton(
            self.corpo, text="Esqueci minha senha", fg_color="transparent",
            text_color=PRIMARY, hover_color=BG, font=fonte(13, "bold"),
            width=10, height=28, cursor="hand2",
        ).pack(anchor="e", pady=(8, 0))

        self.btn_login = ctk.CTkButton(
            self.corpo, text="Entrar", height=54, corner_radius=27,
            fg_color=PRIMARY, hover_color=PRIMARY_HOVER, font=fonte(16, "bold"),
            command=self.fazer_login,
        )
        self.btn_login.pack(fill="x", pady=(22, 0))

    def _criar_rodape(self):
        rodape = ctk.CTkFrame(self.corpo, fg_color="transparent")
        rodape.pack(pady=(24, 28))
        ctk.CTkLabel(rodape, text="Ainda não tem conta?", text_color=MUTED,
                     font=fonte(13)).pack(side="left")
        ctk.CTkButton(
            rodape, text="Cadastre-se", fg_color="transparent", text_color=PRIMARY,
            hover_color=BG, font=fonte(13, "bold"), width=60, cursor="hand2",
        ).pack(side="left", padx=2)

    # ------------------------------------------------------------------
    def _alternar_senha(self):
        self._senha_visivel = not self._senha_visivel
        self.entry_pass.configure(show="" if self._senha_visivel else "•")
        self.btn_olho.configure(text="Ocultar" if self._senha_visivel else "Mostrar")

    def fazer_login(self):
        if self.on_login_success:
            self.destroy()
            self.on_login_success()


if __name__ == "__main__":
    app = JanelaLogin()
    app.mainloop()