import customtkinter as ctk
from PIL import Image

# Cores baseadas na paleta do projeto e na imagem de referência
BG = "#FFFFFF"
PRIMARY = "#062454"
PRIMARY_HOVER = "#041838"
TEXT_DARK = "#000000"
MUTED = "#6B6B6B"

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

        caminho_imagem = r"C:\Users\62477616\Documents\projeto-belem-na-mao_oficial\belem_na_mao_mvp\assets\images\imagem_login.png"
        
        try:
            imagem_pil = Image.open(caminho_imagem)
            imagem_ctk = ctk.CTkImage(light_image=imagem_pil, size=(450, 450))
            label_img = ctk.CTkLabel(frame_esq, text="", image=imagem_ctk)
            label_img.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            ctk.CTkLabel(
                frame_esq, 
                text=f"Não foi possível carregar a imagem:\n{e}", 
                text_color="red"
            ).place(relx=0.5, rely=0.5, anchor="center")

    def _criar_lado_direito(self):
        frame_dir = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        frame_dir.grid(row=0, column=1, sticky="nsew")

        form_container = ctk.CTkFrame(frame_dir, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        lbl_titulo = ctk.CTkLabel(
            form_container, text="Sign in", font=ctk.CTkFont(size=36), text_color=PRIMARY
        )
        lbl_titulo.pack(anchor="center", pady=(0, 50))

        lbl_user = ctk.CTkLabel(form_container, text="Username", font=ctk.CTkFont(size=14), text_color=MUTED)
        lbl_user.pack(anchor="w")
        
        self.entry_user = ctk.CTkEntry(
            form_container, width=320, height=30, border_width=0, 
            fg_color="transparent", text_color=TEXT_DARK, font=ctk.CTkFont(size=14)
        )
        self.entry_user.pack(anchor="w")
        
        ctk.CTkFrame(form_container, width=320, height=2, fg_color=TEXT_DARK).pack(anchor="w", pady=(0, 30))

        lbl_pass = ctk.CTkLabel(form_container, text="Password", font=ctk.CTkFont(size=14), text_color=MUTED)
        lbl_pass.pack(anchor="w")
        
        self.entry_pass = ctk.CTkEntry(
            form_container, width=320, height=30, border_width=0, 
            fg_color="transparent", show="*", text_color=TEXT_DARK, font=ctk.CTkFont(size=14)
        )
        self.entry_pass.pack(anchor="w")
        
        ctk.CTkFrame(form_container, width=320, height=2, fg_color=TEXT_DARK).pack(anchor="w", pady=(0, 40))

        btn_login = ctk.CTkButton(
            form_container, text="Sign in", width=320, height=45, 
            fg_color=PRIMARY, hover_color=PRIMARY_HOVER, corner_radius=4,
            font=ctk.CTkFont(size=15),
            command=self.fazer_login
        )
        btn_login.pack(anchor="w", pady=(0, 30))

        signup_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        signup_frame.pack(anchor="center")
        
        ctk.CTkLabel(signup_frame, text="Don't have an account?", text_color=MUTED, font=ctk.CTkFont(size=13)).pack(side="left")
        
        ctk.CTkButton(
            signup_frame, text="Sign up", fg_color="transparent", text_color=PRIMARY, 
            hover_color=BG, font=ctk.CTkFont(size=13), width=50, cursor="hand2"
        ).pack(side="left", padx=2)

    def fazer_login(self):
        if self.on_login_success:
            self.destroy()            
            self.on_login_success()   

if __name__ == "__main__":
    app = JanelaLogin()
    app.mainloop()