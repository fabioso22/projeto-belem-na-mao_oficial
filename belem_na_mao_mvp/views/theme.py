"""
Design System e Tokens Visuais do BelémNaMão
Inspirado nas diretrizes modernas do Tailwind CSS e Material Symbols:
Cores profundas inspiradas no Guajará, Açaí amazônico, verdes da floresta e interfaces limpas.
Suporte nativo a Modo Claro e Modo Escuro.
"""
from pathlib import Path
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

TERTIARY = ("#012E21", "#024733")              # Verde Floresta Amazônica profundo
TERTIARY_CONTAINER = ("#0A4D38", "#083C2C")    # Container verde
TERTIARY_FIXED = ("#C0ECD7", "#0D3325")        # Menta claro para status positivo
ON_TERTIARY_FIXED = ("#002116", "#C0ECD7")     # Texto escuro sobre menta
ON_TERTIARY_VARIANT = ("#264E3F", "#A4D0BC")   # Verde floresta médio

BG = ("#F8F9FF", "#070E18")                    # Fundo geral ultra clean / Noite amazônica
PANEL = ("#FFFFFF", "#0E1A2B")                 # Cartões e superfícies brancas / Grafite escuro
PANEL_SUBTLE = ("#F1F5F9", "#1E293B")          # Painel elevado / fundo secundário #1E293B
LINE = ("#E2E8F0", "#334155")                  # Bordas sutis padronizadas em 1px #334155
LINE_LIGHT = ("#EEF2F6", "#1E293B")            # Linhas ultrafinas

# Tipografia e Contrastes Aperfeiçoados (Prioridade Máxima Tema Escuro)
TEXT = ("#0B1C30", "#FFFFFF")                  # Texto principal: branco puro #FFFFFF no escuro
TEXT_TITLE = ("#00132C", "#FFFFFF")            # Títulos de página e cards: branco puro #FFFFFF
TEXT_EXPLORAR = ("#0B1C30", "#FFFFFF")         # Alto contraste na tela Explorar (#FFFFFF no escuro)
TEXT_BRAND = ("#0369A1", "#38BDF8")            # Azul celeste vibrante #38BDF8
TEXT_KPI = ("#0284C7", "#38BDF8")              # Valores numéricos dos KPIs: celeste #38BDF8
TEXT_MUTED = ("#475569", "#CBD5E1")            # Textos secundários legíveis em tema escuro
TEXT_LIGHT = ("#64748B", "#CBD5E1")            # Placeholders e textos auxiliares: #CBD5E1

# Botões Secundários Padronizados (Fundo #1E293B, Borda #334155, Texto #FFFFFF no escuro)
BTN_SECONDARY_BG = ("#F1F5F9", "#1E293B")
BTN_SECONDARY_HOVER = ("#E2E8F0", "#26354D")
BTN_SECONDARY_BORDER = ("#CBD5E1", "#334155")
BTN_SECONDARY_TEXT = ("#0B1C30", "#FFFFFF")
SEG_SELECTED_BG = ("#93C5FD", "#0284C7")       # Fundo selecionado do SegmentedButton com ótimo contraste

# Tags e Badges Padronizadas
TAG_BG = ("#EFF6FF", "#1E293B")
TAG_BORDER = ("#BFDBFE", "#334155")
TAG_TEXT = ("#1E40AF", "#FFFFFF")

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
# Gerenciamento e Cache de Imagens em Alta Performance
# ======================================================================
_CACHE_CTK_IMAGENS: Dict[Tuple[str, int, int, int], ctk.CTkImage] = {}

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
    Carrega, recorta no aspecto desejado com LANCZOS, arredonda cantos e
    retorna um CTkImage com cache inteligente para máxima fluidez.
    """
    chave = (local_id, largura, altura, raio, apenas_topo)
    if chave in _CACHE_CTK_IMAGENS:
        return _CACHE_CTK_IMAGENS[chave]

    caminho = obter_caminho_imagem_local(local_id)
    if caminho and caminho.is_file():
        try:
            img = Image.open(caminho).convert("RGBA")
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
            img = img.resize((largura, altura), Image.LANCZOS)
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
