import sqlite3
import profatividades

# --- 1. Camada de Dados ---
class Database:
    def __init__(self, db_name="qualifica.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                endereco TEXT NOT NULL
            );
        ''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

# --- 2. Camada de Modelo ---
class Usuario:
    def __init__(self, nome, senha, tipo, email=None, cpf=None, endereco=None):
        self.nome = nome
        self.senha = senha
        self.tipo = tipo
        self.email = email
        self.cpf = cpf 
        self.endereco = endereco

    def login(self):
        db = Database()
        db.cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=? AND tipo=?", 
                         (self.nome, self.senha, self.tipo))
        user = db.cursor.fetchone()
        db.close_connection()
        
        if user:
            return True
        else:
            return False

    def cadastrar(self):
        db = Database()
        
        db.cursor.execute("SELECT id FROM usuarios WHERE nome=? OR email=? OR cpf=?", 
                         (self.nome, self.email, self.cpf))
        
        usuario_existente = db.cursor.fetchone()

        if usuario_existente:
            print(f"\n[ERRO] O usuário, e-mail ou CPF já está em uso.")
            db.close_connection()
            return False
        else:
            db.cursor.execute("""
                INSERT INTO usuarios (nome, senha, tipo, email, cpf, endereco) 
                VALUES (?, ?, ?, ?, ?, ?)""", 
                (self.nome, self.senha, self.tipo, self.email, self.cpf, self.endereco))
            
            db.conn.commit()
            print(f"\n[SUCESSO] Conta de {self.tipo} '{self.nome}' criada!")
            db.close_connection()
            return True

# --- 3. Telas e Navegação ---
def menu_aluno(nome):
    print(f"\n>>> PAINEL DO ALUNO: {nome}")
    input("Pressione Enter para sair.")

def menu_professor(nome):
    print(f"\n>>> PAINEL DO PROFESSOR: {nome}")
    print("[ 1 ] -->  Curso")
    print("[ 2 ] -->  Módulo")
    print("[ 3 ] -->  Atividade")
    print("[ 4 ] --> sair")
    selecao=int(input("Selecione uma opção: "))
    while True:
        match selecao:
            case 1:
                profatividades.menu_curso()
            case 2:
                profatividades.menu_modulo()
            case 3:
                profatividades.menu_atividade()
            case 4:
                print("Fechando programa...")
                profatividades.fechar_conexao()
                break
            case _:
                print("[!] Opção inválida.")

def menu_coordenador(nome):
    print(f"\n>>> PAINEL DO COORDENADOR: {nome}")
    input("Pressione Enter para sair.")

def tela_cadastro():
    print("\n--- CRIAR NOVA CONTA ---")
    nome = input("Usuário: ")
    senha = input("Senha: ")
    email = input("Email: ")
    cpf = int(input("CPF: "))
    endereco = input("Endereço: ")
    
    print("Tipo: 1. Aluno | 2. Professor | 3. Coordenador")
    tipo_op = input("Opção: ")
    
    mapa = {"1": "Aluno", "2": "Professor", "3": "Coordenador"}
    tipo = mapa.get(tipo_op)
    
    if tipo:
        novo_user = Usuario(nome, senha, tipo, email, cpf, endereco)
        novo_user.cadastrar()
    else:
        print("[!] Tipo inválido.")

def tela_login(tipo_perfil):
    print(f"\n--- LOGIN: {tipo_perfil} ---")
    nome = input("Usuário: ")
    senha = input("Senha: ")
    
    user = Usuario(nome, senha, tipo_perfil)
    if user.login():
        print(f"\nBem-vindo, {nome}!")
        if tipo_perfil == "Aluno":
            menu_aluno(nome)
        elif tipo_perfil == "Professor":
            menu_professor(nome)
        elif tipo_perfil == "Coordenador":
            menu_coordenador(nome)
    else:
        print("[!] Dados incorretos para este perfil.")

def menu_principal():
    # Inicializa o banco antes de começar
    db_inicial = Database()
    db_inicial.close_connection()

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