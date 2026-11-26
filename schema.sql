-- ==============================================================================
-- BELÉMNAMÃO — SCHEMA COMPLETO PARA MYSQL WORKBENCH (LOCAL)
-- Execute este arquivo primeiro no MySQL Workbench, depois execute seeds.sql.
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS `belem_na_mao`
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE `belem_na_mao`;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `visitas_mensais`;
DROP TABLE IF EXISTS `avaliacoes`;
DROP TABLE IF EXISTS `roteiro_itens`;
DROP TABLE IF EXISTS `local_tags`;
DROP TABLE IF EXISTS `local_categorias`;
DROP TABLE IF EXISTS `categorias`;
DROP TABLE IF EXISTS `locais`;
DROP TABLE IF EXISTS `usuarios`;

SET FOREIGN_KEY_CHECKS = 1;

-- 1. Usuários
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

-- 2. Categorias
CREATE TABLE `categorias` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(100) NOT NULL,
    `emoji` VARCHAR(16) DEFAULT NULL,
    `cor` VARCHAR(20) DEFAULT NULL,
    `descricao` VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_categorias_nome` (`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Locais turísticos e gastronômicos
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

-- 4. Relação N:N Locais <-> Categorias
CREATE TABLE `local_categorias` (
    `local_id` VARCHAR(100) NOT NULL,
    `categoria` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`local_id`, `categoria`),
    KEY `idx_local_categorias` (`categoria`),
    CONSTRAINT `fk_lc_local` FOREIGN KEY (`local_id`) REFERENCES `locais` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Tags de busca
CREATE TABLE `local_tags` (
    `local_id` VARCHAR(100) NOT NULL,
    `tag` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`local_id`, `tag`),
    KEY `idx_local_tags` (`tag`),
    CONSTRAINT `fk_lt_local` FOREIGN KEY (`local_id`) REFERENCES `locais` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Favoritos / Itens do Roteiro por usuário
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

-- 7. Avaliações de usuários
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

-- 8. Histórico mensal/semanal de visitas (Ranking & Painel Admin DataInsight)
CREATE TABLE `visitas_mensais` (
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
