#Tabela temporaria 
import sqlite3
conexao=sqlite3.connect('sistema.db')
cursor=conexao.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS opcoes(
        id_opcoes INTEGER PRIMARY KEY UNIQUE,
        opcao_a TEXT NOT NULL,
        opcao_b TEXT NOT NULL,
        opcao_c TEXT NOT NULL,
        opcao_d TEXT NOT NULL,
        opcao_e TEXT NOT NULL,
        FOREING KEY (id_opcoes) REFERENCES atividades(id)
    );
    CREATE TABLE IF NOT EXISTS alunos(
        id_aluno INTEGER PRIMARY KEY UNIQUE AUTOINCREMENT,
        pontuacao INT
    )
    ''')

#o Correspondência (ligar colunas) 
def correspondecia (): 
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    questao=input("Digite o enunciado da atividade: ")
    pares = input("Digite os pares (ex: A-1; B-2; C-3)")
    resposta_correta= pares  
    dica=input("Digite a dica: ")
    pontuacao = 1 
    cursor.execute('''INSET INTO atividades(cursor_id, questao, pares, resposta_correta, dica, pontuacao) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questao, resposta_correta, dica, pontuacao))
    cursor.execute('''INSET INTO opcoes(pares) VALUES (?)''')
    conexao.commit()

# o Classificação (separar categorias)
def classificacao (): 
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    questao=input("Digite o enunciado da atividade: ")
    categorias = input("Digite categorias e itens (ex: Inteiro = 11 ,256 ; Racionais : 3.78 , 4/2 ;)")
    resposta_correta = categorias
    dica = input("Digite a dica: ")
    pontuacao= 1 
    cursor.execute('''INSET INTO atividades(cursor_id, questao, opcoes, categorias , resposta_correta, dica, pontuacao) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questao,resposta_correta, dica, pontuacao))
    conexao.commit()

#o Escolha múltipla (várias corretas)
def escolha_multipla():
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    questão=input("Digite o enunciado da atividade: ")
    opcao_a = input("Digite a 'A' opção : ")
    opcao_b = input("Digite a 'B' opção : ")
    opcao_c = input("Digite a 'C' opção : ")
    opcao_d = input("Digite a 'D' opção : ")
    opcao_e = input("Digite a 'E' opção : ")
    resposta_correta=input("Digite as alternativas certas (ex: A,C) : ")
    dica=input("Digite a dica: ")
    pontuacao= 1 
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, resposta_correta, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e) VALUES (?, ?, ?, ?, ?, ?)''', ( opcao_a, opcao_b, opcao_c, opcao_d, opcao_e)) 
    conexao.commit()

#o Palavra embaralhada
def palavra_embralhada():
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    palavra = input("Digite a palvara correrta : ")
    embralhada = input("Digite a palavra embralhada : ")
    perguntas = f"Desembralhe a palavra {embralhada}: "
    dica=input("Digite a dica: ")
    pontuacao = 1 
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso,perguntas, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(palavra,embralhada,) VALUES (?,?)''' , (palavra,embralhada))
    conexao.commit()

#o Mini-cenários com decisões
def mini_cenarios():
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    cenario=input("Digite o cénario : ")
    decisoes = input("Digite as decisões que o aluno pode tomar : ")
    resposta_correta=input("Digite a decisão certa : ")
    dica=input("Digite a dica: ")
    pontuacao = 1
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, cenario, decisoes, resposta_correta, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(cenario,decisoes) VALUES (?,?)''' , (cenario,decisoes))
    conexao.commit()