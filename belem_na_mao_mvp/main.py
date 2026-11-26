import customtkinter as ctk
from views.main_window import BelemNaMaoApp
from views.admin_window import PainelAdminApp
from views.theme import limpar_cache_imagens_tk
from services.auth import JanelaLogin


def iniciar_painel_admin(usuario=None):
    """Abre o Painel Admin (DataInsight: Pandas + Matplotlib) com botão para voltar ao login."""
    voltar_login = {"ativo": False}

    def ao_sair_admin():
        voltar_login["ativo"] = True
        admin_app.destroy()

    admin_app = PainelAdminApp(usuario=usuario, on_logout=ao_sair_admin)
    admin_app.mainloop()
    limpar_cache_imagens_tk()
    return ("login", None) if voltar_login["ativo"] else (None, None)


def iniciar_dashboard(usuario=None):
    """Abre o dashboard do turista (ou roteia para admin) de forma sequencial sem mainloop aninhado."""
    if usuario and usuario.get("is_admin"):
        return iniciar_painel_admin(usuario)

    voltar_login = {"ativo": False}

    def ao_sair():
        voltar_login["ativo"] = True
        app.destroy()

    app = BelemNaMaoApp(usuario=usuario, on_logout=ao_sair)
    app.mainloop()
    limpar_cache_imagens_tk()
    return ("login", None) if voltar_login["ativo"] else (None, None)


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    destino = "login"
    usuario_atual = None

    while destino is not None:
        if destino == "login":
            proximo = {"destino": None, "usuario": None}

            def ao_logar(u=None):
                if u and u.get("is_admin"):
                    proximo["destino"] = "admin"
                else:
                    proximo["destino"] = "turista"
                proximo["usuario"] = u

            def ao_logar_admin(u=None):
                proximo["destino"] = "admin"
                proximo["usuario"] = u

            login_app = JanelaLogin(
                on_login_success=ao_logar,
                on_admin_login=ao_logar_admin,
            )
            login_app.mainloop()
            limpar_cache_imagens_tk()
            destino, usuario_atual = proximo["destino"], proximo["usuario"]
        elif destino == "admin":
            destino, usuario_atual = iniciar_painel_admin(usuario_atual)
        elif destino == "turista":
            destino, usuario_atual = iniciar_dashboard(usuario_atual)
        else:
            break


if __name__ == "__main__":
    main()
