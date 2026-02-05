import sqlite3

conexao=sqlite3.connect('sistema.db')
cursor=conexao.cursor()

# Alterar tabela 'atividades' para receber opções
cursor.execute('''
    CREATE TABLE IF NOT EXISTS atividades(
        id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
        id_modulo INTEGER NOT NULL,
        id_cursos INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        perguntas TEXT NOT NULL,
        opcao_a TEXT NOT NULL,
        opcao_b TEXT NOT NULL,
        opcao_c TEXT NOT NULL,
        opcao_d TEXT NOT NULL,
        respostas TEXT NOT NULL,
        dica TEXT NOT NULL,
        FOREIGN KEY (id_modulo) REFERENCES modulo(id)
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

# Ver os módulos disponíveis
def ver_modulos(curso_selecionado):
    cursor.execute("SELECT * FROM modulos WHERE id=?", (curso_selecionado))
    modulos=cursor.fetchall()
    for linha in modulos:
        print(linha)

# Entrar no curso e no módulo
def entrar_curso_modulo():
    # Curso
    ver_cursos()
    selecao_curso=int(input("Digite o identificador (ID) do curso que deseja entrar: "))
    print(f"O curso '{selecao_curso}' foi selecionado com sucesso!")

    # Módulo
    ver_modulos(selecao_curso)
    selecao_modulo=int(input("Digite o identificador (ID) do módulo que deseja entrar: "))
    print(f"O curso '{selecao_modulo}' foi selecionado com sucesso!")

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
        INSERT INTO atividades(id_modulo, id_cursos, tipo, perguntas, opcao_a, opcao_b, opcao_c, opcao_d, resposta, dica)
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
    indice_alterar=int(input("Digite o indíce onde a alteração deve ocorrer alteração: "))
    alteracao=input("Digite a alteração da questão: ")
    cursor.execute("UPDATE atividades SET ? WHERE ?=?", (alteracao, tipo_alterar, indice_alterar))