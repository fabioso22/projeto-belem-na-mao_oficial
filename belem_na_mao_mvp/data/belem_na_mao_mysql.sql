-- =====================================================================
-- Dump MySQL — Projeto Belém na Mão
-- Compatível com MySQL 5.7+ / 8.0+ e MariaDB (phpMyAdmin, Workbench, Railway, etc.)
-- =====================================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';

-- ---------------------------------------------------------------------
-- 1. Tabela: usuarios
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS `avaliacoes`;
DROP TABLE IF EXISTS `roteiro_itens`;
DROP TABLE IF EXISTS `local_tags`;
DROP TABLE IF EXISTS `local_categorias`;
DROP TABLE IF EXISTS `categorias`;
DROP TABLE IF EXISTS `locais`;
DROP TABLE IF EXISTS `usuarios`;

CREATE TABLE `usuarios` (
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

-- ---------------------------------------------------------------------
-- 2. Tabela: locais
-- ---------------------------------------------------------------------
CREATE TABLE `locais` (
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

-- ---------------------------------------------------------------------
-- 3. Tabela: categorias
-- ---------------------------------------------------------------------
CREATE TABLE `categorias` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `emoji` VARCHAR(16) DEFAULT NULL,
  `cor` VARCHAR(20) DEFAULT NULL,
  `descricao` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_categorias_nome` (`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 4. Tabela: local_categorias (Relação N:N)
-- ---------------------------------------------------------------------
CREATE TABLE `local_categorias` (
  `local_id` VARCHAR(100) NOT NULL,
  `categoria` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`local_id`, `categoria`),
  KEY `idx_local_categorias` (`categoria`),
  CONSTRAINT `fk_lc_local` FOREIGN KEY (`local_id`) REFERENCES `locais` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 5. Tabela: local_tags
-- ---------------------------------------------------------------------
CREATE TABLE `local_tags` (
  `local_id` VARCHAR(100) NOT NULL,
  `tag` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`local_id`, `tag`),
  KEY `idx_local_tags` (`tag`),
  CONSTRAINT `fk_lt_local` FOREIGN KEY (`local_id`) REFERENCES `locais` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 6. Tabela: roteiro_itens
-- ---------------------------------------------------------------------
CREATE TABLE `roteiro_itens` (
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

-- ---------------------------------------------------------------------
-- 7. Tabela: avaliacoes
-- ---------------------------------------------------------------------
CREATE TABLE `avaliacoes` (
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

-- Dados da tabela `usuarios` (7 registros)
INSERT INTO `usuarios` (`id`, `nome`, `usuario`, `email`, `senha_hash`, `salt`, `criado_em`) VALUES
  (1, 'Turista Belém', 'turista', 'turista@belem.com.br', '03928778ce10a24f549409a02a5d387c0d9802ad0da30122b28ae569401cec24', 'dec1fcfe9d4bf4b89c878a5d1d4dfde2', '2026-10-15 22:38:41'),
  (2, 'Administrador', 'admin', 'admin@belem.com.br', 'a6d9b3bbeeea48045e021a9ef3e57777a821d8973596e1f0f29834df6cde9026', '3b5768e5b5d28700cdb1549808f6f475', '2026-10-15 22:38:41'),
  (3, 'Maria Silva', 'maria', 'maria@email.com', '1f9b09323d57a905b36939cb32bfd21f00c4245fa49c312c96ad1adbdacfacf2', '8078146246253b248d2142d57900fb9f', '2026-10-15 22:43:03'),
  (4, 'Maria Silva', 'maria_1792104238', 'maria_1792104238@email.com', '307b539587e494ab76e30d259786c5e083a7f987803cac161247c16cb33902af', 'bcdd65a5789b73590761221b97fc169e', '2026-10-15 22:43:58'),
  (5, 'fabio so', 'fabioso2', 'fabioso22@yahoo.com.br', '2190b80a69aa2e58b4f668279666b31e46fa48824ff8ade4ac097a93a47dc948', '1026ec7e4755d587b85bd6d84e8d913a', '2026-10-15 22:53:11'),
  (6, 'Maria Silva', 'maria_1792105104', 'maria_1792105104@email.com', '48a166c5206504cdd2612fb6b2dda18115e816452b59a912fdc590f2f03ff417', '9350e1478255ecd3627b0c64699ef7d7', '2026-10-15 22:58:24'),
  (7, 'Maria Silva', 'maria_1792105699', 'maria_1792105699@email.com', 'ecfe67c8e0f6df31617b713e3c77006953230820cbfbd272c37f15ac544468c8', 'c7aca9dc6ccff639eeb090275a602a44', '2026-10-15 23:08:19');

-- Dados da tabela `locais` (8 registros)
INSERT INTO `locais` (`id`, `nome`, `bairro`, `preco`, `descricao`, `por_que_visitar`, `duracao`, `endereco`, `imagem`, `criado_em`) VALUES
  ('ver-o-peso', 'Mercado Ver-o-Peso', 'Cidade Velha', 1, 'Um dos lugares mais conhecidos de Belém, com mercado, ingredientes regionais e movimento às margens da baía.', 'Para conhecer sabores, aromas e parte importante do cotidiano e da cultura paraense.', '1–2 horas', 'Belém, PA — confirme o endereço e o acesso antes da visita.', '', '2026-10-15 22:38:41'),
  ('estacao-das-docas', 'Estação das Docas', 'Campina', 3, 'Complexo à beira da baía com opções de alimentação e espaços para passear.', 'Boa opção para combinar passeio, vista para a água e uma refeição.', '1–3 horas', 'Belém, PA — confirme horários e funcionamento antes da visita.', '', '2026-10-15 22:38:41'),
  ('feliz-lusitania', 'Complexo Feliz Lusitânia', 'Cidade Velha', 2, 'Área histórica de Belém com patrimônio arquitetônico e espaços culturais.', 'Para explorar a história da cidade e conhecer construções emblemáticas.', '1–2 horas', 'Belém, PA — verifique horários dos espaços que pretende visitar.', '', '2026-10-15 22:38:41'),
  ('mangal', 'Mangal das Garças', 'Cidade Velha', 2, 'Parque urbano com áreas verdes e espaços de observação da natureza.', 'Uma pausa ao ar livre para apreciar paisagens e biodiversidade regional.', '1–2 horas', 'Belém, PA — confirme ingresso e horários antes da visita.', '', '2026-10-15 22:38:41'),
  ('teatro-da-paz', 'Theatro da Paz', 'Campina', 2, 'Teatro histórico e marco arquitetônico no centro de Belém.', 'Para conhecer um importante patrimônio cultural da cidade.', '1 hora', 'Belém, PA — confirme visitas guiadas e programação.', '', '2026-10-15 22:38:41'),
  ('praca-republica', 'Praça da República', 'Campina', 1, 'Praça central com áreas arborizadas e construções históricas no entorno.', 'Para caminhar, descansar e observar a vida urbana de Belém.', '30–60 minutos', 'Belém, PA — verifique eventos e condições locais.', '', '2026-10-15 22:38:41'),
  ('ilha-combu', 'Ilha do Combu', 'Região insular', 2, 'Destino insular próximo a Belém, conhecido por paisagens amazônicas e experiências gastronômicas.', 'Para sair do ritmo urbano e conhecer uma paisagem ligada ao ambiente amazônico.', 'Meio período', 'Acesso por transporte fluvial; confirme embarque, custos e condições antes de ir.', '', '2026-10-15 22:38:41'),
  ('basilica-nazare', 'Basílica de Nazaré', 'Nazaré', 1, 'Importante templo religioso e referência cultural da cidade.', 'Para conhecer sua arquitetura e a relevância cultural de Nazaré em Belém.', '30–60 minutos', 'Belém, PA — respeite os horários de celebração e visitação.', '', '2026-10-15 22:38:41');

-- Dados da tabela `categorias` (5 registros)
INSERT INTO `categorias` (`id`, `nome`, `emoji`, `cor`, `descricao`) VALUES
  (1, 'Gastronomia', '🍴', '#FBE9D9', 'Sabores paraenses'),
  (2, 'Cultura', '🏛', '#E6E9F8', 'Arte e patrimônio'),
  (3, 'História', '📜', '#F3EAD7', 'Memória da cidade'),
  (4, 'Natureza', '🌿', '#DFF1E3', 'Verde e ar livre'),
  (5, 'Passeio', '🧭', '#DDEEF6', 'Conheça a cidade');

-- Dados da tabela `local_categorias` (17 registros)
INSERT INTO `local_categorias` (`local_id`, `categoria`) VALUES
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

-- Dados da tabela `local_tags` (25 registros)
INSERT INTO `local_tags` (`local_id`, `tag`) VALUES
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

-- Dados da tabela `roteiro_itens` (0 registros)

-- Dados da tabela `avaliacoes` (0 registros)

SET FOREIGN_KEY_CHECKS = 1;
