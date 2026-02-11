import sqlite3

conexao = sqlite3.connect('trabalho_final.db')
cursor = conexao.cursor()

cursor.executescript('''
CREATE TABLE IF NOT EXISTS "usuario" (
	"id" INTEGER,
	"nome_completo" TEXT NOT NULL,
    "email" TEXT NOT NULL UNIQUE,
	"data_nascimento" DATE,
	"cpf" TEXT NOT NULL UNIQUE,
	"telefone" TEXT,
	"senha" TEXT NOT NULL,
	"tipo_usuario" TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "curso" (
	"id" INTEGER NOT NULL UNIQUE,
	"nome" TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "modulo"("id_curso")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "usuario_curso" (
	"id_usuario" INTEGER NOT NULL UNIQUE,
	"id_curso" INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id_usuario", "id_curso"),
	FOREIGN KEY ("id_usuario") REFERENCES "usuario"("id")
	ON UPDATE NO ACTION ON DELETE CASCADE,
	FOREIGN KEY ("id_curso") REFERENCES "curso"("id")
	ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "atividade" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_modulo INTEGER NOT NULL,
    pergunta TEXT NOT NULL,
    opcao_a TEXT NOT NULL,
    opcao_b TEXT NOT NULL,
    opcao_c TEXT NOT NULL,
    resposta_correta TEXT NOT NULL,
    dica TEXT,
    FOREIGN KEY (id_modulo) REFERENCES modulo(id)
);

CREATE TABLE IF NOT EXISTS "acerto" (
	"id" INTEGER,
	"id_usuario" INTEGER NOT NULL,
	"id_atividade" INTEGER NOT NULL,
	"correta" BOOLEAN NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id_usuario") REFERENCES "usuario"("id")
	ON UPDATE NO ACTION ON DELETE CASCADE,
	FOREIGN KEY ("id_atividade") REFERENCES "atividade"("id")
	ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "modulo" (
	"id" INTEGER NOT NULL UNIQUE,
	"nome" VARCHAR UNIQUE,
	"id_curso" INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "atividade"("id_modulo")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "progresso" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"id_usuario" INTEGER NOT NULL,
	"id_atividade" INTEGER NOT NULL,
	"estrelas" INTEGER DEFAULT 0,
	"acertou" BOOLEAN DEFAULT 0,
	"data" DATE DEFAULT CURRENT_DATE,
	FOREIGN KEY ("id_usuario") REFERENCES "usuario"("id")
	ON UPDATE NO ACTION ON DELETE CASCADE,
	FOREIGN KEY ("id_atividade") REFERENCES "atividade"("id")
	ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "vidas_curso" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"id_usuario" INTEGER NOT NULL,
	"id_curso" INTEGER NOT NULL,
	"vidas_restantes" INTEGER DEFAULT 3,
	UNIQUE("id_usuario", "id_curso"),
	FOREIGN KEY ("id_usuario") REFERENCES "usuario"("id")
	ON UPDATE NO ACTION ON DELETE CASCADE,
	FOREIGN KEY ("id_curso") REFERENCES "curso"("id")
	ON UPDATE NO ACTION ON DELETE CASCADE
);


''')