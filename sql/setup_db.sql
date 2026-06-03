-- 1. Criação do Banco de Dados
-- CREATE DATABASE banco_blindado;

-- 2. Estrutura Relacional (E-commerce 3NF)

-- Tabela de Clientes (Identidade)
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL, -- BCrypt (Salted)
    telefone VARCHAR(20),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Endereços (1:N com Clientes)
CREATE TABLE enderecos (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id) ON DELETE CASCADE,
    rua VARCHAR(150) NOT NULL,
    bairro VARCHAR(100),
    cidade VARCHAR(100) NOT NULL,
    provincia VARCHAR(100),
    tipo VARCHAR(20) DEFAULT 'Entrega' -- Entrega, Cobrança, etc.
);

-- Tabela de Categorias
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT
);

-- Tabela de Produtos
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    categoria_id INT REFERENCES categorias(id),
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco_base DECIMAL(12, 2) NOT NULL,
    estoque INT DEFAULT 0
);

-- Tabela de Pedidos (Cabeçalho)
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    endereco_id INT REFERENCES enderecos(id),
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Pendente',
    total_pedido DECIMAL(12, 2) DEFAULT 0.00
);

-- Tabela de Itens do Pedido (M:N entre Pedidos e Produtos)
CREATE TABLE pedido_itens (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedidos(id) ON DELETE CASCADE,
    produto_id INT REFERENCES produtos(id),
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(12, 2) NOT NULL -- Histórico de preço no momento da compra
);

-- 3. Segurança e Acessos (Blindagem)
-- Criar Papéis (Roles)
CREATE ROLE estagiario;
CREATE ROLE gerente;
CREATE ROLE sistema;

-- Permissões: Menor Privilégio
GRANT SELECT ON ALL TABLES IN SCHEMA public TO estagiario;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gerente;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO sistema;

-- 4. Proteção contra apagamento acidental (Trigger)
CREATE OR REPLACE FUNCTION impedir_truncate() 
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Operação TRUNCATE bloqueada para garantir integridade dos dados.';
END;
$$ LANGUAGE plpgsql;

-- Aplicar Trigger em tabelas críticas
CREATE TRIGGER trg_impedir_truncate_clientes BEFORE TRUNCATE ON clientes FOR EACH STATEMENT EXECUTE FUNCTION impedir_truncate();
CREATE TRIGGER trg_impedir_truncate_pedidos BEFORE TRUNCATE ON pedidos FOR EACH STATEMENT EXECUTE FUNCTION impedir_truncate();
CREATE TRIGGER trg_impedir_truncate_produtos BEFORE TRUNCATE ON produtos FOR EACH STATEMENT EXECUTE FUNCTION impedir_truncate();

-- 5. Otimização (Índices)
CREATE INDEX idx_clientes_email ON clientes(email);
CREATE INDEX idx_produtos_categoria ON produtos(categoria_id);
CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
CREATE INDEX idx_itens_pedido ON pedido_itens(pedido_id);

