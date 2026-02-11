import sqlite3

conexao= sqlite3.connect('trabalho_final.db')
cursor= conexao.cursor()



#----------Menu geral e específico de cada PERFIL

def menu():
    print("Seja bem-vindo!")
    print("Vamos verificar se você tem cadastro...")
    
    
    tipo_usuario = login_usuario()

    if tipo_usuario is None:
        return

    if tipo_usuario == "ALUNO":
        print("-" * 10, "MENU ESTUDANTE", "-" * 10)
        menu_aluno()

    elif tipo_usuario == "PROFESSOR":
        print("Olá professor(a)!")
        menu_professor()

    elif tipo_usuario == "COORDENADOR":
        print("-" * 10, "MENU COORDENADOR", "-" * 10)
        menu_coordenador()

    menu_repeticao(tipo_usuario)

def menu_professor():
    print("-"*10,"MENU PROFESSOR", "-"*10)
    print("1. Adicionar novo curso")
    print("2. Adicionar atividade")
    print("3. Ver lista de cursos") 
    print("4. Ver lista de atividades")
    print("5. Deletar atividade ")
    print("6. Deletar curso")
    print("0. Sair")
    escolha=int(input("Qual sua opção? "))
    match escolha:
        case 1:
            cadastrar_curso()
        case 2:
            cadastrar_atividade()
        case 3:
            ver_cursos()
        case 4:
            ver_atividade()
        case 5: 
            deletar_atividade()
        case 6:
            deletar_curso()
        case 0: 
            print("Encerrando aplicativo...")

def menu_aluno():
    print("-"*10,"MENU ALUNO", "-"*10)
    print("1. Ver lista de cursos")
    print("2.Ver módulo")
    print("3.Ver atividades")
    print("4. Ver estrelas acumuladas")
    print("5. Atividades feitas hoje")
    print("6. Ranking do curso")
    print("0. Sair")
    escolha=int(input("Qual sua opção? "))
    match escolha:
        case 1:
             ver_cursos
        case 2:
            ver_modulos_com_curso
        case 3:
            ver_atividade
        case 4:
            ver_progresso_usuario
        case 5:
            atividades_feitas_hoje
        case 6:
            ver_ranking_top3 
        case 0: 
            print("Encerrando aplicativo...")

def menu_coordenador():
    print("-"*10,"MENU COORDENADOR", "-"*10)
    print("1. Ver ranking completo da turma")
    print("2. Quantidade de tarefas feitas hoje da turma")
    print("3. Desempenho do curso | Aproveitamento ")
    print("0. Sair")
    escolha=int(input("Qual sua opção? "))
    match escolha:
        case 1:
            ver_ranking_completo
        case 2:
            atividades_feitas_hoje
        case 3:
            desempenho_por_curso
        case 0: 
            print("Encerrando aplicativo...")




#''''''''''''''''''''''''''''''''''''''''''FUNÇÃO PARA PROFESSOR ''''''''''''''''''''''''''''''''''

def cadastrar_curso():
    nome_curso = input("Digite o nome do curso que deseja cadastrar: ").upper()
    professor= input("Professor responsavel: ").upper()
    cursor.execute(""" INSERT INTO curso (nome) VALUES (?)""", (nome_curso,))
    conexao.commit()
    print("✅ Curso cadastrado com sucesso.")

def ver_cursos():
    cursor.execute("SELECT nome FROM curso")
    resultados = cursor.fetchall()

    for i, (nome,) in enumerate(resultados, start=1):
        print(f"{i} - {nome}")

def deletar_curso():
    ver_cursos()
    curso_id = int(input("\nID do curso para deletar (0 para cancelar): "))
    
    if curso_id == 0:
        return
    
    cursor.execute("SELECT nome FROM curso WHERE id = ?", (curso_id,))
    resultado = cursor.fetchone()
    
    if not resultado:
        print("❌ Curso não encontrado.")
        return
    
    if input(f"Deletar '{resultado[0]}'? (S/N): ").upper() == 'S':
        cursor.execute("DELETE FROM curso WHERE id = ?", (curso_id,))
        conexao.commit()
        print("✅ Curso deletado.")


