import customtkinter as ctk
from views.main_window import BelemNaMaoApp
from services.auth import JanelaLogin  # Importando a sua nova tela de login

def iniciar_dashboard():
    # Esta função será chamada apenas quando o login for concluído
    app = BelemNaMaoApp()
    app.mainloop()

def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Inicia a aplicação instanciando a tela de login
    # Passamos iniciar_dashboard como o comando a ser executado em caso de sucesso
    login_app = JanelaLogin(on_login_success=iniciar_dashboard)
    login_app.mainloop()

if __name__ == "__main__":
    main()