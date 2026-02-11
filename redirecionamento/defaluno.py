import sqlite3

from redirecionamento.deflogin import hash_senha

conn=sqlite3.connect("qualifica_redirecionamento.db")

cursor=conn.cursor()

def cadastrar_aluno():
    print("\n" + "="*40)
    print("CADASTRO DE ALUNO")
    print("="*40)
    
    nome = input("Nome completo: ")
    usuario = input("Nome de usuário: ")
    senha = input("Senha: ")
    confirmar_senha = input("Confirmar senha: ")
    email = input("Email: ")
    
    if senha != confirmar_senha:
        print("Erro: As senhas não coincidem!")
        return None
    
    if len(senha) < 6:
        print("Erro: A senha deve ter pelo menos 6 caracteres!")
        return None
    
    try:
        cursor.execute('''
        INSERT INTO usuarios (nome, usuario, senha, tipo, email)
        VALUES (?, ?, ?, 'aluno', ?)
        ''', (nome, usuario, hash_senha(senha), email))
        
        usuario_id = cursor.lastrowid
        
        cursor.execute('''
        INSERT INTO ranking (aluno_id, total_pontos, posicao)
        VALUES (?, 0, 0)
        ''', (usuario_id,))
        
        conn.commit()
        print(f"\nAluno {nome} cadastrado com sucesso!")
        print(f"Usuário: {usuario}")
        print(f"Email: {email}")
        
        return usuario_id
    except sqlite3.IntegrityError as e:
        print(f"Erro: Usuário '{usuario}' já existe!")
        return None
    except Exception as e:
        print(f"Erro ao cadastrar: {e}")
        return None
    
def menu_aluno(usuario_info):
    while True:
        print("\n" + "="*40)
        print(f"ALUNO: {usuario_info['nome']}")
        print("="*40)
        print("1. Adicionar Tarefa")
        print("2. Ver Minhas Tarefas")
        print("3. Ver Meu Desempenho")
        print("4. Ver Ranking")
        print("5. Alterar Senha")
        print("6. Meus Dados")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            adicionar_tarefa_aluno(usuario_info['id'])
            
        elif opcao == "2":
            ver_tarefas_aluno(usuario_info['id'])
            
        elif opcao == "3":
            ver_desempenho_aluno(usuario_info['id'])
            
        elif opcao == "4":
            ver_ranking_geral()
            
        elif opcao == "5":
            alterar_senha(usuario_info['id'])
            
        elif opcao == "6":
            mostrar_dados_usuario(usuario_info)
            
        elif opcao == "0":
            print("\nSaindo da conta de aluno...")
            break
            
        else:
            print("Opção inválida!")

def adicionar_tarefa_aluno(aluno_id):
    print("\n" + "="*40)
    print("ADICIONAR TAREFA")
    print("="*40)
    
    descricao = input("Descrição da tarefa: ")
    materia = input("Matéria: ")
    data_entrega = input("Data de entrega (YYYY-MM-DD): ")
    
    try:
        cursor.execute('''
        INSERT INTO tarefas (aluno_id, descricao, materia, data_entrega, status)
        VALUES (?, ?, ?, ?, 'pendente')
        ''', (aluno_id, descricao, materia, data_entrega))
        
        conn.commit()
        print("Tarefa adicionada com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")

def ver_tarefas_aluno(aluno_id):
    print("\n" + "="*40)
    print("MINHAS TAREFAS")
    print("="*40)
    
    cursor.execute('''
    SELECT id, descricao, materia, data_entrega, pontos, status, data_criacao
    FROM tarefas 
    WHERE aluno_id = ?
    ORDER BY data_entrega DESC
    ''', (aluno_id,))
    
    tarefas = cursor.fetchall()
    
    if tarefas:
        print(f"Total de tarefas: {len(tarefas)}")
        for tarefa in tarefas:
            print(f"\nID: {tarefa[0]}")
            print(f"Descrição: {tarefa[1]}")
            print(f"Matéria: {tarefa[2]}")
            print(f"Entrega: {tarefa[3]}")
            print(f"Pontos: {tarefa[4]}")
            print(f"Status: {tarefa[5]}")
            print(f"Criada em: {tarefa[6]}")
            print("-" * 30)
    else:
        print("Nenhuma tarefa encontrada.")

def ver_desempenho_aluno(aluno_id):
    print("\n" + "="*40)
    print("MEU DESEMPENHO")
    print("="*40)
    
    cursor.execute('''
    SELECT total_pontos, posicao FROM ranking 
    WHERE aluno_id = ?
    ''', (aluno_id,))
    
    ranking = cursor.fetchone()
    
    if ranking:
        pontos, posicao = ranking
        print(f"Pontuação total: {pontos}")
        print(f"Posição no ranking: {posicao}º lugar")
        
        cursor.execute('SELECT COUNT(*) FROM tarefas WHERE aluno_id = ?', (aluno_id,))
        total_tarefas = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM tarefas WHERE aluno_id = ? AND pontos > 0', (aluno_id,))
        tarefas_avaliadas = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(pontos) FROM tarefas WHERE aluno_id = ? AND pontos > 0', (aluno_id,))
        media_pontos = cursor.fetchone()[0] or 0
        
        print(f"\nTotal de tarefas: {total_tarefas}")
        print(f"Tarefas avaliadas: {tarefas_avaliadas}")
        print(f"Média de pontos: {media_pontos:.1f}")
    else:
        print("Nenhum desempenho registrado.")