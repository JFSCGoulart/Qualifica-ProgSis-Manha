#Atividade

#Aluno
def listar_atividades():
    cursor.execute("SELECT * FROM atividade")
    atividades = cursor.fetchall()
    cursor.execute("SELECT * FROM curso")
    cursos = cursor.fetchall()
    for curso in cursos:
        print(f"ID: {curso[0]}, Nome: {curso[1]}")
    for atividade in atividades:
        print(f"ID: {atividade[0]}")
        print(f"Curso ID: {atividade[1]}")
        print(f"Pergunta: {atividade[2]}")
        print(f"A: {atividade[3]}")
        print(f"B: {atividade[4]}")
        print(f"C: {atividade[5]}")
        print(f"Resposta Correta: {atividade[6]}")
        print(f"Dica: {atividade[7]}")
        print("-" * 20)

def fazer_atividade(id_usuario):
    id_modulo = int(input("Digite o ID do módulo que deseja acessar: "))
    cursor.execute("SELECT id_curso FROM modulo WHERE id = ?", (id_modulo,))
    resultado = cursor.fetchone()
    if not resultado:
        print("❌ Módulo não encontrado.")
        return
    cursor.execute("""
        SELECT 
            id, pergunta, opcao_a, opcao_b, opcao_c, resposta_correta, dica
        FROM atividade
        WHERE id_modulo = ?
    """, (id_modulo,))
    
    atividades = cursor.fetchall()
    
    if not atividades:
        print("❌ Nenhuma atividade encontrada para este módulo.")
        return
    
    for atividade in atividades:
        id_atividade, pergunta, opcao_a, opcao_b, opcao_c, resposta_correta, dica = atividade
        
        print(f"\nPergunta: {pergunta}")
        print(f"A: {opcao_a}")
        print(f"B: {opcao_b}")
        print(f"C: {opcao_c}")
        
        pedir_dica = input("Deseja uma dica? (s/n): ").lower()
        if pedir_dica == 's':
            if dica:
                print(f"💡 Dica: {dica}")
            else:
                print("💡 Sem dica disponível para esta questão.")
        
        resposta_usuario = input("Digite sua resposta (A, B ou C): ").upper()
        
        if resposta_usuario == resposta_correta:
            print("✅ Resposta correta! Você ganhou 1 estrela.")
            estrelas = 1
            acertou = 1
        else:
            print(f"❌ Resposta incorreta! A resposta correta era {resposta_correta}.")
            estrelas = 0
            acertou = 0
        cursor.execute("""
    INSERT INTO acerto (id_usuario, id_atividade, correta)
    VALUES (?, ?, ?)
""", (id_usuario, id_atividade, acertou))


        conexao.commit()


#Professor
def cadastrar_atividade():
    id_curso = input("Digite o ID do curso para o qual deseja criar a atividade: ")
    pergunta = input("Digite a pergunta da atividade: ")
    opcao_a = input("Digite a opção A: ")
    opcao_b = input("Digite a opção B: ")
    opcao_c = input("Digite a opção C: ")
    resposta_correta = input("Digite a resposta correta (A, B ou C): ")
    dica = input("Digite uma dica para a atividade (opcional): ")

    cursor.execute("""
        INSERT INTO atividade 
        (id_curso, pergunta, opcao_a, opcao_b, opcao_c, resposta_correta, dica)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_curso, pergunta, opcao_a, opcao_b, opcao_c, resposta_correta, dica))

    conexao.commit()
    print("✅ Atividade cadastrada com sucesso.")

def ver_atividade():

    ver_modulos_com_curso()
    
    try:
        id_modulo = int(input("Digite o ID do módulo que deseja acessar: "))
    except ValueError:
        print("ID inválido. Digite apenas números.")
        return

    cursor.execute(
        "SELECT id, pergunta FROM atividade WHERE id_modulo = ?",
        (id_modulo,)
    )
    atividades = cursor.fetchall()

    if not atividades:
        print("Nenhuma atividade encontrada para este módulo.")
        return

    for id_atividade, pergunta in atividades:
        print(f"ID: {id_atividade} | Pergunta: {pergunta}")

def deletar_atividade():
    ver_atividade()

    id_atividade = input("Digite o ID da atividade que deseja excluir: ")

    if not id_atividade.isdigit():
        print("ID inválido. Digite apenas números.")
        return

    id_atividade = int(id_atividade)

    cursor.execute(
        "SELECT pergunta FROM atividade WHERE id = ?",
        (id_atividade,)
    )
    atividade = cursor.fetchone()

    if atividade is None:
        print("Atividade não encontrada.")
        return

    print(f"Atividade selecionada: {atividade[0]}")
    print("Tem certeza que deseja deletar essa atividade?")
    print("1 - SIM")
    print("2 - NÃO")

    decisao = input("Resposta: ")

    if decisao == "1":
        cursor.execute(
            "DELETE FROM atividade WHERE id = ?",
            (id_atividade,)
        )
        conexao.commit()
        print("Atividade deletada com sucesso!")
    elif decisao == "2":
        print("Operação cancelada.")
    else:
        print("Opção inválida.")


#Coordenador 
def atividades_feitas_hoje():
    from datetime import date
    hoje = date.today().isoformat()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM progresso 
        WHERE data = ?
    """, (hoje,))
    total_atividades = cursor.fetchone()[0]
    print(f"\n📊 Atividades feitas hoje: {total_atividades}")