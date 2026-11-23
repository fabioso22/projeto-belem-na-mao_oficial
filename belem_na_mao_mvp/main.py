import customtkinter as ctk
from views.main_window import BelemNaMaoApp
from views.admin_window import PainelAdminApp
from services.auth import JanelaLogin


def iniciar_painel_admin(usuario=None):
    """Abre o Painel Admin (DataInsight: Pandas + Matplotlib) com botão para voltar ao login."""
    def ao_sair_admin():
        admin_app.destroy()
        login_app = JanelaLogin(
            on_login_success=iniciar_dashboard,
            on_admin_login=iniciar_painel_admin,
        )
        login_app.mainloop()

    admin_app = PainelAdminApp(usuario=usuario, on_logout=ao_sair_admin)
    admin_app.mainloop()


def iniciar_dashboard(usuario=None):
    # Roteamento automático caso o login retorne um usuário administrador
    if usuario and usuario.get("is_admin"):
        iniciar_painel_admin(usuario)
        return

    # Esta função é chamada quando o login ou acesso de convidado é concluído
    def ao_sair():
        app.destroy()
        login_app = JanelaLogin(
            on_login_success=iniciar_dashboard,
            on_admin_login=iniciar_painel_admin,
        )
        login_app.mainloop()

    app = BelemNaMaoApp(usuario=usuario, on_logout=ao_sair)
    app.mainloop()


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Inicia a aplicação instanciando a tela de login
    login_app = JanelaLogin(
        on_login_success=iniciar_dashboard,
        on_admin_login=iniciar_painel_admin,
    )
    login_app.mainloop()


if __name__ == "__main__":
    main()
