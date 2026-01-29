import sqlite3

conexao=sqlite3.connect('sistema.db')
cursor=conexao.cursor()
# criar tabela
cursor.execute('''
    CREATE TABLE IF NOT EXISTS opcoes(
        id_opcoes INTEGER NOT NULL UNIQUE,
        opcao_a VARCHAR(200) NOT NULL,
        opcao_b VARCHAR(200) NOT NULL,
        opcao_c VARCHAR(200) NOT NULL,
        opcao_d VARCHAR(200) NOT NULL,
        FOREING KEY (id_opcoes) REFERENCES atividades(id)
    );
               
    CREATE TABLE IF NOT EXISTS cursos(
        id_curso INTEGER NOT NULL UNIQUE,
        nome_completo TEXT NOT NULL,
        PRIMARY KEY("id_curso", "nome_completo")
    );
               
    CREATE TABLE IF NOT EXISTS atividades(
		id INTEGER NOT NULL UNIQUE,
		curso_id INTEGER,
		tipo TEXT,
		perguntas TEXT,
		opcoes INTEGER,
		resposta_correta TEXT,
		dica TEXT,
		pontuacoes INTEGER,
		PRIMARY KEY("id"),
        FOREING KEY (id) REFERENCES cursos(id_cursos)
	);
    '''); #a tabela 'atividades' e 'cursos' já existe, somente alterar umas coisas (opcoes)
conexao.commit()
# atividades
def multipla_escolha(): #OK
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    id_atividade=int("Digite o identificador (ID) da atividade: ")
    questão=input("Digite o enunciado da atividade: ")
    resposta_correta=input("Digite a resposta correta: ")
    opcao_a=input("Digite a primeira opção: ")
    opcao_b=input("Digite a segunda opção: ")
    opcao_c=input("Digite a terceira opção: ")
    opcao_d=input("Digite a quarta opção: ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?)''', (id_curso, questão, resposta_correta, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_opcoes, opcao_a, opcao_b, opcao_c, opcao_d) VALUES (?, ?, ?, ?, ?)''', (id_atividade, opcao_a, opcao_b, opcao_c, opcao_d))
    print("Atividade de Múltipla Escolha adicionada com sucesso!")
    conexao.commit()
def verdadeiro_falso(): #OK
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    id_atividade=int("Digite o identificador (ID) da atividade: ")
    questão=input("Digite o enunciado da atividade: ")
    alternativa_a=input("Digite a primeira opção: ")
    alternativa_b=input("Digite a segunda opção: ")
    alternativa_c=input("Digite a terceira opção: ")
    alternativa_d=input("Digite a quarta opção: ")
    resposta_correta=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, resposta_correta, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_opcoes, opcao_a, opcao_b, opcao_c, opcao_d) VALUES (?, ?, ?, ?, ?)''', (id_atividade, alternativa_a, alternativa_b, alternativa_c, alternativa_d))
    print("Atividade de Verdadeiro e Falso adicionada com sucesso!")
    conexao.commit()
def preencher_lacunas(): #OK
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    questão=input("Digite o enunciado da atividade: ")
    resposta_correta=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, resposta_correta, dica, pontuacao))
    print("Atividade de Preencher Lacunas adicionada com sucesso!")
    conexao.commit()
def ordenar_etapas(): # COLOCAR A TABELA 'opcoes'
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    questão=input("Digite o enunciado da atividade: ")
    
    resposta_correta=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, resposta_correta, dica, pontuacao))
    print("Atividade de Ordenar Etapas adicionada com sucesso")
    conexao.commit()
def sequencia_logica(): # COLOCAR A TABELA 'opcoes'
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    questão=input("Digite o enunciado da atividade: ")
    
    resposta_correta=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, resposta_correta, dica, pontuacao))
    print("Atividade de Sequência Lógica adicionada com sucesso!")
    conexao.commit()