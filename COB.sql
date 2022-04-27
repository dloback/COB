-- -----------------------------------------------------
-- Apagando schema e criando um novo com charset UTF8
-- -----------------------------------------------------
DROP DATABASE IF EXISTS COB;

CREATE DATABASE IF NOT EXISTS COB DEFAULT CHARACTER SET UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;

USE COB;

-- -----------------------------------------------------
-- Desabilitando a opção default do mysql, pois no final do script faço 2 exclusões 
-- de registros que não existem na tabela de relacionamento
-- -----------------------------------------------------
SET SQL_SAFE_UPDATES = 0;

-- -----------------------------------------------------
-- Optei por criar as tabelas sem as chaves estrangeiras
-- Com isso, consigo inserir os registros sem critica na ordem de execução, 
-- se fosse o caso de carga de dados
-- Posteriormente faço update das chaves estrangeiras nas devidas tabelas
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Criando tabela Competição
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS  COMPETICAO (
  Id_Competicao INT NOT NULL AUTO_INCREMENT,
  Nome_Competicao varchar(255) NOT NULL,
  Data_Inscricao date NOT NULL,
  Data_Fim date,
  Metrica_Competicao char(1) NOT NULL,
  Id_Atleta INT,
  Resultado_Campeao Float,
  PRIMARY KEY (Id_Competicao));

-- -----------------------------------------------------
-- Criando tabela Atleta
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS ATLETA (
  Id_Atleta INT NOT NULL AUTO_INCREMENT,
  Nome_Atleta VARCHAR(255) NOT NULL,
  Id_Competicao INT NOT NULL,
  Resultado_Atleta Float NOT NULL,
  PRIMARY KEY (Id_Atleta));

-- -----------------------------------------------------
-- Depois das tabelas criadas e populadas (caso ocorresse)
-- Crio os relacionamentos entre as chaves
-- -----------------------------------------------------

ALTER TABLE COMPETICAO ADD
  CONSTRAINT fk_Atleta_Competicao
    FOREIGN KEY (Id_Atleta)
    REFERENCES Atleta (Id_Atleta)
    ON DELETE CASCADE
    ON UPDATE CASCADE;    

ALTER TABLE ATLETA ADD
  CONSTRAINT fk_Competicao_Atleta
    FOREIGN KEY (Id_Competicao)
    REFERENCES COMPETICAO (Id_Competicao)
    ON DELETE CASCADE
    ON UPDATE CASCADE;  
