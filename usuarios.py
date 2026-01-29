from dataclasses import dataclass, asdict
import json
import os

# ===== USUARIO =====
@dataclass
class usuario:
    nome: str
    telefone: str
    cpf_cnpj: str
    email: str = ''

    def to_dict(self):
        return asdict(self)

# ===== DADOS =====
DATA_FILE = "cadastro_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"usuario": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===== FUNÇÕES =====
def cadastrar_usuario():
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    cpf_cnpj = input("CPF/CNPJ: ")
    email = input("Email (opcional): ")

    usuario = usuario(nome, telefone, cpf_cnpj, email)
    data = load_data()
    data["usuario"].append(usuario.to_dict())
    save_data(data)
    print("usuario cadastrado!\n")

def mostrar_usuario():
    data = load_data()
    if not data["usuario"]:
        print("Nenhum usuario cadastrado.\n")
        return
    print("\n--- usuario ---")
    for c in data["usuario"]:
        print(c)
    print()

# ===== MENU =====
while True:
    print("1 - Cadastrar usuario")
    print("2 - Visualizar usuario")
    print("0 - Sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        cadastrar_usuario()
    elif opcao == "2":
        mostrar_usuario()
    elif opcao == "0":
        print("Encerrando...")
        break
    else:
        print("Opção inválida\n")
