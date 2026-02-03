import sqlite3
import sys

# --- Classes de Banco de Dados e Usuários ---

class Database:
    """Gerencia a conexão e criação de tabelas no banco de dados SQLite."""
    def __init__(self, db_name="qualifica.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Tabela de usuários conforme especificado no PDF
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL
            );
        """)
        # Adicione outras tabelas aqui (cursos, atividades, progresso, etc.)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

class Usuario:
    """Classe base para gerenciar usuários."""
    def __init__(self, nome, senha, tipo):
        self.nome = nome
        self.senha = senha
        self.tipo = tipo

    def login(self):
        db = Database()
        # Consulta para verificar o usuário
        db.cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=? AND tipo=?", (self.nome, self.senha, self.tipo))
        user = db.cursor.fetchone()
        db.close_connection()
        return user is not None

    def cadastrar(self):
        db = Database()
        try:
            db.cursor.execute("INSERT INTO usuarios (nome, senha, tipo) VALUES (?, ?, ?)", (self.nome, self.senha, self.tipo))
            db.conn.commit()
            print(f"Usuário {self.nome} ({self.tipo}) cadastrado com sucesso!")
        except sqlite3.IntegrityError:
            print("Erro: Usuário já existe.")
        finally:
            db.close_connection()

# Classes filhas específicas
class Aluno(Usuario):
    def __init__(self, nome, senha):
        super().__init__(nome, senha, "Aluno")
    # Adicione métodos específicos do aluno aqui

class Professor(Usuario):
    def __init__(self, nome, senha):
        super().__init__(nome, senha, "Professor")
    # Adicione métodos específicos do professor aqui

class Coordenador(Usuario):
    def __init__(self, nome, senha):
        super().__init__(nome, senha, "Coordenador")
    # Adicione métodos específicos do coordenador aqui

# --- Funções do Menu ---

def menu_aluno_view(nome_usuario):
    """Menu exclusivo para alunos."""
    while True:
        print(f"\n### Menu do Aluno - {nome_usuario} ###")
        print("1. Ver cursos disponíveis")
        print("2. Fazer atividades")
        print("3. Ver progresso")
        print("4. Sair")
        
        escolha = input("Escolha uma opção: ")
        if escolha == "4":
            break
        else:
            print("Funcionalidade ainda não implementada.")

def login_handler(tipo_usuario):
    """Função genérica para gerenciar o login."""
    nome = input(f"Nome do {tipo_usuario}: ")
    senha = input("Senha: ")
    
    usuario = None
    if tipo_usuario == "Aluno":
        usuario = Aluno(nome, senha)
    elif tipo_usuario == "Professor":
        usuario = Professor(nome, senha)
    elif tipo_usuario == "Coordenador":
        usuario = Coordenador(nome, senha)

    if usuario and usuario.login():
        print(f"Bem-vindo(a), {tipo_usuario} {nome}!")
        if tipo_usuario == "Aluno":
            menu_aluno_view(nome) # Redireciona para o menu específico
        # Adicionar redirecionamentos para Professor e Coordenador aqui
    else:
        # Se o login falhar, o sistema pode perguntar se deseja cadastrar
        print("Login falhou. Você precisa se cadastrar primeiro.")
        # Lógica de cadastro pode ser adicionada aqui.

def menu_principal():
    """Menu principal de navegação."""
    while True:
        print("\n### Menu Principal Qualifica ###")
        print("1. Login como Aluno")
        print("2. Login como Professor")
        print("3. Login como Coordenador")
        print("4. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            login_handler("Aluno")
        elif escolha == "2":
            login_handler("Professor")
        elif escolha == "3":
            login_handler("Coordenador")
        elif escolha == "4":
            print("Saindo...")
            sys.exit()
        else:
            print("Opção inválida.")

# --- Execução Principal ---
if __name__ == "__main__":
    # Garante que o banco e tabelas existam ao iniciar
    db_setup = Database()
    db_setup.close_connection()
    print("Sistema iniciado. Banco de dados pronto.")
    
    menu_principal()

