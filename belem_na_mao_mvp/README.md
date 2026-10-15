# BelémNaMão — MVP Desktop com Banco de Dados SQLite

Protótipo funcional em Python + CustomTkinter com persistência em SQLite para demonstração e uso completo.

## O que já funciona
- **Banco de Dados Relacional SQLite** (`data/belem_na_mao.db`) com criação automática e migração inicial.
- **Autenticação Real de Usuários**:
  - Senhas criptografadas com `PBKDF2-HMAC-SHA256` e salt dinâmico.
  - Tela de cadastro de novos usuários com validação de unicidade de login/e-mail.
  - Usuários de demonstração pré-configurados:
    - `turista` / `123456`
    - `admin` / `admin123`
  - Opção rápida para entrar como visitante.
- **Catálogo de Pontos Turísticos e Experiências**:
  - Locais, categorias estruturadas e tags salvas e consultadas no SQLite.
  - Busca textual e filtros por categoria e faixa de preço.
- **Roteiro Personalizado por Usuário**:
  - Salva e remove locais no banco de dados SQLite individualmente para cada usuário.
  - Sincronização automática para compatibilidade e backup em `data/roteiro.json`.
  - Confirmação visual para limpar roteiro.
- **Interface Moderna Mobile-First**:
  - Design inspirado em smartphones (430x860), paleta profissional, botões arredondados, toasts e feedback interativo.

---

## Modelo de Dados (SQLite)

O banco é estruturado com integridade referencial (`PRAGMA foreign_keys = ON;`) e índices otimizados:

1. **`usuarios`**:
   - `id`: Chave primária autoincrementada.
   - `nome`, `usuario` (único), `email` (único), `senha_hash`, `salt`, `criado_em`.
2. **`locais`**:
   - `id`: Identificador textual único (ex.: `ver-o-peso`).
   - `nome`, `bairro`, `preco` (1 a 3), `descricao`, `por_que_visitar`, `duracao`, `endereco`, `imagem`, `criado_em`.
3. **`categorias`**:
   - `id`, `nome`, `emoji`, `cor`, `descricao`.
4. **`local_categorias`**:
   - Tabela de junção N:N (`local_id`, `categoria`).
5. **`local_tags`**:
   - Tags de busca vinculadas a cada local (`local_id`, `tag`).
6. **`roteiro_itens`**:
   - Itens salvos no roteiro (`id`, `usuario_id`, `local_id`, `ordem`, `adicionado_em`).
7. **`avaliacoes`**:
   - Estrutura pronta para avaliações futuras (`usuario_id`, `local_id`, `nota`, `comentario`).

---

## Requisitos
- Python 3.10+
- Windows, macOS ou Linux com ambiente gráfico.

## Instalação e Execução

Abra o terminal na pasta do projeto e execute:

```bash
# 1. Criar e ativar o ambiente virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar o aplicativo
python main.py
```

### Testar o Banco de Dados
Para rodar a suíte de testes do banco e verificar a integridade do SQLite:
```bash
python test_db.py
```

---

## Estrutura do Projeto
```text
belem_na_mao_mvp/
├── main.py                     # Ponto de entrada do sistema
├── test_db.py                  # Testes automatizados do banco SQLite
├── requirements.txt            # Dependências (customtkinter, Pillow)
├── README.md                   # Documentação detalhada
├── data/
│   ├── belem_na_mao.db         # Banco de dados SQLite relacional
│   ├── locais.json             # Dados originais de apoio/fallback
│   └── roteiro.json            # Backup de sincronização do roteiro
├── services/
│   ├── database.py             # Camada do SQLite (CRUD, auth, hashing)
│   ├── auth.py                 # Telas de login e cadastro
│   ├── catalogo.py             # Consultas e filtros do catálogo
│   └── roteiro.py              # Gerenciamento do roteiro do usuário
├── views/
│   └── main_window.py          # Dashboard e telas principais
└── assets/
    ├── README.txt
    └── images/                 # Imagens do sistema
```
