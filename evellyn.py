import sqlite3

conexao=sqlite3.connect('sistema.db')
cursor=conexao.cursor()

# Criar tabela para receber opções
cursor.execute('''
    CREATE TABLE IF NOT EXISTS opcoes(
        id INTEGER PRIMARY KEY UNIQUE,
        id_atividade INT NOT NULL,
        opcao_a TEXT NOT NULL,
        opcao_b TEXT NOT NULL,
        opcao_c TEXT NOT NULL,
        opcao_d TEXT NOT NULL,
        opcao_e TEXT NOT NULL,
        FOREIGN KEY (id_atividade) REFERENCES atividades(id)
    );
''')
conexao.commit()
conexao.close()

# Atividades de múltipla escolha
def multipla_escolha():
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    numero_atividade=int(input("Digite o número da atividade: "))
    questão=input("Digite o enunciado da atividade: ")
    opcao_a=input("Digite a opção 'A': ")
    opcao_b=input("Digite a opção 'B': ")
    opcao_c=input("Digite a opção 'C': ")
    opcao_d=input("Digite a opção 'D': ")
    opcao_e=input("Digite a opção 'E': ")
    resposta=input("Digite a resposta correta (A, B, C, D ou E): ").upper()
    dica=input("Digite a dica: ")
    pontuacao=float(input("Digite o valor total da atividade: "))
    tipo="Múltipla Escolha"

    # Inserir a atividade
    cursor.execute('''
        INSERT INTO atividades(cursos_id, tipo, perguntas, respostas, dica, pontuacoes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_curso, tipo, questão, resposta, dica, pontuacao))
    
    # inserir as opções
    cursor.execute('''
        INSERT INTO opcoes(id_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (numero_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e))
    
    conexao.commit()
    conexao.close()
    print("Atividade de Múltipla Escolha adicionada com sucesso!")

# Atividades de verdadeiro ou falso
def verdadeiro_falso():
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    numero_atividade=int(input("Digite o número da atividade: "))
    questão=input("Digite o enunciado da atividade: ")
    alternativa_a=input("Digite a afirmação 'A': ")
    alternativa_b=input("Digite a afirmação 'B': ")
    alternativa_c=input("Digite a afirmação 'C': ")
    alternativa_d=input("Digite a afirmação 'D': ")
    alternativa_e=input("Digite a afirmação 'E': ")
    respostas=input("Digite a resposta correta (ex: A-V, B-F, C-V, D-V, E-F): ")
    dica=input("Digite a dica: ")
    pontuacao=float(input("Digite o valor total da atividade: "))
    tipo="Verdadeiro ou Falso"

    cursor.execute('''
        INSERT INTO atividades(cursos_id, tipo, perguntas, respostas, dica, pontuacoes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_curso, tipo, questão, respostas, dica, pontuacao))
    
    cursor.execute('''
        INSERT INTO opcoes(id_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (numero_atividade, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e))
    
    conexao.commit()
    conexao.close()
    print("Atividade de Verdadeiro e Falso adicionada com sucesso!")

# Atividades de preencher lacunas
def preencher_lacunas():
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    numero_atividade=int(input("Digite o número da atividade: "))
    questão=input("Digite o enunciado da atividade (use ___ para as lacunas): ")
    opcao_a=input("Digite a opção 'A': ")
    opcao_b=input("Digite a opção 'B': ")
    opcao_c=input("Digite a opção 'C': ")
    opcao_d=input("Digite a opção 'D': ")
    opcao_e=input("Digite a opção 'E': ")
    respostas=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=float(input("Digite o valor total da atividade: "))
    tipo="Preencher Lacunas"

    cursor.execute('''
        INSERT INTO atividades(cursos_id, tipo, perguntas, respostas, dica, pontuacoes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_curso, tipo, questão, respostas, dica, pontuacao))
    
    cursor.execute('''
        INSERT INTO opcoes(id_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (numero_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e))
    
    conexao.commit()
    conexao.close()
    print("Atividade de Preencher Lacunas adicionada com sucesso!")

# Atividades de ordenar etapas
def ordenar_etapas():
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    numero_atividade=int(input("Digite o número da atividade: "))
    questão=input("Digite o enunciado da atividade: ")
    etapa_a=input("Digite a etapa A: ")
    etapa_b=input("Digite a etapa B: ")
    etapa_c=input("Digite a etapa C: ")
    etapa_d=input("Digite a etapa D: ")
    etapa_e=input("Digite a etapa E: ")
    respostas=input("Digite a resposta correta (ex: A-1, B-2, C-3, D-4, E-5): ")
    dica=input("Digite a dica: ")
    pontuacao=float(input("Digite o valor total da atividade: "))
    tipo="Ordenar Etapas"

    cursor.execute('''
        INSERT INTO atividades(cursos_id, tipo, perguntas, respostas, dica, pontuacoes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_curso, tipo, questão, respostas, dica, pontuacao))
    
    cursor.execute('''
        INSERT INTO opcoes(id_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (numero_atividade, etapa_a, etapa_b, etapa_c, etapa_d, etapa_e))
    
    conexao.commit()
    conexao.close()
    print("Atividade de Ordenar Etapas adicionada com sucesso")

# Atividades de sequência lógica
def sequencia_logica(): # OK
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    numero_atividade=int(input("Digite o número da atividade: "))
    questão=input("Digite o enunciado da atividade: ")
    sequencia_a=input("Digite o item A da sequência: ")
    sequencia_b=input("Digite o item B da sequência: ")
    sequencia_c=input("Digite o item C da sequência: ")
    sequencia_d=input("Digite o item D da sequência: ")
    sequencia_e=input("Digite o item E da sequência: ")
    respostas=input("Digite a resposta correta: ")
    dica=input("Digite a dica: ")
    pontuacao=float(input("Digite o valor total da atividade: "))
    tipo="Sequência Lógica"

    cursor.execute('''
        INSERT INTO atividades(cursos_id, tipo, perguntas, respostas, dica, pontuacoes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_curso, questão, respostas, dica, pontuacao))
    
    cursor.execute('''
        INSERT INTO opcoes(id_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (numero_atividade, sequencia_a, sequencia_b, sequencia_c, sequencia_d, sequencia_e))
    
    conexao.commit()
    conexao.close()
    print("Atividade de Sequência Lógica adicionada com sucesso!")
