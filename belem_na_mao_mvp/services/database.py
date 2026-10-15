import hashlib
import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "belem_na_mao.db"
LOCAIS_JSON = DATA_DIR / "locais.json"
ROTEIRO_JSON = DATA_DIR / "roteiro.json"


def obter_conexao() -> sqlite3.Connection:
    """Retorna uma conexão ativa com o banco SQLite configurado."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------------------------------------------------
# Segurança e Senhas (PBKDF2 com Salt)
# ----------------------------------------------------------------------
def gerar_hash_senha(senha: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """Gera hash PBKDF2-HMAC-SHA256 seguro com salt único."""
    if not salt:
        salt = os.urandom(16).hex()
    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        bytes.fromhex(salt),
        iterations=100_000,
    )
    return hash_bytes.hex(), salt


def verificar_senha(senha: str, hash_esperado: str, salt: str) -> bool:
    """Verifica se a senha fornecida confere com o hash e salt armazenados."""
    hash_calculado, _ = gerar_hash_senha(senha, salt)
    return hash_calculado == hash_esperado


# ----------------------------------------------------------------------
# Criação do Esquema e Inicialização
# ----------------------------------------------------------------------
def criar_tabelas():
    """Cria as tabelas do banco de dados relacional SQLite se não existirem."""
    with obter_conexao() as conn:
        cursor = conn.cursor()

        # 1. Usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                usuario TEXT NOT NULL UNIQUE COLLATE NOCASE,
                email TEXT UNIQUE COLLATE NOCASE,
                senha_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. Locais turísticos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locais (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                bairro TEXT NOT NULL,
                preco INTEGER NOT NULL CHECK(preco BETWEEN 1 AND 3),
                descricao TEXT,
                por_que_visitar TEXT,
                duracao TEXT,
                endereco TEXT,
                imagem TEXT,
                criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 3. Categorias estruturadas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                emoji TEXT,
                cor TEXT,
                descricao TEXT
            );
        """)

        # 4. Relação N:N Locais <-> Categorias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS local_categorias (
                local_id TEXT NOT NULL,
                categoria TEXT NOT NULL,
                PRIMARY KEY (local_id, categoria),
                FOREIGN KEY (local_id) REFERENCES locais(id) ON DELETE CASCADE
            );
        """)

        # 5. Tags de busca por local
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS local_tags (
                local_id TEXT NOT NULL,
                tag TEXT NOT NULL,
                PRIMARY KEY (local_id, tag),
                FOREIGN KEY (local_id) REFERENCES locais(id) ON DELETE CASCADE
            );
        """)

        # 6. Itens do Roteiro (com suporte a usuário)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roteiro_itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                local_id TEXT NOT NULL,
                ordem INTEGER DEFAULT 0,
                adicionado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (local_id) REFERENCES locais(id) ON DELETE CASCADE
            );
        """)

        # 7. Avaliações futuras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS avaliacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                local_id TEXT NOT NULL,
                nota INTEGER CHECK(nota BETWEEN 1 AND 5),
                comentario TEXT,
                criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (local_id) REFERENCES locais(id) ON DELETE CASCADE
            );
        """)

        # Índices para performance em buscas e filtros
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_locais_bairro ON locais(bairro);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_locais_preco ON locais(preco);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_local_categorias ON local_categorias(categoria);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_local_tags ON local_tags(tag);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_roteiro_usuario ON roteiro_itens(usuario_id);")

        conn.commit()


def popular_dados_iniciais():
    """Migra dados de locais.json e cria categorias e usuários padrão."""
    with obter_conexao() as conn:
        cursor = conn.cursor()

        # 1. Inserir Categorias Padrão
        categorias_padrao = [
            ("Gastronomia", "🍴", "#FBE9D9", "Sabores paraenses"),
            ("Cultura", "🏛", "#E6E9F8", "Arte e patrimônio"),
            ("História", "📜", "#F3EAD7", "Memória da cidade"),
            ("Natureza", "🌿", "#DFF1E3", "Verde e ar livre"),
            ("Passeio", "🧭", "#DDEEF6", "Conheça a cidade"),
        ]
        for nome, emoji, cor, desc in categorias_padrao:
            cursor.execute("""
                INSERT OR IGNORE INTO categorias (nome, emoji, cor, descricao)
                VALUES (?, ?, ?, ?);
            """, (nome, emoji, cor, desc))

        # 2. Inserir Usuários Padrão (Ex.: turista / 123456 e admin / admin123)
        cursor.execute("SELECT COUNT(*) FROM usuarios;")
        total_usuarios = cursor.fetchone()[0]
        if total_usuarios == 0:
            h1, s1 = gerar_hash_senha("123456")
            cursor.execute("""
                INSERT INTO usuarios (nome, usuario, email, senha_hash, salt)
                VALUES (?, ?, ?, ?, ?);
            """, ("Turista Belém", "turista", "turista@belem.com.br", h1, s1))

            h2, s2 = gerar_hash_senha("admin123")
            cursor.execute("""
                INSERT INTO usuarios (nome, usuario, email, senha_hash, salt)
                VALUES (?, ?, ?, ?, ?);
            """, ("Administrador", "admin", "admin@belem.com.br", h2, s2))

        # 3. Migrar locais de locais.json se a tabela estiver vazia
        cursor.execute("SELECT COUNT(*) FROM locais;")
        total_locais = cursor.fetchone()[0]
        if total_locais == 0 and LOCAIS_JSON.exists():
            try:
                with LOCAIS_JSON.open("r", encoding="utf-8") as f:
                    locais = json.load(f)

                for item in locais:
                    cursor.execute("""
                        INSERT OR REPLACE INTO locais 
                        (id, nome, bairro, preco, descricao, por_que_visitar, duracao, endereco, imagem)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """, (
                        item.get("id"),
                        item.get("nome"),
                        item.get("bairro"),
                        item.get("preco", 2),
                        item.get("descricao", ""),
                        item.get("por_que_visitar", ""),
                        item.get("duracao", ""),
                        item.get("endereco", ""),
                        item.get("imagem", ""),
                    ))

                    # Categorias do local
                    for cat in item.get("categoria", []):
                        cursor.execute("""
                            INSERT OR IGNORE INTO local_categorias (local_id, categoria)
                            VALUES (?, ?);
                        """, (item.get("id"), cat))

                    # Tags do local
                    for tag in item.get("tags", []):
                        cursor.execute("""
                            INSERT OR IGNORE INTO local_tags (local_id, tag)
                            VALUES (?, ?);
                        """, (item.get("id"), tag))

            except Exception as e:
                print(f"[Aviso] Erro ao carregar locais.json inicial: {e}")

        # 4. Migrar roteiro.json existente para o usuário padrão (id=1)
        cursor.execute("SELECT COUNT(*) FROM roteiro_itens;")
        total_roteiro = cursor.fetchone()[0]
        if total_roteiro == 0 and ROTEIRO_JSON.exists():
            try:
                with ROTEIRO_JSON.open("r", encoding="utf-8") as f:
                    roteiro = json.load(f)
                for idx, item in enumerate(roteiro):
                    lid = item.get("id") if isinstance(item, dict) else str(item)
                    if lid:
                        cursor.execute("""
                            INSERT INTO roteiro_itens (usuario_id, local_id, ordem)
                            VALUES (1, ?, ?);
                        """, (lid, idx))
            except Exception as e:
                print(f"[Aviso] Erro ao migrar roteiro.json inicial: {e}")

        conn.commit()


def inicializar_banco():
    """Garante a criação de tabelas e carregamento inicial de dados."""
    criar_tabelas()
    popular_dados_iniciais()


# ----------------------------------------------------------------------
# Serviços de Autenticação / Usuários
# ----------------------------------------------------------------------
def cadastrar_usuario(nome: str, usuario: str, email: str, senha: str) -> Tuple[bool, str]:
    """Cadastra um novo usuário no SQLite com validações de unicidade."""
    nome = nome.strip()
    usuario = usuario.strip().lower()
    email = email.strip().lower()

    if not nome or not usuario or not senha:
        return False, "Nome, usuário e senha são obrigatórios."
    if len(senha) < 4:
        return False, "A senha deve ter pelo menos 4 caracteres."

    senha_hash, salt = gerar_hash_senha(senha)

    with obter_conexao() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (nome, usuario, email, senha_hash, salt)
                VALUES (?, ?, ?, ?, ?);
            """, (nome, usuario, email or None, senha_hash, salt))
            conn.commit()
            return True, "Cadastro realizado com sucesso!"
        except sqlite3.IntegrityError as e:
            msg = str(e).lower()
            if "usuario" in msg:
                return False, "Nome de usuário já está em uso."
            if "email" in msg:
                return False, "E-mail já está em uso."
            return False, "Erro ao registrar usuário: dados duplicados."


def autenticar_usuario(login: str, senha: str) -> Optional[Dict[str, Any]]:
    """Autentica o usuário por nome de usuário ou e-mail."""
    login = login.strip().lower()
    if not login or not senha:
        return None

    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, usuario, email, senha_hash, salt
            FROM usuarios
            WHERE usuario = ? OR email = ?;
        """, (login, login))
        usuario = cursor.fetchone()

        if usuario and verificar_senha(senha, usuario["senha_hash"], usuario["salt"]):
            return {
                "id": usuario["id"],
                "nome": usuario["nome"],
                "usuario": usuario["usuario"],
                "email": usuario["email"],
            }
        return None


def buscar_usuario_por_id(usuario_id: int) -> Optional[Dict[str, Any]]:
    """Busca detalhes de um usuário pelo ID."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, usuario, email FROM usuarios WHERE id = ?;", (usuario_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


# ----------------------------------------------------------------------
# Serviços do Catálogo de Locais
# ----------------------------------------------------------------------
def listar_todos_locais() -> List[Dict[str, Any]]:
    """Retorna todos os locais cadastrados no SQLite com suas categorias e tags."""
    inicializar_banco()
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, bairro, preco, descricao, por_que_visitar, duracao, endereco, imagem
            FROM locais
            ORDER BY rowid ASC;
        """)
        locais = [dict(row) for row in cursor.fetchall()]

        # Buscar categorias e tags agrupadas
        for loc in locais:
            loc_id = loc["id"]
            cursor.execute("SELECT categoria FROM local_categorias WHERE local_id = ?;", (loc_id,))
            loc["categoria"] = [r[0] for r in cursor.fetchall()]

            cursor.execute("SELECT tag FROM local_tags WHERE local_id = ?;", (loc_id,))
            loc["tags"] = [r[0] for r in cursor.fetchall()]

        return locais


def buscar_locais_db(texto: str = "", categoria: str = "Todas", preco: str = "Qualquer") -> List[Dict[str, Any]]:
    """Busca locais com filtros usando SQL otimizado."""
    inicializar_banco()
    mapa_preco = {"Baixo": 1, "Médio": 2, "Alto": 3}
    limite_preco = mapa_preco.get(preco)
    termo = f"%{texto.strip().lower()}%" if texto.strip() else None

    query = """
        SELECT DISTINCT l.id, l.nome, l.bairro, l.preco, l.descricao, 
                        l.por_que_visitar, l.duracao, l.endereco, l.imagem
        FROM locais l
        LEFT JOIN local_categorias lc ON l.id = lc.local_id
        LEFT JOIN local_tags lt ON l.id = lt.local_id
        WHERE 1=1
    """
    params: List[Any] = []

    if termo:
        query += """
            AND (
                LOWER(l.nome) LIKE ? OR
                LOWER(l.bairro) LIKE ? OR
                LOWER(l.descricao) LIKE ? OR
                LOWER(lt.tag) LIKE ?
            )
        """
        params.extend([termo, termo, termo, termo])

    if categoria != "Todas":
        query += " AND lc.categoria = ?"
        params.append(categoria)

    if limite_preco is not None:
        query += " AND l.preco <= ?"
        params.append(limite_preco)

    query += " ORDER BY l.rowid ASC"

    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        locais = [dict(row) for row in cursor.fetchall()]

        for loc in locais:
            loc_id = loc["id"]
            cursor.execute("SELECT categoria FROM local_categorias WHERE local_id = ?;", (loc_id,))
            loc["categoria"] = [r[0] for r in cursor.fetchall()]

            cursor.execute("SELECT tag FROM local_tags WHERE local_id = ?;", (loc_id,))
            loc["tags"] = [r[0] for r in cursor.fetchall()]

        return locais


def obter_local_por_id(local_id: str) -> Optional[Dict[str, Any]]:
    """Retorna um local específico com detalhes, categorias e tags."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, bairro, preco, descricao, por_que_visitar, duracao, endereco, imagem
            FROM locais
            WHERE id = ?;
        """, (local_id,))
        row = cursor.fetchone()
        if not row:
            return None
        loc = dict(row)
        cursor.execute("SELECT categoria FROM local_categorias WHERE local_id = ?;", (local_id,))
        loc["categoria"] = [r[0] for r in cursor.fetchall()]
        cursor.execute("SELECT tag FROM local_tags WHERE local_id = ?;", (local_id,))
        loc["tags"] = [r[0] for r in cursor.fetchall()]
        return loc


# ----------------------------------------------------------------------
# Serviços do Roteiro no SQLite
# ----------------------------------------------------------------------
def obter_roteiro_db(usuario_id: Optional[int] = 1) -> List[Dict[str, Any]]:
    """Carrega os locais salvos no roteiro do usuário."""
    inicializar_banco()
    with obter_conexao() as conn:
        cursor = conn.cursor()
        if usuario_id is not None:
            cursor.execute("""
                SELECT l.id, l.nome, l.bairro, l.preco, l.descricao, 
                       l.por_que_visitar, l.duracao, l.endereco, l.imagem
                FROM roteiro_itens r
                JOIN locais l ON r.local_id = l.id
                WHERE r.usuario_id = ?
                ORDER BY r.ordem ASC, r.id ASC;
            """, (usuario_id,))
        else:
            cursor.execute("""
                SELECT l.id, l.nome, l.bairro, l.preco, l.descricao, 
                       l.por_que_visitar, l.duracao, l.endereco, l.imagem
                FROM roteiro_itens r
                JOIN locais l ON r.local_id = l.id
                WHERE r.usuario_id IS NULL
                ORDER BY r.ordem ASC, r.id ASC;
            """)

        locais = [dict(row) for row in cursor.fetchall()]
        for loc in locais:
            loc_id = loc["id"]
            cursor.execute("SELECT categoria FROM local_categorias WHERE local_id = ?;", (loc_id,))
            loc["categoria"] = [r[0] for r in cursor.fetchall()]
            cursor.execute("SELECT tag FROM local_tags WHERE local_id = ?;", (loc_id,))
            loc["tags"] = [r[0] for r in cursor.fetchall()]
        return locais


def adicionar_ao_roteiro_db(local_id: str, usuario_id: Optional[int] = 1) -> bool:
    """Adiciona um local ao roteiro no SQLite se não estiver presente."""
    inicializar_banco()
    with obter_conexao() as conn:
        cursor = conn.cursor()
        # Verificar se já existe
        if usuario_id is not None:
            cursor.execute("""
                SELECT id FROM roteiro_itens WHERE usuario_id = ? AND local_id = ?;
            """, (usuario_id, local_id))
        else:
            cursor.execute("""
                SELECT id FROM roteiro_itens WHERE usuario_id IS NULL AND local_id = ?;
            """, (local_id,))

        if cursor.fetchone() is not None:
            return False  # Já existe

        # Próxima ordem
        cursor.execute("SELECT COALESCE(MAX(ordem), 0) + 1 FROM roteiro_itens WHERE usuario_id IS ?;", (usuario_id,))
        proxima_ordem = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO roteiro_itens (usuario_id, local_id, ordem)
            VALUES (?, ?, ?);
        """, (usuario_id, local_id, proxima_ordem))
        conn.commit()
        return True


def remover_do_roteiro_db(local_id: str, usuario_id: Optional[int] = 1) -> bool:
    """Remove um local do roteiro do usuário no SQLite."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        if usuario_id is not None:
            cursor.execute("""
                DELETE FROM roteiro_itens WHERE usuario_id = ? AND local_id = ?;
            """, (usuario_id, local_id))
        else:
            cursor.execute("""
                DELETE FROM roteiro_itens WHERE usuario_id IS NULL AND local_id = ?;
            """, (local_id,))
        conn.commit()
        return cursor.rowcount > 0


def limpar_roteiro_db(usuario_id: Optional[int] = 1) -> bool:
    """Remove todos os locais do roteiro de um usuário no SQLite."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        if usuario_id is not None:
            cursor.execute("DELETE FROM roteiro_itens WHERE usuario_id = ?;", (usuario_id,))
        else:
            cursor.execute("DELETE FROM roteiro_itens WHERE usuario_id IS NULL;")
        conn.commit()
        return True


if __name__ == "__main__":
    print("[*] Inicializando banco de dados SQLite...")
    inicializar_banco()
    print(f"[OK] Banco de dados inicializado em: {DB_PATH}")

    locais = listar_todos_locais()
    print(f"[OK] Total de locais cadastrados: {len(locais)}")
    for l in locais:
        print(f"  - {l['nome']} ({l['bairro']}) | Categorias: {', '.join(l['categoria'])}")

    roteiro = obter_roteiro_db(1)
    print(f"[OK] Itens no roteiro inicial do usuário 1: {len(roteiro)}")
