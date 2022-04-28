-- -----------------------------------------------------
-- Apagando schema e criando um novo com charset UTF8
-- -----------------------------------------------------
DROP DATABASE IF EXISTS COB;

CREATE DATABASE IF NOT EXISTS COB; -- DEFAULT CHARACTER SET UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;

USE COB;
SET SQL_SAFE_UPDATES = 0;

-- -----------------------------------------------------
-- Criando tabela Competição
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS  COMPETICAO (
  Id_Competicao INT NOT NULL AUTO_INCREMENT,
  Nome_Competicao varchar(255) NOT NULL,
  Data_Inscricao date NOT NULL,
  Data_Fim date,
  Metrica_Competicao char(1) NOT NULL,
  Tentativas_Competicao int NOT NULL,
  PRIMARY KEY (Id_Competicao));

-- -----------------------------------------------------
-- Criando tabela Atleta
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS ATLETA (
  Id_Atleta INT NOT NULL AUTO_INCREMENT,
  Nome_Atleta VARCHAR(255) NOT NULL,
  Id_Competicao INT NOT NULL,
  Resultado_Atleta DECIMAL(6,3) NOT NULL,
  PRIMARY KEY (Id_Atleta),
  CONSTRAINT fk_Competicao_Atleta
    FOREIGN KEY (Id_Competicao)
    REFERENCES COMPETICAO (Id_Competicao)
    ON DELETE CASCADE
    ON UPDATE CASCADE);  
