#• Ao iniciar, o usuário escolhe: "Aluno", "Professor" ou "Coordenador". ✅
#• Depois digita nome e senha.
#• Se for um nome novo, o sistema pergunta o tipo e cadastra. ✅
#• Cada tipo tem acesso a um menu diferente.
def login_usuario():
    pass
def cadastrar_usuario():
    pass

while True:
    print("Bem-vindo(a) ao Programa do QualificaDF!")
    print("[ 1 ] --> Aluno(a)") # Botão
    print("[ 2 ] --> Professor(a)") # Botão
    print("[ 3 ] --> Coordenador(a)") # Botão
    selecao_tipo=int(input("Selecione uma opção: "))
    match selecao_tipo:
        case 1:
            login_usuario()
            if ValueError:
                cadastrar_usuario() # Parte que Luiz fez/tá fazendo
        case 2:
            login_usuario()
            if ValueError:
                cadastrar_usuario() # Parte que Luiz fez/tá fazendo
        case 3:
            login_usuario()
            if ValueError:
                cadastrar_usuario() # Parte que Luiz fez/tá fazendo
        case _:
            print("Opção inválida. Tente novamente.")