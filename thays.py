import sqlite3
import sys

# --- 1. Camada de Dados (Banco de Dados) ---

class Database:
    def __init__(self, db_name="qualifica.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

# --- 2. Camada de Modelo (Classes de Usuário) ---

class Usuario:
    def __init__(self, nome, senha, tipo):
        self.nome = nome
        self.senha = senha
        self.tipo = tipo

    def login(self):
        db = Database()
        db.cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=? AND tipo=?", 
                         (self.nome, self.senha, self.tipo))
        user = db.cursor.fetchone()
        db.close_connection()
        return user is not None

    def cadastrar(self):
        db = Database()
        try:
            db.cursor.execute("INSERT INTO usuarios (nome, senha, tipo) VALUES (?, ?, ?)", 
                             (self.nome, self.senha, self.tipo))
            db.conn.commit()
            print(f"\n[SUCESSO] Conta de {self.tipo} '{self.nome}' criada!")
            return True
        except sqlite3.IntegrityError:
            print(f"\n[ERRO] O nome '{self.nome}' já está em uso.")
            return False
        finally:
            db.close_connection()

# --- 3. Telas Específicas ---

def menu_aluno(nome):
    print(f"\n>>> PAINEL DO ALUNO: {nome}")
    input("Funcionalidades em breve... Enter para sair.")

def menu_professor(nome):
    print(f"\n>>> PAINEL DO PROFESSOR: {nome}")
    input("Funcionalidades em breve... Enter para sair.")

def menu_coordenador(nome):
    print(f"\n>>> PAINEL DO COORDENADOR: {nome}")
    input("Funcionalidades em breve... Enter para sair.")

# --- 4. Lógica de Navegação ---

def tela_cadastro():
    print("\n--- CRIAR NOVA CONTA ---")
    nome = input("Escolha um nome de usuário: ")
    senha = input("Escolha uma senha: ")
    print("Tipo de conta: 1. Aluno | 2. Professor | 3. Coordenador")
    tipo_op = input("Opção: ")
    
    mapa = {"1": "Aluno", "2": "Professor", "3": "Coordenador"}
    tipo = mapa.get(tipo_op)
    
    if tipo:
        novo_user = Usuario(nome, senha, tipo)
        novo_user.cadastrar()
    else:
        print("[!] Tipo de conta inválido.")

def tela_login(tipo_perfil):
    print(f"\n--- LOGIN: {tipo_perfil} ---")
    nome = input("Usuário: ")
    senha = input("Senha: ")
    
    user = Usuario(nome, senha, tipo_perfil)
    if user.login():
        print(f"Bem-vindo, {nome}!")
        if tipo_perfil == "Aluno": menu_aluno(nome)
        elif tipo_perfil == "Professor": menu_professor(nome)
        elif tipo_perfil == "Coordenador": menu_coordenador(nome)
    else:
        print("[!] Nome ou senha incorretos para este perfil.")

def menu_principal():
    # Garante que o banco de dados exista
    Database().close_connection()

    while True:
        print("\n" + "="*25)
        print("    SISTEMA QUALIFICA")
        print("="*25)
        print("1. Login como Aluno")
        print("2. Login como Professor")
        print("3. Login como Coordenador")
        print("4. CADASTRAR NOVO USUÁRIO")
        print("5. Sair")
        
        escolha = input("\nEscolha uma opção: ")

        if escolha == "1":
            tela_login("Aluno")
        elif escolha == "2":
            tela_login("Professor")
        elif escolha == "3":
            tela_login("Coordenador")
        elif escolha == "4":
            tela_cadastro()
        elif escolha == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()
