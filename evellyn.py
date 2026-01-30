#• Ao iniciar, o usuário escolhe: "Aluno", "Professor" ou "Coordenador". ✅
#• Depois digita nome e senha.
#• Se for um nome novo, o sistema pergunta o tipo e cadastra. ✅
#• Cada tipo tem acesso a um menu diferente.
def login_usuario():
    pass

import usuarios
import atividades
import progresso

while True:
    print("Bem-vindo(a) ao Progrma do QualificaDF!")
    print("[ 1 ] --> Aluno(a)") # Botão
    print("[ 2 ] --> Professor(a)") # Botão
    print("[ 3 ] --> Coordenador(a)") # Botão
    selecao_tipo=int(input("Selecione uma opção: "))
    match selecao_tipo:
        case 1:
            print("Selecione o tipo de usuário:")
            print("[ 1 ] --> Usuário Existente") # Botão
            print("[ 2 ] --> Usuário Novo") # Botão
            selecao_usuario=int(input("Selecione uma opção: "))
            if selecao_usuario==1:
                pass
            elif selecao_usuario==2:
                cadastrar_usuario() # Parte que Luiz fez/tá fazendo
        case 2:
            print("Selecione o tipo de usuário:")
            print("[ 1 ] --> Usuário Existente") # Botão
            print("[ 2 ] --> Usuário Novo") # Botão
            selecao_usuario=int(input("Selecione uma opção: "))
            if selecao_usuario==1:
                pass
            elif selecao_usuario==2:
                cadastrar_usuario() # Parte que Luiz fez/tá fazendo
        case 3:
            print("Selecione o tipo de usuário:")
            print("[ 1 ] --> Usuário Existente") # Botão
            print("[ 2 ] --> Usuário Novo") # Botão
            selecao_usuario=int(input("Selecione uma opção: "))
            if selecao_usuario==1:
                pass
            elif selecao_usuario==2:
                cadastrar_usuario() # Parte que Luiz fez/tá fazendo
        case _:
            print("Opção inválida. Tente novamente.")