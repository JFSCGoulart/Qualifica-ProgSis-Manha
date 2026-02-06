import sqlite3

conexao = sqlite3.connect('sistema.db')
cursor = conexao.cursor()

def criar_tabelas():
    # Tabela de cursos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos(
            id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL
        );
    ''')

    # Tabela de módulos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modulos(
            id_modulo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_curso INTEGER NOT NULL,
            nome_modulo TEXT NOT NULL,
            FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
        );
    ''')

    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            data_nascimento DATE NOT NULL,
            CPF INTEGER NOT NULL,
            telefone INTEGER NOT NULL,
            id_tipo_usuario VARCHAR NOT NULL,
            senha TEXT NOT NULL,   
            tipo TEXT NOT NULL CHECK (tipo IN ('aluno', 'professor', 'coordenador'))
        );
    ''')

    # Tabela de atividades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atividades(
            id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
            id_modulo INTEGER NOT NULL,
            id_curso INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            pergunta TEXT NOT NULL,
            opcao_a TEXT NOT NULL,
            opcao_b TEXT NOT NULL,
            opcao_c TEXT NOT NULL,
            opcao_d TEXT NOT NULL,
            resposta TEXT NOT NULL,
            dica TEXT NOT NULL,
            FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
            FOREIGN KEY (id_modulo) REFERENCES modulos(id_modulo)
        );
    ''')
    
    # Tabela de progresso
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progresso(
            id_progresso INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_atividade INTEGER NOT NULL,
            acertou INTEGER NOT NULL CHECK (acertou IN (0, 1)),
            data_execucao TEXT NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
            FOREIGN KEY (id_atividade) REFERENCES atividades(id_atividade)
        );
    ''')

    # Tabela de estrelas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estrelas(
            id_usuario INTEGER PRIMARY KEY,
            total_estrelas INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        );
    ''')
    conexao.commit()
    conexao.close()

# Ver os cursos disponíveis
def ver_cursos():
    cursor.execute("SELECT * FROM cursos")
    cursos=cursor.fetchall()
    for linha in cursos:
        print(linha)

# Criar curso
def criar_curso():
    nome=input("Digite o nome do curso: ")
    descricao=input("Digite a descrição do curso: ")

    cursor.execute('''
        INSERT INTO cursos(nome, descricao)
        VALUES (?, ?)
    ''', (nome, descricao))
    conexao.commit()
    conexao.close()

# Exluir cursos
def excluir_curso():
    ver_cursos()
    excluir=int(input("Digite o nº da questão a ser excluida: "))
    cursor.execute("DELETE FROM cursos WHERE id=?", (excluir))
    conexao.commit()
    print("Curso excluída com sucesso.")

# Editar cursos
def editar_curso():
    ver_cursos()
    tipo_alterar=input("Digite o que deseja alterar: ")
    indice_alterar=int(input("Digite o indíce onde a alteração deve ocorrer alteração: "))-1
    alteracao=input("Digite a alteração da questão: ")
    cursor.execute("UPDATE cursos SET ? WHERE ?=?", (alteracao, tipo_alterar, indice_alterar))

# Ver os módulos disponíveis
def ver_modulos(curso_selecionado,):
    cursor.execute("SELECT * FROM modulos WHERE id_curso=?", (curso_selecionado,))
    modulos=cursor.fetchall()
    for linha in modulos:
        print(linha)

# Criar modulo
def criar_modulo():
    ver_cursos()
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    nome=input("Digite o nome do módulo: ")

    cursor.execute('''
        INSERT INTO modulos(id_curso, nome_modulo)
        VALUES (?, ?)
    ''', (id_curso, nome))
    conexao.commit()
    conexao.close()

# Excluir modulo
def excluir_modulo():
    ver_modulos()
    excluir=int(input("Digite o nº da questão a ser excluida: "))
    cursor.execute("DELETE FROM modulos WHERE id_atividade=?", (excluir))
    conexao.commit()
    print("Módulo excluída com sucesso.")

# Editar modulo
def editar_modulo():
    ver_modulos()
    tipo_alterar=input("Digite o que deseja alterar: ")
    indice_alterar=int(input("Digite o indíce onde a alteração deve ocorrer alteração: "))-1
    alteracao=input("Digite a alteração da questão: ")
    cursor.execute("UPDATE modulos SET ? WHERE ?=?", (alteracao, tipo_alterar, indice_alterar))

# Entrar no curso e no módulo
def entrar_curso_modulo():
    # Curso
    ver_cursos()
    selecao_curso=int(input("Digite o identificador (ID) do curso que deseja entrar: "))
    print(f"O curso '{selecao_curso}' foi selecionado com sucesso!")

    # Módulo
    ver_modulos(selecao_curso)
    selecao_modulo=int(input("Digite o identificador (ID) do módulo que deseja entrar: "))
    print(f"O módulo '{selecao_modulo}' foi selecionado com sucesso!")

# Criar atividades
def criar_atividade():
    selecao_modulo, selecao_curso=entrar_curso_modulo()
    print(f"Você está no curso {selecao_curso} e módulo {selecao_modulo}.")
    # Adicionar atividades
    tipo=input("Digite o tipo de atividade: ")
    questão=input("Digite o enunciado da atividade: ")
    opcao_a=input("Digite a opção 'A': ")
    opcao_b=input("Digite a opção 'B': ")
    opcao_c=input("Digite a opção 'C': ")
    opcao_d=input("Digite a opção 'D': ")
    resposta=input("Digite a resposta correta: ").upper()
    dica=input("Digite a dica: ")
    
    # Inserir a atividade
    cursor.execute('''
        INSERT INTO atividades(id_modulo, id_curso, tipo, pergunta, opcao_a, opcao_b, opcao_c, opcao_d, resposta, dica)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (selecao_modulo, selecao_curso, tipo, questão, opcao_a, opcao_b, opcao_c, opcao_d, resposta, dica))
    conexao.commit()
    conexao.close()
    print(f"Atividade de {tipo} adicionada com sucesso!")

# Ver as atividades
def ver_atividades():
    cursor.execute("SELECT * FROM atividades")
    atividades=cursor.fetchall()
    for linha in atividades:
        print(linha)

# Excluir atividade
def excluir_atividade():
    ver_atividades()
    excluir=int(input("Digite o nº da questão a ser excluida: "))
    cursor.execute("DELETE FROM atividades WHERE id_atividade=?", (excluir))
    conexao.commit()
    print("Atividade excluída com sucesso.")

# Editar atividade
def editar_atividade():
    ver_atividades()
    tipo_alterar=input("Digite o que deseja alterar: ")
    indice_alterar=int(input("Digite o indíce onde a alteração deve ocorrer alteração: "))-1
    alteracao=input("Digite a alteração da questão: ")
    cursor.execute("UPDATE atividades SET ? WHERE ?=?", (alteracao, tipo_alterar, indice_alterar))

# Menu de curso - integrado com menu de professor
def menu_curso():
    print("\n>>> CURSOS <<<")
    print("[ 1 ] --> Ver")
    print("[ 2 ] --> Adicionar")
    print("[ 3 ] --> Editar")
    print("[ 4 ] --> Excluir")
    selecao_curso=int(input("Escolha uma opção: "))
    match selecao_curso:
        case 1:
            ver_cursos()
        case 2:
            criar_curso()
        case 3:
            editar_curso()
        case 4:
            excluir_curso()
        case _:
            print("[!] Opção inválida. Tente novamente com um número entre '1' e '4'.")

# Menu de módulo - integrado com menu de professor
def menu_modulo():
    print("\n>>> MODULOS <<<")
    print("[ 1 ] --> Ver")
    print("[ 2 ] --> Adicionar")
    print("[ 3 ] --> Editar")
    print("[ 4 ] --> Excluir")
    selecao_modulo=int(input("Escolha uma opção: "))
    match selecao_modulo:
        case 1:
            ver_modulos()
        case 2:
            criar_modulo()
        case 3:
            editar_modulo()
        case 4:
            excluir_modulo()
        case _:
            print("[!] Opção inválida. Tente novamente com um número entre '1' e '4'.")

# Menu de atividades - integrado com menu de professor
def menu_atividade():
    print("\n>>> ATIVIDADES <<<")
    print("[ 1 ] --> Ver")
    print("[ 2 ] --> Adicionar")
    print("[ 3 ] --> Editar")
    print("[ 4 ] --> Excluir")
    selecao_atividade=int(input("Escolha uma opção: "))
    match selecao_atividade:
        case 1:
            ver_atividades()
        case 2:
            criar_atividade()
        case 3:
            editar_atividade()
        case 4:
            excluir_atividade()
        case _:
            print("[!] Opção inválida. Tente novamente com um número entre '1' e '4'.")

# Menu de redirecionamento do professor - main.py
def menu_professor(nome):
    print(f"\n>>> PAINEL DO PROFESSOR: {nome}")
    print("[ 1 ] -->  Curso")
    print("[ 2 ] -->  Módulo")
    print("[ 3 ] -->  Atividade")
    selecao=int(input("Selecione uma opção: "))
    while True:
        match selecao:
            case 1:
                menu_curso()
            case 2:
                menu_modulo()
            case 3:
                menu_atividade()