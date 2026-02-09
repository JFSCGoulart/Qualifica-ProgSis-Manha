#• Ao iniciar, o usuário escolhe: "Aluno", "Professor" ou "Coordenador".
#• Depois digita nome e senha.
#• Se for um nome novo, o sistema pergunta o tipo e cadastra.
#• Cada tipo tem acesso a um menu diferente.
import sqlite3, hashlib, getpass, os

class SistemaEscolar:
    def __init__(self):
        self.criar_banco_dados()
        self.usuario_logado = None
    
    def criar_banco_dados(self):
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('aluno', 'professor', 'coordenador')),
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (aluno_id) REFERENCES usuarios (id)
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ranking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER UNIQUE NOT NULL,
            pontos INTEGER DEFAULT 0,
            FOREIGN KEY (aluno_id) REFERENCES usuarios (id)
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            professor_id INTEGER,
            FOREIGN KEY (professor_id) REFERENCES usuarios (id)
        )''')
        
        if cursor.execute("SELECT COUNT(*) FROM materias").fetchone()[0] == 0:
            cursor.execute("INSERT INTO materias (nome) VALUES ('Programação')")
        
        conn.commit()
        conn.close()
    
    def hash_senha(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def registrar_aluno(self):
        print("\n=== REGISTRO DE ALUNO ===")
        nome = input("Nome completo: ").strip()
        email = input("Email: ").strip()
        
        if not nome or not email:
            print("Nome e email são obrigatórios!")
            return False
        
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()
        if cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,)).fetchone():
            print("Email já cadastrado!")
            conn.close()
            return False
        
        while True:
            senha = getpass.getpass("Senha (mínimo 6 caracteres): ")
            confirmar = getpass.getpass("Confirmar senha: ")
            if len(senha) < 6:
                print("A senha deve ter no mínimo 6 caracteres!")
            elif senha != confirmar:
                print("As senhas não coincidem!")
            else:
                break
        
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha_hash, tipo) VALUES (?, ?, ?, 'aluno')",
                (nome, email, self.hash_senha(senha))
            )
            cursor.execute("INSERT INTO ranking (aluno_id, pontos) VALUES (?, 0)", (cursor.lastrowid,))
            conn.commit()
            print(f"\n✓ Aluno {nome} registrado com sucesso!")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao registrar aluno: {e}")
            return False
        finally:
            conn.close()
    
    def registrar_professor(self):
        print("\n=== REGISTRO DE PROFESSOR ===")
        nome = input("Nome completo: ").strip()
        email = input("Email institucional: ").strip()
        
        if "@escola.com" not in email:
            print("Por favor, use email institucional (@escola.com)")
            return False
        
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()
        if cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,)).fetchone():
            print("Email já cadastrado!")
            conn.close()
            return False
        
        while True:
            senha = getpass.getpass("Senha (mínimo 8 caracteres): ")
            confirmar = getpass.getpass("Confirmar senha: ")
            if len(senha) < 8: print("A senha deve ter no mínimo 8 caracteres!")
            elif senha != confirmar: print("As senhas não coincidem!")
            else: break
        
        if input("Código de acesso especial: ") != "PROF123":
            print("Código de acesso inválido!")
            conn.close()
            return False
        
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha_hash, tipo) VALUES (?, ?, ?, 'professor')",
                (nome, email, self.hash_senha(senha))
            )
            conn.commit()
            print(f"\n✓ Professor {nome} registrado com sucesso!")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao registrar professor: {e}")
            return False
        finally:
            conn.close()
    
    def registrar_coordenador(self):
        print("\n=== REGISTRO DE COORDENADOR ===")
        nome = input("Nome completo: ").strip()
        email = input("Email institucional: ").strip()
        
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()
        if cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,)).fetchone():
            print("Email já cadastrado!")
            conn.close()
            return False
        
        while True:
            senha = getpass.getpass("Senha (mínimo 10 caracteres): ")
            confirmar = getpass.getpass("Confirmar senha: ")
            if len(senha) < 10: print("A senha deve ter no mínimo 10 caracteres!")
            elif senha != confirmar: print("As senhas não coincidem!")
            else: break
        
        if getpass.getpass("Código de acesso de administrador: ") != "ADMIN789":
            print("Código de acesso inválido!")
            conn.close()
            return False
        
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha_hash, tipo) VALUES (?, ?, ?, 'coordenador')",
                (nome, email, self.hash_senha(senha))
            )
            conn.commit()
            print(f"\n✓ Coordenador {nome} registrado com sucesso!")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao registrar coordenador: {e}")
            return False
        finally:
            conn.close()
    
    def login(self):
        print("\n=== LOGIN ===")
        email = input("Email: ").strip()
        senha = getpass.getpass("Senha: ")
        
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, senha_hash, tipo FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conn.close()
        
        if not usuario:
            print("Email não encontrado!")
            return None
        
        usuario_id, nome, senha_hash, tipo = usuario
        if self.hash_senha(senha) != senha_hash:
            print("Senha incorreta!")
            return None
        
        self.usuario_logado = {'id': usuario_id, 'nome': nome, 'email': email, 'tipo': tipo}
        print(f"\n✓ Login bem-sucedido! Bem-vindo(a), {nome}!")
        return self.usuario_logado
    
    def logout(self):
        if self.usuario_logado:
            print(f"\nAté logo, {self.usuario_logado['nome']}!")
            self.usuario_logado = None
        return True
    
    # ========== FUNÇÕES DE ALUNO ==========
    def adicionar_tarefa(self):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'aluno':
            print("Acesso negado!"); return False
        
        descricao = input("\n=== ADICIONAR TAREFA ===\nDigite a descrição: ").strip()
        if not descricao: print("Descrição não pode ser vazia!"); return False
        
        conn = sqlite3.connect('escola.db')
        try:
            conn.execute(
                "INSERT INTO tarefas (aluno_id, descricao) VALUES (?, ?)",
                (self.usuario_logado['id'], descricao)
            )
            conn.commit()
            print("✓ Tarefa adicionada com sucesso!")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao adicionar tarefa: {e}")
            return False
        finally:
            conn.close()
    
    def ver_minhas_tarefas(self):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'aluno':
            print("Acesso negado!"); return
        
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT descricao, data_criacao FROM tarefas 
            WHERE aluno_id = ? ORDER BY data_criacao DESC
        ''', (self.usuario_logado['id'],))
        
        print(f"\n=== SUAS TAREFAS ===")
        tarefas = cursor.fetchall()
        if tarefas:
            for i, (descricao, data) in enumerate(tarefas, 1):
                print(f"{i}. {descricao} ({data})")
        else:
            print("Você não tem tarefas cadastradas.")
        conn.close()
    
    def ver_meu_ranking(self):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'aluno':
            print("Acesso negado!"); return
        
        conn = sqlite3.connect('escola.db')
        pontos = conn.execute('SELECT pontos FROM ranking WHERE aluno_id = ?', 
                             (self.usuario_logado['id'],)).fetchone()
        conn.close()
        print(f"\nSeus pontos no ranking: {pontos[0]}" if pontos else "Você ainda não tem pontos no ranking.")
    
    # ========== FUNÇÕES DE PROFESSOR ==========
    def ver_ranking_alunos(self):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'professor':
            print("Acesso negado!"); return
        
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.nome, r.pontos FROM ranking r
            JOIN usuarios u ON r.aluno_id = u.id
            WHERE u.tipo = 'aluno' ORDER BY r.pontos DESC
        ''')
        
        print("\n=== RANKING DOS ALUNOS ===")
        resultados = cursor.fetchall()
        if resultados:
            for i, (aluno_nome, pontos) in enumerate(resultados, 1):
                print(f"{i}. {aluno_nome}: {pontos} pontos")
        else:
            print("Nenhum aluno no ranking ainda.")
        conn.close()
    
    def ver_materias(self):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'professor':
            print("Acesso negado!"); return
        
        conn = sqlite3.connect('escola.db')
        materias = conn.execute('SELECT nome FROM materias').fetchall()
        conn.close()
        
        print("\n=== MATÉRIAS DISPONÍVEIS ===")
        if materias:
            for materia in materias: print(f"- {materia[0]}")
        else: print("Nenhuma matéria cadastrada.")
    
    def adicionar_materia(self):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'professor':
            print("Acesso negado!"); return False
        
        nome = input("\n=== ADICIONAR MATÉRIA ===\nNome da nova matéria: ").strip()
        if not nome: print("Nome da matéria não pode ser vazio!"); return False
        
        conn = sqlite3.connect('escola.db')
        try:
            conn.execute(
                "INSERT INTO materias (nome, professor_id) VALUES (?, ?)",
                (nome, self.usuario_logado['id'])
            )
            conn.commit()
            print(f"✓ Matéria '{nome}' adicionada com sucesso!")
            return True
        except sqlite3.IntegrityError:
            print("Esta matéria já está cadastrada.")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao adicionar matéria: {e}")
            return False
        finally:
            conn.close()
    
    # ========== FUNÇÕES DE COORDENADOR ==========
    def ver_todos_alunos(self):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'coordenador':
            print("Acesso negado!"); return
        
        conn = sqlite3.connect('escola.db')
        alunos = conn.execute("SELECT nome, email, data_cadastro FROM usuarios WHERE tipo = 'aluno'").fetchall()
        conn.close()
        
        print("\n=== LISTA DE ALUNOS ===")
        if alunos:
            for nome, email, data in alunos:
                print(f"- {nome} ({email}) - Cadastrado em: {data}")
        else: print("Nenhum aluno cadastrado.")
    
    def ver_todos_professores(self):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'coordenador':
            print("Acesso negado!"); return
        
        conn = sqlite3.connect('escola.db')
        professores = conn.execute("SELECT nome, email, data_cadastro FROM usuarios WHERE tipo = 'professor'").fetchall()
        conn.close()
        
        print("\n=== LISTA DE PROFESSORES ===")
        if professores:
            for nome, email, data in professores:
                print(f"- {nome} ({email}) - Cadastrado em: {data}")
        else: print("Nenhum professor cadastrado.")
    
    def ver_todos_coordenadores(self):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'coordenador':
            print("Acesso negado!"); return
        
        conn = sqlite3.connect('escola.db')
        coordenadores = conn.execute("SELECT nome, email, data_cadastro FROM usuarios WHERE tipo = 'coordenador'").fetchall()
        conn.close()
        
        print("\n=== LISTA DE COORDENADORES ===")
        if coordenadores:
            for nome, email, data in coordenadores:
                print(f"- {nome} ({email}) - Cadastrado em: {data}")
        else: print("Nenhum coordenador cadastrado.")
    
    def adicionar_pontos(self):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'coordenador':
            print("Acesso negado!"); return False
        
        conn = sqlite3.connect('escola.db')
        alunos = conn.execute("SELECT nome FROM usuarios WHERE tipo = 'aluno'").fetchall()
        if not alunos: print("Nenhum aluno cadastrado."); conn.close(); return False
        
        print("\n=== ADICIONAR PONTOS ===\nAlunos disponíveis:")
        for aluno in alunos: print(f"- {aluno[0]}")
        
        aluno_escolhido = input("\nDigite o nome do aluno: ").strip()
        aluno_id = conn.execute("SELECT id FROM usuarios WHERE nome = ? AND tipo = 'aluno'", 
                               (aluno_escolhido,)).fetchone()
        
        if not aluno_id: print("Aluno não encontrado!"); conn.close(); return False
        
        try:
            pontos = int(input(f"Quantos pontos adicionar para {aluno_escolhido}? "))
            if pontos < 0: print("Os pontos devem ser um número positivo!"); conn.close(); return False
            
            conn.execute(
                'UPDATE ranking SET pontos = pontos + ? WHERE aluno_id = ?',
                (pontos, aluno_id[0])
            )
            conn.commit()
            print(f"✓ {pontos} pontos adicionados para {aluno_escolhido}!")
            return True
        except ValueError:
            print("Por favor, digite um número válido.")
            return False
        finally:
            conn.close()
    
    def alterar_senha(self):
        if not self.usuario_logado: print("Nenhum usuário logado!"); return False
        
        print(f"\n=== ALTERAR SENHA ===")
        senha_atual = getpass.getpass("Senha atual: ")
        
        conn = sqlite3.connect('escola.db')
        senha_hash = conn.execute("SELECT senha_hash FROM usuarios WHERE email = ?", 
                                 (self.usuario_logado['email'],)).fetchone()[0]
        
        if self.hash_senha(senha_atual) != senha_hash:
            print("Senha atual incorreta!"); conn.close(); return False
        
        while True:
            nova = getpass.getpass("Nova senha: ")
            confirmar = getpass.getpass("Confirmar nova senha: ")
            if nova != confirmar: print("As senhas não coincidem!")
            else: break
        
        conn.execute(
            "UPDATE usuarios SET senha_hash = ? WHERE email = ?",
            (self.hash_senha(nova), self.usuario_logado['email'])
        )
        conn.commit()
        conn.close()
        print("✓ Senha alterada com sucesso!")
        return True
    
    def remover_usuario(self):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'coordenador':
            print("Acesso negado!"); return False
        
        email = input("\n=== REMOVER USUÁRIO ===\nEmail do usuário: ").strip()
        if email == self.usuario_logado['email']:
            print("Você não pode remover a si mesmo!"); return False
        
        conn = sqlite3.connect('escola.db')
        usuario = conn.execute("SELECT nome, tipo FROM usuarios WHERE email = ?", (email,)).fetchone()
        if not usuario: print("Usuário não encontrado!"); conn.close(); return False
        
        nome, tipo = usuario
        if input(f"Tem certeza que deseja remover {nome} ({tipo})? (s/n): ").lower() != 's':
            print("Operação cancelada."); conn.close(); return False
        
        conn.execute("DELETE FROM usuarios WHERE email = ?", (email,))
        if tipo == 'aluno':
            conn.execute("DELETE FROM ranking WHERE aluno_id IN (SELECT id FROM usuarios WHERE email = ?)", (email,))
            conn.execute("DELETE FROM tarefas WHERE aluno_id IN (SELECT id FROM usuarios WHERE email = ?)", (email,))
        
        conn.commit()
        conn.close()
        print(f"✓ Usuário {nome} removido com sucesso!")
        return True
    
    def executar(self):
        while True:
            print("\n" + "="*50)
            print("           SISTEMA ESCOLAR")
            print("="*50)
            
            if not self.usuario_logado:
                print("1. Fazer Login")
                print("2. Registrar como Aluno")
                print("3. Registrar como Professor")
                print("4. Registrar como Coordenador")
                print("0. Sair do Sistema")
                
                escolha = input("\nEscolha uma opção: ")
                
                if escolha == "1": self.login()
                elif escolha == "2": self.registrar_aluno()
                elif escolha == "3": self.registrar_professor()
                elif escolha == "4": self.registrar_coordenador()
                elif escolha == "0": print("Saindo do sistema... Até logo!"); break
                else: print("Opção inválida!")
            
            else:
                tipo, nome = self.usuario_logado['tipo'], self.usuario_logado['nome']
                print(f"Usuário: {nome} ({tipo.upper()})\n" + "-"*50)
                
                if tipo == 'aluno':
                    print("1. Adicionar Tarefa\n2. Ver minhas Tarefas\n3. Ver meu Ranking\n4. Alterar Senha\n5. Logout")
                    escolha = input("\nEscolha uma opção: ")
                    if escolha == "1": self.adicionar_tarefa()
                    elif escolha == "2": self.ver_minhas_tarefas()
                    elif escolha == "3": self.ver_meu_ranking()
                    elif escolha == "4": self.alterar_senha()
                    elif escolha == "5": self.logout()
                    elif escolha == "0": print("Saindo do sistema... Até logo!"); break
                    else: print("Opção inválida!")
                
                elif tipo == 'professor':
                    print("1. Ver Ranking dos Alunos\n2. Ver Matérias\n3. Adicionar Matéria\n4. Alterar Senha\n5. Logout")
                    escolha = input("\nEscolha uma opção: ")
                    if escolha == "1": self.ver_ranking_alunos()
                    elif escolha == "2": self.ver_materias()
                    elif escolha == "3": self.adicionar_materia()
                    elif escolha == "4": self.alterar_senha()
                    elif escolha == "5": self.logout()
                    elif escolha == "0": print("Saindo do sistema... Até logo!"); break
                    else: print("Opção inválida!")
                
                elif tipo == 'coordenador':
                    print("1. Ver todos os Alunos\n2. Ver todos os Professores\n3. Ver todos os Coordenadores")
                    print("4. Adicionar pontos ao Ranking\n5. Alterar Senha\n6. Remover Usuário\n7. Logout")
                    escolha = input("\nEscolha uma opção: ")
                    if escolha == "1": self.ver_todos_alunos()
                    elif escolha == "2": self.ver_todos_professores()
                    elif escolha == "3": self.ver_todos_coordenadores()
                    elif escolha == "4": self.adicionar_pontos()
                    elif escolha == "5": self.alterar_senha()
                    elif escolha == "6": self.remover_usuario()
                    elif escolha == "7": self.logout()
                    elif escolha == "0": print("Saindo do sistema... Até logo!"); break
                    else: print("Opção inválida!")
            
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    SistemaEscolar().executar()