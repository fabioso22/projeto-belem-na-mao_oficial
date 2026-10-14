from pathlib import Path
from PIL import Image
import customtkinter as ctk

# Cores baseadas na paleta do projeto e na imagem de referência
BG = "#FFFFFF"
PRIMARY = "#062454"
PRIMARY_HOVER = "#041838"
TEXT_DARK = "#000000"
MUTED = "#6B6B6B"

# Função para obter o caminho da imagem de login, considerando diferentes estruturas de diretórios, até criar o banco de dados
def obter_caminho_imagem() -> Path:
  diretorio_script = Path(__file__).resolve().parent

  # Lista de locais possíveis para encontrar a imagem conforme a estrutura do projeto
  possiveis_caminhos = [
      # Se o script está dentro de 'services/' e 'assets/' está no mesmo nível que 'services/':
      diretorio_script.parent / "assets" / "images" / "imagem_login.png",
      # Se o script está na raiz do projeto:
      (
          diretorio_script
          / "belem_na_mao_mvp"
          / "assets"
          / "images"
          / "imagem_login.png"
      ),
      # Se o script está diretamente dentro da pasta 'belem_na_mao_mvp':
      diretorio_script / "assets" / "images" / "imagem_login.png",
      # Se o script está em 'services/' e precisa subir 2 níveis:
      (
          diretorio_script.parent.parent
          / "belem_na_mao_mvp"
          / "assets"
          / "images"
          / "imagem_login.png"
      ),
  ]

  for caminho in possiveis_caminhos:
    if caminho.is_file():
      return caminho

  return possiveis_caminhos[0]
#-----------------FIM--------------------------#

class JanelaLogin(ctk.CTk):

  def __init__(self, on_login_success=None):
    super().__init__()
    self.on_login_success = on_login_success
    self.title("Login")

    self.geometry("900x550")
    self.minsize(800, 500)
    self.configure(fg_color=BG)

    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=1)
    self.grid_rowconfigure(0, weight=1)

    self._criar_lado_esquerdo()
    self._criar_lado_direito()

  def _criar_lado_esquerdo(self):
    frame_esq = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
    frame_esq.grid(row=0, column=0, sticky="nsew")

    caminho_imagem = obter_caminho_imagem()

    try:
      imagem_pil = Image.open(caminho_imagem)
      imagem_ctk = ctk.CTkImage(light_image=imagem_pil, size=(450, 450))
      label_img = ctk.CTkLabel(frame_esq, text="", image=imagem_ctk)
      label_img.place(relx=0.5, rely=0.5, anchor="center")
    except Exception as e:
      ctk.CTkLabel(
          frame_esq,
          text=(
              "Não foi possível carregar a imagem:\n"
              f"{e}\n"
              f"Tentando acessar: {caminho_imagem}"
          ),
          text_color="red",
      ).place(relx=0.5, rely=0.5, anchor="center")

  def _criar_lado_direito(self):
    frame_dir = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
    frame_dir.grid(row=0, column=1, sticky="nsew")

    form_container = ctk.CTkFrame(frame_dir, fg_color="transparent")
    form_container.place(relx=0.5, rely=0.5, anchor="center")

    lbl_titulo = ctk.CTkLabel(
        form_container,
        text="Sign in",
        font=ctk.CTkFont(size=36),
        text_color=PRIMARY,
    )
    lbl_titulo.pack(anchor="center", pady=(0, 50))

    lbl_user = ctk.CTkLabel(
        form_container,
        text="Username",
        font=ctk.CTkFont(size=14),
        text_color=MUTED,
    )
    lbl_user.pack(anchor="w")

    self.entry_user = ctk.CTkEntry(
        form_container,
        width=320,
        height=30,
        border_width=0,
        fg_color="transparent",
        text_color=TEXT_DARK,
        font=ctk.CTkFont(size=14),
    )
    self.entry_user.pack(anchor="w")

    ctk.CTkFrame(
        form_container, width=320, height=2, fg_color=TEXT_DARK
    ).pack(anchor="w", pady=(0, 30))

    lbl_pass = ctk.CTkLabel(
        form_container,
        text="Password",
        font=ctk.CTkFont(size=14),
        text_color=MUTED,
    )
    lbl_pass.pack(anchor="w")

    self.entry_pass = ctk.CTkEntry(
        form_container,
        width=320,
        height=30,
        border_width=0,
        fg_color="transparent",
        show="*",
        text_color=TEXT_DARK,
        font=ctk.CTkFont(size=14),
    )
    self.entry_pass.pack(anchor="w")

    ctk.CTkFrame(
        form_container, width=320, height=2, fg_color=TEXT_DARK
    ).pack(anchor="w", pady=(0, 40))

    btn_login = ctk.CTkButton(
        form_container,
        text="Sign in",
        width=320,
        height=45,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        corner_radius=4,
        font=ctk.CTkFont(size=15),
        command=self.fazer_login,
    )
    btn_login.pack(anchor="w", pady=(0, 30))

    signup_frame = ctk.CTkFrame(form_container, fg_color="transparent")
    signup_frame.pack(anchor="center")

    ctk.CTkLabel(
        signup_frame,
        text="Don't have an account?",
        text_color=MUTED,
        font=ctk.CTkFont(size=13),
    ).pack(side="left")

    ctk.CTkButton(
        signup_frame,
        text="Sign up",
        fg_color="transparent",
        text_color=PRIMARY,
        hover_color=BG,
        font=ctk.CTkFont(size=13),
        width=50,
        cursor="hand2",
    ).pack(side="left", padx=2)

  def fazer_login(self):
    if self.on_login_success:
      self.destroy()
      self.on_login_success()


if __name__ == "__main__":
  app = JanelaLogin()
  app.mainloop()