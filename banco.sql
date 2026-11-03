CREATE TABLE IF NOT EXISTS categoria(
   id integer primary key autoincrement,
   nome varchar(50) not null,
   descricao text, 
   ativo boolean,
   imagem blob,
   img varchar(100)
);

CREATE TABLE IF NOT EXISTS produto(
   id integer primary key autoincrement,
   nome varchar(50) not null,
   preco float,
   ativo boolean, 
   imagem blob,
   img varchar(100),
   id_categoria int,
   foreign key ('id_categoria') references categoria('id')
);




