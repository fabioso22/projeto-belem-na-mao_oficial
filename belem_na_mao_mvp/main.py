import customtkinter as ctk
from views.main_window import BelemNaMaoApp


def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = BelemNaMaoApp()
    app.mainloop()


if __name__ == "__main__":
    main()