import sqlite3 

conexao= sqlite3.connect('sistema.db')
cursor= conexao.cursor()

cursor.executescript('''
	CREATE TABLE IF NOT EXISTS usuario  (
		id INTEGER NOT NULL UNIQUE,
		nome_completo TEXT NOT NULL,
		data_nascimento DATE NOT NULL,
		CPF INTEGER NOT NULL,
		telefone INTEGER NOT NULL,
		id_tipo_usuario VARCHAR NOT NULL,
		senha TEXT NOT NULL,
		PRIMARY KEY(id)
	);

	CREATE TABLE IF NOT EXISTS tipo_usuario (
		id INTEGER NOT NULL UNIQUE,
		aluno,
		professor,
		coordenador,
		PRIMARY KEY(id)
	);

	CREATE TABLE IF NOT EXISTS cursos (
		id INTEGER NOT NULL UNIQUE,
		nome TEXT NOT NULL,
		PRIMARY KEY(id)
	);

	CREATE TABLE IF NOT EXISTS atividades (
		id INTEGER NOT NULL UNIQUE,
		cursos_id INTEGER NOT NULL,
		tipo TEXT NOT NULL,
		perguntas TEXT NOT NULL,
		opcoes TEXT NOT NULL,
		respostas TEXT NOT NULL,
		dica TEXT NOT NULL,
		pontuacoes INTEGER NOT NULL,
		PRIMARY KEY(id)
	);

	CREATE TABLE IF NOT EXISTS ranking_pontuacoes (
		id INTEGER NOT NULL UNIQUE,
		CPF INTEGER NOT NULL,
		pontuacao_id INTEGER NOT NULL,
		PRIMARY KEY(id)
	);
	''')

conexao.commit()

