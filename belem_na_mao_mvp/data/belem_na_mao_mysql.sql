-- ==============================================================================
-- PROJETO: BelémNaMão (Belém na Mão)
-- SCRIPT DE CRIAÇÃO E CARGA DE DADOS PARA MYSQL / MYSQL WORKBENCH
-- Compatibilidade: MySQL 8.0+ / MariaDB 10.3+
-- Codificação: UTF-8 (utf8mb4 para suporte total a emojis e caracteres especiais)
-- ==============================================================================

-- 1. CRIAÇÃO DO BANCO DE DADOS
CREATE DATABASE IF NOT EXISTS belem_na_mao
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE belem_na_mao;

-- Configurações de sessão para garantir compatibilidade e UTF-8
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 2. LIMPEZA PREVENTIVA DE TABELAS (DROP NA ORDEM CORRETA DE DEPENDÊNCIAS)
DROP TABLE IF EXISTS avaliacoes;
DROP TABLE IF EXISTS roteiro_itens;
DROP TABLE IF EXISTS local_tags;
DROP TABLE IF EXISTS local_categorias;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS locais;
DROP TABLE IF EXISTS usuarios;

SET FOREIGN_KEY_CHECKS = 1;

-- ==============================================================================
-- 3. CRIAÇÃO DAS TABELAS (DDL)
-- ==============================================================================

-- Tabela: usuarios
-- Armazena os usuários cadastrados e credenciais com hash PBKDF2 + Salt
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) UNIQUE,
    senha_hash VARCHAR(64) NOT NULL,
    salt VARCHAR(32) NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela: locais
-- Armazena os pontos turísticos e atrações de Belém
CREATE TABLE locais (
    id VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    preco TINYINT NOT NULL CHECK (preco BETWEEN 1 AND 3),
    descricao TEXT,
    por_que_visitar TEXT,
    duracao VARCHAR(50),
    endereco TEXT,
    imagem VARCHAR(255) DEFAULT '',
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_locais_bairro (bairro),
    INDEX idx_locais_preco (preco)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela: categorias
-- Categorias temáticas das atrações (ex: Gastronomia, Cultura, Natureza)
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    emoji VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    cor VARCHAR(20),
    descricao VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela: local_categorias (Relação N:N entre Locais e Categorias)
CREATE TABLE local_categorias (
    local_id VARCHAR(50) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    PRIMARY KEY (local_id, categoria),
    CONSTRAINT fk_local_categorias_local 
        FOREIGN KEY (local_id) REFERENCES locais(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_local_categorias_categoria 
        FOREIGN KEY (categoria) REFERENCES categorias(nome) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_local_categorias_cat (categoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela: local_tags (Tags de pesquisa vinculadas aos locais)
CREATE TABLE local_tags (
    local_id VARCHAR(50) NOT NULL,
    tag VARCHAR(50) NOT NULL,
    PRIMARY KEY (local_id, tag),
    CONSTRAINT fk_local_tags_local 
        FOREIGN KEY (local_id) REFERENCES locais(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_local_tags_tag (tag)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela: roteiro_itens (Itens salvos no roteiro de cada usuário)
CREATE TABLE roteiro_itens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NULL,
    local_id VARCHAR(50) NOT NULL,
    ordem INT DEFAULT 0,
    adicionado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_roteiro_usuario 
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_roteiro_local 
        FOREIGN KEY (local_id) REFERENCES locais(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_roteiro_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela: avaliacoes (Módulo de avaliações e comentários)
CREATE TABLE avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    local_id VARCHAR(50) NOT NULL,
    nota TINYINT CHECK (nota BETWEEN 1 AND 5),
    comentario TEXT,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_avaliacoes_usuario 
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_avaliacoes_local 
        FOREIGN KEY (local_id) REFERENCES locais(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_avaliacoes_usuario (usuario_id),
    INDEX idx_avaliacoes_local (local_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- 4. INSERÇÃO DE DADOS INICIAIS (SEEDS / DML)
-- ==============================================================================

-- Categorias do Sistema
INSERT INTO categorias (id, nome, emoji, cor, descricao) VALUES
(1, 'Gastronomia', '🍴', '#FBE9D9', 'Sabores paraenses'),
(2, 'Cultura', '🏛', '#E6E9F8', 'Arte e patrimônio'),
(3, 'História', '📜', '#F3EAD7', 'Memória da cidade'),
(4, 'Natureza', '🌿', '#DFF1E3', 'Verde e ar livre'),
(5, 'Passeio', '🧭', '#DDEEF6', 'Conheça a cidade');

-- Locais Turísticos Oficiais de Belém
INSERT INTO locais (id, nome, bairro, preco, descricao, por_que_visitar, duracao, endereco, imagem, criado_em) VALUES
('ver-o-peso', 'Mercado Ver-o-Peso', 'Cidade Velha', 1, 
 'Um dos lugares mais conhecidos de Belém, com mercado, ingredientes regionais e movimento às margens da baía.', 
 'Para conhecer sabores, aromas e parte importante do cotidiano e da cultura paraense.', 
 '1–2 horas', 'Belém, PA — confirme o endereço e o acesso antes da visita.', '', '2026-10-15 22:38:41'),

('estacao-das-docas', 'Estação das Docas', 'Campina', 3, 
 'Complexo à beira da baía com opções de alimentação e espaços para passear.', 
 'Boa opção para combinar passeio, vista para a água e uma refeição.', 
 '1–3 horas', 'Belém, PA — confirme horários e funcionamento antes da visita.', '', '2026-10-15 22:38:41'),

('feliz-lusitania', 'Complexo Feliz Lusitânia', 'Cidade Velha', 2, 
 'Área histórica de Belém com patrimônio arquitetônico e espaços culturais.', 
 'Para explorar a história da cidade e conhecer construções emblemáticas.', 
 '1–2 horas', 'Belém, PA — verifique horários dos espaços que pretende visitar.', '', '2026-10-15 22:38:41'),

('mangal', 'Mangal das Garças', 'Cidade Velha', 2, 
 'Parque urbano com áreas verdes e espaços de observação da natureza.', 
 'Uma pausa ao ar livre para apreciar paisagens e biodiversidade regional.', 
 '1–2 horas', 'Belém, PA — confirme ingresso e horários antes da visita.', '', '2026-10-15 22:38:41'),

('teatro-da-paz', 'Theatro da Paz', 'Campina', 2, 
 'Teatro histórico e marco arquitetônico no centro de Belém.', 
 'Para conhecer um importante patrimônio cultural da cidade.', 
 '1 hora', 'Belém, PA — confirme visitas guiadas e programação.', '', '2026-10-15 22:38:41'),

('praca-republica', 'Praça da República', 'Campina', 1, 
 'Praça central com áreas arborizadas e construções históricas no entorno.', 
 'Para caminhar, descansar e observar a vida urbana de Belém.', 
 '30–60 minutos', 'Belém, PA — verifique eventos e condições locais.', '', '2026-10-15 22:38:41'),

('ilha-combu', 'Ilha do Combu', 'Região insular', 2, 
 'Destino insular próximo a Belém, conhecido por paisagens amazônicas e experiências gastronômicas.', 
 'Para sair do ritmo urbano e conhecer uma paisagem ligada ao ambiente amazônico.', 
 'Meio período', 'Acesso por transporte fluvial; confirme embarque, custos e condições antes de ir.', '', '2026-10-15 22:38:41'),

('basilica-nazare', 'Basílica de Nazaré', 'Nazaré', 1, 
 'Importante templo religioso e referência cultural da cidade.', 
 'Para conhecer sua arquitetura e a relevância cultural de Nazaré em Belém.', 
 '30–60 minutos', 'Belém, PA — respeite os horários de celebração e visitação.', '', '2026-10-15 22:38:41');

-- Associação de Categorias por Local (N:N)
INSERT INTO local_categorias (local_id, categoria) VALUES
('ver-o-peso', 'Gastronomia'),
('ver-o-peso', 'Cultura'),
('estacao-das-docas', 'Gastronomia'),
('estacao-das-docas', 'Passeio'),
('feliz-lusitania', 'Cultura'),
('feliz-lusitania', 'História'),
('mangal', 'Natureza'),
('mangal', 'Passeio'),
('teatro-da-paz', 'Cultura'),
('teatro-da-paz', 'História'),
('praca-republica', 'Passeio'),
('praca-republica', 'Natureza'),
('ilha-combu', 'Natureza'),
('ilha-combu', 'Gastronomia'),
('ilha-combu', 'Passeio'),
('basilica-nazare', 'Cultura'),
('basilica-nazare', 'História');

-- Tags de Pesquisa por Local
INSERT INTO local_tags (local_id, tag) VALUES
('ver-o-peso', 'comida típica'),
('ver-o-peso', 'mercado'),
('ver-o-peso', 'cultura'),
('estacao-das-docas', 'orla'),
('estacao-das-docas', 'restaurantes'),
('estacao-das-docas', 'passeio'),
('feliz-lusitania', 'história'),
('feliz-lusitania', 'arquitetura'),
('feliz-lusitania', 'museu'),
('mangal', 'parque'),
('mangal', 'natureza'),
('mangal', 'família'),
('teatro-da-paz', 'teatro'),
('teatro-da-paz', 'arquitetura'),
('teatro-da-paz', 'história'),
('praca-republica', 'praça'),
('praca-republica', 'caminhada'),
('praca-republica', 'centro'),
('ilha-combu', 'ilha'),
('ilha-combu', 'amazônia'),
('ilha-combu', 'chocolate'),
('ilha-combu', 'comida típica'),
('basilica-nazare', 'arquitetura'),
('basilica-nazare', 'religião'),
('basilica-nazare', 'cultura');

-- Usuários Padrão e de Demonstração
-- Senha de 'turista': 123456
-- Senha de 'admin': admin123
INSERT INTO usuarios (id, nome, usuario, email, senha_hash, salt, criado_em) VALUES
(1, 'Turista Belém', 'turista', 'turista@belem.com.br', '03928778ce10a24f549409a02a5d387c0d9802ad0da30122b28ae569401cec24', 'dec1fcfe9d4bf4b89c878a5d1d4dfde2', '2026-10-15 22:38:41'),
(2, 'Administrador', 'admin', 'admin@belem.com.br', 'a6d9b3bbeeea48045e021a9ef3e57777a821d8973596e1f0f29834df6cde9026', '3b5768e5b5d28700cdb1549808f6f475', '2026-10-15 22:38:41'),
(3, 'Maria Silva', 'maria', 'maria@email.com', '1f9b09323d57a905b36939cb32bfd21f00c4245fa49c312c96ad1adbdacfacf2', '8078146246253b248d2142d57900fb9f', '2026-10-15 22:43:03');

-- Exemplo de Roteiro Salvo para o Turista (usuario_id = 1)
INSERT INTO roteiro_itens (id, usuario_id, local_id, ordem, adicionado_em) VALUES
(1, 1, 'ver-o-peso', 1, '2026-10-15 22:38:41'),
(2, 1, 'estacao-das-docas', 2, '2026-10-15 22:38:41'),
(3, 1, 'ilha-combu', 3, '2026-10-15 22:38:41');

-- Ajustar ponteiro de AUTO_INCREMENT das tabelas
ALTER TABLE usuarios AUTO_INCREMENT = 10;
ALTER TABLE categorias AUTO_INCREMENT = 6;
ALTER TABLE roteiro_itens AUTO_INCREMENT = 30;

-- ==============================================================================
-- 5. CONSULTAS DE TESTE E VALIDAÇÃO (ÚTEIS NO WORKBENCH)
-- ==============================================================================

-- Visualizar todos os locais com suas categorias concatenadas
-- SELECT 
--     l.id,
--     l.nome,
--     l.bairro,
--     CASE l.preco 
--         WHEN 1 THEN '$ (Econômico)' 
--         WHEN 2 THEN ' (Moderado)' 
--         WHEN 3 THEN '$ (Mais elevado)' 
--     END AS faixa_preco,
--     GROUP_CONCAT(DISTINCT lc.categoria ORDER BY lc.categoria SEPARATOR ', ') AS categorias,
--     GROUP_CONCAT(DISTINCT lt.tag ORDER BY lt.tag SEPARATOR ', ') AS tags
-- FROM locais l
-- LEFT JOIN local_categorias lc ON l.id = lc.local_id
-- LEFT JOIN local_tags lt ON l.id = lt.local_id
-- GROUP BY l.id, l.nome, l.bairro, l.preco
-- ORDER BY l.nome;

-- Visualizar o roteiro montado para o usuário 'turista'
-- SELECT 
--     u.nome AS usuario,
--     r.ordem,
--     l.nome AS ponto_turistico,
--     l.bairro,
--     l.duracao
-- FROM roteiro_itens r
-- JOIN usuarios u ON r.usuario_id = u.id
-- JOIN locais l ON r.local_id = l.id
-- WHERE u.usuario = 'turista'
-- ORDER BY r.ordem ASC;
