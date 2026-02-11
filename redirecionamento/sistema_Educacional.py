import sqlite3
import hashlib
import os

conn = sqlite3.connect(' qualifica_redirecionamento.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('aluno', 'professor', 'coordenador')),
    email TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    materia TEXT,
    data_entrega DATE,
    pontos INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pendente',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES usuarios(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL,
    professor_id INTEGER,
    FOREIGN KEY (professor_id) REFERENCES usuarios(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ranking (
    aluno_id INTEGER PRIMARY KEY,
    total_pontos INTEGER DEFAULT 0,
    posicao INTEGER,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES usuarios(id)
)
''')

conn.commit()

def hash_senha(senha):
    """Criptografa a senha usando SHA-256"""
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha_digitada, senha_hash):
    """Verifica se a senha está correta"""
    return hash_senha(senha_digitada) == senha_hash

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

def fazer_login():
    print("\n" + "="*40)
    print("LOGIN")
    print("="*40)
    
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    
    cursor.execute('''
    SELECT id, nome, senha, tipo, email FROM usuarios 
    WHERE usuario = ?
    ''', (usuario,))
    
    resultado = cursor.fetchone()
    
    if resultado:
        usuario_id, nome, senha_hash, tipo, email = resultado
        
        if verificar_senha(senha, senha_hash):
            print(f"\nLogin bem-sucedido!")
            print(f"Bem-vindo(a), {nome}!")
            print(f"Tipo: {tipo}")
            
            info_usuario = {
                'id': usuario_id,
                'nome': nome,
                'usuario': usuario,
                'tipo': tipo,
                'email': email
            }
            
            return info_usuario
        else:
            print("Senha incorreta!")
    else:
        print("Usuário não encontrado!")
    
    return None

def alterar_senha(usuario_id):
    print("\n" + "="*40)
    print("ALTERAR SENHA")
    print("="*40)
    
    senha_atual = input("Senha atual: ")
    
    cursor.execute('SELECT senha FROM usuarios WHERE id = ?', (usuario_id,))
    resultado = cursor.fetchone()
    
    if resultado and verificar_senha(senha_atual, resultado[0]):
        nova_senha = input("Nova senha: ")
        confirmar_senha = input("Confirmar nova senha: ")
        
        if nova_senha == confirmar_senha:
            if len(nova_senha) >= 6:
                cursor.execute('UPDATE usuarios SET senha = ? WHERE id = ?', 
                (hash_senha(nova_senha), usuario_id))
                conn.commit()
                print("Senha alterada com sucesso!")
            else:
                print("A senha deve ter pelo menos 6 caracteres!")
        else:
            print("As senhas não coincidem!")
    else:
        print("Senha atual incorreta!")

# Funções do menu do Aluno
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
    
    # Contagem de usuários por tipo
    cursor.execute('SELECT COUNT(*) FROM usuarios WHERE tipo = "aluno"')
    total_alunos = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM usuarios WHERE tipo = "professor"')
    total_professores = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM usuarios WHERE tipo = "coordenador"')
    total_coordenadores = cursor.fetchone()[0]
    
    # Contagem de tarefas
    cursor.execute('SELECT COUNT(*) FROM tarefas')
    total_tarefas = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM tarefas WHERE status = "pendente"')
    tarefas_pendentes = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM materias')
    total_materias = cursor.fetchone()[0]
    
    # Pontuação total
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
    
    # Médias
    if total_alunos > 0:
        media_pontos = total_pontos / total_alunos if total_alunos > 0 else 0
        print(f"  Média de pontos por aluno: {media_pontos:.1f}")

def ver_ranking_completo():
    print("\n" + "="*40)
    print("RANKING COMPLETO")
    print("="*40)
    
    # Atualizar posições no ranking
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

# Funções auxiliares compartilhadas
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

def menu_principal():
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo = 'coordenador'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
        INSERT INTO usuarios (nome, usuario, senha, tipo, email)
        VALUES (?, ?, ?, 'coordenador', ?)
        ''', ('Administrador', 'admin', hash_senha('admin123'), 'admin@escola.com'))
        conn.commit()
        print("\nUsuário administrador padrão criado!")
        print("Usuário: admin")
        print("Senha: admin123")
        print("Use este usuário para criar outros coordenadores.")
    
    while True:
        print("\n" + "="*50)
        print("| qualifica/DF/ - /menu / |")
        print("="*50)
        print("1. Login")
        print("2. Cadastrar Aluno")
        print("3. Cadastrar Professor")
        print("4. Cadastrar Coordenador")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            usuario = fazer_login()
            if usuario:
                if usuario['tipo'] == 'aluno':
                    menu_aluno(usuario)
                elif usuario['tipo'] == 'professor':
                    menu_professor(usuario)
                elif usuario['tipo'] == 'coordenador':
                    menu_coordenador(usuario)
        
        elif opcao == "2":
            cadastrar_aluno()
            
        elif opcao == "3":
            cadastrar_professor()
            
        elif opcao == "4":
            cadastrar_coordenador()
            
        elif opcao == "0":
            print("\nSaindo do sistema...")
            conn.close()
            break
            
        else:
            print("Opção inválida!")
if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
        conn.close()
    except Exception as e:
        print(f"\nErro no sistema: {e}")
        conn.close()