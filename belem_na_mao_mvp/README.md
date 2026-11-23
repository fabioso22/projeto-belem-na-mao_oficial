# BelémNaMão — Guia Inteligente da Amazônia Atlântica

Aplicativo desktop moderno, limpo e profissional em Python + CustomTkinter + Pillow com persistência em banco de dados relacional SQLite, suporte a áudio-guia interativo, inteligência climática e otimização de roteiros com IA.

---

## 🎨 Design System e Identidade Visual

O visual da aplicação foi completamente redesenhado para refletir a estética contemporânea das metrópoles da Amazônia Atlântica:

- **Paleta de Cores Inspirada em Belém**:
  - `Midnight Guajará (#00132C & #0F2847)`: Tons nobres de azul escuro para containers, cabeçalho e tipografia de alto contraste.
  - `Rubi Açaí (#A13A53 & #FFD9DE)`: Acento regional quente para badges, botões de ação e tags históricas.
  - `Verde Floresta (#012E21 & #C0ECD7)`: Indicadores de patrimônio ambiental, turismo sustentável e status positivo.
  - `Clean Canvas (#F8F9FF & #FFFFFF)`: Fundos limpos, cartões puros e divisores sutis com sombras suaves.
- **Tipografia Moderna**:
  - Hierarquia visual limpa e refinada com `Segoe UI`, com títulos marcantes, labels em caixa alta com espaçamento e corpo de texto legível.
- **Galeria Visual Bento Showcase**:
  - Imagens de alta resolução com cantos arredondados (`LANCZOS` + máscara alpha) e carregamento otimizado com cache em memória.

---

## 🚀 Principais Telas e Funcionalidades

### 1. Tela de Login e Cadastro (Split-Screen)
- **Painel Esquerdo (Autenticação)**:
  - Logotipo oficial com emblema náutico e selo *Pará, Amazônia*.
  - Banner interativo com credenciais de teste (`turista` / `123456`) e botão **Preencher** automático.
  - Campos com bordas de foco reativas e botão **Mostrar/Ocultar** senha.
  - Opções para lembrar login, entrar como convidado e cadastrar nova conta (com hashing `PBKDF2-SHA256`).
- **Painel Direito (Hero Showcase)**:
  - Fotografia panorâmica do pôr do sol na Baía do Guajará.
  - Cartão *Glassmorphism* flutuante com selo *Amazônia Urbana & Cultural* e destaques das principais atrações.

### 2. Barra Superior Fixo (Header & Micro-Intel)
- Logotipo oficial com tipografia integrada (`Belém` + `NaMão`).
- **Widget de Clima e Marés em Tempo Real**: `🕒 Chuva das 16h: Provável (82%) • 🌊 Maré: Enchendo`.
- Navegação em pílulas: `Início`, `Explorar`, `Meu Roteiro` e `Sobre Belém`.
- Contador dinâmico de favoritos salvos (`🔖 X salvos`) com atalho direto para o roteiro.
- Identificação do usuário logado e botão de saída.

### 3. Início (Dashboard de Boas-Vindas)
- **Hero Banner Imersivo**: Fotografia da orla e chamada para ação.
- **Strip de Inteligência Climática**: 4 cartões com temperatura (29°C), chuva típica da tarde, tábua de marés da baía e policiamento DPTUR.
- **Categorias Bento**: Gastronomia, Cultura, História, Natureza e Passeio com atalhos de clique direto.
- **Destaques de Belém**: Cartões com fotos reais, avaliação (★ 4.9), bairro e botão de salvar.
- **Banner Sonoro**: Divulgação do Áudio-Tour narrado por historiadores locais.

### 4. Explorar (Catálogo Completo & Filtros)
- Busca instantânea por nome, bairro ou palavra-chave com botão de limpar (✕).
- Pílulas horizontais de categorias (`Todas`, `Gastronomia`, `Cultura`, `História`, `Natureza`, `Passeio`).
- Filtros segmentados por faixa de preço (`Qualquer`, `$ Econômico`, `$$ Médio`, `$$$ Alto`) e seleção de bairro.
- Alternância instantânea entre modo **Grade** (Bento Cards) e **Mapa Interativo**.

### 5. Detalhes da Atração (Showcase Completo)
- Navegação contextual com *breadcrumbs* (`Início / Explorar / Bairro / Local`) e botão de retorno.
- Galeria Bento com foto principal e miniaturas secundárias.
- **Mini-Player de Áudio-Guia Integrado**: Simulação de áudio com botão de Play/Pause, barra de progresso e contador de tempo.
- Sessão *Sobre o Marco Histórico* e 4 cartões de destaques (*Mirante 360°*, *Museu do Encontro*, etc.).
- Cartão lateral fixo com preço, horário (*Aberto Agora*), previsão de chuva, botão de adicionar ao roteiro e atalho para o Google Maps.

### 6. Meu Roteiro (Timeline Inteligente)
- Métricas consolidadas: Duração total (~8h30), Paradas programadas, Estimativa de gasto e Distância a pé.
- Botão **✨ Otimizar Ordem (IA)**: Reorganiza os pontos na ordem geográfica e cronológica ideal para evitar a chuva do meio da tarde.
- Linha do tempo dividida em períodos:
  - *Turno da Manhã (08h00 às 12h30)* com conectores de caminhada.
  - *Pausa de Almoço Sugerida (12h30 às 14h00)*.
  - *Turno da Tarde (14h30 às 19h30)* sincronizado com a climatização durante a chuva e pôr do sol nas Docas.
- Deck de Apoio com mini-mapa, previsão de marés e checklist interativo (*O que levar no dia*).
- Salva diretamente no banco relacional SQLite com backup em JSON.

### 7. Sobre Belém
- Guia cultural detalhado: A lenda e ciência da *Chuva das 16h*, Gastronomia Criativa UNESCO (açaí com peixe frito, tacacá, tucupi e jambu), navegação na baía e contatos de emergência e apoio ao turista.

---

## 🛠️ Requisitos e Execução

- **Python 3.10+**
- Dependências: `customtkinter`, `Pillow`

```bash
# 1. Ativar o ambiente virtual
.venv\Scripts\activate

# 2. Executar o aplicativo
python main.py
```
