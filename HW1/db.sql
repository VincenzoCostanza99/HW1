CREATE DATABASE IF NOT EXISTS hw1;
USE hw1;
-- Creazione della tabella "utenti" se non esiste
CREATE TABLE IF NOT EXISTS utenti (
    email VARCHAR(255) PRIMARY KEY,
    ticker VARCHAR(255) NOT NULL
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
GRANT ALL PRIVILEGES ON hw1.* TO 'pippo'@'%';
FLUSH PRIVILEGES;

INSERT INTO utenti (email, ticker) VALUES 
('mario.rossi@example.com', 'AAPL'),
('lucia.bianchi@example.com', 'TSLA');
