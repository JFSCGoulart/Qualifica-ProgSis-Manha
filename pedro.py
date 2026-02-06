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
        coluna_1 TEXT NOT NULL,
        coluna_2 TEXT NOT NULL,
        pares TEXT NOT NULL,
        categorias TEXT NOT NULL,
        embaralhada TEXT NOT NULL,
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
    
    pergunta=input("Digite o enunciado da atividade: ")
    coluna_1=input("Digite a primeira coluna: ")
    coluna_2=input("Digite a segunda coluna: ")
    pares = input("Digite os pares das colunas(ex: A-1; B-2; C-3): ")
    resposta= pares  
    dica=input("Digite a dica: ")
    cursor.execute('''INSERT INTO atividades(pergunta ,coluna_1, coluna_2, pares, resposta, dica,) VALUES (?, ?, ?, ?, ?, ?)''', (pergunta,coluna_1,coluna_2, resposta, pares, dica,))
    cursor.execute('''INSERT INTO opcoes(pares) VALUES (?)''')
    conexao.commit()

# o Classificação (separar categorias)
def classificacao (): 
    
    perguntas=input("Digite o enunciado da atividade: ")
    categorias = input("Digite categorias : (Inteiro, Racionais ): ")
    itens=input("Digite os itens para relacionar (Ex: 4 , 45 , 3.4) : ")
    resposta = itens
    dica = input("Digite a dica: ")
    cursor.execute('''INSERT INTO atividades( perguntas, categorias,itens, resposta, dica,) VALUES (?, ?, ?, ?, ?)''', (perguntas,categorias,itens,resposta, dica,))
    conexao.commit()

#o Escolha múltipla (várias corretas)
def escolha_multipla():
    
    pergunta=input("Digite o enunciado da atividade: ")
    opcao_a = input("Digite a 'A' opção : ")
    opcao_b = input("Digite a 'B' opção : ")
    opcao_c = input("Digite a 'C' opção : ")
    opcao_d = input("Digite a 'D' opção : ")
    resposta=input("Digite as alternativas certas (ex: A,C) : ")
    dica=input("Digite a dica: ") 
    cursor.execute('''INSERT INTO atividades(pergunta ,resposta ,dica) VALUES (?, ?, ?)''', ( pergunta, resposta, dica, ))
    cursor.execute('''INSERT INTO opcoes(opcao_a, opcao_b, opcao_c, opcao_d) VALUES (?, ?, ?, ?)''', ( opcao_a, opcao_b, opcao_c, opcao_d,)) 
    conexao.commit()

#o Palavra embaralhada
def palavra_embaralhada():

    palavra = input("Digite a palvara correrta : ")
    embaralhada = input("Digite a palavra embaralhada : ")
    perguntas = f"Desembralhe a palavra {embaralhada}: "
    dica=input("Digite a dica: ") 
    cursor.execute('''INSERT INTO atividades( perguntas, opcoes, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (perguntas, dica, ))
    cursor.execute('''INSERT INTO opcoes(palavra,embaralhada,) VALUES (?,?)''' , (palavra,embaralhada))
    conexao.commit()

#o Mini-cenários com decisões
def mini_cenarios():
    
    cenario=input("Digite o cénario : ")
    decisoes = input("Digite as decisões que o aluno pode tomar : ")
    resposta=input("Digite a decisão certa : ")
    dica=input("Digite a dica: ")
    cursor.execute('''INSERT INTO atividades(perguntas, opcoes, resposta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', ( cenario, decisoes, resposta, dica, ))
    cursor.execute('''INSERT INTO opcoes(cenario,decisoes) VALUES (?,?)''' , (cenario,decisoes))
    conexao.commit()