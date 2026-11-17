import customtkinter as ctk
from views.main_window import BelemNaMaoApp
from services.auth import JanelaLogin

def iniciar_dashboard(usuario=None):
    # Esta função é chamada quando o login ou acesso de convidado é concluído
    def ao_sair():
        app.destroy()
        login_app = JanelaLogin(on_login_success=iniciar_dashboard)
        login_app.mainloop()

    app = BelemNaMaoApp(usuario=usuario, on_logout=ao_sair)
    app.mainloop()

def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Inicia a aplicação instanciando a tela de login
    login_app = JanelaLogin(on_login_success=iniciar_dashboard)
    login_app.mainloop()

if __name__ == "__main__":
    main()
