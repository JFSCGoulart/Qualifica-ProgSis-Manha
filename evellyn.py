import sqlite3

conexao=sqlite3.connect('sistema.db')
cursor=conexao.cursor()

# Alterar tabela 'atividades' para receber opções
cursor.execute('''
    CREATE TABLE IF NOT EXISTS atividades(
        id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
        cursos_id INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        perguntas TEXT NOT NULL,
        opcao_a TEXT NOT NULL,
        opcao_b TEXT NOT NULL,
        opcao_c TEXT NOT NULL,
        opcao_d TEXT NOT NULL,
        opcao_e TEXT NOT NULL,
        resposta TEXT NOT NULL,
        dica TEXT NOT NULL,
        pontuacoes FLOAT NOT NULL
    );
''')
conexao.commit()
conexao.close()

# Atividades
def adicionar_atividades():
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    tipo=input("Digite o tipo de atividade: ")
    questão=input("Digite o enunciado da atividade: ")
    opcao_a=input("Digite a opção 'A': ")
    opcao_b=input("Digite a opção 'B': ")
    opcao_c=input("Digite a opção 'C': ")
    opcao_d=input("Digite a opção 'D': ")
    opcao_e=input("Digite a opção 'E': ")
    resposta=input("Digite a resposta correta (A, B, C, D ou E): ").upper()
    dica=input("Digite a dica: ")
    pontuacao=float(input("Digite o valor total da atividade: "))

    # Inserir a atividade
    cursor.execute('''
        INSERT INTO atividades(cursos_id, tipo, perguntas, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, resposta, dica, pontuacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id_curso, tipo, questão, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, resposta, dica, pontuacao))
        
    conexao.commit()
    conexao.close()
    print(f"Atividade de {tipo} adicionada com sucesso!")