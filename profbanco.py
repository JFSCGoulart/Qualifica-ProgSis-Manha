import sqlite3

conexao = sqlite3.connect('sistema.db')
cursor = conexao.cursor()

def criar_tabelas():
    # Tabela de cursos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos(
            id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL
        );
    ''')

    # Tabela de módulos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modulos(
            id_modulo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_curso INTEGER NOT NULL,
            nome_modulo TEXT NOT NULL,
            FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
        );
    ''')

    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            data_nascimento DATE NOT NULL,
            CPF VARCHAR(11) NOT NULL UNIQUE,
            telefone VARCHAR(11) NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            id_tipo_usuario VARCHAR NOT NULL,
            senha TEXT NOT NULL,   
            tipo TEXT NOT NULL CHECK (tipo IN ('aluno', 'professor', 'coordenador'))
        );
    ''')

    # Tabela de atividades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atividades(
            id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
            id_modulo INTEGER NOT NULL,
            id_curso INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            pergunta TEXT NOT NULL,
            opcao_a TEXT,
            opcao_b TEXT,
            opcao_c TEXT,
            opcao_d TEXT,
            coluna_1 TEXT,
            coluna_2 TEXT,
            pares TEXT,
            categoria TEXT,
            embaralhada TEXT,
            cenario TEXT,
            resposta TEXT NOT NULL,
            dica TEXT NOT NULL,
            FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
            FOREIGN KEY (id_modulo) REFERENCES modulos(id_modulo)
        );
    ''')
    
    # Tabela de progresso
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progresso(
            id_progresso INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_atividade INTEGER NOT NULL,
            acertou INTEGER NOT NULL CHECK (acertou IN (0, 1)),
            data_execucao TEXT NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
            FOREIGN KEY (id_atividade) REFERENCES atividades(id_atividade)
        );
    ''')

    # Tabela de estrelas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estrelas(
            id_usuario INTEGER PRIMARY KEY,
            total_estrelas INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        );
    ''')
    conexao.commit()
    conexao.close()    