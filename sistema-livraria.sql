-- Banco de Dados SQLite - Livraria
-- Adaptado para SQLite Online

-- Criar tabela Clientes
CREATE TABLE IF NOT EXISTS Clientes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeCliente VARCHAR(100) NOT NULL,
    emailCliente VARCHAR(100) NOT NULL UNIQUE
);

-- Criar tabela Compras
CREATE TABLE IF NOT EXISTS Compras (
    CompraID INTEGER PRIMARY KEY AUTOINCREMENT,
    ClienteID INTEGER NOT NULL,
    NomeLivro VARCHAR(150) NOT NULL,
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ID) ON DELETE CASCADE
);

-- Inserir dados de exemplo na tabela Clientes
INSERT INTO Clientes (nomeCliente, emailCliente) VALUES
('João Silva', 'joao@email.com'),
('Maria Santos', 'maria@email.com'),
('Pedro Oliveira', 'pedro@email.com'),
('Ana Costa', 'ana@email.com');

-- Inserir dados de exemplo na tabela Compras
INSERT INTO Compras (ClienteID, NomeLivro) VALUES
(1, 'O Senhor dos Anéis'),
(1, 'Harry Potter e a Pedra Filosofal'),
(2, '1984'),
(2, 'O Pequeno Príncipe'),
(3, 'Dom Casmurro'),
(4, 'Cem Anos de Solidão');

-- Consultas úteis para teste

-- Listar todos os clientes
SELECT * FROM Clientes;

-- Listar todas as compras com informações do cliente
SELECT 
    c.ID,
    c.nomeCliente,
    c.emailCliente,
    comp.CompraID,
    comp.NomeLivro
FROM Clientes c
LEFT JOIN Compras comp ON c.ID = comp.ClienteID
ORDER BY c.ID;

-- Contar compras por cliente
SELECT 
    c.nomeCliente,
    COUNT(comp.CompraID) as TotalCompras
FROM Clientes c
LEFT JOIN Compras comp ON c.ID = comp.ClienteID
GROUP BY c.ID, c.nomeCliente;
