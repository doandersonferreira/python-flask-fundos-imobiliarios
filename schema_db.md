# Versão inicial do Schema do Banco de Dados

## Criação das Tabelas:
```
DROP DATABASE fii;
CREATE DATABASE fii;

use fii

CREATE TABLE `usuario` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `email` varchar(40) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `administrador_ativo` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `cnpj` varchar(14) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    
CREATE TABLE `ativo` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `ticker` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `cnpj` varchar(14) COLLATE utf8_bin NOT NULL,
      `id_administrador` int(11) NOT NULL,
      PRIMARY KEY (`id`),
      FOREIGN KEY (id_administrador) REFERENCES administrador_ativo(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    
CREATE TABLE `operacao` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `data` varchar(10) COLLATE utf8_bin NOT NULL,
      `valor_cota` int(10) COLLATE utf8_bin NOT NULL,
      `quantidade` int(4) COLLATE utf8_bin NOT NULL,
      `id_ativo` int(11) NOT NULL,
      `id_usuario` int(11) NOT NULL,
      PRIMARY KEY (`id`),
      FOREIGN KEY (id_ativo) REFERENCES ativo(id),
      FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


INSERT INTO administrador_ativo (nome, cnpj) VALUES 
('Votorantim Asset', '03384738000198'),
('Planner','00806535000154'),
('BTG Pactual','59281253000123'),
('BRL Trust','13486793000142'),
('Vortx','22610500000188'),
('Credit Suisse Hedging-Griffo','61809182000130');

INSERT INTO ativo (ticker,nome, cnpj, id_administrador) VALUES
('BBPO11','BB Progressivo II','14410722000129',1),
('MFII11','Mérito Desenvolvimento Imobiliário I','16915968000188',2),
('MXRF11','Maxi Renda','97521225000125',3),
('BCFF11','BTG Fundo de Fundos','11026627000138',3),
('RECT11','FII UBS BR Office','32274163000159',4),
('VISC11','Vinci Shopping Centers','17554274000125',4),
('XPLG11','XP Log','26502794000185',5),
('HGLG11','CGHG Logística','11728688000147',6);
```
