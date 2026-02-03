import sqlite3
conexao=sqlite3.connect('sistema.db')
cursor=conexao.cursor()
# criar tabela
cursor.execute('''
    CREATE TABLE IF NOT EXISTS opcoes(
<<<<<<< Updated upstream
        id_opcoes INTEGER PRIMARY KEY UNIQUE,
=======
        id INTEGER PRIMARY KEY UNIQUE,
        id_atividade INT NOT NULL,
>>>>>>> Stashed changes
        opcao_a TEXT NOT NULL,
        opcao_b TEXT NOT NULL,
        opcao_c TEXT NOT NULL,
        opcao_d TEXT NOT NULL,
        opcao_e TEXT NOT NULL,
<<<<<<< Updated upstream
        FOREING KEY (id_opcoes) REFERENCES atividades(id)
    );
    CREATE TABLE IF NOT EXISTS alunos(
        id_aluno INTEGER PRIMARY KEY UNIQUE AUTOINCREMENT,
        pontuacao INT
    )
    ''')
conexao.commit()
=======
        FOREING KEY (id_atividade) REFERENCES atividades(id)
    );
    ''')
conexao.commit()
conexao.close()
>>>>>>> Stashed changes
# atividades
def multipla_escolha(): #OK
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    numero_atividade=int("Digite o número da atividade: ")
    questão=input("Digite o enunciado da atividade: ")
    opcao_a=input("Digite a opção 'A': ")
    opcao_b=input("Digite a opção 'B': ")
    opcao_c=input("Digite a opção 'C': ")
    opcao_d=input("Digite a opção 'D': ")
    opcao_e=input("Digite a opção 'E': ")
<<<<<<< Updated upstream
    resposta_correta=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSERT INTO atividades(cursor_id, perguntas, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?)''', (id_curso, questão, resposta_correta, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_opcoes, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e) VALUES (?, ?, ?, ?, ?, ?)''', (numero_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e))
    print("Atividade de Múltipla Escolha adicionada com sucesso!")
    conexao.commit()
=======
    respostas=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSERT INTO atividades(cursos_id, perguntas, respostas, dica, pontuacoes) VALUES (?, ?, ?, ?, ?)''', (id_curso, questão, respostas, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e) VALUES (?, ?, ?, ?, ?, ?)''', (numero_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e))
    print("Atividade de Múltipla Escolha adicionada com sucesso!")
    conexao.commit()
    conexao.close()
>>>>>>> Stashed changes
def verdadeiro_falso(): #OK
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    numero_atividade=int("Digite o número da atividade: ")
    questão=input("Digite o enunciado da atividade: ")
    alternativa_a=input("Digite a opção 'A': ")
    alternativa_b=input("Digite a opção 'B': ")
    alternativa_c=input("Digite a opção 'C': ")
    alternativa_d=input("Digite a opção 'D': ")
    alternativa_e=input("Digite a opção 'E': ")
<<<<<<< Updated upstream
    resposta_correta=input("Digite a resposta correta (ex: A(V), B(F)): ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSERT INTO atividades(cursor_id, perguntas, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?)''', (id_curso, questão, resposta_correta, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_opcoes, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e) VALUES (?, ?, ?, ?, ?, ?)''', (numero_atividade, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e))
    print("Atividade de Verdadeiro e Falso adicionada com sucesso!")
    conexao.commit()
=======
    respostas=input("Digite a resposta correta (ex: A(V), B(F)): ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSERT INTO atividades(cursos_id, perguntas, respostas, dica, pontuacoes) VALUES (?, ?, ?, ?, ?)''', (id_curso, questão, respostas, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e) VALUES (?, ?, ?, ?, ?, ?)''', (numero_atividade, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e))
    print("Atividade de Verdadeiro e Falso adicionada com sucesso!")
    conexao.commit()
    conexao.close()
>>>>>>> Stashed changes
def preencher_lacunas(): #OK
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    numero_atividade=int("Digite o número da atividade: ")
    questão=input("Digite o enunciado da atividade: ")
    opcao_a=input("Digite a opção 'A': ")
    opcao_b=input("Digite a opção 'B': ")
    opcao_c=input("Digite a opção 'C': ")
    opcao_d=input("Digite a opção 'D': ")
    opcao_e=input("Digite a opção 'E': ")
<<<<<<< Updated upstream
    resposta_correta=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSERT INTO atividades(cursor_id, perguntas, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?)''', (id_curso, questão, resposta_correta, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_opcoes, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e) VALUES (?, ?, ?, ?, ?, ?)''', (numero_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e))
    print("Atividade de Preencher Lacunas adicionada com sucesso!")
    conexao.commit()
=======
    respostas=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSERT INTO atividades(cursos_id, perguntas, respostas, dica, pontuacoes) VALUES (?, ?, ?, ?, ?)''', (id_curso, questão, respostas, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e) VALUES (?, ?, ?, ?, ?, ?)''', (numero_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e))
    print("Atividade de Preencher Lacunas adicionada com sucesso!")
    conexao.commit()
    conexao.close()
>>>>>>> Stashed changes
def ordenar_etapas(): # OK
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    numero_atividade=int("Digite o número da atividade: ")
    questão=input("Digite o enunciado da atividade: ")
    etapa_a=input("Digite a etapa: ")
    etapa_b=input("Digite a etapa: ")
    etapa_c=input("Digite a etapa: ")
    etapa_d=input("Digite a etapa: ")
    etapa_e=input("Digite a etapa: ")
<<<<<<< Updated upstream
    resposta_correta=input("Digite a resposta correta (ex: A(1), B(2)): ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSERT INTO atividades(cursor_id, perguntas, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?)''', (id_curso, questão, resposta_correta, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_opcoes, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e) VALUES (?, ?, ?, ?, ?, ?)''', (numero_atividade, etapa_a, etapa_b, etapa_c, etapa_d, etapa_e))
    print("Atividade de Ordenar Etapas adicionada com sucesso")
    conexao.commit()
def sequencia_logica(): # COLOCAR A TABELA 'opcoes'
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    questão=input("Digite o enunciado da atividade: ")
    resposta_correta=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSERT INTO atividades(cursor_id, perguntas, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?)''', (id_curso, questão, resposta_correta, dica, pontuacao))
    print("Atividade de Sequência Lógica adicionada com sucesso!")
    conexao.commit()
=======
    respostas=input("Digite a resposta correta (ex: A(1), B(2)): ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSERT INTO atividades(cursos_id, perguntas, respostas, dica, pontuacoes) VALUES (?, ?, ?, ?, ?)''', (id_curso, questão, respostas, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e) VALUES (?, ?, ?, ?, ?, ?)''', (numero_atividade, etapa_a, etapa_b, etapa_c, etapa_d, etapa_e))
    print("Atividade de Ordenar Etapas adicionada com sucesso")
    conexao.commit()
    conexao.close()
def sequencia_logica(): # COLOCAR A TABELA 'opcoes'
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    questão=input("Digite o enunciado da atividade: ")
    respostas=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=1
    cursor.execute('''INSERT INTO atividades(cursos_id, perguntas, respostas, dica, pontuacoes) VALUES (?, ?, ?, ?, ?)''', (id_curso, questão, respostas, dica, pontuacao))
    print("Atividade de Sequência Lógica adicionada com sucesso!")
    conexao.commit()
    conexao.close()
>>>>>>> Stashed changes
def estrela(): # tabela de usuário (tipo aluno) necessária para receber
    cursor.execute('''INSERT INTO aluno(pontuacao) VALUES (?)''', (1))