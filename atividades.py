import sqlite3

conexao = sqlite3.connect('sistema.db')
cursor = conexao.cursor()

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
    
# Excluir curso
def excluir_curso():
    ver_cursos()
    excluir=int(input("Digite o nº da questão a ser excluida: "))
    cursor.execute("DELETE FROM cursos WHERE id_curso=?", (excluir,))
    conexao.commit()
    print("Curso excluída com sucesso.")

# Editar curso
def editar_curso():
    ver_cursos()
    id_curso=int(input("Digite o ID do curso que deseja editar: "))
    
    print("\nO que deseja alterar?")
    print("[ 1 ] --> Nome")
    print("[ 2 ]--> Descrição")
    opcao=input("Escolha: ")
    
    if opcao=="1":
        novo_nome=input("Digite o novo nome: ")
        cursor.execute("UPDATE cursos SET nome=? WHERE id_curso=?", (novo_nome, id_curso))
    elif opcao=="2":
        nova_descricao=input("Digite a nova descrição: ")
        cursor.execute("UPDATE cursos SET descricao=? WHERE id_curso=?", (nova_descricao, id_curso))
    else:
        print("Opção inválida!")
        return
    
    conexao.commit()
    print("Curso atualizado com sucesso!")

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

# Ver os módulos disponíveis
def ver_modulos(curso_selecionado,):
    cursor.execute("SELECT * FROM modulos WHERE id_curso=?", (curso_selecionado,))
    modulos=cursor.fetchall()
    for linha in modulos:
        print(linha)

    ver_cursos()
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    nome=input("Digite o nome do módulo: ")

    cursor.execute('''
        INSERT INTO modulos(id_curso, nome_modulo)
        VALUES (?, ?)
    ''', (id_curso, nome))
    conexao.commit()

# Criar módulo
def criar_modulo():
    ver_cursos()
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    nome=input("Digite o nome do módulo: ")

    cursor.execute('''
        INSERT INTO modulos(id_curso, nome_modulo)
        VALUES (?, ?)
    ''', (id_curso, nome))
    conexao.commit()

# Excluir módulo
def excluir_modulo():
    ver_modulos()
    excluir=int(input("Digite o nº da questão a ser excluida: "))
    cursor.execute("DELETE FROM modulos WHERE id_modulo=?", (excluir,))
    conexao.commit()
    print("Módulo excluída com sucesso.")

# Editar módulo
def editar_modulo():
    ver_modulos()
    id_modulo=int(input("Digite o ID do módulo que deseja editar: "))
    
    print("\nO que deseja alterar?")
    print("[ 1 ] --> Nome do módulo")
    print("[ 2 ] --> ID do curso")
    opcao=input("Escolha: ")
    
    if opcao=="1":
        novo_nome=input("Digite o novo nome: ")
        cursor.execute("UPDATE modulos SET nome_modulo=? WHERE id_modulo=?", (novo_nome, id_modulo))
    elif opcao=="2":
        ver_cursos()
        novo_id_curso = int(input("Digite o novo ID do curso: "))
        cursor.execute("UPDATE modulos SET id_curso=? WHERE id_modulo=?", (novo_id_curso, id_modulo))
    else:
        print("Opção inválida!")
        return
    
    conexao.commit()
    print("Módulo atualizado com sucesso!")

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

# Entrar no curso e no módulo
def entrar_curso_modulo():
    # Curso
    ver_cursos()
    selecao_curso=int(input("Digite o identificador (ID) do curso que deseja entrar: "))
    cursor.execute("SELECT nome FROM cursos WHERE id_curso=?", (selecao_curso,))
    resultado=cursor.fetchone()

    if not resultado:
        print("[!] Curso não encontrado!")
        return None

    nome_curso=resultado[0]
    print(f"O curso '{nome_curso}' foi selecionado com sucesso!")

    # Módulo
    ver_modulos(selecao_curso)
    selecao_modulo=int(input("Digite o identificador (ID) do módulo que deseja entrar: "))
    cursor.execute("SELECT nome_modulo FROM modulos WHERE id_modulo=?", (selecao_modulo,))
    resultado=cursor.fetchone()

    if not resultado:
        print("[!] Módulo não encontrado!")
        return None

    nome_modulo=resultado[0]
    print(f"O módulo '{nome_modulo}' foi selecionado com sucesso!")

    return {
        'id_curso':selecao_curso,
        'nome_curso':nome_curso,
        'id_modulo':selecao_modulo,
        'nome_modulo':nome_modulo
    }

# Múltipla escolha
def multipla_escolha():
    dados=entrar_curso_modulo()

    if dados is None:
        print("Operação cancelada.")
        return

    print(f"\n Você está em:")
    print(f"   Curso: {dados['nome_curso']} (ID: {dados['id_curso']})")
    print(f"   Módulo: {dados['nome_modulo']} (ID: {dados['id_modulo']})\n")
    
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
    ''', (dados['id_modulo'], dados['id_curso'], tipo, questão, opcao_a, opcao_b, opcao_c, opcao_d, resposta, dica))
    conexao.commit()
    print(f"Atividade de {tipo} adicionada com sucesso!")

# Correspondência (ligar colunas) 
def correspondecia ():
    dados=entrar_curso_modulo()

    if dados is None:
        print("Operação cancelada.")
        return

    print(f"\n Você está em:")
    print(f"   Curso: {dados['nome_curso']} (ID: {dados['id_curso']})")
    print(f"   Módulo: {dados['nome_modulo']} (ID: {dados['id_modulo']})\n")

    pergunta=input("Digite o enunciado da atividade: ")
    tipo="Correspondência"
    coluna_1=input("Digite a primeira coluna: ")
    coluna_2=input("Digite a segunda coluna: ")
    pares = input("Digite os pares das colunas(ex: A-1; B-2; C-3): ")
    resposta=pares
    dica=input("Digite a dica: ")
    cursor.execute('''
        INSERT INTO atividades(id_curso, id_modulo, pergunta, tipo, coluna_1, coluna_2, pares, resposta, dica)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (dados['id_modulo'], dados['id_curso'], pergunta, tipo, coluna_1, coluna_2, pares, resposta, dica,))
    conexao.commit()
    print(f"Atividade de {tipo} adicionada com sucesso!")

# Classificação (separar categorias)
def classificacao ():
    dados=entrar_curso_modulo()

    if dados is None:
        print("Operação cancelada.")
        return

    print(f"\n Você está em:")
    print(f"   Curso: {dados['nome_curso']} (ID: {dados['id_curso']})")
    print(f"   Módulo: {dados['nome_modulo']} (ID: {dados['id_modulo']})\n")

    perguntas=input("Digite o enunciado da atividade: ")
    tipo="Classificação"
    categorias = input("Digite categorias : (Inteiro, Racionais ): ")
    resposta =input("Digite os itens para relacionar (Ex: 4 , 45 , 3.4) : ")
    dica = input("Digite a dica: ")
    cursor.execute('''
        INSERT INTO atividades(id_curso, id_modulo, pergunta, tipo, categorias, resposta, dica)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (dados['id_modulo'], dados['id_curso'],perguntas, tipo, categorias, resposta, dica))
    conexao.commit()
    print(f"Atividade de {tipo} adicionada com sucesso!")

# Escolha múltipla (várias corretas)
def escolha_multipla():
    dados=entrar_curso_modulo()

    if dados is None:
        print("Operação cancelada.")
        return

    print(f"\n Você está em:")
    print(f"   Curso: {dados['nome_curso']} (ID: {dados['id_curso']})")
    print(f"   Módulo: {dados['nome_modulo']} (ID: {dados['id_modulo']})\n")

    pergunta=input("Digite o enunciado da atividade: ")
    tipo="Escolha Múltipla"
    opcao_a = input("Digite a 'A' opção : ")
    opcao_b = input("Digite a 'B' opção : ")
    opcao_c = input("Digite a 'C' opção : ")
    opcao_d = input("Digite a 'D' opção : ")
    resposta=input("Digite as alternativas certas (ex: A,C) : ")
    dica=input("Digite a dica: ") 
    cursor.execute('''
        INSERT INTO atividades(id_curso, id_modulo, pergunta, tipo, opcao_a, opcao_b, opcao_c, opcao_d, resposta ,dica)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (dados['id_modulo'], dados['id_curso'], pergunta, tipo, opcao_a, opcao_b, opcao_c, opcao_d, resposta, dica))
    conexao.commit()
    print(f"Atividade de {tipo} adicionada com sucesso!")

# Palavra embaralhada
def palavra_embaralhada():
    dados=entrar_curso_modulo()

    if dados is None:
        print("Operação cancelada.")
        return

    print(f"\n Você está em:")
    print(f"   Curso: {dados['nome_curso']} (ID: {dados['id_curso']})")
    print(f"   Módulo: {dados['nome_modulo']} (ID: {dados['id_modulo']})\n")

    embaralhada = input("Digite a palavra embaralhada: ")
    perguntas = f"Desembralhe a palavra {embaralhada}: "
    tipo="Palavra Embaralhada"
    resposta = input("Digite a palavra correta: ")
    dica=input("Digite a dica: ") 
    cursor.execute('''
        INSERT INTO atividades(id_curso, id_modulo, pergunta, tipo, embaralhada, resposta, dica)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (dados['id_modulo'], dados['id_curso'], perguntas, tipo, embaralhada, resposta, dica))
    conexao.commit()
    print(f"Atividade de {tipo} adicionada com sucesso!")

# Mini-cenários com decisões
def mini_cenarios():
    dados=entrar_curso_modulo()

    if dados is None:
        print("Operação cancelada.")
        return

    print(f"\n Você está em:")
    print(f"   Curso: {dados['nome_curso']} (ID: {dados['id_curso']})")
    print(f"   Módulo: {dados['nome_modulo']} (ID: {dados['id_modulo']})\n")
    
    cenario=input("Digite o cénario : ")
    tipo="Mini-Cenários"
    decisao_a = input("Digite a decisão que o aluno pode tomar: ")
    decisao_b = input("Digite as decisões que o aluno pode tomar : ")
    decisao_c = input("Digite as decisões que o aluno pode tomar : ")
    decisao_d = input("Digite as decisões que o aluno pode tomar : ")
    resposta=input("Digite a decisão certa : ")
    dica=input("Digite a dica: ")
    cursor.execute('''
        INSERT INTO atividades(id_curso, id_modulo, pergunta, tipo, opcao_a, opcao_b, opcao_c, opcao_d, resposta, dica)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (dados['id_modulo'], dados['id_curso'], cenario, tipo, decisao_a, decisao_b, decisao_c, decisao_d, resposta, dica))
    conexao.commit()
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
    cursor.execute("DELETE FROM atividades WHERE id_atividade=?", (excluir,))
    conexao.commit()
    print("Atividade excluída com sucesso.")

# Editar atividade
def editar_atividade():
    ver_atividades()
    id_atividade=int(input("Digite o ID da atividade que deseja editar: "))
    
    print("\nO que deseja alterar?")
    print("[ 1 ] --> Tipo")
    print("[ 2 ] --> Pergunta")
    print("[ 3 ] --> Opção A")
    print("[ 4 ] --> Opção B")
    print("[ 5 ] --> Opção C")
    print("[ 6 ] --> Opção D")
    print("[ 7 ] --> Coluna 1")
    print("[ 8 ] --> Coluna 2")
    print("[ 9 ] --> Pares")
    print("[ 10 ] --> Categoria")
    print("[ 11 ] --> Embaralhada")
    print("[ 12 ] --> Cenário")
    print("[ 13 ] --> Resposta")
    print("[ 14 ] --> Dica")
    opcao=input("Escolha: ")
    
    alteracao=input("Digite a nova informação: ")
    
    campos={
        "1": "tipo",
        "2": "pergunta",
        "3": "opcao_a",
        "4": "opcao_b",
        "5": "opcao_c",
        "6": "opcao_d",
        "7": "coluna_1",
        "8": "coluna_2",
        "9": "pares",
        "10": "categoria",
        "11": "embaralhada",
        "12": "cenario",
        "13": "resposta",
        "14": "dica"
    }
    
    if opcao in campos:
        campo = campos[opcao]
        cursor.execute(f"UPDATE atividades SET {campo}=? WHERE id_atividade=?", (alteracao, id_atividade))
        conexao.commit()
        print("Atividade atualizada com sucesso!")
    else:
        print("[!] Opção inválida.")

# Integração de todos os tipos de atividades
def criar_atividade():
    while True:
        print("Qual tipo de atividade deseja add:")
        print("[ 1 ] --> Múltipla Escolha, Verdadeiro ou Falso")
        print("[ 2 ] --> Correspondência")
        print("[ 3 ] --> Classificação")
        print("[ 4 ] --> Escolha Múltipla")
        print("[ 5 ] --> Palavra Embaralhada")
        print("[ 6 ] --> Mini-Cenários")
        print("[ 7 ] --> Sair")
        selecao_atividade=int(input("Selecione uma opção: "))
        match selecao_atividade:
            case 1:
                multipla_escolha()
            case 2:
                correspondecia()
            case 3:
                classificacao()
            case 4:
                escolha_multipla()
            case 5:
                palavra_embaralhada()
            case 6:
                mini_cenarios()
            case 7:
                fechar_conexao()
                print("Fechando atividades...")
                break
            case _:
                print("[!] Opção inválida.")

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
            
# Fechar conexão com o banco de dados
def fechar_conexao():
    conexao.close()