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


cursor.execute('''
   CREATE TABLE IF NOT EXISTS modulos(
       id_modulo TEXT NOT NULL,
       nome_modulo TEXT NOT NULL 
   ); 
    CREATE TABLE IF NOT EXISTS cursos (
        id_curso TEXT NOT NULL,
        nome_curso TEXT NOT NULL     
    )
''')

#o Correspondência (ligar colunas) 
def correspondecia (): 
    
    perguntas=input("Digite o enunciado da atividade: ")
    coluna_1=input("Digite a primeira coluna: ")
    coluna_2=input("Digite a segunda coluna: ")
    pares = input("Digite os pares das colunas(ex: A-1; B-2; C-3): ")
    respostas= pares  
    dica=input("Digite a dica: ")
    pontuacao = 1 
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, pares, respostas, dica, pontuacao) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, perguntas, respostas, dica, pontuacao))
    cursor.execute('''INSET INTO opcoes(pares) VALUES (?)''')
    conexao.commit()

# o Classificação (separar categorias)
def classificacao (): 
    
    perguntas=input("Digite o enunciado da atividade: ")
    categorias = input("Digite categorias : (Inteiro, Racionais ) : e itens (ex: Inteiro = 11 ,256 ; Racionais : 3.78 , 4/2 ;)")
    itens=input("Digite os itens para relacionar (Ex: 4 , 45 , 3.4) : ")
    respostas = itens
    dica = input("Digite a dica: ")
    pontuacao= 1 
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, categorias , respostas, dica, pontuacao) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso,perguntas,respostas, dica, pontuacao))
    conexao.commit()

#o Escolha múltipla (várias corretas)
def escolha_multipla():
    
    questão=input("Digite o enunciado da atividade: ")
    opcao_a = input("Digite a 'A' opção : ")
    opcao_b = input("Digite a 'B' opção : ")
    opcao_c = input("Digite a 'C' opção : ")
    opcao_d = input("Digite a 'D' opção : ")
    opcao_e = input("Digite a 'E' opção : ")
    respostas=input("Digite as alternativas certas (ex: A,C) : ")
    dica=input("Digite a dica: ")
    pontuacao= 1 
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, respostas, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, respostas, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(id_atividade, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e) VALUES (?, ?, ?, ?, ?, ?)''', ( opcao_a, opcao_b, opcao_c, opcao_d, opcao_e)) 
    conexao.commit()

#o Palavra embaralhada
def palavra_embralhada():

    palavra = input("Digite a palvara correrta : ")
    embralhada = input("Digite a palavra embralhada : ")
    perguntas = f"Desembralhe a palavra {embralhada}: "
    dica=input("Digite a dica: ")
    pontuacao = 1 
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso,perguntas, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(palavra,embralhada,) VALUES (?,?)''' , (palavra,embralhada))
    conexao.commit()

#o Mini-cenários com decisões
def mini_cenarios():
    
    cenario=input("Digite o cénario : ")
    decisoes = input("Digite as decisões que o aluno pode tomar : ")
    respostas=input("Digite a decisão certa : ")
    dica=input("Digite a dica: ")
    pontuacao = 1
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, respostas, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, cenario, decisoes, respostas, dica, pontuacao))
    cursor.execute('''INSERT INTO opcoes(cenario,decisoes) VALUES (?,?)''' , (cenario,decisoes))
    conexao.commit()