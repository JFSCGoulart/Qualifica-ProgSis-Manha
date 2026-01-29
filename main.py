#1 cadastro

print("Cadastre-se") #Front-end(criar um botão)
nome= input("Nome Completo: ") #armazenar no banco de dados
data_nascimento= input("Data de Nascimento: ") 
CPF= int(input("CPF: "))
CEP= int(input("CEP: "))
endereco= input("Endereço: ")
telefone= int(input("Telefone: "))
email= input("E-mail: ")
tipo_user= input("Você é ALUNO, PROFESSOR ou COORDENADOR?").upper()
senha= input("Escolha uma senha: ")
#armazenar em TABELA  CADASTRO
#puxar nome do usario

print(f"Seja bem-vindo(a) {nome} a plataforma")#informativo do front end
