-- ==============================================================================
-- Script Idempotente de Atualização — BelémNaMão (MySQL)
-- Nota: O aplicativo também executa essas atualizações automaticamente na
-- inicialização via services/database.py (sincronizar_catalogo_db).
-- Use este script caso deseje aplicar manualmente no MySQL Workbench.
-- ==============================================================================

USE bnamao;
SET NAMES utf8mb4;

-- 1. Garantir faixa de preço única ($) para o Mercado Ver-o-Peso
UPDATE locais
SET preco = 1
WHERE id = 'ver-o-peso';

-- 2. Atualizar Estação das Docas com destaque para o período noturno
UPDATE locais
SET
    descricao = 'Complexo turístico e gastronômico à beira da Baía do Guajará que ganha vida especial à noite, com iluminação cênica dos guindastes históricos, bares, cervejaria artesanal, restaurantes regionais e música ao vivo.',
    por_que_visitar = 'Destino imperdível no fim de tarde e período noturno em Belém: combine o pôr do sol na orla com jantares típicos, chopes amazônicos, sorvetes regionais e apresentações musicais noturnas no Anfiteatro.',
    duracao = '2–4 horas (Noite)',
    endereco = 'Av. Boulevard Castilhos França, s/n — Campina, Belém, PA. Aberto até 00h (Sex/Sáb até 01h).'
WHERE id = 'estacao-das-docas';

INSERT IGNORE INTO local_tags (local_id, tag) VALUES
('estacao-das-docas', 'noturno'),
('estacao-das-docas', 'vida noturna'),
('estacao-das-docas', 'música ao vivo'),
('estacao-das-docas', 'bares');

-- 3. Inserir/Atualizar o novo restaurante noturno Bistrô do Guajará
INSERT INTO locais (id, nome, bairro, preco, descricao, por_que_visitar, duracao, endereco, imagem)
VALUES (
    'bistro-guajara-noturno',
    'Bistrô do Guajará',
    'Umarizal',
    3,
    'Restaurante regional contemporâneo no coração do Umarizal, especializado em jantares amazônicos noturnos com filhote na brasa, pato no tucupi, drinques de jambu e música paraense ao vivo.',
    'Ideal para aproveitar a vida noturna gastronômica de Belém com alta culinária paraense, ambiente climatizado e carta autoral de coquetéis amazônicos.',
    '2–3 horas (Noturno)',
    'Av. Visconde de Souza Franco (Doca), Umarizal — Belém, PA. Funcionamento noturno: 18h30 às 00h30.',
    ''
)
ON DUPLICATE KEY UPDATE
    nome = VALUES(nome),
    bairro = VALUES(bairro),
    preco = VALUES(preco),
    descricao = VALUES(descricao),
    por_que_visitar = VALUES(por_que_visitar),
    duracao = VALUES(duracao),
    endereco = VALUES(endereco);

INSERT IGNORE INTO local_categorias (local_id, categoria) VALUES
('bistro-guajara-noturno', 'Gastronomia'),
('bistro-guajara-noturno', 'Passeio');

INSERT IGNORE INTO local_tags (local_id, tag) VALUES
('bistro-guajara-noturno', 'noturno'),
('bistro-guajara-noturno', 'jantar'),
('bistro-guajara-noturno', 'restaurante'),
('bistro-guajara-noturno', 'comida típica'),
('bistro-guajara-noturno', 'umarizal'),
('bistro-guajara-noturno', 'música ao vivo');

-- 4. Criar tabela de histórico mensal/semanal para o ranking "Mais Visitados"
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
