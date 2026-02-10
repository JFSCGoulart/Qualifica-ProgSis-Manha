def cadastrar_professor():
    print("\n" + "="*40)
    print("CADASTRO DE PROFESSOR")
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
        VALUES (?, ?, ?, 'professor', ?)
        ''', (nome, usuario, hash_senha(senha), email))
        
        usuario_id = cursor.lastrowid
        conn.commit()
        
        print(f"\nProfessor {nome} cadastrado com sucesso!")
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
        
def menu_professor(usuario_info):
    while True:
        print("\n" + "="*40)
        print(f"PROFESSOR: {usuario_info['nome']}")
        print("="*40)
        print("1. Gerenciar Matérias")
        print("2. Avaliar Tarefas")
        print("3. Ver Alunos")
        print("4. Ver Ranking")
        print("5. Minhas Matérias")
        print("6. Alterar Senha")
        print("7. Meus Dados")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            gerenciar_materias(usuario_info['id'])
            
        elif opcao == "2":
            avaliar_tarefas(usuario_info['id'])
            
        elif opcao == "3":
            ver_alunos()
            
        elif opcao == "4":
            ver_ranking_geral()
            
        elif opcao == "5":
            minhas_materias(usuario_info['id'])
            
        elif opcao == "6":
            alterar_senha(usuario_info['id'])
            
        elif opcao == "7":
            mostrar_dados_usuario(usuario_info)
            
        elif opcao == "0":
            print("\nSaindo da conta de professor...")
            break
            
        else:
            print("Opção inválida!")

def gerenciar_materias(professor_id):
    while True:
        print("\n" + "="*40)
        print("GERENCIAR MATÉRIAS")
        print("="*40)
        print("1. Adicionar Matéria")
        print("2. Ver Minhas Matérias")
        print("3. Ver Todas as Matérias")
        print("0. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            nome_materia = input("Nome da matéria: ")
            
            try:
                cursor.execute('''
                INSERT INTO materias (nome, professor_id)
                VALUES (?, ?)
                ''', (nome_materia, professor_id))
                
                conn.commit()
                print(f"Matéria '{nome_materia}' adicionada com sucesso!")
            except sqlite3.IntegrityError:
                print("Esta matéria já existe!")
            except Exception as e:
                print(f"Erro: {e}")
                
        elif opcao == "2":
            cursor.execute('''
            SELECT id, nome FROM materias 
            WHERE professor_id = ?
            ''', (professor_id,))
            
            materias = cursor.fetchall()
            
            if materias:
                print(f"\nSuas matérias ({len(materias)}):")
                for materia in materias:
                    print(f"ID: {materia[0]} - {materia[1]}")
            else:
                print("Você não tem matérias cadastradas.")
                
        elif opcao == "3":
            cursor.execute('''
            SELECT m.id, m.nome, u.nome as professor 
            FROM materias m
            LEFT JOIN usuarios u ON m.professor_id = u.id
            ORDER BY m.nome
            ''')
            
            todas_materias = cursor.fetchall()
            
            if todas_materias:
                print("\nTodas as matérias:")
                for materia in todas_materias:
                    professor = materia[2] if materia[2] else "Sem professor"
                    print(f"ID: {materia[0]} - {materia[1]} (Professor: {professor})")
            else:
                print("Nenhuma matéria cadastrada.")
                
        elif opcao == "0":
            break
            
        else:
            print("Opção inválida!")

def avaliar_tarefas(professor_id):
    print("\n" + "="*40)
    print("AVALIAR TAREFAS")
    print("="*40)
    
    cursor.execute('''
    SELECT t.id, t.descricao, t.materia, u.nome as aluno_nome, t.data_entrega
    FROM tarefas t
    JOIN usuarios u ON t.aluno_id = u.id
    WHERE t.status = 'pendente'
    ORDER BY t.data_entrega
    ''')
    
    tarefas = cursor.fetchall()
    
    if tarefas:
        print(f"Tarefas pendentes: {len(tarefas)}")
        for tarefa in tarefas:
            print(f"\nID: {tarefa[0]}")
            print(f"Aluno: {tarefa[3]}")
            print(f"Matéria: {tarefa[2]}")
            print(f"Descrição: {tarefa[1]}")
            print(f"Entrega: {tarefa[4]}")
            
            avaliar = input("Avaliar esta tarefa? (s/n): ")
            if avaliar.lower() == 's':
                try:
                    pontos = int(input("Pontuação (0-100): "))
                    if 0 <= pontos <= 100:
                        cursor.execute('''
                        UPDATE tarefas 
                        SET pontos = ?, status = 'avaliada' 
                        WHERE id = ?
                        ''', (pontos, tarefa[0]))
                        
                        cursor.execute('''
                        SELECT aluno_id FROM tarefas WHERE id = ?
                        ''', (tarefa[0],))
                        aluno_id = cursor.fetchone()[0]
                        
                        cursor.execute('''
                        UPDATE ranking 
                        SET total_pontos = total_pontos + ?
                        WHERE aluno_id = ?
                        ''', (pontos, aluno_id))
                        
                        conn.commit()
                        print("Tarefa avaliada com sucesso!")
                    else:
                        print("Pontuação deve ser entre 0 e 100!")
                except ValueError:
                    print("Valor inválido!")
    else:
        print("Nenhuma tarefa pendente para avaliar.")

def ver_alunos():
    print("\n" + "="*40)
    print("LISTA DE ALUNOS")
    print("="*40)
    
    cursor.execute('''
    SELECT u.id, u.nome, u.email, r.total_pontos
    FROM usuarios u
    LEFT JOIN ranking r ON u.id = r.aluno_id
    WHERE u.tipo = 'aluno'
    ORDER BY u.nome
    ''')
    
    alunos = cursor.fetchall()
    
    if alunos:
        print(f"Total de alunos: {len(alunos)}")
        for aluno in alunos:
            print(f"\nID: {aluno[0]}")
            print(f"Nome: {aluno[1]}")
            print(f"Email: {aluno[2]}")
            print(f"Pontuação: {aluno[3] or 0}")
            print("-" * 30)
    else:
        print("Nenhum aluno cadastrado.")