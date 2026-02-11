
import sqlite3
import usuario
conexao = sqlite3.connect('trabalho_final.db')
cursor = conexao.cursor()

#Geral 
def cadastrar_usuario():
    nome_completo= input("Nome Completo: ")
    email= input("Seu email: ") #armazenar no banco de dados
    data_nascimento= input("Data de Nascimento: ") #armazenar no banco de dados
    cpf= input("CPF: ") #armazenar no banco de dados
    telefone= input("Telefone: ") #armazenar no banco de dados
    print("Tipo de usuário: 1. Aluno | 2. Professor | 3. Coordenador")
    resposta= int(input("Escolha uma opção: ")) #armazenar no banco de dados / front end (fazer botão de seleção)
    while resposta not in (1, 2, 3):
        print("Opção inválida. Tente novamente!")
        resposta = int(input("Escolha uma opção: "))
    if resposta == 1:
        tipo_usuario = "ALUNO"
    elif resposta == 2:
        tipo_usuario = "PROFESSOR"
    else:
        tipo_usuario = "COORDENADOR"
    senha= input("Escolha uma senha: ") #armazenar no banco de dados
    print(f"Seja bem-vindo(a) {nome_completo},  à plataforma!") #informativo do front en

    cursor.execute("""
    INSERT INTO usuario 
    (nome_completo, email, data_nascimento, cpf, telefone, tipo_usuario, senha)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (nome_completo, email, data_nascimento, cpf, telefone,tipo_usuario,senha))
    conexao.commit()

def login_existe(login):
    cursor.execute("SELECT 1 FROM usuario WHERE email = ?", (login,))
    resultado = cursor.fetchone()
    return resultado is not None

def login_usuario():
    
    email = input("Email: ")

    if not login_existe(email):
        print("Email não cadastrado.")
        cadastrar_usuario()
        return None

    _, tipo_usuario = tentativa_login(email)
    return tipo_usuario

def tentativa_login(login):
    tentativa_senha = input("Digite sua senha: ")
    cursor.execute(
        "SELECT senha, nome_completo, tipo_usuario FROM usuario WHERE email = ?",
        (login,)
    )
    resultado = cursor.fetchone()
    if resultado is None:
        print("Usuário não encontrado.")
        return None, None

    senha, nome_completo, tipo_usuario = resultado

    tentativas = 3
    while tentativa_senha != senha and tentativas > 1:
        tentativas -= 1
        print(f"Acesso negado. Por favor, tente novamente!")
        print(f"Tentativas restantes: {tentativas}")
        tentativa_senha = input("Digite sua senha: ")

    if tentativa_senha != senha:
        print("Número máximo de tentativas atingido. Acesso bloqueado!")
        return None, None

    print(f"Acesso permitido, seja bem-vindo {nome_completo}! Seu perfil é do tipo: {tipo_usuario}")
    return senha, tipo_usuario

def menu_repeticao(tipo_usuario):
    while True:
        print("Deseja fazer algo a mais?")
        print("1- SIM")
        print("2- NÃO")
        decisao = int(input("Sua escolha: "))

        if decisao == 1:
            if tipo_usuario == "ALUNO":
                menu_aluno()
            elif tipo_usuario == "PROFESSOR":
                menu_professor()
            elif tipo_usuario == "COORDENADOR":
                menu_coordenador()
        else:
            print("Encerrando programa...")
            break

    pass


menu()conexao.close()

