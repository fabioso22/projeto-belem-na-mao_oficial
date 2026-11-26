"""
Módulo centralizado de Internacionalização (i18n) do BelémNaMão.
Suporta Português (BR) como padrão, Inglês (EN) e Espanhol (ES).
"""
from typing import Any, Dict, List, Tuple

IDIOMAS_DISPONIVEIS: Tuple[str, ...] = ("pt-br", "en", "es")
ROTULOS_IDIOMA: Dict[str, str] = {
    "pt-br": "PT-BR",
    "en": "EN",
    "es": "ES",
}

_IDIOMA_ATUAL: str = "pt-br"


def get_idioma() -> str:
    """Retorna o código do idioma ativo ('pt-br', 'en' ou 'es')."""
    return _IDIOMA_ATUAL


def set_idioma(codigo: str) -> str:
    """Define o idioma ativo e retorna o código normalizado."""
    global _IDIOMA_ATUAL
    norm = str(codigo or "").strip().lower()
    if norm in IDIOMAS_DISPONIVEIS:
        _IDIOMA_ATUAL = norm
    return _IDIOMA_ATUAL


# ======================================================================
# Dicionário Centralizado de Traduções (UI, Menus, Filtros e Mensagens)
# ======================================================================
TRADUCOES: Dict[str, Dict[str, str]] = {
    "pt-br": {
        # Janela e Navegação Principal
        "app_title": "BelémNaMão — Guia Inteligente da Amazônia Atlântica",
        "clima_pill": "🕒 Chuva das 16h: Provável (82%)  •  🌊 Maré: Enchendo",
        "nav_inicio": "Início",
        "nav_explorar": "Explorar",
        "nav_roteiro": "Meu Roteiro",
        "nav_ranking": "Mais Visitados",
        "btn_buscar_nav": "🔍 Buscar...",
        "btn_salvos_nav": "🔖 {n} salvos",
        "tema_claro": "☀️ Modo Claro",
        "tema_escuro": "🌙 Modo Escuro",
        "toast_tema_claro": "Modo Claro ativado",
        "toast_tema_escuro": "Modo Escuro ativado",
        "ola_usuario": "Olá, {nome}",
        "btn_sair": "🚪 Sair",
        "rodape_texto": "BelémNaMão • Guia Inteligente da Amazônia Atlântica",
        "idioma_label": "Idioma:",
        "toast_idioma": "Idioma alterado para Português (BR)",

        # Tela Início
        "hero_titulo": "Descubra Belém do seu jeito",
        "hero_subtitulo": "Menos tempo procurando. Mais tempo vivendo as feiras, docas, noites e sabores da Amazônia Atlântica.",
        "hero_btn_explorar": "Explorar Catálogo  →",
        "hero_btn_roteiro": "Ver Meu Roteiro",
        "inicio_cats_titulo": "O que você quer fazer?",
        "cat_experiencias": "{qtd} experiências",
        "inicio_destaques_titulo": "Destaques de Belém",
        "inicio_destaques_ver_todas": "Ver todas as atrações  →",
        "btn_add_roteiro": "+ Roteiro",
        "btn_no_roteiro": "✓ No Roteiro",
        "btn_detalhes": "Detalhes",

        # Tela Explorar
        "explorar_eyebrow": "EXPLORAR PARÁ",
        "explorar_titulo": "Explorar Belém",
        "explorar_subtitulo": "Descubra pontos turísticos, feiras culturais, gastronomia ribeirinha e vida noturna.",
        "explorar_busca_placeholder": "Buscar por nome, bairro (ex: Cidade Velha, Campina, Umarizal) ou palavra-chave...",
        "explorar_preco_label": "Preço:",
        "explorar_contagem": "Mostrando {n} de {total} locais",
        "filtro_todos_bairros": "Todos os Bairros",
        "vazio_titulo": "Nenhum local encontrado",
        "vazio_subtitulo": "Tente outro termo na busca ou remova algum filtro de categoria/bairro.",
        "vazio_btn_limpar": "Limpar Filtros",

        # Tela Detalhes
        "btn_voltar": "‹ Voltar",
        "breadcrumb_inicio": "Início",
        "breadcrumb_explorar": "Explorar",
        "btn_compartilhar": "Compartilhar",
        "toast_compartilhar": "Link copiado para a área de transferência!",
        "btn_salvar_fav": "Salvar nos Favoritos",
        "btn_salvo_roteiro": "✓ Salvo no Roteiro",
        "avaliacoes_suffix": "avaliações",
        "detalhes_sobre_titulo": "Sobre o Local",
        "detalhes_importancia": "Importância e Memória:",
        "detalhes_destaques_titulo": "Destaques & Por Que Visitar",
        "detalhes_ingresso": "FAIXA DE PREÇO & ACESSO",
        "detalhes_aberto_agora": "● Funcionamento",
        "detalhes_clima": "🌧️ Previsão: Chuva rápida às 16h; noite agradável com brisa da baía (27°C)",
        "detalhes_add_roteiro": "+ Adicionar ao Meu Roteiro",
        "detalhes_salvo_roteiro": "✓ Salvo no Meu Roteiro",
        "detalhes_maps": "🗺️ Abrir Rota no Google Maps",
        "detalhes_tempo_sugerido": "Tempo sugerido: {duracao}",
        "detalhes_clima_ar": "Opções climatizadas e ao ar livre",
        "detalhes_fotos": "Permitido fotos (atenção às normas locais)",
        "detalhes_acessibilidade": "Acesso facilitado para visitantes",

        # Tela Meu Roteiro
        "roteiro_tag": "ROTEIRO INTELIGENTE • PARÁ",
        "roteiro_titulo": "O Melhor de Belém Histórica, Baía & Noite",
        "roteiro_subtitulo": "Percurso com os aromas do Ver-o-Peso, a imponência de 1616 e a gastronomia noturna da cidade.",
        "btn_otimizar_ia": "✨ Otimizar Ordem (IA)",
        "btn_salvar": "💾 Salvar",
        "btn_limpar": "Limpar",
        "kpi_duracao": "Duração Total",
        "kpi_paradas": "Paradas Salvas",
        "kpi_gasto": "Estimativa de Gasto",
        "kpi_distancia": "Distância a Pé",
        "kpi_duracao_val": "~{h}h com pausas",
        "kpi_paradas_val": "{n} locais programados",
        "kpi_paradas_zero": "0 locais",
        "kpi_gasto_val": "R$ {v} / pessoa",
        "kpi_distancia_val": "{km} km a pé",
        "turno_manha_titulo": "🌅 Turno da Manhã (08h00 às 12h30)",
        "turno_manha_sub": "Coração Histórico e Gastronômico",
        "conector_manha": "🚶 Caminhada leve de 6 min (450m) via Boulevard Castilhos França",
        "almoco_tag": "PAUSA DE ALMOÇO SUGERIDA • 12:30 - 14:00",
        "almoco_titulo": "Casa das Onze Janelas ou Box do Peixe Frito com Açaí",
        "almoco_desc": "Opte por almoçar com vista para a baía (filhote e tucupi) ou no autêntico box da feira.",
        "turno_tarde_titulo": "🌙 Tarde & Noite (14h30 às 23h00)",
        "turno_tarde_sub": "Arquitetura, Pôr do Sol e Gastronomia Noturna",
        "conector_carro": "🚗 Deslocamento de 8 min (2.1 km) para evitar o calor do meio-dia",
        "conector_tarde": "🚶 Caminhada arborizada até o entardecer e programação noturna",
        "btn_ver_guia": "Ver Guia",
        "rota_titulo": "Traçado da Rota (Dia 1)",
        "rota_subtitulo": "{n} Paradas conectadas em Belém",
        "btn_maps_rota": "Abrir Trajeto no Google Maps ↗",
        "checklist_titulo": "O que levar no dia",
        "checklist_sub": "Itens essenciais para o clima equatorial",
        "check_1": "Guarda-chuva compacto ou capa",
        "check_2": "Dinheiro em espécie (trocado para feirantes)",
        "check_3": "Calçado leve e antiderrapante (paralelepípedo úmido)",
        "check_4": "Garrafa d'água reutilizável (hidratação)",
        "sugestoes_titulo": "Adicionar Paradas Sugeridas",
        "roteiro_vazio_titulo": "Seu roteiro ainda está vazio",
        "roteiro_vazio_desc": "Explore as atrações de Belém e clique em '+ Roteiro' para montar seu roteiro personalizado.",
        "roteiro_vazio_btn": "Explorar Locais de Belém",
        "toast_add_roteiro": "✓ {nome} adicionado ao roteiro!",
        "toast_rem_roteiro": "{nome} removido do roteiro",
        "toast_rem_generico": "Local removido do roteiro",
        "toast_ia_otimizado": "✨ Ordem ideal recalculada com fluxo diurno e noturno!",
        "toast_roteiro_salvo": "💾 Roteiro com {n} locais salvo com sucesso!",
        "toast_roteiro_limpo": "Roteiro limpo",

        # Tela Mais Visitados (Ranking)
        "ranking_eyebrow": "EM ALTA EM BELÉM",
        "ranking_titulo": "Mais Visitados",
        "ranking_subtitulo": "Acompanhe os destinos mais populares e bem avaliados de Belém por semana, mês ou ano.",
        "ranking_periodo_label": "Período:",
        "ranking_mes_label": "Mês:",
        "ranking_ano_label": "Ano:",
        "periodo_semana": "Semana",
        "periodo_mes": "Mês",
        "periodo_ano": "Ano",
        "ranking_kpi_visitas": "Visitas no Período",
        "ranking_kpi_lider": "Líder do Ranking",
        "ranking_kpi_media": "Média Ponderada Geral",
        "ranking_visitas_qtd": "{n} visitas",
        "ranking_avaliacoes_qtd": "{n} avaliações",
        "ranking_fonte_mysql": "● Conectado ao MySQL",
        "ranking_fonte_local": "● Base Estruturada Local",
        "ranking_subtitulo_periodo_semana": "Ranking semanal referente a {mes} de {ano}",
        "ranking_subtitulo_periodo_mes": "Consolidado mensal de {mes} de {ano}",
        "ranking_subtitulo_periodo_ano": "Consolidado anual completo de {ano}",
        "ranking_vazio": "Nenhum dado de visitação encontrado para o filtro selecionado.",

        # Login & Cadastro
        "login_window_title": "BelémNaMão — Guia Inteligente",
        "login_selo": "● Pará, Amazônia",
        "login_boas_vindas": "Bem-vindo a Belém",
        "login_subtitulo": "Entre para montar seu roteiro do seu jeito e explorar a história, gastronomia e vida noturna da cidade das mangueiras.",
        "login_demo_label": "💡 Demo:",
        "login_btn_preencher": "Preencher",
        "login_btn_pronto": "✓ Pronto!",
        "login_demo_msg": "Credenciais demo inseridas. Clique em 'Entrar'.",
        "login_user_label": "USUÁRIO OU E-MAIL",
        "login_user_placeholder": "ex: turista ou nome@exemplo.com",
        "login_pass_label": "SENHA",
        "login_pass_placeholder": "Digite sua senha de acesso",
        "login_mostrar": "Mostrar",
        "login_ocultar": "Ocultar",
        "login_lembrar": "Permanecer conectado neste computador",
        "login_entrar": "Entrar  →",
        "login_convidado": "Continuar sem login (Convidado)",
        "login_sem_conta": "Ainda não tem conta?",
        "login_cadastre_se": "Cadastre-se",
        "login_rodape": "© 2026 BelémNaMão Guia Inteligente • Feito no Pará",
        "login_erro_vazio": "Por favor, preencha o usuário e a senha.",
        "login_erro_invalido": "Usuário ou senha incorretos. Dica: use o botão 'Preencher' ou senha 'admin'.",
        "login_cadastro_ok": "Conta '{user}' cadastrada com sucesso! Digite sua senha para entrar.",
        "login_showcase_pill": "★ Pôr do sol na Baía do Guajará",
        "login_showcase_tag": "AMAZÔNIA URBANA & CULTURAL",
        "login_showcase_titulo": "Descubra as cores, sabores e a história viva de Belém do Pará.",
        "login_showcase_desc": "Pontos turísticos catalogados, feiras tradicionais, noites gastronômicas nas docas e roteiros fluviais ao alcance das suas mãos.",
        "cad_window_title": "Criar Conta — BelémNaMão",
        "cad_titulo": "Criar sua Conta",
        "cad_subtitulo": "Cadastre-se para personalizar roteiros, salvar atrações favoritas e explorar a cidade.",
        "cad_nome": "Nome completo",
        "cad_nome_ph": "ex: Maria Santos",
        "cad_usuario": "Nome de usuário (login)",
        "cad_usuario_ph": "ex: mariasantos",
        "cad_email": "E-mail",
        "cad_email_ph": "ex: maria@exemplo.com",
        "cad_senha": "Senha (mínimo 4 dígitos)",
        "cad_senha_ph": "Digite sua senha",
        "cad_confirma": "Confirmar senha",
        "cad_confirma_ph": "Repita a senha",
        "cad_btn_criar": "Criar minha conta",
        "cad_btn_voltar": "Voltar ao login",
        "cad_erro_campos": "Preencha nome, usuário e senha.",
        "cad_erro_senha_curta": "A senha deve ter no mínimo 4 dígitos.",
        "cad_erro_confirma": "As senhas digitadas não coincidem.",
    },
    "en": {
        # Window & Navbar
        "app_title": "BelémNaMão — Smart Guide to Atlantic Amazonia",
        "clima_pill": "🕒 4 PM Rain: Likely (82%)  •  🌊 Tide: Rising",
        "nav_inicio": "Home",
        "nav_explorar": "Explore",
        "nav_roteiro": "My Itinerary",
        "nav_ranking": "Most Visited",
        "btn_buscar_nav": "🔍 Search...",
        "btn_salvos_nav": "🔖 {n} saved",
        "tema_claro": "☀️ Light Mode",
        "tema_escuro": "🌙 Dark Mode",
        "toast_tema_claro": "Light Mode enabled",
        "toast_tema_escuro": "Dark Mode enabled",
        "ola_usuario": "Hi, {nome}",
        "btn_sair": "🚪 Sign out",
        "rodape_texto": "BelémNaMão • Smart Guide to Atlantic Amazonia",
        "idioma_label": "Language:",
        "toast_idioma": "Language switched to English",

        # Home Screen
        "hero_titulo": "Discover Belém your way",
        "hero_subtitulo": "Less time searching. More time experiencing open markets, waterfront docks, nightlife, and Amazonian flavors.",
        "hero_btn_explorar": "Explore Catalog  →",
        "hero_btn_roteiro": "View My Itinerary",
        "inicio_cats_titulo": "What would you like to do?",
        "cat_experiencias": "{qtd} experiences",
        "inicio_destaques_titulo": "Belém Highlights",
        "inicio_destaques_ver_todas": "See all attractions  →",
        "btn_add_roteiro": "+ Itinerary",
        "btn_no_roteiro": "✓ In Itinerary",
        "btn_detalhes": "Details",

        # Explore Screen
        "explorar_eyebrow": "EXPLORE PARÁ",
        "explorar_titulo": "Explore Belém",
        "explorar_subtitulo": "Discover landmarks, cultural markets, riverside gastronomy, and vibrant nightlife spots.",
        "explorar_busca_placeholder": "Search by name, neighborhood (e.g. Cidade Velha, Campina, Umarizal) or keyword...",
        "explorar_preco_label": "Price:",
        "explorar_contagem": "Showing {n} of {total} places",
        "filtro_todos_bairros": "All Neighborhoods",
        "vazio_titulo": "No places found",
        "vazio_subtitulo": "Try a different search term or clear category/neighborhood filters.",
        "vazio_btn_limpar": "Clear Filters",

        # Details Screen
        "btn_voltar": "‹ Back",
        "breadcrumb_inicio": "Home",
        "breadcrumb_explorar": "Explore",
        "btn_compartilhar": "Share",
        "toast_compartilhar": "Link copied to clipboard!",
        "btn_salvar_fav": "Save to Favorites",
        "btn_salvo_roteiro": "✓ Saved in Itinerary",
        "avaliacoes_suffix": "reviews",
        "detalhes_sobre_titulo": "About This Place",
        "detalhes_importancia": "Significance & Heritage:",
        "detalhes_destaques_titulo": "Highlights & Why Visit",
        "detalhes_ingresso": "PRICE TIER & ACCESS",
        "detalhes_aberto_agora": "● Hours",
        "detalhes_clima": "🌧️ Forecast: Brief rain at 4 PM; pleasant evening breeze by the bay (27°C)",
        "detalhes_add_roteiro": "+ Add to My Itinerary",
        "detalhes_salvo_roteiro": "✓ Saved in My Itinerary",
        "detalhes_maps": "🗺️ Open Route in Google Maps",
        "detalhes_tempo_sugerido": "Suggested time: {duracao}",
        "detalhes_clima_ar": "Air-conditioned & open-air areas",
        "detalhes_fotos": "Photos allowed (check local guidelines)",
        "detalhes_acessibilidade": "Visitor-friendly access",

        # My Itinerary Screen
        "roteiro_tag": "SMART ITINERARY • PARÁ",
        "roteiro_titulo": "Best of Historic Belém, Bay & Nightlife",
        "roteiro_subtitulo": "A route through Ver-o-Peso aromas, 1616 heritage, and the city's nighttime dining scene.",
        "btn_otimizar_ia": "✨ Optimize Order (AI)",
        "btn_salvar": "💾 Save",
        "btn_limpar": "Clear",
        "kpi_duracao": "Total Duration",
        "kpi_paradas": "Saved Stops",
        "kpi_gasto": "Estimated Budget",
        "kpi_distancia": "Walking Distance",
        "kpi_duracao_val": "~{h}h with breaks",
        "kpi_paradas_val": "{n} scheduled places",
        "kpi_paradas_zero": "0 places",
        "kpi_gasto_val": "R$ {v} / person",
        "kpi_distancia_val": "{km} km walk",
        "turno_manha_titulo": "🌅 Morning Shift (08:00 AM – 12:30 PM)",
        "turno_manha_sub": "Historic & Gastronomic Heart",
        "conector_manha": "🚶 Easy 6 min walk (450m) along Boulevard Castilhos França",
        "almoco_tag": "SUGGESTED LUNCH BREAK • 12:30 - 14:00",
        "almoco_titulo": "Casa das Onze Janelas or Fried Fish & Açaí Stall",
        "almoco_desc": "Enjoy bayfront dining (filhote fish & tucupi) or an authentic market stall lunch.",
        "turno_tarde_titulo": "🌙 Afternoon & Night (02:30 PM – 11:00 PM)",
        "turno_tarde_sub": "Architecture, Sunset & Evening Dining",
        "conector_carro": "🚗 Short 8 min ride (2.1 km) to beat the midday heat",
        "conector_tarde": "🚶 Tree-lined walk into sunset and evening attractions",
        "btn_ver_guia": "View Guide",
        "rota_titulo": "Route Map (Day 1)",
        "rota_subtitulo": "{n} connected stops in Belém",
        "btn_maps_rota": "Open Route in Google Maps ↗",
        "checklist_titulo": "What to bring",
        "checklist_sub": "Essentials for the equatorial climate",
        "check_1": "Compact umbrella or rain poncho",
        "check_2": "Cash (small bills for market vendors)",
        "check_3": "Light non-slip shoes (damp cobblestones)",
        "check_4": "Reusable water bottle (stay hydrated)",
        "sugestoes_titulo": "Add Suggested Stops",
        "roteiro_vazio_titulo": "Your itinerary is still empty",
        "roteiro_vazio_desc": "Explore Belém's attractions and click '+ Itinerary' to build your custom trip.",
        "roteiro_vazio_btn": "Explore Belém Places",
        "toast_add_roteiro": "✓ {nome} added to itinerary!",
        "toast_rem_roteiro": "{nome} removed from itinerary",
        "toast_rem_generico": "Place removed from itinerary",
        "toast_ia_otimizado": "✨ Optimal daytime & nighttime order recalculated!",
        "toast_roteiro_salvo": "💾 Itinerary with {n} places saved successfully!",
        "toast_roteiro_limpo": "Itinerary cleared",

        # Most Visited Screen (Ranking)
        "ranking_eyebrow": "TRENDING IN BELÉM",
        "ranking_titulo": "Most Visited",
        "ranking_subtitulo": "Explore Belém's most popular and top-rated destinations by week, month, or year.",
        "ranking_periodo_label": "Period:",
        "ranking_mes_label": "Month:",
        "ranking_ano_label": "Year:",
        "periodo_semana": "Week",
        "periodo_mes": "Month",
        "periodo_ano": "Year",
        "ranking_kpi_visitas": "Visits in Period",
        "ranking_kpi_lider": "Top Ranked Place",
        "ranking_kpi_media": "Weighted Average Rating",
        "ranking_visitas_qtd": "{n} visits",
        "ranking_avaliacoes_qtd": "{n} reviews",
        "ranking_fonte_mysql": "● Connected to MySQL",
        "ranking_fonte_local": "● Local Structured Data",
        "ranking_subtitulo_periodo_semana": "Weekly ranking for {mes} {ano}",
        "ranking_subtitulo_periodo_mes": "Monthly summary for {mes} {ano}",
        "ranking_subtitulo_periodo_ano": "Full annual ranking for {ano}",
        "ranking_vazio": "No visitation data found for the selected filter.",

        # Login & Sign-up
        "login_window_title": "BelémNaMão — Smart Guide",
        "login_selo": "● Pará, Amazonia",
        "login_boas_vindas": "Welcome to Belém",
        "login_subtitulo": "Sign in to build your personalized itinerary and explore the history, cuisine, and nightlife of the City of Mango Trees.",
        "login_demo_label": "💡 Demo:",
        "login_btn_preencher": "Autofill",
        "login_btn_pronto": "✓ Ready!",
        "login_demo_msg": "Demo credentials filled. Click 'Sign In'.",
        "login_user_label": "USERNAME OR EMAIL",
        "login_user_placeholder": "e.g. turista or name@example.com",
        "login_pass_label": "PASSWORD",
        "login_pass_placeholder": "Enter your password",
        "login_mostrar": "Show",
        "login_ocultar": "Hide",
        "login_lembrar": "Keep me signed in on this computer",
        "login_entrar": "Sign In  →",
        "login_convidado": "Continue without login (Guest)",
        "login_sem_conta": "Don't have an account yet?",
        "login_cadastre_se": "Sign up",
        "login_rodape": "© 2026 BelémNaMão Smart Guide • Made in Pará",
        "login_erro_vazio": "Please enter both username and password.",
        "login_erro_invalido": "Incorrect username or password. Tip: use 'Autofill' or password 'admin'.",
        "login_cadastro_ok": "Account '{user}' created! Enter your password to sign in.",
        "login_showcase_pill": "★ Sunset over Guajará Bay",
        "login_showcase_tag": "URBAN & CULTURAL AMAZONIA",
        "login_showcase_titulo": "Discover the colors, flavors, and living history of Belém do Pará.",
        "login_showcase_desc": "Curated landmarks, traditional open markets, vibrant waterfront dining nights, and riverboat routes at your fingertips.",
        "cad_window_title": "Create Account — BelémNaMão",
        "cad_titulo": "Create Your Account",
        "cad_subtitulo": "Sign up to customize itineraries, save favorite attractions, and explore the city.",
        "cad_nome": "Full name",
        "cad_nome_ph": "e.g. Maria Santos",
        "cad_usuario": "Username (login)",
        "cad_usuario_ph": "e.g. mariasantos",
        "cad_email": "Email",
        "cad_email_ph": "e.g. maria@example.com",
        "cad_senha": "Password (min. 4 characters)",
        "cad_senha_ph": "Enter your password",
        "cad_confirma": "Confirm password",
        "cad_confirma_ph": "Repeat your password",
        "cad_btn_criar": "Create my account",
        "cad_btn_voltar": "Back to login",
        "cad_erro_campos": "Please fill in name, username, and password.",
        "cad_erro_senha_curta": "Password must be at least 4 characters long.",
        "cad_erro_confirma": "The passwords do not match.",
    },
    "es": {
        # Ventana y Navegación
        "app_title": "BelémNaMão — Guía Inteligente de la Amazonía Atlántica",
        "clima_pill": "🕒 Lluvia 16h: Probable (82%)  •  🌊 Marea: Subiendo",
        "nav_inicio": "Inicio",
        "nav_explorar": "Explorar",
        "nav_roteiro": "Mi Itinerario",
        "nav_ranking": "Más Visitados",
        "btn_buscar_nav": "🔍 Buscar...",
        "btn_salvos_nav": "🔖 {n} guardados",
        "tema_claro": "☀️ Modo Claro",
        "tema_escuro": "🌙 Modo Oscuro",
        "toast_tema_claro": "Modo Claro activado",
        "toast_tema_escuro": "Modo Oscuro activado",
        "ola_usuario": "Hola, {nome}",
        "btn_sair": "🚪 Salir",
        "rodape_texto": "BelémNaMão • Guía Inteligente de la Amazonía Atlántica",
        "idioma_label": "Idioma:",
        "toast_idioma": "Idioma cambiado a Español",

        # Pantalla Inicio
        "hero_titulo": "Descubre Belém a tu manera",
        "hero_subtitulo": "Menos tiempo buscando. Más tiempo viviendo mercados, muelles, noches y sabores de la Amazonía Atlántica.",
        "hero_btn_explorar": "Explorar Catálogo  →",
        "hero_btn_roteiro": "Ver Mi Itinerario",
        "inicio_cats_titulo": "¿Qué te gustaría hacer?",
        "cat_experiencias": "{qtd} experiencias",
        "inicio_destaques_titulo": "Destacados de Belém",
        "inicio_destaques_ver_todas": "Ver todas las atracciones  →",
        "btn_add_roteiro": "+ Itinerario",
        "btn_no_roteiro": "✓ En Itinerario",
        "btn_detalhes": "Detalles",

        # Pantalla Explorar
        "explorar_eyebrow": "EXPLORAR PARÁ",
        "explorar_titulo": "Explorar Belém",
        "explorar_subtitulo": "Descubre puntos turísticos, mercados culturales, gastronomía ribereña y vida nocturna.",
        "explorar_busca_placeholder": "Buscar por nombre, barrio (ej: Cidade Velha, Campina, Umarizal) o palabra clave...",
        "explorar_preco_label": "Precio:",
        "explorar_contagem": "Mostrando {n} de {total} lugares",
        "filtro_todos_bairros": "Todos los Barrios",
        "vazio_titulo": "No se encontraron lugares",
        "vazio_subtitulo": "Prueba otro término de búsqueda o quita algún filtro de categoría/barrio.",
        "vazio_btn_limpar": "Limpiar Filtros",

        # Pantalla Detalles
        "btn_voltar": "‹ Volver",
        "breadcrumb_inicio": "Inicio",
        "breadcrumb_explorar": "Explorar",
        "btn_compartilhar": "Compartir",
        "toast_compartilhar": "¡Enlace copiado al portapapeles!",
        "btn_salvar_fav": "Guardar en Favoritos",
        "btn_salvo_roteiro": "✓ Guardado en Itinerario",
        "avaliacoes_suffix": "reseñas",
        "detalhes_sobre_titulo": "Sobre el Lugar",
        "detalhes_importancia": "Importancia y Memoria:",
        "detalhes_destaques_titulo": "Destacados & Por Qué Visitar",
        "detalhes_ingresso": "RANGO DE PRECIO Y ACCESO",
        "detalhes_aberto_agora": "● Horario",
        "detalhes_clima": "🌧️ Pronóstico: Lluvia breve a las 16h; noche fresca junto a la bahía (27°C)",
        "detalhes_add_roteiro": "+ Añadir a Mi Itinerario",
        "detalhes_salvo_roteiro": "✓ Guardado en Mi Itinerario",
        "detalhes_maps": "🗺️ Abrir Ruta en Google Maps",
        "detalhes_tempo_sugerido": "Tiempo sugerido: {duracao}",
        "detalhes_clima_ar": "Áreas climatizadas y al aire libre",
        "detalhes_fotos": "Fotos permitidas (consulta normas locales)",
        "detalhes_acessibilidade": "Acceso facilitado para visitantes",

        # Pantalla Mi Itinerario
        "roteiro_tag": "ITINERARIO INTELIGENTE • PARÁ",
        "roteiro_titulo": "Lo Mejor de Belém Histórica, Bahía y Noche",
        "roteiro_subtitulo": "Recorrido por los aromas del Ver-o-Peso, la historia de 1616 y la gastronomía nocturna.",
        "btn_otimizar_ia": "✨ Optimizar Orden (IA)",
        "btn_salvar": "💾 Guardar",
        "btn_limpar": "Limpiar",
        "kpi_duracao": "Duración Total",
        "kpi_paradas": "Paradas Guardadas",
        "kpi_gasto": "Gasto Estimado",
        "kpi_distancia": "Distancia a Pie",
        "kpi_duracao_val": "~{h}h con pausas",
        "kpi_paradas_val": "{n} lugares programados",
        "kpi_paradas_zero": "0 lugares",
        "kpi_gasto_val": "R$ {v} / persona",
        "kpi_distancia_val": "{km} km a pie",
        "turno_manha_titulo": "🌅 Turno de Mañana (08:00 a 12:30)",
        "turno_manha_sub": "Corazón Histórico y Gastronómico",
        "conector_manha": "🚶 Caminata ligera de 6 min (450m) por Boulevard Castilhos França",
        "almoco_tag": "PAUSA DE ALMUERZO SUGERIDA • 12:30 - 14:00",
        "almoco_titulo": "Casa das Onze Janelas o Puesto de Pescado Frito con Açaí",
        "almoco_desc": "Almuerza con vista a la bahía (filhote y tucupi) o en los auténticos puestos del mercado.",
        "turno_tarde_titulo": "🌙 Tarde y Noche (14:30 a 23:00)",
        "turno_tarde_sub": "Arquitectura, Atardecer y Gastronomía Nocturna",
        "conector_carro": "🚗 Traslado de 8 min (2.1 km) para evitar el calor del mediodía",
        "conector_tarde": "🚶 Paseo arbolado hasta el atardecer y agenda nocturna",
        "btn_ver_guia": "Ver Guía",
        "rota_titulo": "Trazado de la Ruta (Día 1)",
        "rota_subtitulo": "{n} paradas conectadas en Belém",
        "btn_maps_rota": "Abrir Trayecto en Google Maps ↗",
        "checklist_titulo": "Qué llevar en el día",
        "checklist_sub": "Esenciales para el clima ecuatorial",
        "check_1": "Paraguas compacto o impermeable",
        "check_2": "Efectivo (cambio para vendedores)",
        "check_3": "Calzado ligero antideslizante (adoquín húmedo)",
        "check_4": "Botella de agua reutilizable (hidratación)",
        "sugestoes_titulo": "Añadir Paradas Sugeridas",
        "roteiro_vazio_titulo": "Tu itinerario aún está vacío",
        "roteiro_vazio_desc": "Explora las atracciones de Belém y haz clic en '+ Itinerario' para armar tu ruta.",
        "roteiro_vazio_btn": "Explorar Lugares de Belém",
        "toast_add_roteiro": "✓ ¡{nome} añadido al itinerario!",
        "toast_rem_roteiro": "{nome} eliminado del itinerario",
        "toast_rem_generico": "Lugar eliminado del itinerario",
        "toast_ia_otimizado": "✨ ¡Orden óptimo diurno y nocturno recalculado!",
        "toast_roteiro_salvo": "💾 ¡Itinerario con {n} lugares guardado con éxito!",
        "toast_roteiro_limpo": "Itinerario limpiado",

        # Pantalla Más Visitados (Ranking)
        "ranking_eyebrow": "TENDENCIAS EN BELÉM",
        "ranking_titulo": "Más Visitados",
        "ranking_subtitulo": "Consulta los destinos más populares y mejor valorados de Belém por semana, mes o año.",
        "ranking_periodo_label": "Período:",
        "ranking_mes_label": "Mes:",
        "ranking_ano_label": "Año:",
        "periodo_semana": "Semana",
        "periodo_mes": "Mes",
        "periodo_ano": "Año",
        "ranking_kpi_visitas": "Visitas del Período",
        "ranking_kpi_lider": "Líder del Ranking",
        "ranking_kpi_media": "Media Ponderada General",
        "ranking_visitas_qtd": "{n} visitas",
        "ranking_avaliacoes_qtd": "{n} reseñas",
        "ranking_fonte_mysql": "● Conectado a MySQL",
        "ranking_fonte_local": "● Base Estructurada Local",
        "ranking_subtitulo_periodo_semana": "Ranking semanal de {mes} de {ano}",
        "ranking_subtitulo_periodo_mes": "Consolidado mensual de {mes} de {ano}",
        "ranking_subtitulo_periodo_ano": "Consolidado anual completo de {ano}",
        "ranking_vazio": "No se encontraron datos de visitas para el filtro seleccionado.",

        # Login y Registro
        "login_window_title": "BelémNaMão — Guía Inteligente",
        "login_selo": "● Pará, Amazonía",
        "login_boas_vindas": "Bienvenido a Belém",
        "login_subtitulo": "Inicia sesión para crear tu itinerario y explorar la historia, gastronomía y vida nocturna de la ciudad de los mangos.",
        "login_demo_label": "💡 Demo:",
        "login_btn_preencher": "Rellenar",
        "login_btn_pronto": "✓ ¡Listo!",
        "login_demo_msg": "Credenciales demo insertadas. Haz clic en 'Entrar'.",
        "login_user_label": "USUARIO O CORREO",
        "login_user_placeholder": "ej: turista o nombre@ejemplo.com",
        "login_pass_label": "CONTRASEÑA",
        "login_pass_placeholder": "Ingresa tu contraseña",
        "login_mostrar": "Mostrar",
        "login_ocultar": "Ocultar",
        "login_lembrar": "Mantener sesión iniciada en este equipo",
        "login_entrar": "Entrar  →",
        "login_convidado": "Continuar sin iniciar sesión (Invitado)",
        "login_sem_conta": "¿Aún no tienes cuenta?",
        "login_cadastre_se": "Regístrate",
        "login_rodape": "© 2026 BelémNaMão Guía Inteligente • Hecho en Pará",
        "login_erro_vazio": "Por favor, completa el usuario y la contraseña.",
        "login_erro_invalido": "Usuario o contraseña incorrectos. Consejo: usa 'Rellenar' o contraseña 'admin'.",
        "login_cadastro_ok": "¡Cuenta '{user}' registrada! Ingresa tu contraseña para entrar.",
        "login_showcase_pill": "★ Atardecer en la Bahía de Guajará",
        "login_showcase_tag": "AMAZONÍA URBANA Y CULTURAL",
        "login_showcase_titulo": "Descubre los colores, sabores y la historia viva de Belém do Pará.",
        "login_showcase_desc": "Lugares catalogados, mercados tradicionales, noches gastronómicas en los muelles y rutas fluviales en tus manos.",
        "cad_window_title": "Crear Cuenta — BelémNaMão",
        "cad_titulo": "Crea tu Cuenta",
        "cad_subtitulo": "Regístrate para personalizar itinerarios, guardar favoritos y explorar la ciudad.",
        "cad_nome": "Nombre completo",
        "cad_nome_ph": "ej: Maria Santos",
        "cad_usuario": "Nombre de usuario (login)",
        "cad_usuario_ph": "ej: mariasantos",
        "cad_email": "Correo electrónico",
        "cad_email_ph": "ej: maria@ejemplo.com",
        "cad_senha": "Contraseña (mínimo 4 caracteres)",
        "cad_senha_ph": "Ingresa tu contraseña",
        "cad_confirma": "Confirmar contraseña",
        "cad_confirma_ph": "Repite la contraseña",
        "cad_btn_criar": "Crear mi cuenta",
        "cad_btn_voltar": "Volver al inicio",
        "cad_erro_campos": "Completa nombre, usuario y contraseña.",
        "cad_erro_senha_curta": "La contraseña debe tener al menos 4 caracteres.",
        "cad_erro_confirma": "Las contraseñas no coinciden.",
    },
}

CATEGORIAS_TRADUCAO: Dict[str, Dict[str, Tuple[str, str]]] = {
    "pt-br": {
        "Todas": ("Todas", "Todas as categorias"),
        "Gastronomia": ("Gastronomia", "Sabores paraenses, açaí e tucupi"),
        "Cultura": ("Cultura", "Arte, museus e arquitetura nobre"),
        "História": ("História", "Marco zero 1616 e ciclo da borracha"),
        "Natureza": ("Natureza", "Parques, mangueiras e fauna fluvial"),
        "Passeio": ("Passeio", "Orla, docas, noites e ilhas"),
    },
    "en": {
        "Todas": ("All", "All categories"),
        "Gastronomia": ("Gastronomy", "Amazonian cuisine, açaí & tucupi"),
        "Cultura": ("Culture", "Art, museums & historic architecture"),
        "História": ("History", "1616 founding & Rubber Boom heritage"),
        "Natureza": ("Nature", "Parks, mango trees & river wildlife"),
        "Passeio": ("Sightseeing", "Waterfront, nightlife & island tours"),
    },
    "es": {
        "Todas": ("Todas", "Todas las categorías"),
        "Gastronomia": ("Gastronomía", "Sabores amazónicos, açaí y tucupi"),
        "Cultura": ("Cultura", "Arte, museos y arquitectura noble"),
        "História": ("Historia", "Hito 1616 y ciclo del caucho"),
        "Natureza": ("Naturaleza", "Parques, mangos y fauna fluvial"),
        "Passeio": ("Paseo", "Orla, muelles, noches e islas"),
    },
}

MESES_TRADUCAO: Dict[str, List[str]] = {
    "pt-br": [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
    ],
    "en": [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ],
    "es": [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
    ],
}

PRECO_FILTRO_TRADUCAO: Dict[str, Dict[str, str]] = {
    "pt-br": {
        "Qualquer": "Qualquer",
        "Baixo": "$ Econômico",
        "Médio": "$$ Médio",
        "Alto": "$$$ Alto",
    },
    "en": {
        "Qualquer": "Any",
        "Baixo": "$ Budget",
        "Médio": "$$ Moderate",
        "Alto": "$$$ Upscale",
    },
    "es": {
        "Qualquer": "Cualquiera",
        "Baixo": "$ Económico",
        "Médio": "$$ Medio",
        "Alto": "$$$ Alto",
    },
}

PRECO_ROTULO_TRADUCAO: Dict[str, Dict[int, str]] = {
    "pt-br": {1: "$ • Acessível", 2: "$$ • Médio", 3: "$$$ • Alto"},
    "en": {1: "$ • Budget", 2: "$$ • Moderate", 3: "$$$ • Upscale"},
    "es": {1: "$ • Accesible", 2: "$$ • Medio", 3: "$$$ • Alto"},
}

LOCAIS_TRADUCOES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "ver-o-peso": {
        "en": {
            "descricao": "Belém's iconic open-air waterfront market featuring regional Amazonian ingredients, herbs, crafts, and riverside street food.",
            "por_que_visitar": "To experience authentic Pará flavors, aromas, and vibrant daily culture along Guajará Bay.",
            "duracao": "1–2 hours",
            "endereco": "Av. Boulevard Castilhos França — Cidade Velha, Belém, PA.",
            "subtitulo": "Latin America's largest open-air market • Guamá Estuary",
            "horario": "05:00 AM – 06:00 PM (Fish hall from 03:00 AM)",
            "melhor_horario": "Early morning (07:00 – 09:30 AM)",
            "preco_tag": "$ • Budget / Free Entry",
            "destaque_tag": "Culture & Gastronomy",
            "destaques_cards": [
                ("🥭", "Amazonian Flavors", "Taste fresh açaí with fried fish, tacacá, cupuaçu, and artisanal cheeses."),
                ("🌿", "Herb & Potion Stalls", "Traditional medicinal herbs, aromatic baths, and regional spices."),
                ("⚓", "Fisherman's Wharf", "Historic iron market hall built in 1901 beside colorful riverboats."),
                ("📸", "Living Heritage", "Vibrant stalls and iconic blue towers overlooking Guajará Bay."),
            ],
        },
        "es": {
            "descricao": "El mercado al aire libre más emblemático de Belém, con ingredientes amazónicos, hierbas tradicionales y comida regional frente a la bahía.",
            "por_que_visitar": "Para conocer sabores, aromas y la cultura cotidiana del pueblo paraense.",
            "duracao": "1–2 horas",
            "endereco": "Av. Boulevard Castilhos França — Cidade Velha, Belém, PA.",
            "subtitulo": "La feria al aire libre más grande de América Latina • Bahía de Guajará",
            "horario": "05:00 a 18:00 (Sector de pescados desde las 03:00)",
            "melhor_horario": "Temprano por la mañana (07:00 a 09:30)",
            "preco_tag": "$ • Accesible / Entrada Libre",
            "destaque_tag": "Cultura y Gastronomía",
            "destaques_cards": [
                ("🥭", "Sabores Amazónicos", "Prueba açaí fresco con pescado frito, tacacá, cupuaçu y quesos regionales."),
                ("🌿", "Hierbas Tradicionales", "Puestos históricos de hierbas medicinales y aromas de la selva."),
                ("⚓", "Mercado de Hierro", "Pabellón histórico de 1901 junto a los barcos ribereños."),
                ("📸", "Patrimonio Vivo", "Colores y torres emblemáticas frente a la Bahía de Guajará."),
            ],
        },
    },
    "estacao-das-docas": {
        "en": {
            "descricao": "Waterfront cultural & dining complex that comes alive at night with illuminated historic cranes, craft brewery, Amazonian restaurants, and live music.",
            "por_que_visitar": "A must-visit sunset and nighttime hotspot in Belém: pair bay breezes with regional fine dining, craft beers, and live evening shows.",
            "duracao": "2–4 hours (Night)",
            "endereco": "Av. Boulevard Castilhos França, s/n — Campina, Belém, PA. Open until 12 AM (Fri/Sat until 1 AM).",
            "subtitulo": "Illuminated historic iron warehouses • Sunset & Nightlife on Guajará Bay",
            "horario": "10:00 AM – 12:00 AM • Nightlife Peak from 6:00 PM (Fri/Sat until 01:00 AM)",
            "melhor_horario": "Sunset & Night (05:30 PM – 11:30 PM)",
            "preco_tag": "$$$ • Upscale",
            "destaque_tag": "Nightlife & Gastronomy",
            "destaques_cards": [
                ("🌙", "Bayfront Nightlife", "Scenic illumination across the historic docks, live music, and lively bars."),
                ("🍺", "Amazonian Craft Brewery", "Amazon Beer taproom with exotic fruit brews like priprioca and bacuri."),
                ("🍽️", "Evening Waterfront Dining", "Renowned restaurants serving pato no tucupi, filhote, and riverside seafood."),
                ("🎶", "Sunset & Amphitheater", "Daily bay views followed by cultural performances at the São Pedro Nolasco amphitheater."),
            ],
        },
        "es": {
            "descricao": "Complejo turístico y gastronómico junto a la bahía que cobra vida por la noche con grúas iluminadas, cervecería artesanal, restaurantes regionales y música en vivo.",
            "por_que_visitar": "Imperdible al atardecer y de noche en Belém: combina brisa de la bahía con cenas amazónicas, cervezas artesanales y espectáculos nocturnos.",
            "duracao": "2–4 horas (Noche)",
            "endereco": "Av. Boulevard Castilhos França, s/n — Campina, Belém, PA. Abierto hasta las 00h (Vie/Sáb hasta 01h).",
            "subtitulo": "Almacenes portuarios iluminados • Atardecer y Vida Nocturna en el Guajará",
            "horario": "10:00 a 00:00 • Destacado Nocturno desde las 18:00 (Vie/Sáb hasta 01:00)",
            "melhor_horario": "Atardecer y Noche (17:30 a 23:30)",
            "preco_tag": "$$$ • Alto",
            "destaque_tag": "Vida Nocturna y Gastronomía",
            "destaques_cards": [
                ("🌙", "Noches frente a la Bahía", "Iluminación escénica en los muelles históricos, bares y música en vivo."),
                ("🍺", "Cervecería Amazónica", "Cervezas artesanales con ingredientes locales como bacuri y priprioca."),
                ("🍽️", "Cenas Regionales", "Restaurantes con vista al río especializados en pato no tucupi y filhote."),
                ("🎶", "Anfiteatro y Brisa", "Atardecer inolvidable seguido de presentaciones culturales nocturnas."),
            ],
        },
    },
    "bistro-guajara-noturno": {
        "en": {
            "descricao": "Contemporary regional restaurant in Umarizal specializing in nighttime Amazonian dining with grilled filhote fish, pato no tucupi, jambu cocktails, and live Pará music.",
            "por_que_visitar": "Ideal for enjoying Belém's nighttime culinary scene with modern Amazonian gastronomy, cozy evening ambiance, and signature local cocktails.",
            "duracao": "2–3 hours (Nighttime)",
            "endereco": "Av. Visconde de Souza Franco (Doca), Umarizal — Belém, PA. Night service: 06:30 PM – 12:30 AM.",
            "subtitulo": "Contemporary Amazonian evening dining & signature cocktails • Umarizal",
            "horario": "06:30 PM – 12:30 AM (Tue–Sun • Nighttime Exclusive)",
            "melhor_horario": "Dinner & Live Music (08:00 PM – 11:00 PM)",
            "preco_tag": "$$$ • Upscale",
            "destaque_tag": "Nighttime Gastronomy",
            "destaques_cards": [
                ("🍷", "Amazonian Chef's Menu", "Charcoal-grilled filhote, maniçoba croquettes, and tucupi reductions."),
                ("🍸", "Jambu & Taperebá Bar", "Signature evening cocktails crafted with Amazonian cachaça and botanicals."),
                ("🎸", "Live Acoustic Carimbó & MPB", "Intimate nighttime performances celebrating Pará musical traditions."),
                ("✨", "Umarizal Night District", "Located on Doca avenue in Belém's liveliest evening dining corridor."),
            ],
        },
        "es": {
            "descricao": "Restaurante regional contemporáneo en Umarizal especializado en cenas amazónicas nocturnas con filhote a la brasa, pato no tucupi, cócteles de jambu y música en vivo.",
            "por_que_visitar": "Ideal para disfrutar de la gastronomía nocturna de Belém con alta cocina paraense, ambiente climatizado y coctelería de autor.",
            "duracao": "2–3 horas (Nocturno)",
            "endereco": "Av. Visconde de Souza Franco (Doca), Umarizal — Belém, PA. Horario nocturno: 18:30 a 00:30.",
            "subtitulo": "Alta gastronomía amazónica nocturna y coctelería de autor • Umarizal",
            "horario": "18:30 a 00:30 (Martes a Domingo • Exclusivo Nocturno)",
            "melhor_horario": "Cena y Música en Vivo (20:00 a 23:00)",
            "preco_tag": "$$$ • Alto",
            "destaque_tag": "Gastronomía Nocturna",
            "destaques_cards": [
                ("🍷", "Cocina Amazónica Nocturna", "Filhote a la brasa, croquetas de maniçoba y reducciones de tucupi."),
                ("🍸", "Barra de Jambu y Frutas", "Cócteles nocturnos exclusivos con cachaça de jambu y frutas regionales."),
                ("🎸", "Música Paraense en Vivo", "Veladas acústicas con ritmos amazónicos y MPB en un ambiente acogedor."),
                ("✨", "Corredor Gastronómico Doca", "Ubicado en Umarizal, el polo nocturno más vibrante de Belém."),
            ],
        },
    },
    "feliz-lusitania": {
        "en": {
            "descricao": "Belém's 1616 founding historic complex featuring Forte do Presépio, Casa das Onze Janelas, and colonial churches.",
            "por_que_visitar": "To explore the city's founding fortress, Marajoara archaeological artifacts, and panoramic bay views.",
            "duracao": "1–2 hours",
            "endereco": "Praça Dom Frei Caetano Brandão — Cidade Velha, Belém, PA.",
            "subtitulo": "Founding site of Belém (1616) • Fortress & Museums",
            "horario": "09:00 AM – 06:00 PM (Closed Mondays)",
            "melhor_horario": "Late afternoon (04:30 PM for sunset)",
            "preco_tag": "$ (R$ 6 / Free Tue)",
            "destaque_tag": "IPHAN Heritage",
            "destaques_cards": [
                ("🌅", "360° Bay Overlook", "Sweeping views of riverboats and the Amazonian sunset."),
                ("🏺", "Marajoara Collection", "Over 2,000 years of preserved indigenous ceramics and history."),
                ("🛡️", "Fortress & Cannons", "17th-century ramparts guarding the Guamá estuary."),
                ("🍲", "Historic Dining", "Adjacent gardens and contemporary Amazonian restaurant."),
            ],
        },
        "es": {
            "descricao": "Conjunto histórico fundacional de Belém (1616) que reúne el Fuerte del Pesebre, Casa das Onze Janelas e iglesias coloniales.",
            "por_que_visitar": "Para explorar la historia fundacional, cerámica marajoara y vistas panorámicas de la bahía.",
            "duracao": "1–2 horas",
            "endereco": "Praça Dom Frei Caetano Brandão — Cidade Velha, Belém, PA.",
            "subtitulo": "Hito fundacional de Belém en 1616 • Fortaleza y Museos",
            "horario": "09:00 a 18:00 (Cierra los lunes)",
            "melhor_horario": "Tarde (16:30 para ver el atardecer)",
            "preco_tag": "$ (R$ 6 / Martes Gratis)",
            "destaque_tag": "Patrimonio Histórico",
            "destaques_cards": [
                ("🌅", "Mirador 360° de la Bahía", "Panorámica de las embarcaciones ribereñas y el atardecer."),
                ("🏺", "Acervo Marajoara", "Cerámicas indígenas y vestigios históricos preservados."),
                ("🛡️", "Murallas y Cañones", "Fortificación histórica frente a la desembocadura del río."),
                ("🍲", "Cultura y Sabores", "Jardines y restaurante regional con vista al agua."),
            ],
        },
    },
    "mangal": {
        "en": {
            "descricao": "Ecological riverfront park featuring a giant butterfly house, observation tower, lakes, and scarlet ibises.",
            "por_que_visitar": "An open-air sanctuary of Amazonian flora, fauna, and peaceful trails overlooking the Guamá River.",
            "duracao": "1–2 hours",
            "endereco": "R. Carneiro da Rocha, s/n — Cidade Velha, Belém, PA.",
            "subtitulo": "Ecological park with butterfly sanctuary, lighthouse & scarlet ibises",
            "horario": "08:00 AM – 06:00 PM (Closed Mondays)",
            "melhor_horario": "Ibis feeding at 11:15 AM & 03:00 PM",
            "preco_tag": "Free Park (Exhibits R$ 5)",
            "destaque_tag": "Nature & Wildlife",
            "destaques_cards": [
                ("🦩", "Scarlet Ibises", "Vibrant red guarás roaming freely around wetlands and boardwalks."),
                ("🦋", "Butterfly Sanctuary", "Largest butterfly house in Northern Brazil surrounded by orchids."),
                ("🗼", "47m Observation Tower", "Elevated 360° vista of the Guamá River and Belém skyline."),
                ("🌿", "Amazonian Flora", "Shaded trails, water lilies, and peaceful lakeside decks."),
            ],
        },
        "es": {
            "descricao": "Parque ecológico frente al río con mariposario gigante, mirador panorámico, lagos y guarás escarlata.",
            "por_que_visitar": "Una pausa al aire libre para admirar paisajes y biodiversidad amazónica.",
            "duracao": "1–2 horas",
            "endereco": "R. Carneiro da Rocha, s/n — Cidade Velha, Belém, PA.",
            "subtitulo": "Parque ecológico con mariposario, faro mirador y guarás",
            "horario": "08:00 a 18:00 (Cierra los lunes)",
            "melhor_horario": "Alimentación de guarás a las 11:15 y 15:00",
            "preco_tag": "Parque Gratis (Espacios R$ 5)",
            "destaque_tag": "Naturaleza y Fauna",
            "destaques_cards": [
                ("🦩", "Guarás Escarlata", "Aves rojas amazónicas caminando libres junto a las pasarelas."),
                ("🦋", "Mariposario y Orquideario", "Especies amazónicas en un entorno botánico exuberante."),
                ("🗼", "Faro Mirador de 47m", "Vista panorámica del río Guamá y la ciudad."),
                ("🌿", "Senderos Verdes", "Pasarelas sobre lagos con victorias regias y tortugas."),
            ],
        },
    },
    "teatro-da-paz": {
        "en": {
            "descricao": "Neoclassical opera house built in 1878 during the Amazon Rubber Boom, famed for Carrara marble and gold leaf.",
            "por_que_visitar": "To step inside one of Brazil's most magnificent historic theaters and admire imperial acoustics.",
            "duracao": "1 hour",
            "endereco": "Av. da Paz — Praça da República, Campina, Belém, PA.",
            "subtitulo": "Neoclassical jewel of the Rubber Boom on Praça da República",
            "horario": "Guided tours: Tue–Sun every hour",
            "melhor_horario": "Afternoon (03:00 PM — air-conditioned during rain)",
            "preco_tag": "$ (R$ 10 full / R$ 5 half)",
            "destaque_tag": "Imperial Architecture",
            "destaques_cards": [
                ("🎭", "Neoclassical Grandeur", "Italian marble staircases, French chandeliers, and bronze details."),
                ("🎶", "World-Class Acoustics", "Historic horseshoe auditorium hosting opera and symphonic concerts."),
                ("🎨", "Amazonian Ceiling Fresco", "Artistic tributes to regional mythology and classical muses."),
                ("🏛️", "Guided Heritage Tours", "Rich storytelling of Belém's Belle Époque golden age."),
            ],
        },
        "es": {
            "descricao": "Joya neoclásica de 1878 construida durante el Ciclo del Caucho, famosa por su mármol de Carrara y acústica.",
            "por_que_visitar": "Para conocer uno de los teatros históricos más emblemáticos de Brasil.",
            "duracao": "1 hora",
            "endereco": "Av. da Paz — Praça da República, Campina, Belém, PA.",
            "subtitulo": "Joya neoclásica del Ciclo del Caucho en la Praça da República",
            "horario": "Visitas guiadas: Martes a Domingo cada hora",
            "melhor_horario": "Tarde (15:00 — climatizado durante la lluvia)",
            "preco_tag": "$ (R$ 10 general / R$ 5 reducida)",
            "destaque_tag": "Arquitectura Imperial",
            "destaques_cards": [
                ("🎭", "Salón Neoclásico", "Escaleras de mármol italiano, candelabros franceses y pan de oro."),
                ("🎶", "Acústica Histórica", "Escenario de óperas y orquestas desde el siglo XIX."),
                ("🎨", "Fresco Amazónico", "Pinturas en el techo inspiradas en la mitología regional."),
                ("🏛️", "Visitas Guiadas", "Recorrido cultural por la Belle Époque amazónica."),
            ],
        },
    },
    "praca-republica": {
        "en": {
            "descricao": "Leafy central square framed by century-old mango trees, monuments, cafés, and Sunday craft fairs.",
            "por_que_visitar": "For a relaxing stroll beneath the mango canopy and observing everyday urban life in Belém.",
            "duracao": "30–60 min",
            "endereco": "Av. Presidente Vargas — Campina, Belém, PA.",
            "subtitulo": "Shaded green heart with century-old mango trees & Sunday craft market",
            "horario": "Open 24 hours",
            "melhor_horario": "Sunday morning (Artisan fair)",
            "preco_tag": "Free",
            "destaque_tag": "Walk & Leisure",
            "destaques_cards": [
                ("🌳", "Mango Tree Canopy", "Cool natural shade under historic centennial mango trees."),
                ("🛍️", "Sunday Artisan Fair", "Local crafts, ceramics, street snacks, and regional souvenirs."),
                ("🗿", "Republic Monument", "19th-century marble sculptures and Belle Époque surroundings."),
                ("☕", "Historic Center Access", "Steps away from Theatro da Paz and local cafés."),
            ],
        },
        "es": {
            "descricao": "Plaza central arbolada con mangos centenarios, monumentos históricos y feria dominical de artesanías.",
            "por_que_visitar": "Para caminar bajo la sombra de los mangos y disfrutar la vida urbana de Belém.",
            "duracao": "30–60 minutos",
            "endereco": "Av. Presidente Vargas — Campina, Belém, PA.",
            "subtitulo": "Corazón verde con mangos centenarios y feria los domingos",
            "horario": "Acceso libre 24 horas",
            "melhor_horario": "Domingo por la mañana (Feria artesanal)",
            "preco_tag": "Gratuito",
            "destaque_tag": "Paseo y Ocio",
            "destaques_cards": [
                ("🌳", "Túnel de Mangos", "Sombra fresca bajo árboles históricos en pleno centro."),
                ("🛍️", "Feria Dominical", "Artesanías paraenses, cerámica marajoara y comidas típicas."),
                ("🗿", "Monumento Histórico", "Esculturas del siglo XIX frente al Theatro da Paz."),
                ("☕", "Vida Urbana", "Ideal para descansar y tomar un café o agua de coco."),
            ],
        },
    },
    "ilha-combu": {
        "en": {
            "descricao": "Lush riverside island across the Guamá River, famous for artisanal native cocoa and riverside restaurants.",
            "por_que_visitar": "To escape the city pace with boat rides, forest trails, chocolate workshops, and riverfront dining.",
            "duracao": "Half day",
            "endereco": "Boat departure from Praça Princesa Isabel — Belém, PA.",
            "subtitulo": "Riverside gastronomic island & artisanal native Amazonian cocoa",
            "horario": "Boats 09:00 AM – 06:00 PM (Praça Princesa Isabel)",
            "melhor_horario": "Weekend lunch (11:00 AM – 04:00 PM)",
            "preco_tag": "$$ • Moderate",
            "destaque_tag": "Riverside & Cocoa",
            "destaques_cards": [
                ("🍫", "Artisanal Jungle Cocoa", "Visit family-run workshops producing organic Combu chocolate."),
                ("🚤", "15-Minute River Crossing", "Scenic boat trip across the Guamá River past stilt houses."),
                ("🐟", "Decks Over the River", "Riverside restaurants serving fresh fish, crab, and fresh açaí."),
                ("🌴", "Flooded Forest Trails", "Walkways surrounded by towering samaúma trees and igarapés."),
            ],
        },
        "es": {
            "descricao": "Isla fluvial frente a Belém famosa por sus restaurantes sobre el río, selva amazónica y cacao artesanal.",
            "por_que_visitar": "Para desconectar de la ciudad con paseos en lancha, chocolate nativo y cocina ribereña.",
            "duracao": "Medio día",
            "endereco": "Embarque fluvial desde Praça Princesa Isabel — Belém, PA.",
            "subtitulo": "Polo gastronómico ribereño y cultivo artesanal de cacao nativo",
            "horario": "Lanchas de 09:00 a 18:00 (Praça Princesa Isabel)",
            "melhor_horario": "Almuerzo de fin de semana (11:00 a 16:00)",
            "preco_tag": "$$ • Medio",
            "destaque_tag": "Ribereño y Cacao",
            "destaques_cards": [
                ("🍫", "Cacao Artesanal", "Conoce fábricas familiares de chocolate orgánico de la selva."),
                ("🚤", "Travesía Fluvial", "Navegación de 15 minutos por el río Guamá entre igarapés."),
                ("🐟", "Restaurantes sobre el Agua", "Muelles gastronómicos con pescado fresco y açaí puro."),
                ("🌴", "Senderos Amazónicos", "Árboles gigantes de samaúma y contacto directo con la naturaleza."),
            ],
        },
    },
    "basilica-nazare": {
        "en": {
            "descricao": "Grand neoclassical basilica inspired by Rome's St. Paul Outside the Walls and heart of the Círio de Nazaré.",
            "por_que_visitar": "To admire its stained glass, marble mosaics, and deep spiritual significance in Amazonian culture.",
            "duracao": "30–60 min",
            "endereco": "Praça Santuário — Nazaré, Belém, PA.",
            "subtitulo": "Sanctuary of Our Lady of Nazaré & heart of the Círio pilgrimage",
            "horario": "06:00 AM – 08:00 PM daily",
            "melhor_horario": "Early morning or late afternoon",
            "preco_tag": "Free",
            "destaque_tag": "Faith & Tradition",
            "destaques_cards": [
                ("⛪", "Roman-Inspired Basilica", "Ornate polychrome marble, mosaics, and European stained glass."),
                ("🕯️", "Círio de Nazaré Heritage", "UNESCO-recognized center of Brazil's largest Marian pilgrimage."),
                ("🏛️", "Santuário Square", "Peaceful plaza with cultural spaces and museum exhibitions."),
                ("🎵", "Sacred Acoustics", "Pipe organ and serene atmosphere throughout the day."),
            ],
        },
        "es": {
            "descricao": "Majestuosa basílica santuario inspirada en San Pablo Extramuros y corazón del Círio de Nazaré.",
            "por_que_visitar": "Para admirar sus vitrales, mármoles y profunda relevancia espiritual y cultural.",
            "duracao": "30–60 minutos",
            "endereco": "Praça Santuário — Nazaré, Belém, PA.",
            "subtitulo": "Santuario de Nuestra Señora de Nazaré y epicentro del Círio",
            "horario": "06:00 a 20:00 todos los días",
            "melhor_horario": "Mañana temprano o final de la tarde",
            "preco_tag": "Gratuito",
            "destaque_tag": "Fe y Tradición",
            "destaques_cards": [
                ("⛪", "Arquitectura Monumental", "Mármoles polícromos, mosaicos venecianos y vitrales históricos."),
                ("🕯️", "Tradición del Círio", "Centro de la mayor peregrinación mariana de Brasil."),
                ("🏛️", "Plaza Santuario", "Entorno arbolado ideal para visitar con tranquilidad."),
                ("🎵", "Atmósfera Serena", "Órgano monumental y espacio de recogimiento."),
            ],
        },
    },
}


def t(chave: str, **kwargs) -> str:
    """Retorna a string traduzida no idioma atual com fallback seguro."""
    lang = get_idioma()
    texto = TRADUCOES.get(lang, {}).get(chave)
    if texto is None:
        texto = TRADUCOES["pt-br"].get(chave, chave)
    if kwargs:
        try:
            return texto.format(**kwargs)
        except Exception:
            return texto
    return texto


def traduzir_categoria(categoria: str) -> str:
    """Traduz o nome de uma categoria canônica mantendo compatibilidade interna."""
    lang = get_idioma()
    par = CATEGORIAS_TRADUCAO.get(lang, {}).get(categoria)
    if par:
        return par[0]
    return categoria


def traduzir_categoria_desc(categoria: str) -> str:
    """Traduz a descrição curta de uma categoria na tela inicial."""
    lang = get_idioma()
    par = CATEGORIAS_TRADUCAO.get(lang, {}).get(categoria)
    if par:
        return par[1]
    return ""


def traduzir_mes(mes: int) -> str:
    """Retorna o nome do mês (1..12) no idioma atual."""
    lang = get_idioma()
    nomes = MESES_TRADUCAO.get(lang, MESES_TRADUCAO["pt-br"])
    idx = max(1, min(12, int(mes))) - 1
    return nomes[idx]


def lista_meses() -> List[str]:
    """Retorna a lista de 12 meses no idioma atual."""
    return list(MESES_TRADUCAO.get(get_idioma(), MESES_TRADUCAO["pt-br"]))


def traduzir_preco_filtro(chave_canonica: str) -> str:
    """Traduz uma opção do filtro de preço ('Qualquer', 'Baixo', 'Médio', 'Alto')."""
    lang = get_idioma()
    return PRECO_FILTRO_TRADUCAO.get(lang, PRECO_FILTRO_TRADUCAO["pt-br"]).get(chave_canonica, chave_canonica)


def chave_preco_por_rotulo(rotulo: str) -> str:
    """Converte o rótulo exibido noSegmentedButton para a chave canônica."""
    for mapa in PRECO_FILTRO_TRADUCAO.values():
        for chave, texto in mapa.items():
            if texto == rotulo:
                return chave
    return "Qualquer"


def traduzir_rotulo_preco(valor: Any) -> str:
    """Retorna o rótulo de preço legível (1, 2 ou 3) no idioma atual."""
    lang = get_idioma()
    mapa = PRECO_ROTULO_TRADUCAO.get(lang, PRECO_ROTULO_TRADUCAO["pt-br"])
    try:
        v = int(valor)
    except (TypeError, ValueError):
        return str(valor or "")
    return mapa.get(v, str(valor))


def traduzir_local(local: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    """Retorna os campos de exibição de um local traduzidos para o idioma ativo."""
    lang = get_idioma()
    loc_id = local.get("id", "")
    trad = LOCAIS_TRADUCOES.get(loc_id, {}).get(lang, {})

    padrao_cards_pt = meta.get("destaques_cards") or [
        ("🌅", "Mirante 360° da Baía", "Panorama deslumbrante das embarcações ribeirinhas e o pôr do sol amazônico."),
        ("🏺", "Acervo e Memória Viva", "Cultura paraense preservada em arquitetura e experiências autênticas."),
        ("✨", "Experiência Regional", "Programação diurna e noturna conectada ao melhor de Belém do Pará."),
        ("🍲", "Cultura & Sabores", "Gastronomia típica e ambiente acolhedor no coração da Amazônia."),
    ]

    return {
        "nome": local.get("nome", ""),
        "descricao": trad.get("descricao", local.get("descricao", "")),
        "por_que_visitar": trad.get("por_que_visitar", local.get("por_que_visitar", "")),
        "duracao": trad.get("duracao", local.get("duracao", "")),
        "endereco": trad.get("endereco", local.get("endereco", "")),
        "subtitulo": trad.get("subtitulo", meta.get("subtitulo", "")),
        "horario": trad.get("horario", meta.get("horario", "09h às 18h")),
        "melhor_horario": trad.get("melhor_horario", meta.get("melhor_horario", "")),
        "preco_tag": trad.get("preco_tag", meta.get("preco_tag", traduzir_rotulo_preco(local.get("preco")))),
        "destaque_tag": trad.get("destaque_tag", meta.get("destaque_tag", "")),
        "destaques_cards": trad.get("destaques_cards", padrao_cards_pt),
    }
