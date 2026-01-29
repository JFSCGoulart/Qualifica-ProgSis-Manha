import sqlite3 

conexao= sqlite3.connect('sistema.db')
cursor= conexao.cursor()

cursor.executescript('''
CREATE TABLE IF NOT EXISTS "cadastro_usuario" (
	"id" INTEGER NOT NULL UNIQUE,
	"nome_completo" TEXT,
	"data_nascimento" DATE,
	"CPF" INTEGER,
	"CEP" INTEGER,
	"Endereco" TEXT,
	"telefone" INTEGER,
	"email" TEXT,
	"tipo_user" VARCHAR,
	"senha_hash" TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "Cursos" (
	"id" INTEGER NOT NULL UNIQUE,
	"nome_completo" TEXT NOT NULL,
	PRIMARY KEY("id", "nome_completo")
);

CREATE TABLE IF NOT EXISTS "atividades" (
	"id" INTEGER NOT NULL UNIQUE,
	"curso_id" INTEGER,
	"tipo" TEXT,
	"perguntas" TEXT,
	"opcoes" TEXT,
	"resposta_correta" TEXT,
	"dica" TEXT,
	"pontuacoes" INTEGER,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "ranking_pontuacoes" (
	"id" INTEGER NOT NULL UNIQUE,
	"CPF" INTEGER,
	"pontuacao_id" INTEGER NOT NULL,
	PRIMARY KEY("id", "pontuacao_id")
);

 ''')

conexao.commit()

