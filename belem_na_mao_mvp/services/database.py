from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple

import mysql.connector
from mysql.connector import Error as MySQLError, IntegrityError

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
LOCAIS_JSON = DATA_DIR / "locais.json"
ROTEIRO_JSON = DATA_DIR / "roteiro.json"

# ----------------------------------------------------------------------
# Configuração da Conexão MySQL Online / Local
# Preencha abaixo com os dados do seu servidor MySQL online ou defina
# variáveis de ambiente (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, etc.)
# ----------------------------------------------------------------------
MYSQL_CONFIG: Dict[str, Any] = {
    "host": os.environ.get("MYSQL_HOST", "mysql-bnamao-belem-na-mao.f.aivencloud.com"),
    "port": int(os.environ.get("MYSQL_PORT", "10947")),
    "user": os.environ.get("MYSQL_USER", "avnadmin"),
    "password": os.environ.get("MYSQL_PASSWORD", "AVNS_cxfMQGehEqHY5DvsFc_"),
    "database": os.environ.get("MYSQL_DATABASE", "bnamao"),
    "charset": "utf8mb4",
    "use_unicode": True,
    "autocommit": False,
}


@contextmanager
def obter_conexao() -> Generator[mysql.connector.MySQLConnection, None, None]:
    """Retorna uma conexão ativa com o banco de dados MySQL configurado."""
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    try:
        yield conn
    finally:
        if conn.is_connected():
            conn.close()


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
# Criação do Esquema e Inicialização (MySQL)
# ----------------------------------------------------------------------
def criar_tabelas():
    """Cria as tabelas do banco de dados relacional MySQL se não existirem."""
    with obter_conexao() as conn:
        cursor = conn.cursor()

        # 1. Usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `usuarios` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `nome` VARCHAR(150) NOT NULL,
                `usuario` VARCHAR(80) NOT NULL,
                `email` VARCHAR(150) DEFAULT NULL,
                `senha_hash` VARCHAR(128) NOT NULL,
                `salt` VARCHAR(64) NOT NULL,
                `criado_em` DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                UNIQUE KEY `uk_usuarios_usuario` (`usuario`),
                UNIQUE KEY `uk_usuarios_email` (`email`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 2. Locais turísticos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `locais` (
                `id` VARCHAR(100) NOT NULL,
                `nome` VARCHAR(200) NOT NULL,
                `bairro` VARCHAR(120) NOT NULL,
                `preco` TINYINT NOT NULL,
                `descricao` TEXT,
                `por_que_visitar` TEXT,
                `duracao` VARCHAR(80) DEFAULT NULL,
                `endereco` VARCHAR(255) DEFAULT NULL,
                `imagem` VARCHAR(255) DEFAULT NULL,
                `criado_em` DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                KEY `idx_locais_bairro` (`bairro`),
                KEY `idx_locais_preco` (`preco`),
                CONSTRAINT `chk_locais_preco` CHECK (`preco` BETWEEN 1 AND 3)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 3. Categorias estruturadas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `categorias` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `nome` VARCHAR(100) NOT NULL,
                `emoji` VARCHAR(16) DEFAULT NULL,
                `cor` VARCHAR(20) DEFAULT NULL,
                `descricao` VARCHAR(255) DEFAULT NULL,
                PRIMARY KEY (`id`),
                UNIQUE KEY `uk_categorias_nome` (`nome`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 4. Relação N:N Locais <-> Categorias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `local_categorias` (
                `local_id` VARCHAR(100) NOT NULL,
                `categoria` VARCHAR(100) NOT NULL,
                PRIMARY KEY (`local_id`, `categoria`),
                KEY `idx_local_categorias` (`categoria`),
                CONSTRAINT `fk_lc_local` FOREIGN KEY (`local_id`) REFERENCES `locais` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 5. Tags de busca por local
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `local_tags` (
                `local_id` VARCHAR(100) NOT NULL,
                `tag` VARCHAR(100) NOT NULL,
                PRIMARY KEY (`local_id`, `tag`),
                KEY `idx_local_tags` (`tag`),
                CONSTRAINT `fk_lt_local` FOREIGN KEY (`local_id`) REFERENCES `locais` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 6. Itens do Roteiro (com suporte a usuário)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `roteiro_itens` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `usuario_id` INT DEFAULT NULL,
                `local_id` VARCHAR(100) NOT NULL,
                `ordem` INT DEFAULT 0,
                `adicionado_em` DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                KEY `idx_roteiro_usuario` (`usuario_id`),
                KEY `fk_roteiro_local` (`local_id`),
                CONSTRAINT `fk_roteiro_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
                CONSTRAINT `fk_roteiro_local` FOREIGN KEY (`local_id`) REFERENCES `locais` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 7. Avaliações futuras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `avaliacoes` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `usuario_id` INT NOT NULL,
                `local_id` VARCHAR(100) NOT NULL,
                `nota` TINYINT DEFAULT NULL,
                `comentario` TEXT,
                `criado_em` DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                KEY `fk_aval_usuario` (`usuario_id`),
                KEY `fk_aval_local` (`local_id`),
                CONSTRAINT `fk_aval_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
                CONSTRAINT `fk_aval_local` FOREIGN KEY (`local_id`) REFERENCES `locais` (`id`) ON DELETE CASCADE,
                CONSTRAINT `chk_aval_nota` CHECK (`nota` BETWEEN 1 AND 5)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        conn.commit()
        cursor.close()


def popular_dados_iniciais():
    """Migra dados de locais.json e cria categorias e usuários padrão no MySQL."""
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
                INSERT IGNORE INTO categorias (nome, emoji, cor, descricao)
                VALUES (%s, %s, %s, %s);
            """, (nome, emoji, cor, desc))

        # 2. Inserir Usuários Padrão (Ex.: turista / 123456 e admin / admin123)
        cursor.execute("SELECT COUNT(*) FROM usuarios;")
        total_usuarios = cursor.fetchone()[0]
        if total_usuarios == 0:
            h1, s1 = gerar_hash_senha("123456")
            cursor.execute("""
                INSERT INTO usuarios (nome, usuario, email, senha_hash, salt)
                VALUES (%s, %s, %s, %s, %s);
            """, ("Turista Belém", "turista", "turista@belem.com.br", h1, s1))

            h2, s2 = gerar_hash_senha("admin123")
            cursor.execute("""
                INSERT INTO usuarios (nome, usuario, email, senha_hash, salt)
                VALUES (%s, %s, %s, %s, %s);
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
                        INSERT INTO locais 
                        (id, nome, bairro, preco, descricao, por_que_visitar, duracao, endereco, imagem)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            nome = VALUES(nome),
                            bairro = VALUES(bairro),
                            preco = VALUES(preco),
                            descricao = VALUES(descricao),
                            por_que_visitar = VALUES(por_que_visitar),
                            duracao = VALUES(duracao),
                            endereco = VALUES(endereco),
                            imagem = VALUES(imagem);
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
                            INSERT IGNORE INTO local_categorias (local_id, categoria)
                            VALUES (%s, %s);
                        """, (item.get("id"), cat))

                    # Tags do local
                    for tag in item.get("tags", []):
                        cursor.execute("""
                            INSERT IGNORE INTO local_tags (local_id, tag)
                            VALUES (%s, %s);
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
                            VALUES (1, %s, %s);
                        """, (lid, idx))
            except Exception as e:
                print(f"[Aviso] Erro ao migrar roteiro.json inicial: {e}")

        conn.commit()
        cursor.close()


def inicializar_banco():
    """Garante a criação de tabelas e carregamento inicial de dados no MySQL."""
    criar_tabelas()
    popular_dados_iniciais()


# ----------------------------------------------------------------------
# Serviços de Autenticação / Usuários
# ----------------------------------------------------------------------
def cadastrar_usuario(nome: str, usuario: str, email: str, senha: str) -> Tuple[bool, str]:
    """Cadastra um novo usuário no MySQL com validações de unicidade."""
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
                VALUES (%s, %s, %s, %s, %s);
            """, (nome, usuario, email or None, senha_hash, salt))
            conn.commit()
            return True, "Cadastro realizado com sucesso!"
        except IntegrityError as e:
            msg = str(e).lower()
            if "usuario" in msg or "uk_usuarios_usuario" in msg:
                return False, "Nome de usuário já está em uso."
            if "email" in msg or "uk_usuarios_email" in msg:
                return False, "E-mail já está em uso."
            return False, "Erro ao registrar usuário: dados duplicados."
        finally:
            cursor.close()


def autenticar_usuario(login: str, senha: str) -> Optional[Dict[str, Any]]:
    """Autentica o usuário por nome de usuário ou e-mail."""
    login = login.strip().lower()
    if not login or not senha:
        return None

    with obter_conexao() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nome, usuario, email, senha_hash, salt
            FROM usuarios
            WHERE usuario = %s OR email = %s;
        """, (login, login))
        usuario = cursor.fetchone()
        cursor.close()

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
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, usuario, email FROM usuarios WHERE id = %s;", (usuario_id,))
        row = cursor.fetchone()
        cursor.close()
        return dict(row) if row else None


# ----------------------------------------------------------------------
# Serviços do Catálogo de Locais
# ----------------------------------------------------------------------
def listar_todos_locais() -> List[Dict[str, Any]]:
    """Retorna todos os locais cadastrados no MySQL com suas categorias e tags."""
    inicializar_banco()
    with obter_conexao() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nome, bairro, preco, descricao, por_que_visitar, duracao, endereco, imagem
            FROM locais
            ORDER BY criado_em ASC, id ASC;
        """)
        locais = [dict(row) for row in cursor.fetchall()]

        # Buscar categorias e tags agrupadas
        for loc in locais:
            loc_id = loc["id"]
            cursor.execute("SELECT categoria FROM local_categorias WHERE local_id = %s;", (loc_id,))
            loc["categoria"] = [r["categoria"] for r in cursor.fetchall()]

            cursor.execute("SELECT tag FROM local_tags WHERE local_id = %s;", (loc_id,))
            loc["tags"] = [r["tag"] for r in cursor.fetchall()]

        cursor.close()
        return locais


def buscar_locais_db(texto: str = "", categoria: str = "Todas", preco: str = "Qualquer") -> List[Dict[str, Any]]:
    """Busca locais com filtros usando SQL otimizado no MySQL."""
    inicializar_banco()
    mapa_preco = {"Baixo": 1, "Médio": 2, "Alto": 3}
    limite_preco = mapa_preco.get(preco)
    termo = f"%{texto.strip().lower()}%" if texto.strip() else None

    query = """
        SELECT DISTINCT l.id, l.nome, l.bairro, l.preco, l.descricao, 
                        l.por_que_visitar, l.duracao, l.endereco, l.imagem, l.criado_em
        FROM locais l
        LEFT JOIN local_categorias lc ON l.id = lc.local_id
        LEFT JOIN local_tags lt ON l.id = lt.local_id
        WHERE 1=1
    """
    params: List[Any] = []

    if termo:
        query += """
            AND (
                LOWER(l.nome) LIKE %s OR
                LOWER(l.bairro) LIKE %s OR
                LOWER(l.descricao) LIKE %s OR
                LOWER(lt.tag) LIKE %s
            )
        """
        params.extend([termo, termo, termo, termo])

    if categoria != "Todas":
        query += " AND lc.categoria = %s"
        params.append(categoria)

    if limite_preco is not None:
        query += " AND l.preco <= %s"
        params.append(limite_preco)

    query += " ORDER BY l.criado_em ASC, l.id ASC"

    with obter_conexao() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        locais = []
        for row in cursor.fetchall():
            d = dict(row)
            d.pop("criado_em", None)
            locais.append(d)

        for loc in locais:
            loc_id = loc["id"]
            cursor.execute("SELECT categoria FROM local_categorias WHERE local_id = %s;", (loc_id,))
            loc["categoria"] = [r["categoria"] for r in cursor.fetchall()]

            cursor.execute("SELECT tag FROM local_tags WHERE local_id = %s;", (loc_id,))
            loc["tags"] = [r["tag"] for r in cursor.fetchall()]

        cursor.close()
        return locais


def obter_local_por_id(local_id: str) -> Optional[Dict[str, Any]]:
    """Retorna um local específico com detalhes, categorias e tags."""
    with obter_conexao() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nome, bairro, preco, descricao, por_que_visitar, duracao, endereco, imagem
            FROM locais
            WHERE id = %s;
        """, (local_id,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            return None
        loc = dict(row)
        cursor.execute("SELECT categoria FROM local_categorias WHERE local_id = %s;", (local_id,))
        loc["categoria"] = [r["categoria"] for r in cursor.fetchall()]
        cursor.execute("SELECT tag FROM local_tags WHERE local_id = %s;", (local_id,))
        loc["tags"] = [r["tag"] for r in cursor.fetchall()]
        cursor.close()
        return loc


# ----------------------------------------------------------------------
# Serviços do Roteiro no MySQL
# ----------------------------------------------------------------------
def obter_roteiro_db(usuario_id: Optional[int] = 1) -> List[Dict[str, Any]]:
    """Carrega os locais salvos no roteiro do usuário."""
    inicializar_banco()
    with obter_conexao() as conn:
        cursor = conn.cursor(dictionary=True)
        if usuario_id is not None:
            cursor.execute("""
                SELECT l.id, l.nome, l.bairro, l.preco, l.descricao, 
                       l.por_que_visitar, l.duracao, l.endereco, l.imagem
                FROM roteiro_itens r
                JOIN locais l ON r.local_id = l.id
                WHERE r.usuario_id = %s
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
            cursor.execute("SELECT categoria FROM local_categorias WHERE local_id = %s;", (loc_id,))
            loc["categoria"] = [r["categoria"] for r in cursor.fetchall()]
            cursor.execute("SELECT tag FROM local_tags WHERE local_id = %s;", (loc_id,))
            loc["tags"] = [r["tag"] for r in cursor.fetchall()]
        cursor.close()
        return locais


def adicionar_ao_roteiro_db(local_id: str, usuario_id: Optional[int] = 1) -> bool:
    """Adiciona um local ao roteiro no MySQL se não estiver presente."""
    inicializar_banco()
    with obter_conexao() as conn:
        cursor = conn.cursor()
        # Verificar se já existe
        if usuario_id is not None:
            cursor.execute("""
                SELECT id FROM roteiro_itens WHERE usuario_id = %s AND local_id = %s;
            """, (usuario_id, local_id))
        else:
            cursor.execute("""
                SELECT id FROM roteiro_itens WHERE usuario_id IS NULL AND local_id = %s;
            """, (local_id,))

        if cursor.fetchone() is not None:
            cursor.close()
            return False  # Já existe

        # Próxima ordem (operador <=> é null-safe no MySQL)
        cursor.execute("SELECT COALESCE(MAX(ordem), 0) + 1 FROM roteiro_itens WHERE usuario_id <=> %s;", (usuario_id,))
        proxima_ordem = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO roteiro_itens (usuario_id, local_id, ordem)
            VALUES (%s, %s, %s);
        """, (usuario_id, local_id, proxima_ordem))
        conn.commit()
        cursor.close()
        return True


def remover_do_roteiro_db(local_id: str, usuario_id: Optional[int] = 1) -> bool:
    """Remove um local do roteiro do usuário no MySQL."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        if usuario_id is not None:
            cursor.execute("""
                DELETE FROM roteiro_itens WHERE usuario_id = %s AND local_id = %s;
            """, (usuario_id, local_id))
        else:
            cursor.execute("""
                DELETE FROM roteiro_itens WHERE usuario_id IS NULL AND local_id = %s;
            """, (local_id,))
        conn.commit()
        removido = cursor.rowcount > 0
        cursor.close()
        return removido


def limpar_roteiro_db(usuario_id: Optional[int] = 1) -> bool:
    """Remove todos os locais do roteiro de um usuário no MySQL."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        if usuario_id is not None:
            cursor.execute("DELETE FROM roteiro_itens WHERE usuario_id = %s;", (usuario_id,))
        else:
            cursor.execute("DELETE FROM roteiro_itens WHERE usuario_id IS NULL;")
        conn.commit()
        cursor.close()
        return True


if __name__ == "__main__":
    print("[*] Inicializando banco de dados MySQL...")
    inicializar_banco()
    print(f"[OK] Banco de dados MySQL inicializado em: {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}")

    locais = listar_todos_locais()
    print(f"[OK] Total de locais cadastrados: {len(locais)}")
    for l in locais:
        print(f"  - {l['nome']} ({l['bairro']}) | Categorias: {', '.join(l['categoria'])}")

    roteiro = obter_roteiro_db(1)
    print(f"[OK] Itens no roteiro inicial do usuário 1: {len(roteiro)}")

# fim