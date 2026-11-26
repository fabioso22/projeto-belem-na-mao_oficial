"""
Design System e Tokens Visuais do BelémNaMão
Inspirado nas diretrizes modernas do Tailwind CSS e Material Symbols:
Cores profundas inspiradas no Guajará, Açaí amazônico, verdes da floresta e interfaces limpas.
Suporte nativo a Modo Claro e Modo Escuro.
"""
from pathlib import Path
import tkinter as tk
from typing import Dict, Tuple, Optional
import customtkinter as ctk
from PIL import Image, ImageDraw

# ======================================================================
# Paleta de Cores (Tuplas para suporte automático a Modo Claro e Modo Escuro)
# ======================================================================
PRIMARY = ("#00132C", "#0284C7")               # Azul Meia-Noite / Azul vibrante em Dark
PRIMARY_BTN = ("#00132C", "#0284C7")           # Botão de ação primária
PRIMARY_HOVER = ("#173860", "#0369A1")         # Hover primário
PRIMARY_CONTAINER = ("#0F2847", "#10233D")     # Container de destaque escuro
PRIMARY_SOFT = ("#EFF4FF", "#1E293B")          # Gelo / azul suave para fundos ativos
ON_PRIMARY_CONTAINER = ("#7990B4", "#94A3B8")  # Texto suave sobre container escuro

SECONDARY = ("#A13A53", "#C24B68")             # Rubi Açaí / Acento regional característico
SECONDARY_HOVER = ("#7E273C", "#9E344D")       # Hover do acento
SECONDARY_CONTAINER = ("#FD829B", "#E0657F")   # Açaí claro
SECONDARY_FIXED = ("#FFD9DE", "#40131F")       # Rosa / Açaí pastel para badges
ON_SECONDARY_FIXED = ("#400014", "#FFD9DE")    # Texto sobre badge pastel

TERTIARY = ("#047857", "#059669")              # Verde Floresta Amazônica acessível
TERTIARY_CONTAINER = ("#065F46", "#065F46")    # Container verde com texto branco
TERTIARY_FIXED = ("#D1FAE5", "#064E3B")        # Menta claro / Esmeralda escuro para status positivo
ON_TERTIARY_FIXED = ("#065F46", "#34D399")     # Alto contraste: esmeralda escuro no claro / esmeralda vibrante no escuro
ON_TERTIARY_VARIANT = ("#047857", "#6EE7B7")   # Verde legível em ambos os temas

BG = ("#F8FAFC", "#070E18")                    # Fundo geral harmônico claro (#F8FAFC) / Noite amazônica
PANEL = ("#FFFFFF", "#0E1A2B")                 # Cartões brancos (#FFFFFF) / Grafite escuro
PANEL_SUBTLE = ("#F1F5F9", "#1E293B")          # Painel elevado / fundo secundário
LINE = ("#E2E8F0", "#334155")                  # Bordas sutis padronizadas (#E2E8F0 / #334155)
LINE_LIGHT = ("#EEF2F6", "#1E293B")            # Linhas ultrafinas

# Tipografia e Contrastes Aperfeiçoados (Light Mode #0F172A/#475569 e Dark Mode #FFFFFF/#CBD5E1)
TEXT = ("#0F172A", "#FFFFFF")                  # Texto principal
TEXT_TITLE = ("#0F172A", "#FFFFFF")            # Títulos de página e cards
TEXT_EXPLORAR = ("#0F172A", "#FFFFFF")         # Alto contraste na tela Explorar
TEXT_BRAND = ("#0369A1", "#38BDF8")            # Azul celeste vibrante
TEXT_KPI = ("#0284C7", "#38BDF8")              # Valores numéricos dos KPIs
TEXT_MUTED = ("#475569", "#CBD5E1")            # Textos secundários legíveis em ambos os temas
TEXT_LIGHT = ("#64748B", "#94A3B8")            # Placeholders e textos auxiliares

# Botões Secundários Padronizados
BTN_SECONDARY_BG = ("#F8FAFC", "#1E293B")
BTN_SECONDARY_HOVER = ("#E2E8F0", "#26354D")
BTN_SECONDARY_BORDER = ("#CBD5E1", "#334155")
BTN_SECONDARY_TEXT = ("#0F172A", "#FFFFFF")
SEG_SELECTED_BG = ("#BAE6FD", "#0284C7")       # Fundo selecionado do SegmentedButton com alto contraste

# Tags e Badges Padronizadas
TAG_BG = ("#EFF6FF", "#1E293B")
TAG_BORDER = ("#BFDBFE", "#334155")
TAG_TEXT = ("#1D4ED8", "#FFFFFF")

AMBER = "#F59E0B"                               # Estrelas de avaliação e destaques solares
SUCCESS = "#10B981"                             # Sucesso / confirmado
ERROR = "#EF4444"                               # Erro / alerta

FONT_FAMILY = "Segoe UI"

# ======================================================================
# Categorias e Metadados
# ======================================================================
CATEGORIAS_INFO = {
    "Gastronomia": {
        "emoji": "🍴",
        "cor_bg": ("#FEF3EB", "#2D1A10"),
        "cor_texto": ("#9A3412", "#FDBA74"),
        "desc": "Sabores paraenses, açaí e tucupi",
        "qtd": 16
    },
    "Cultura": {
        "emoji": "🏛",
        "cor_bg": ("#EFF4FF", "#162238"),
        "cor_texto": ("#1E40AF", "#93C5FD"),
        "desc": "Arte, museus e arquitetura nobre",
        "qtd": 11
    },
    "História": {
        "emoji": "📜",
        "cor_bg": ("#FEF9C3", "#2C2607"),
        "cor_texto": ("#854D0E", "#FDE047"),
        "desc": "Marco zero 1616 e ciclo da borracha",
        "qtd": 9
    },
    "Natureza": {
        "emoji": "🌿",
        "cor_bg": ("#ECFDF5", "#0B2B1E"),
        "cor_texto": ("#065F46", "#6EE7B7"),
        "desc": "Parques, mangueiras e fauna fluvial",
        "qtd": 7
    },
    "Passeio": {
        "emoji": "🧭",
        "cor_bg": ("#F0F9FF", "#11293B"),
        "cor_texto": ("#0369A1", "#7DD3FC"),
        "desc": "Orla, docas e travessias nas ilhas",
        "qtd": 5
    },
}

# ======================================================================
# Helpers Tipográficos
# ======================================================================
def fonte(size: int = 14, weight: str = "normal") -> ctk.CTkFont:
    """Retorna uma fonte configurada com o padrão da identidade visual."""
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight=weight)


# ======================================================================
# Gerenciamento e Cache de Imagens em Alta Performance (Multi-Janela Seguro)
# ======================================================================
_CACHE_PIL_IMAGENS: Dict[Tuple[str, int, int, int, bool], Image.Image] = {}
_CACHE_CTK_IMAGENS: Dict[Tuple[str, int, int, int, bool], ctk.CTkImage] = {}
_ULTIMO_ROOT_ID: Optional[int] = None


def limpar_cache_imagens_tk() -> None:
    """Limpa o cache de CTkImage ao encerrar uma janela Tk, mantendo o cache PIL puro."""
    global _ULTIMO_ROOT_ID
    _CACHE_CTK_IMAGENS.clear()
    _ULTIMO_ROOT_ID = None

def obter_caminho_imagem_local(local_id: str) -> Optional[Path]:
    """Localiza o arquivo de imagem do local em assets/images."""
    raiz = Path(__file__).resolve().parents[1]
    pasta_imagens = raiz / "assets" / "images"
    
    extensoes = [".jpg", ".png", ".jpeg"]
    for ext in extensoes:
        candidato = pasta_imagens / f"{local_id}{ext}"
        if candidato.is_file():
            return candidato
            
    # Mapeamentos alternativos de ID
    mapa_aliases = {
        "teatro-da-paz": "teatro-da-paz.jpg",
        "praca-republica": "praca-republica.jpg",
        "basilica-nazare": "basilica-nazare.jpg",
        "feliz-lusitania": "feliz-lusitania.jpg",
        "ver-o-peso": "ver-o-peso.jpg",
        "estacao-das-docas": "estacao-das-docas.jpg",
        "mangal": "mangal.jpg",
        "ilha-combu": "ilha-combu.jpg",
        "bistro-guajara-noturno": "bistro-guajara-noturno.jpg",
    }
    alias = mapa_aliases.get(local_id)
    if alias and (pasta_imagens / alias).is_file():
        return pasta_imagens / alias
        
    return None


def obter_imagem_processada(
    local_id: str,
    largura: int,
    altura: int,
    raio: int = 12,
    apenas_topo: bool = False
) -> ctk.CTkImage:
    """
    Carrega, recorta no aspecto desejado, arredonda cantos e retorna um CTkImage
    vinculado com segurança à janela Tk atual (evita TclError após logout/troca).
    """
    global _ULTIMO_ROOT_ID
    root_atual_id = id(tk._default_root) if tk._default_root is not None else None
    if root_atual_id != _ULTIMO_ROOT_ID:
        _CACHE_CTK_IMAGENS.clear()
        _ULTIMO_ROOT_ID = root_atual_id

    chave = (local_id, largura, altura, raio, apenas_topo)
    if chave in _CACHE_CTK_IMAGENS:
        return _CACHE_CTK_IMAGENS[chave]

    img = _CACHE_PIL_IMAGENS.get(chave)
    if img is None:
        caminho = obter_caminho_imagem_local(local_id)
        if caminho and caminho.is_file():
            try:
                with Image.open(caminho) as raw:
                    if raw.format == "JPEG":
                        raw.draft("RGB", (largura * 2, altura * 2))
                    img = raw.convert("RGBA")
                target_ratio = largura / altura
                img_ratio = img.width / img.height
                if img_ratio > target_ratio:
                    new_w = int(img.height * target_ratio)
                    left = (img.width - new_w) // 2
                    img = img.crop((left, 0, left + new_w, img.height))
                else:
                    new_h = int(img.width / target_ratio)
                    top = (img.height - new_h) // 2
                    img = img.crop((0, top, img.width, top + new_h))
                img = img.resize((largura, altura), Image.Resampling.BILINEAR)
            except Exception:
                img = _criar_imagem_placeholder(local_id, largura, altura)
        else:
            img = _criar_imagem_placeholder(local_id, largura, altura)

        # Arredondamento suave de cantos com máscara alpha
        if raio > 0:
            mascara = Image.new("L", (largura, altura), 0)
            draw = ImageDraw.Draw(mascara)
            if apenas_topo:
                draw.rounded_rectangle((0, 0, largura, altura), radius=raio, corners=(True, True, False, False), fill=255)
            else:
                draw.rounded_rectangle((0, 0, largura, altura), radius=raio, fill=255)
            img.putalpha(mascara)

        _CACHE_PIL_IMAGENS[chave] = img

    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(largura, altura))
    _CACHE_CTK_IMAGENS[chave] = ctk_img
    return ctk_img


def _criar_imagem_placeholder(local_id: str, largura: int, altura: int) -> Image.Image:
    """Gera um banner estilizado em gradiente sutil quando não há foto."""
    img = Image.new("RGBA", (largura, altura), (15, 40, 71, 255))
    draw = ImageDraw.Draw(img)
    
    for y in range(altura):
        fator = y / altura
        r = int(15 + fator * 10)
        g = int(40 + fator * 20)
        b = int(71 + fator * 40)
        draw.line([(0, y), (largura, y)], fill=(r, g, b, 255))
        
    return img
