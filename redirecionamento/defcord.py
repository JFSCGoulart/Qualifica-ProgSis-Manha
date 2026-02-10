def cadastrar_coordenador():
    print("\n" + "="*40)
    print("CADASTRO DE COORDENADOR")
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
    
    codigo_autorizacao = input("Código de autorização: ")
    if codigo_autorizacao != "COORD2024":
        print("Erro: Código de autorização inválido!")
        return None
    
    try:
        cursor.execute('''
        INSERT INTO usuarios (nome, usuario, senha, tipo, email)
        VALUES (?, ?, ?, 'coordenador', ?)
        ''', (nome, usuario, hash_senha(senha), email))
        
        usuario_id = cursor.lastrowid
        conn.commit()
        
        print(f"\nCoordenador {nome} cadastrado com sucesso!")
        print(f"Usuário: {usuario}")
        print("Acesso total ao sistema concedido.")
        
        return usuario_id
    except sqlite3.IntegrityError as e:
        print(f"Erro: Usuário '{usuario}' já existe!")
        return None
    except Exception as e:
        print(f"Erro ao cadastrar: {e}")
        return None
    
def menu_coordenador(usuario_info):
    while True:
        print("\n" + "="*40)
        print(f"COORDENADOR: {usuario_info['nome']}")
        print("ACESSO TOTAL AO SISTEMA")
        print("="*40)
        print("1. Gerenciar Usuários")
        print("2. Gerenciar Matérias")
        print("3. Ver Estatísticas")
        print("4. Ver Ranking Completo")
        print("5. Relatórios")
        print("6. Alterar Senha")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            gerenciar_usuarios()
            
        elif opcao == "2":
            gerenciar_materias_coordenador()
            
        elif opcao == "3":
            ver_estatisticas()
            
        elif opcao == "4":
            ver_ranking_completo()
            
        elif opcao == "5":
            gerar_relatorios()
            
        elif opcao == "6":
            alterar_senha(usuario_info['id'])
            
        elif opcao == "0":
            print("\nSaindo da conta de coordenador...")
            break
            
        else:
            print("Opção inválida!")

def gerenciar_usuarios():
    while True:
        print("\n" + "="*40)
        print("GERENCIAR USUÁRIOS")
        print("="*40)
        print("1. Ver Todos os Usuários")
        print("2. Buscar Usuário")
        print("3. Editar Usuário")
        print("4. Remover Usuário")
        print("0. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            cursor.execute('''
            SELECT u.id, u.nome, u.usuario, u.tipo, u.email, u.data_cadastro
            FROM usuarios u
            ORDER BY u.tipo, u.nome
            ''')
            
            usuarios = cursor.fetchall()
            
            if usuarios:
                print(f"\nTotal de usuários: {len(usuarios)}")
                print("-" * 60)
                for usuario in usuarios:
                    print(f"ID: {usuario[0]}")
                    print(f"Nome: {usuario[1]}")
                    print(f"Usuário: {usuario[2]}")
                    print(f"Tipo: {usuario[3]}")
                    print(f"Email: {usuario[4]}")
                    print(f"Cadastro: {usuario[5]}")
                    print("-" * 30)
            else:
                print("Nenhum usuário cadastrado.")
                
        elif opcao == "2":
            termo = input("Buscar por nome ou usuário: ")
            
            cursor.execute('''
            SELECT id, nome, usuario, tipo, email 
            FROM usuarios 
            WHERE nome LIKE ? OR usuario LIKE ?
            ''', (f'%{termo}%', f'%{termo}%'))
            
            resultados = cursor.fetchall()
            
            if resultados:
                print(f"\nResultados encontrados: {len(resultados)}")
                for resultado in resultados:
                    print(f"ID: {resultado[0]} | Nome: {resultado[1]} | Usuário: {resultado[2]} | Tipo: {resultado[3]}")
            else:
                print("Nenhum resultado encontrado.")
                
        elif opcao == "3":
            try:
                usuario_id = int(input("ID do usuário a editar: "))
                
                cursor.execute('SELECT nome, tipo FROM usuarios WHERE id = ?', (usuario_id,))
                usuario = cursor.fetchone()
                
                if usuario:
                    print(f"\nEditando: {usuario[0]} ({usuario[1]})")
                    print("Deixe em branco para manter o valor atual.")
                    
                    novo_nome = input(f"Nome [{usuario[0]}]: ") or usuario[0]
                    novo_tipo = input(f"Tipo (aluno/professor/coordenador) [{usuario[1]}]: ") or usuario[1]
                    
                    cursor.execute('''
                    UPDATE usuarios 
                    SET nome = ?, tipo = ?
                    WHERE id = ?
                    ''', (novo_nome, novo_tipo, usuario_id))
                    
                    conn.commit()
                    print("Usuário atualizado com sucesso!")
                else:
                    print("Usuário não encontrado!")
            except ValueError:
                print("ID inválido!")
                
        elif opcao == "4":
            try:
                usuario_id = int(input("ID do usuário a remover: "))
                
                confirmar = input("Tem certeza? Esta ação não pode ser desfeita! (s/n): ")
                if confirmar.lower() == 's':
                    cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))
                    conn.commit()
                    print("Usuário removido com sucesso!")
            except ValueError:
                print("ID inválido!")
                
        elif opcao == "0":
            break
            
        else:
            print("Opção inválida!")

def ver_estatisticas():
    print("\n" + "="*40)
    print("ESTATÍSTICAS DO SISTEMA")
    print("="*40)
    
    cursor.execute('SELECT COUNT(*) FROM usuarios WHERE tipo = "aluno"')
    total_alunos = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM usuarios WHERE tipo = "professor"')
    total_professores = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM usuarios WHERE tipo = "coordenador"')
    total_coordenadores = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM tarefas')
    total_tarefas = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM tarefas WHERE status = "pendente"')
    tarefas_pendentes = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM materias')
    total_materias = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(total_pontos) FROM ranking')
    total_pontos = cursor.fetchone()[0] or 0
    
    print(f"Usuários:")
    print(f"  Alunos: {total_alunos}")
    print(f"  Professores: {total_professores}")
    print(f"  Coordenadores: {total_coordenadores}")
    print(f"  Total: {total_alunos + total_professores + total_coordenadores}")
    
    print(f"\nAtividades:")
    print(f"  Tarefas totais: {total_tarefas}")
    print(f"  Tarefas pendentes: {tarefas_pendentes}")
    print(f"  Matérias: {total_materias}")
    print(f"  Pontuação total: {total_pontos}")
    
    
    if total_alunos > 0:
        media_pontos = total_pontos / total_alunos if total_alunos > 0 else 0
        print(f"  Média de pontos por aluno: {media_pontos:.1f}")

def ver_ranking_completo():
    print("\n" + "="*40)
    print("RANKING COMPLETO")
    print("="*40)
    
    cursor.execute('''
    UPDATE ranking 
    SET posicao = (
        SELECT COUNT(*) + 1 
        FROM ranking r2 
        WHERE r2.total_pontos > ranking.total_pontos
    )
    ''')
    
    cursor.execute('''
    SELECT u.nome, r.total_pontos, r.posicao
    FROM usuarios u
    JOIN ranking r ON u.id = r.aluno_id
    WHERE u.tipo = 'aluno'
    ORDER BY r.posicao
    LIMIT 20
    ''')
    
    ranking = cursor.fetchall()
    
    if ranking:
        print("TOP 20 ALUNOS:")
        print("-" * 50)
        for aluno in ranking:
            posicao = f"{aluno[2]}º"
            print(f"{posicao} {aluno[0]} - {aluno[1]} pontos")
    else:
        print("Nenhum aluno no ranking.")

def ver_ranking_geral():
    print("\n" + "="*40)
    print("RANKING GERAL")
    print("="*40)
    
    cursor.execute('''
    SELECT u.nome, r.total_pontos
    FROM usuarios u
    JOIN ranking r ON u.id = r.aluno_id
    WHERE u.tipo = 'aluno'
    ORDER BY r.total_pontos DESC
    LIMIT 10
    ''')
    
    ranking = cursor.fetchall()
    
    if ranking:
        print("TOP 10 ALUNOS:")
        for i, aluno in enumerate(ranking, 1):
            print(f"{i}º - {aluno[0]}: {aluno[1]} pontos")
    else:
        print("Nenhum aluno no ranking.")

def mostrar_dados_usuario(usuario_info):
    print("\n" + "="*40)
    print("MEUS DADOS")
    print("="*40)
    
    print(f"Nome: {usuario_info['nome']}")
    print(f"Usuário: {usuario_info['usuario']}")
    print(f"Email: {usuario_info['email']}")
    print(f"Tipo: {usuario_info['tipo']}")

def minhas_materias(professor_id):
    cursor.execute('''
    SELECT m.id, m.nome, COUNT(t.id) as total_tarefas
    FROM materias m
    LEFT JOIN tarefas t ON m.nome = t.materia
    WHERE m.professor_id = ?
    GROUP BY m.id
    ''', (professor_id,))
    
    materias = cursor.fetchall()
    
    if materias:
        print(f"\nSuas matérias ({len(materias)}):")
        for materia in materias:
            print(f"\n{materia[1]}")
            print(f"  ID: {materia[0]}")
            print(f"  Tarefas relacionadas: {materia[2]}")
    else:
        print("Você não tem matérias cadastradas.")

def gerenciar_materias_coordenador():
    while True:
        print("\n" + "="*40)
        print("GERENCIAR MATÉRIAS (COORDENADOR)")
        print("="*40)
        print("1. Ver Todas as Matérias")
        print("2. Adicionar Matéria")
        print("3. Atribuir Professor")
        print("4. Remover Matéria")
        print("0. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            cursor.execute('''
            SELECT m.id, m.nome, u.nome as professor, 
            COUNT(t.id) as total_tarefas
            FROM materias m
            LEFT JOIN usuarios u ON m.professor_id = u.id
            LEFT JOIN tarefas t ON m.nome = t.materia
            GROUP BY m.id
            ''')
            
            materias = cursor.fetchall()
            
            if materias:
                print(f"\nTotal de matérias: {len(materias)}")
                for materia in materias:
                    professor = materia[2] if materia[2] else "Sem professor"
                    print(f"\nID: {materia[0]} - {materia[1]}")
                    print(f"  Professor: {professor}")
                    print(f"  Tarefas: {materia[3]}")
            else:
                print("Nenhuma matéria cadastrada.")
                
        elif opcao == "2":
            nome_materia = input("Nome da matéria: ")
            
            try:
                cursor.execute('INSERT INTO materias (nome) VALUES (?)', (nome_materia,))
                conn.commit()
                print(f"Matéria '{nome_materia}' adicionada com sucesso!")
            except sqlite3.IntegrityError:
                print("Esta matéria já existe!")
                
        elif opcao == "3":
            try:
                materia_id = int(input("ID da matéria: "))
                professor_id = int(input("ID do professor: "))
                
                cursor.execute('''
                UPDATE materias 
                SET professor_id = ?
                WHERE id = ?
                ''', (professor_id, materia_id))
                
                conn.commit()
                print("Professor atribuído com sucesso!")
            except ValueError:
                print("IDs inválidos!")
                
        elif opcao == "4":
            try:
                materia_id = int(input("ID da matéria a remover: "))
                
                confirmar = input("Tem certeza? (s/n): ")
                if confirmar.lower() == 's':
                    cursor.execute('DELETE FROM materias WHERE id = ?', (materia_id,))
                    conn.commit()
                    print("Matéria removida com sucesso!")
            except ValueError:
                print("ID inválido!")
                
        elif opcao == "0":
            break
            
        else:
            print("Opção inválida!")

def gerar_relatorios():
    print("\n" + "="*40)
    print("RELATÓRIOS")
    print("="*40)
    print("1. Relatório de Alunos")
    print("2. Relatório de Tarefas")
    print("3. Relatório de Desempenho")
    print("0. Voltar")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == "1":
        cursor.execute('''
        SELECT u.nome, r.total_pontos,
        COUNT(t.id) as total_tarefas,
        AVG(t.pontos) as media
        FROM usuarios u
        LEFT JOIN ranking r ON u.id = r.aluno_id
        LEFT JOIN tarefas t ON u.id = t.aluno_id
        WHERE u.tipo = 'aluno'
        GROUP BY u.id
        ORDER BY r.total_pontos DESC
        ''')
        
        alunos = cursor.fetchall()
        
        print("\nRELATÓRIO DE ALUNOS")
        print("-" * 80)
        for aluno in alunos:
            print(f"{aluno[0]} | Pontos: {aluno[1] or 0}")
            print(f"  Tarefas: {aluno[2]} | Média: {aluno[3] or 0:.1f}")
            print("-" * 40)
            
    elif opcao == "2":
        cursor.execute('''
        SELECT m.nome, 
        COUNT(t.id) as total,
        AVG(t.pontos) as media_pontos,
        COUNT(CASE WHEN t.status = 'pendente' THEN 1 END) as pendentes
        FROM materias m
        LEFT JOIN tarefas t ON m.nome = t.materia
        GROUP BY m.id
        ''')
        
        materias = cursor.fetchall()
        
        print("\nRELATÓRIO DE TAREFAS POR MATÉRIA")
        print("-" * 60)
        for materia in materias:
            print(f"{materia[0]}:")
            print(f"  Total: {materia[1]}")
            print(f"  Média de pontos: {materia[2] or 0:.1f}")
            print(f"  Pendentes: {materia[3] or 0}")
            print("-" * 30)