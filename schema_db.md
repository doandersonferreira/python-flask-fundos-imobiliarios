# Versão inicial do Schema do Banco de Dados

## Criação das Tabelas:
```
CREATE TABLE `usuario` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `email` varchar(40) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `administrador_ativo` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
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
```
