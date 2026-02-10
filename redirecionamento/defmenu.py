import sqlite3
import hashlib
import os

conn = sqlite3.connect(' qualifica_redirecionamento.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('aluno', 'professor', 'coordenador')),
    email TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    materia TEXT,
    data_entrega DATE,
    pontos INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pendente',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES usuarios(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL,
    professor_id INTEGER,
    FOREIGN KEY (professor_id) REFERENCES usuarios(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ranking (
    aluno_id INTEGER PRIMARY KEY,
    total_pontos INTEGER DEFAULT 0,
    posicao INTEGER,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES usuarios(id)
)
''')

conn.commit()
def menu_principal():
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo = 'coordenador'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
        INSERT INTO usuarios (nome, usuario, senha, tipo, email)
        VALUES (?, ?, ?, 'coordenador', ?)
        ''', ('Administrador', 'admin', hash_senha('admin123'), 'admin@escola.com'))
        conn.commit()
        print("\nUsuário administrador padrão criado!")
        print("Usuário: admin")
        print("Senha: admin123")
        print("Use este usuário para criar outros coordenadores.")
    
    while True:
        print("\n" + "="*50)
        print("| qualifica/DF/ - /menu / |")
        print("="*50)
        print("1. Login")
        print("2. Cadastrar Aluno")
        print("3. Cadastrar Professor")
        print("4. Cadastrar Coordenador")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            usuario = fazer_login()
            if usuario:
                if usuario['tipo'] == 'aluno':
                    menu_aluno(usuario)
                elif usuario['tipo'] == 'professor':
                    menu_professor(usuario)
                elif usuario['tipo'] == 'coordenador':
                    menu_coordenador(usuario)
        
        elif opcao == "2":
            cadastrar_aluno()
            
        elif opcao == "3":
            cadastrar_professor()
            
        elif opcao == "4":
            cadastrar_coordenador()
            
        elif opcao == "0":
            print("\n Saindo do sistema...")
            conn.close()
            break
            
        else:
            print("Opção inválida!")
if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
        conn.close()
    except Exception as e:
        print(f"\nErro no sistema: {e}")
        conn.close()