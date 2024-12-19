CREATE DATABASE IF NOT EXISTS hw2;
USE hw2;
-- Creazione della tabella "utenti" se non esiste
CREATE TABLE IF NOT EXISTS utenti (
    email VARCHAR(255) PRIMARY KEY,
    ticker VARCHAR(255) NOT NULL,
    high_value DOUBLE DEFAULT NULL,
    low_value DOUBLE DEFAULT NULL 
);
-- Creazione della tabella "dati_finanziari" se non esiste
CREATE TABLE IF NOT EXISTS dati_finanziari (
    email VARCHAR(255) NOT NULL,
    ticker VARCHAR(255) NOT NULL,
    valore DOUBLE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email) REFERENCES utenti(email) ON DELETE CASCADE
);
CREATE USER IF NOT EXISTS 'pippo'@'%' IDENTIFIED BY 'ciao';
GRANT ALL PRIVILEGES ON hw2.* TO 'pippo'@'%';
FLUSH PRIVILEGES;

INSERT INTO utenti (email, ticker,high_value,low_value) VALUES 
('costanzavincenzo99@gmail.com', 'AAPL',230,5),
('joseaquila20@gmail.com', 'AAPL',500,5);
