import sqlite3
import sys
import os
import hashlib
import binascii
import getpass
from datetime import datetime

DB_FILENAME = "qualifica.db"
PBKDF2_ITERATIONS = 120_000  # aumenta a segurança; em produção considere bcrypt/argon2


class Database:
    """Gerencia conexão com contexto e operações básicas no DB."""
    def __init__(self, db_name=DB_FILENAME):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

    def create_tables(self):
        # Tabela de usuários: armazenamos hash e salt separadamente
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha_hash TEXT NOT NULL,
            senha_salt TEXT NOT NULL,
            tipo TEXT NOT NULL,
            criado_em TEXT NOT NULL,
            UNIQUE(nome, tipo)
        );
        """)
        # Crie outras tabelas (cursos, atividades, progresso) quando necessário.

    # Operações de alto nível:
    def add_user(self, nome, senha_hash_hex, salt_hex, tipo):
        criado_em = datetime.utcnow().isoformat()
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (nome, senha_hash, senha_salt, tipo, criado_em) VALUES (?, ?, ?, ?, ?)",
                (nome, senha_hash_hex, salt_hex, tipo, criado_em)
            )
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, nome, tipo):
        self.cursor.execute("SELECT * FROM usuarios WHERE nome=? AND tipo=?", (nome, tipo))
        row = self.cursor.fetchone()
        return row


# --- Funções úteis para senha (PBKDF2) ---

def generate_salt(length=16):
    return os.urandom(length)

def hash_password(password: str, salt: bytes, iterations=PBKDF2_ITERATIONS):
    """
    Retorna o hash em bytes. Usamos SHA256 na PBKDF2.
    """
    pwd = password.encode("utf-8")
    dk = hashlib.pbkdf2_hmac("sha256", pwd, salt, iterations)
    return dk

def to_hex(b: bytes) -> str:
    return binascii.hexlify(b).decode("ascii")

def from_hex(h: str) -> bytes:
    return binascii.unhexlify(h.encode("ascii"))


# --- Classes de Usuário ---

class Usuario:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo

    @staticmethod
    def cadastrar(nome: str, senha: str, tipo: str) -> bool:
        salt = generate_salt()
        senha_hash = hash_password(senha, salt)
        salt_hex = to_hex(salt)
        hash_hex = to_hex(senha_hash)

        with Database() as db:
            success = db.add_user(nome, hash_hex, salt_hex, tipo)
            return success

    @staticmethod
    def login(nome: str, senha: str, tipo: str) -> bool:
        with Database() as db:
            row = db.get_user(nome, tipo)
            if not row:
                return False
            stored_hash_hex = row["senha_hash"]
            stored_salt_hex = row["senha_salt"]

            stored_salt = from_hex(stored_salt_hex)
            stored_hash = from_hex(stored_hash_hex)

            attempt_hash = hash_password(senha, stored_salt)

            # Compare byte-by-byte (timing-safe not strictly necessary aqui, mas ok):
            return hashlib.compare_digest(stored_hash, attempt_hash)


class Aluno(Usuario):
    def __init__(self, nome):
        super().__init__(nome, "Aluno")
    # Métodos específicos do Aluno


class Professor(Usuario):
    def __init__(self, nome):
        super().__init__(nome, "Professor")
    # Métodos específicos do Professor


class Coordenador(Usuario):
    def __init__(self, nome):
        super().__init__(nome, "Coordenador")
    # Métodos específicos do Coordenador


# --- Menus e Handlers ---

def menu_aluno_view(nome_usuario):
    """Menu exclusivo para alunos."""
    while True:
        print(f"\n### Menu do Aluno - {nome_usuario} ###")
        print("1. Ver cursos disponíveis")
        print("2. Fazer atividades")
        print("3. Ver progresso")
        print("4. Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "4":
            break
        else:
            print("Funcionalidade ainda não implementada.")


def menu_professor_view(nome_usuario):
    while True:
        print(f"\n### Menu do Professor - {nome_usuario} ###")
        print("1. Criar atividade")
        print("2. Ver turmas")
        print("3. Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "3":
            break
        else:
            print("Funcionalidade ainda não implementada.")


def menu_coordenador_view(nome_usuario):
    while True:
        print(f"\n### Menu do Coordenador - {nome_usuario} ###")
        print("1. Gerenciar cursos")
        print("2. Relatórios")
        print("3. Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "3":
            break
        else:
            print("Funcionalidade ainda não implementada.")


def register_flow(tipo_usuario):
    print(f"\n--- Cadastro ({tipo_usuario}) ---")
    nome = input("Nome: ").strip()
    senha = getpass.getpass("Senha: ")
    senha_confirm = getpass.getpass("Confirme a senha: ")
    if senha != senha_confirm:
        print("As senhas não conferem. Cadastro cancelado.")
        return

    success = Usuario.cadastrar(nome, senha, tipo_usuario)
    if success:
        print(f"Usuário {nome} cadastrado como {tipo_usuario} com sucesso.")
    else:
        print("Erro: já existe um usuário com esse nome e tipo.")


def login_flow(tipo_usuario):
    print(f"\n--- Login ({tipo_usuario}) ---")
    nome = input("Nome: ").strip()
    senha = getpass.getpass("Senha: ")

    ok = Usuario.login(nome, senha, tipo_usuario)
    if ok:
        print(f"Bem-vindo(a), {tipo_usuario} {nome}!")
        if tipo_usuario == "Aluno":
            menu_aluno_view(nome)
        elif tipo_usuario == "Professor":
            menu_professor_view(nome)
        elif tipo_usuario == "Coordenador":
            menu_coordenador_view(nome)
    else:
        print("Login falhou. Usuário ou senha incorretos, ou usuário não cadastrado.")
        # Oferecer cadastro
        escolha = input("Deseja se cadastrar? (s/n): ").strip().lower()
        if escolha == "s":
            register_flow(tipo_usuario)


def menu_principal():
    while True:
        print("\n### Menu Principal Qualifica ###")
        print("1. Login como Aluno")
        print("2. Login como Professor")
        print("3. Login como Coordenador")
        print("4. Cadastrar novo usuário")
        print("5. Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            login_flow("Aluno")
        elif escolha == "2":
            login_flow("Professor")
        elif escolha == "3":
            login_flow("Coordenador")
        elif escolha == "4":
            # pedir qual tipo no cadastro
            tipo = input("Tipo (Aluno/Professor/Coordenador): ").strip().capitalize()
            if tipo in ("Aluno", "Professor", "Coordenador"):
                register_flow(tipo)
            else:
                print("Tipo inválido.")
        elif escolha == "5":
            print("Saindo...")
            sys.exit(0)
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    # Inicializa DB (garante criação de tabelas)
    with Database():
        pass
    print("Sistema iniciado. Banco de dados pronto.")
    menu_principal()
