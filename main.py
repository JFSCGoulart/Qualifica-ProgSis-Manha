#1 cadastro

def cadastrar_usuario():
  print("Cadastre-se") #Front-end(criar um botão)
  nome= input("Nome Completo: ") #armazenar no banco de dados
  data_nascimento= input("Data de Nascimento: ") #armazenar no banco de dados
  CPF= int(input("CPF: ")) #armazenar no banco de dados
  telefone= int(input("Telefone: ")) #armazenar no banco de dados
  id_tipo_usuario= int(input("Escolha uma opção: Aluno(1), Professor(2), Coordenador(3) ")) #armazenar no banco de dados / front end (fazer botão de seleção)
  senha= input("Escolha uma senha: ") #armazenar no banco de dados
  print(f"Seja bem-vindo(a) {nome} a plataforma") #informativo do front end