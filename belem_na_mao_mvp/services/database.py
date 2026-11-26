from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple

import mysql.connector
from mysql.connector import Error as MySQLError, IntegrityError
from mysql.connector.pooling import MySQLConnectionPool

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
LOCAIS_JSON = DATA_DIR / "locais.json"
ROTEIRO_JSON = DATA_DIR / "roteiro.json"


def _carregar_env() -> None:
    """Carrega variáveis de um arquivo .env local (se existir) sem dependências extras."""
    for candidato in (ROOT / ".env", ROOT.parent / ".env"):
        if candidato.is_file():
            try:
                for linha in candidato.read_text(encoding="utf-8").splitlines():
                    linha = linha.strip()
                    if not linha or linha.startswith("#") or "=" not in linha:
                        continue
                    chave, valor = linha.split("=", 1)
                    chave = chave.strip()
                    valor = valor.strip().strip('"').strip("'")
                    if chave and chave not in os.environ:
                        os.environ[chave] = valor
            except Exception:
                pass


_carregar_env()

# ----------------------------------------------------------------------
# Configuração da Conexão MySQL Workbench (Local)
# Pode ser sobrescrita por arquivo .env ou variáveis de ambiente.
# ----------------------------------------------------------------------
MYSQL_CONFIG: Dict[str, Any] = {
    "host": os.environ.get("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.environ.get("MYSQL_PORT", "3306")),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DATABASE", "belem_na_mao"),
    "charset": "utf8mb4",
    "use_unicode": True,
    "autocommit": False,
    "connection_timeout": int(os.environ.get("MYSQL_TIMEOUT", "6")),
}

_POOL_MYSQL: Optional[MySQLConnectionPool] = None
_BANCO_INICIALIZADO: bool = False
_CACHE_LOCAIS: Optional[List[Dict[str, Any]]] = None
_CACHE_TOP3: Dict[str, Tuple[List[Dict[str, Any]], bool]] = {}


def limpar_cache_memoria() -> None:
    """Limpa caches em memória quando há escrita ou troca de dados."""
    global _CACHE_LOCAIS
    _CACHE_LOCAIS = None
    _CACHE_TOP3.clear()


def _garantir_database_existe() -> None:
    """Cria o schema configurado no MySQL local caso ainda não exista."""
    cfg_sem_db = {k: v for k, v in MYSQL_CONFIG.items() if k != "database"}
    conn = mysql.connector.connect(**cfg_sem_db)
    try:
        cur = conn.cursor()
        db_name = MYSQL_CONFIG["database"]
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            "DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;"
        )
        conn.commit()
        cur.close()
    finally:
        if conn.is_connected():
            conn.close()


def _obter_pool() -> MySQLConnectionPool:
    global _POOL_MYSQL
    if _POOL_MYSQL is None:
        try:
            _POOL_MYSQL = MySQLConnectionPool(pool_name="belem_pool", pool_size=5, **MYSQL_CONFIG)
        except MySQLError:
            _garantir_database_existe()
            _POOL_MYSQL = MySQLConnectionPool(pool_name="belem_pool", pool_size=5, **MYSQL_CONFIG)
    return _POOL_MYSQL


@contextmanager
def obter_conexao() -> Generator[mysql.connector.MySQLConnection, None, None]:
    """Retorna uma conexão reutilizada do pool MySQL local."""
    pool = _obter_pool()
    conn = pool.get_connection()
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

        # 8. Histórico mensal/semanal de visitação para Ranking "Mais Visitados"
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `visitas_mensais` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `local_id` VARCHAR(100) NOT NULL,
                `ano` SMALLINT NOT NULL,
                `mes` TINYINT NOT NULL,
                `visitas_mes` INT NOT NULL DEFAULT 0,
                `visitas_semana` INT NOT NULL DEFAULT 0,
                `avaliacoes_qtd` INT NOT NULL DEFAULT 0,
                `nota_media` DECIMAL(3,2) NOT NULL DEFAULT 4.80,
                PRIMARY KEY (`id`),
                UNIQUE KEY `uk_visitas_local_ano_mes` (`local_id`, `ano`, `mes`),
                KEY `idx_visitas_ano_mes` (`ano`, `mes`),
                CONSTRAINT `fk_visitas_local` FOREIGN KEY (`local_id`) REFERENCES `locais` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        conn.commit()
        cursor.close()


def _gerar_dados_visitas_padrao() -> List[Dict[str, Any]]:
    """
    Gera registros mensais e semanais estruturados de visitação e avaliações (2025–2026)
    para todos os locais, refletindo a sazonalidade real de Belém do Pará.
    """
    perfis = [
        {"local_id": "ver-o-peso", "base": 1480, "nota": 4.82, "aval": 210, "picos": {7: 1.28, 10: 1.42, 12: 1.18}},
        {"local_id": "estacao-das-docas", "base": 1520, "nota": 4.91, "aval": 255, "picos": {7: 1.38, 10: 1.25, 12: 1.48}},
        {"local_id": "bistro-guajara-noturno", "base": 1060, "nota": 4.93, "aval": 165, "picos": {7: 1.32, 10: 1.22, 12: 1.55}},
        {"local_id": "feliz-lusitania", "base": 1120, "nota": 4.88, "aval": 150, "picos": {7: 1.20, 10: 1.38, 12: 1.18}},
        {"local_id": "mangal", "base": 1240, "nota": 4.84, "aval": 190, "picos": {7: 1.46, 8: 1.18, 12: 1.12}},
        {"local_id": "teatro-da-paz", "base": 890, "nota": 4.92, "aval": 120, "picos": {10: 1.28, 12: 1.44}},
        {"local_id": "praca-republica", "base": 760, "nota": 4.71, "aval": 95, "picos": {7: 1.18, 10: 1.26, 12: 1.20}},
        {"local_id": "ilha-combu", "base": 1180, "nota": 4.86, "aval": 175, "picos": {1: 1.24, 7: 1.62, 12: 1.22}},
        {"local_id": "basilica-nazare", "base": 1310, "nota": 4.95, "aval": 230, "picos": {5: 1.16, 10: 1.92, 12: 1.20}},
    ]
    fatores_mes = {
        1: 1.04, 2: 0.92, 3: 0.88, 4: 0.86, 5: 0.95, 6: 1.05,
        7: 1.38, 8: 1.08, 9: 1.02, 10: 1.52, 11: 1.14, 12: 1.34,
    }
    registros: List[Dict[str, Any]] = []
    for ano in (2025, 2026):
        fator_ano = 1.00 if ano == 2025 else 1.11
        for idx, p in enumerate(perfis):
            for mes in range(1, 13):
                f_mes = fatores_mes[mes]
                f_local = p["picos"].get(mes, 1.0)
                osc = 1.0 + (((idx * 7 + mes * 3 + ano) % 9) - 4) * 0.012
                visitas_mes = max(120, int(round(p["base"] * f_mes * f_local * fator_ano * osc)))
                visitas_semana = max(35, int(round(visitas_mes * (0.24 + ((mes + idx) % 4) * 0.015))))
                avaliacoes_qtd = max(15, int(round(p["aval"] * f_mes * f_local * fator_ano)))
                nota_mes = round(min(4.99, max(4.50, p["nota"] + (((mes + idx) % 5) - 2) * 0.02)), 2)
                registros.append({
                    "local_id": p["local_id"],
                    "ano": ano,
                    "mes": mes,
                    "visitas_mes": visitas_mes,
                    "visitas_semana": visitas_semana,
                    "avaliacoes_qtd": avaliacoes_qtd,
                    "nota_media": nota_mes,
                })
    return registros


def sincronizar_catalogo_db(conn) -> None:
    """
    Garante que correções de dados (Ver-o-Peso = preço 1, Estação das Docas noturna,
    novo restaurante Bistrô do Guajará e histórico visitas_mensais) existam no MySQL.
    """
    cursor = conn.cursor()

    # 1. Garante que Mercado Ver-o-Peso tenha apenas a faixa de preço 1 ($ Acessível)
    cursor.execute("UPDATE locais SET preco = 1 WHERE id = 'ver-o-peso';")

    # 2. Atualiza Estação das Docas com destaque noturno e insere Bistrô do Guajará
    atualizacoes = [
        (
            "estacao-das-docas",
            "Estação das Docas",
            "Campina",
            3,
            "Complexo turístico e gastronômico à beira da Baía do Guajará que ganha vida especial à noite, com iluminação cênica dos guindastes históricos, bares, cervejaria artesanal, restaurantes regionais e música ao vivo.",
            "Destino imperdível no fim de tarde e período noturno em Belém: combine o pôr do sol na orla com jantares típicos, chopes amazônicos, sorvetes regionais e apresentações musicais noturnas no Anfiteatro.",
            "2–4 horas (Noite)",
            "Av. Boulevard Castilhos França, s/n — Campina, Belém, PA. Aberto até 00h (Sex/Sáb até 01h).",
            "",
        ),
        (
            "bistro-guajara-noturno",
            "Bistrô do Guajará",
            "Umarizal",
            3,
            "Restaurante regional contemporâneo no coração do Umarizal, especializado em jantares amazônicos noturnos com filhote na brasa, pato no tucupi, drinques de jambu e música paraense ao vivo.",
            "Ideal para aproveitar a vida noturna gastronômica de Belém com alta culinária paraense, ambiente climatizado e carta autoral de coquetéis amazônicos.",
            "2–3 horas (Noturno)",
            "Av. Visconde de Souza Franco (Doca), Umarizal — Belém, PA. Funcionamento noturno: 18h30 às 00h30.",
            "",
        ),
    ]
    for row in atualizacoes:
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
                endereco = VALUES(endereco);
        """, row)

    for cat in ("Gastronomia", "Passeio"):
        cursor.execute(
            "INSERT IGNORE INTO local_categorias (local_id, categoria) VALUES ('bistro-guajara-noturno', %s);",
            (cat,),
        )

    tags_docas = ["orla", "restaurantes", "passeio", "noturno", "vida noturna", "música ao vivo", "bares"]
    for tag in tags_docas:
        cursor.execute(
            "INSERT IGNORE INTO local_tags (local_id, tag) VALUES ('estacao-das-docas', %s);",
            (tag,),
        )

    tags_bistro = ["noturno", "jantar", "restaurante", "comida típica", "umarizal", "música ao vivo"]
    for tag in tags_bistro:
        cursor.execute(
            "INSERT IGNORE INTO local_tags (local_id, tag) VALUES ('bistro-guajara-noturno', %s);",
            (tag,),
        )

    # 3. Popula histórico de visitas mensais se ainda incompleto
    cursor.execute("SELECT COUNT(*) FROM visitas_mensais WHERE ano = 2026;")
    qtd_2026 = cursor.fetchone()[0]
    if qtd_2026 < 9 * 12:
        dados_visitas = _gerar_dados_visitas_padrao()
        cursor.executemany("""
            INSERT IGNORE INTO visitas_mensais
            (local_id, ano, mes, visitas_mes, visitas_semana, avaliacoes_qtd, nota_media)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, [
            (
                r["local_id"], r["ano"], r["mes"],
                r["visitas_mes"], r["visitas_semana"], r["avaliacoes_qtd"], r["nota_media"],
            )
            for r in dados_visitas
        ])

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

        # 5. Sincronizar correções de dados, locais noturnos e visitas mensais
        sincronizar_catalogo_db(conn)

        conn.commit()
        cursor.close()


def inicializar_banco(forcar: bool = False):
    """Garante a criação de tabelas e carga inicial apenas uma vez por sessão."""
    global _BANCO_INICIALIZADO
    if _BANCO_INICIALIZADO and not forcar:
        return
    criar_tabelas()
    popular_dados_iniciais()
    _BANCO_INICIALIZADO = True


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
def listar_todos_locais(usar_cache: bool = True) -> List[Dict[str, Any]]:
    """Retorna todos os locais do MySQL em consulta única (sem N+1) com cache em memória."""
    global _CACHE_LOCAIS
    if usar_cache and _CACHE_LOCAIS is not None:
        return [dict(item) for item in _CACHE_LOCAIS]

    inicializar_banco()
    with obter_conexao() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                l.id, l.nome, l.bairro, l.preco, l.descricao,
                l.por_que_visitar, l.duracao, l.endereco, l.imagem,
                GROUP_CONCAT(DISTINCT lc.categoria ORDER BY lc.categoria SEPARATOR '||') AS categorias_str,
                GROUP_CONCAT(DISTINCT lt.tag ORDER BY lt.tag SEPARATOR '||') AS tags_str
            FROM locais l
            LEFT JOIN local_categorias lc ON l.id = lc.local_id
            LEFT JOIN local_tags lt ON l.id = lt.local_id
            GROUP BY l.id, l.nome, l.bairro, l.preco, l.descricao,
                     l.por_que_visitar, l.duracao, l.endereco, l.imagem, l.criado_em
            ORDER BY l.criado_em ASC, l.id ASC;
        """)
        locais = []
        for row in cursor.fetchall():
            d = dict(row)
            cats = d.pop("categorias_str", None)
            tags = d.pop("tags_str", None)
            d["categoria"] = cats.split("||") if cats else []
            d["tags"] = tags.split("||") if tags else []
            locais.append(d)

        cursor.close()
        _CACHE_LOCAIS = [dict(item) for item in locais]
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
        query += " AND l.preco = %s"
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


# ----------------------------------------------------------------------
# Ranking de Locais Mais Visitados (Semana / Mês / Ano)
# ----------------------------------------------------------------------
def obter_ranking_locais_db(
    periodo: str = "mes",
    mes: int = 11,
    ano: int = 2026,
) -> Tuple[List[Dict[str, Any]], bool]:
    """
    Consulta o ranking dos locais mais visitados/populares no MySQL com filtros
    dinâmicos por período ('semana', 'mes', 'ano'), mês (1..12) e ano.
    Preserva cálculo de média ponderada (visitas_mensais + avaliações reais).
    Retorna (lista_ranking, conectado_mysql).
    """
    periodo_norm = str(periodo or "mes").strip().lower()
    mes_norm = max(1, min(12, int(mes)))
    ano_norm = int(ano)

    try:
        inicializar_banco()
        with obter_conexao() as conn:
            cursor = conn.cursor(dictionary=True)

            if periodo_norm == "ano":
                cursor.execute("""
                    SELECT
                        l.id AS local_id,
                        l.nome,
                        l.bairro,
                        l.preco,
                        SUM(v.visitas_mes) AS visitas,
                        (SUM(v.avaliacoes_qtd) + COALESCE(MAX(a.real_qtd), 0)) AS avaliacoes_qtd,
                        ROUND(
                            (SUM(v.nota_media * v.avaliacoes_qtd) + COALESCE(MAX(a.real_soma), 0)) /
                            NULLIF(SUM(v.avaliacoes_qtd) + COALESCE(MAX(a.real_qtd), 0), 0),
                            2
                        ) AS nota_media
                    FROM visitas_mensais v
                    JOIN locais l ON v.local_id = l.id
                    LEFT JOIN (
                        SELECT local_id, COUNT(*) AS real_qtd, SUM(nota) AS real_soma
                        FROM avaliacoes
                        WHERE YEAR(criado_em) = %s AND nota IS NOT NULL
                        GROUP BY local_id
                    ) a ON a.local_id = l.id
                    WHERE v.ano = %s
                    GROUP BY l.id, l.nome, l.bairro, l.preco
                    ORDER BY visitas DESC, nota_media DESC;
                """, (ano_norm, ano_norm))
            elif periodo_norm == "semana":
                cursor.execute("""
                    SELECT
                        l.id AS local_id,
                        l.nome,
                        l.bairro,
                        l.preco,
                        v.visitas_semana AS visitas,
                        (GREATEST(1, ROUND(v.avaliacoes_qtd / 4)) + COALESCE(a.real_qtd, 0)) AS avaliacoes_qtd,
                        ROUND(
                            ((v.nota_media * GREATEST(1, ROUND(v.avaliacoes_qtd / 4))) + COALESCE(a.real_soma, 0)) /
                            NULLIF(GREATEST(1, ROUND(v.avaliacoes_qtd / 4)) + COALESCE(a.real_qtd, 0), 0),
                            2
                        ) AS nota_media
                    FROM visitas_mensais v
                    JOIN locais l ON v.local_id = l.id
                    LEFT JOIN (
                        SELECT local_id, COUNT(*) AS real_qtd, SUM(nota) AS real_soma
                        FROM avaliacoes
                        WHERE YEAR(criado_em) = %s AND MONTH(criado_em) = %s AND nota IS NOT NULL
                        GROUP BY local_id
                    ) a ON a.local_id = l.id
                    WHERE v.ano = %s AND v.mes = %s
                    ORDER BY visitas DESC, nota_media DESC;
                """, (ano_norm, mes_norm, ano_norm, mes_norm))
            else:
                cursor.execute("""
                    SELECT
                        l.id AS local_id,
                        l.nome,
                        l.bairro,
                        l.preco,
                        v.visitas_mes AS visitas,
                        (v.avaliacoes_qtd + COALESCE(a.real_qtd, 0)) AS avaliacoes_qtd,
                        ROUND(
                            ((v.nota_media * v.avaliacoes_qtd) + COALESCE(a.real_soma, 0)) /
                            NULLIF(v.avaliacoes_qtd + COALESCE(a.real_qtd, 0), 0),
                            2
                        ) AS nota_media
                    FROM visitas_mensais v
                    JOIN locais l ON v.local_id = l.id
                    LEFT JOIN (
                        SELECT local_id, COUNT(*) AS real_qtd, SUM(nota) AS real_soma
                        FROM avaliacoes
                        WHERE YEAR(criado_em) = %s AND MONTH(criado_em) = %s AND nota IS NOT NULL
                        GROUP BY local_id
                    ) a ON a.local_id = l.id
                    WHERE v.ano = %s AND v.mes = %s
                    ORDER BY visitas DESC, nota_media DESC;
                """, (ano_norm, mes_norm, ano_norm, mes_norm))

            rows = [dict(r) for r in cursor.fetchall()]
            for idx, r in enumerate(rows, start=1):
                r["posicao"] = idx
                r["visitas"] = int(r.get("visitas") or 0)
                r["avaliacoes_qtd"] = int(r.get("avaliacoes_qtd") or 0)
                r["nota_media"] = float(r.get("nota_media") or 4.8)
                cursor.execute("SELECT categoria FROM local_categorias WHERE local_id = %s;", (r["local_id"],))
                r["categoria"] = [c["categoria"] for c in cursor.fetchall()]

            cursor.close()
            if rows:
                return rows, True
    except Exception as e:
        print(f"[Aviso] Usando base estruturada local para ranking ({e})")

    # Fallback estruturado caso o banco MySQL esteja inacessível
    locais_mapa: Dict[str, Dict[str, Any]] = {}
    if LOCAIS_JSON.exists():
        try:
            with LOCAIS_JSON.open("r", encoding="utf-8") as f:
                for loc in json.load(f):
                    locais_mapa[loc["id"]] = loc
        except Exception:
            pass

    registros = _gerar_dados_visitas_padrao()
    agrupado: Dict[str, Dict[str, Any]] = {}
    for r in registros:
        if r["ano"] != ano_norm:
            continue
        if periodo_norm != "ano" and r["mes"] != mes_norm:
            continue

        lid = r["local_id"]
        info = locais_mapa.get(lid, {})
        vis = r["visitas_semana"] if periodo_norm == "semana" else r["visitas_mes"]
        avals = max(1, round(r["avaliacoes_qtd"] / 4)) if periodo_norm == "semana" else r["avaliacoes_qtd"]

        if lid not in agrupado:
            agrupado[lid] = {
                "local_id": lid,
                "nome": info.get("nome", lid),
                "bairro": info.get("bairro", "Belém"),
                "preco": info.get("preco", 2),
                "categoria": info.get("categoria", ["Turismo"]),
                "visitas": 0,
                "avaliacoes_qtd": 0,
                "soma_ponderada": 0.0,
            }
        agrupado[lid]["visitas"] += vis
        agrupado[lid]["avaliacoes_qtd"] += avals
        agrupado[lid]["soma_ponderada"] += r["nota_media"] * avals

    ranking = []
    for item in agrupado.values():
        avals_total = item.pop("avaliacoes_qtd")
        soma_pond = item.pop("soma_ponderada")
        item["avaliacoes_qtd"] = avals_total
        item["nota_media"] = round(soma_pond / avals_total, 2) if avals_total > 0 else 4.8
        ranking.append(item)

    ranking.sort(key=lambda x: (x["visitas"], x["nota_media"]), reverse=True)
    for idx, item in enumerate(ranking, start=1):
        item["posicao"] = idx
    return ranking, False


def obter_top3_por_categoria_db(
    categoria: str = "Todas",
    usar_cache: bool = True,
) -> Tuple[List[Dict[str, Any]], bool]:
    """
    Retorna o Top 3 dos locais mais visitados para a categoria selecionada
    ('Todas', 'Gastronomia', 'Cultura', 'História', 'Passeio', 'Natureza'),
    com soma de visitas, média ponderada de avaliações e cache em memória.
    """
    cat_norm = str(categoria or "Todas").strip()
    if usar_cache and cat_norm in _CACHE_TOP3:
        itens, conectado = _CACHE_TOP3[cat_norm]
        return [dict(i) for i in itens], conectado

    try:
        inicializar_banco()
        with obter_conexao() as conn:
            cursor = conn.cursor(dictionary=True)
            filtro_cat = ""
            params: List[Any] = []
            if cat_norm != "Todas":
                filtro_cat = "WHERE EXISTS (SELECT 1 FROM local_categorias lc2 WHERE lc2.local_id = l.id AND lc2.categoria = %s)"
                params.append(cat_norm)

            cursor.execute(f"""
                SELECT
                    l.id AS local_id,
                    l.nome,
                    l.bairro,
                    l.preco,
                    SUM(v.visitas_mes) AS visitas,
                    (SUM(v.avaliacoes_qtd) + COALESCE(MAX(a.real_qtd), 0)) AS avaliacoes_qtd,
                    ROUND(
                        (SUM(v.nota_media * v.avaliacoes_qtd) + COALESCE(MAX(a.real_soma), 0)) /
                        NULLIF(SUM(v.avaliacoes_qtd) + COALESCE(MAX(a.real_qtd), 0), 0),
                        2
                    ) AS nota_media,
                    GROUP_CONCAT(DISTINCT lc.categoria ORDER BY lc.categoria SEPARATOR '||') AS categorias_str
                FROM locais l
                JOIN visitas_mensais v ON v.local_id = l.id
                LEFT JOIN local_categorias lc ON lc.local_id = l.id
                LEFT JOIN (
                    SELECT local_id, COUNT(*) AS real_qtd, SUM(nota) AS real_soma
                    FROM avaliacoes
                    WHERE nota IS NOT NULL
                    GROUP BY local_id
                ) a ON a.local_id = l.id
                {filtro_cat}
                GROUP BY l.id, l.nome, l.bairro, l.preco
                ORDER BY visitas DESC, nota_media DESC
                LIMIT 3;
            """, params)

            rows = []
            for idx, r in enumerate(cursor.fetchall(), start=1):
                d = dict(r)
                cats = d.pop("categorias_str", None)
                d["posicao"] = idx
                d["visitas"] = int(d.get("visitas") or 0)
                d["avaliacoes_qtd"] = int(d.get("avaliacoes_qtd") or 0)
                d["nota_media"] = float(d.get("nota_media") or 4.8)
                d["categoria"] = cats.split("||") if cats else []
                rows.append(d)

            cursor.close()
            if rows:
                _CACHE_TOP3[cat_norm] = ([dict(i) for i in rows], True)
                return rows, True
    except Exception as e:
        print(f"[Aviso] Usando base estruturada local para Top 3 ({e})")

    # Fallback estruturado offline
    locais_mapa: Dict[str, Dict[str, Any]] = {}
    if LOCAIS_JSON.exists():
        try:
            with LOCAIS_JSON.open("r", encoding="utf-8") as f:
                for loc in json.load(f):
                    locais_mapa[loc["id"]] = loc
        except Exception:
            pass

    agrupado: Dict[str, Dict[str, Any]] = {}
    for r in _gerar_dados_visitas_padrao():
        lid = r["local_id"]
        info = locais_mapa.get(lid, {})
        cats = info.get("categoria", ["Passeio"])
        if cat_norm != "Todas" and cat_norm not in cats:
            continue

        if lid not in agrupado:
            agrupado[lid] = {
                "local_id": lid,
                "nome": info.get("nome", lid),
                "bairro": info.get("bairro", "Belém"),
                "preco": info.get("preco", 2),
                "categoria": cats,
                "visitas": 0,
                "avaliacoes_qtd": 0,
                "soma_ponderada": 0.0,
            }
        agrupado[lid]["visitas"] += r["visitas_mes"]
        agrupado[lid]["avaliacoes_qtd"] += r["avaliacoes_qtd"]
        agrupado[lid]["soma_ponderada"] += r["nota_media"] * r["avaliacoes_qtd"]

    ranking = []
    for item in agrupado.values():
        avals_total = item["avaliacoes_qtd"]
        soma_pond = item.pop("soma_ponderada")
        item["nota_media"] = round(soma_pond / avals_total, 2) if avals_total > 0 else 4.8
        ranking.append(item)

    ranking.sort(key=lambda x: (x["visitas"], x["nota_media"]), reverse=True)
    top3 = ranking[:3]
    for idx, item in enumerate(top3, start=1):
        item["posicao"] = idx

    _CACHE_TOP3[cat_norm] = ([dict(i) for i in top3], False)
    return top3, False


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