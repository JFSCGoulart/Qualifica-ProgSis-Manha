# ===============================
# MINI-GAME EDUCACIONAL COM ESTRELAS E SQLITE
# ===============================

import sqlite3

class Aluno:
    def __init__(self, nome):
        self.nome = nome
        self.nota = 0
        self.id = None

    def acertou(self):
        self.nota += 1

    def errou(self):
        if self.nota > 0:
            self.nota -= 1

    def estrelas(self):
        if self.nota <= 1:
            return "*"
        elif self.nota <= 3:
            return "**"
        elif self.nota <= 5:
            return "***"
        elif self.nota <= 7:
            return "****"
        else:
            return "*****"

    def desempenho(self):
        if self.nota >= 8:
            return "EXCELENTE"
        elif self.nota >= 5:
            return "BOM"
        else:
            return "EM DESENVOLVIMENTO"


class Pergunta:
    def __init__(self, texto, resposta):
        self.texto = texto
        self.resposta = resposta.lower()

    def fazer(self):
        resposta_usuario = input(self.texto + " ").strip().lower()
        return resposta_usuario == self.resposta


class DatabaseManager:
    def __init__(self, db_name="alunos.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Inicializa o banco de dados e cria tabelas se não existirem"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabela de alunos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                nota INTEGER DEFAULT 0,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def salvar_aluno(self, aluno):
        """Salva ou atualiza um aluno no banco de dados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # Verifica se o aluno já existe
            cursor.execute("SELECT id, nota FROM alunos WHERE nome = ?", (aluno.nome,))
            resultado = cursor.fetchone()
            
            if resultado:
                # Atualiza aluno existente
                aluno.id, nota_existente = resultado
                cursor.execute(
                    "UPDATE alunos SET nota = ? WHERE id = ?",
                    (aluno.nota, aluno.id)
                )
            else:
                # Insere novo aluno
                cursor.execute(
                    "INSERT INTO alunos (nome, nota) VALUES (?, ?)",
                    (aluno.nome, aluno.nota)
                )
                aluno.id = cursor.lastrowid
            
            conn.commit()
            print("Progresso salvo no banco de dados!")
            
        except sqlite3.Error as e:
            print(f"Erro ao salvar no banco de dados: {e}")
        finally:
            conn.close()

    def carregar_aluno(self, nome):
        """Carrega um aluno do banco de dados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nome, nota FROM alunos WHERE nome = ?", (nome,))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            aluno_id, aluno_nome, nota = resultado
            aluno = Aluno(aluno_nome)
            aluno.id = aluno_id
            aluno.nota = nota
            return aluno
        return None

    def resetar_aluno(self, nome):
        """Reseta as estrelas de um aluno no banco de dados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE alunos SET nota = 0 WHERE nome = ?",
                (nome,)
            )
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                return True
            else:
                conn.close()
                return False
                
        except sqlite3.Error:
            conn.close()
            return False


# ===============================
# FUNÇÕES DO MENU
# ===============================

def exibir_menu():
    """Exibe o menu principal"""
    print("\n" + "="*40)
    print("MENU PRINCIPAL - MINI-GAME EDUCATIVO")
    print("="*40)
    print("1. Jogar novo quiz")
    print("2. Continuar de onde parou")
    print("3. Resetar minhas estrelas")
    print("4. Sair")
    print("="*40)

def jogar_quiz(aluno, db_manager):
    """Executa o quiz para um aluno"""
    perguntas = [
        Pergunta("Python é uma linguagem de programação? (sim/nao)", "sim"),
        Pergunta("JavaScript é banco de dados? (sim/nao)", "nao"),
        Pergunta("SQLite funciona sem internet? (sim/nao)", "sim"),
        Pergunta("HTML é uma linguagem de programação? (sim/nao)", "nao"),
        Pergunta("MySQL é um banco de dados relacional? (sim/nao)", "sim"),
    ]

    print(f"\nInicio do desafio para {aluno.nome}!")
    print(f"Nota atual: {aluno.nota} | Estrelas: {aluno.estrelas()}\n")

    for i, pergunta in enumerate(perguntas, 1):
        print(f"Pergunta {i}/{len(perguntas)}:")
        if pergunta.fazer():
            aluno.acertou()
            print("Resposta correta!")
        else:
            aluno.errou()
            print("Resposta incorreta!")

        print(f"Nota atual: {aluno.nota} | Estrelas: {aluno.estrelas()}\n")

    # Salva o resultado no banco de dados
    db_manager.salvar_aluno(aluno)

    # Mostra resultado final
    print("="*40)
    print("RESULTADO FINAL DO QUIZ")
    print("="*40)
    print(f"Aluno: {aluno.nome}")
    print(f"Nota final: {aluno.nota}")
    print(f"Estrelas: {aluno.estrelas()}")
    print(f"Desempenho: {aluno.desempenho()}")
    print("="*40)

def resetar_estrelas_menu(db_manager):
    """Menu para resetar estrelas"""
    print("\n" + "="*40)
    print("RESETAR ESTRELAS")
    print("="*40)
    nome = input("Digite seu nome para resetar as estrelas: ").strip()
    
    if nome:
        if db_manager.resetar_aluno(nome):
            print(f"Estrelas de {nome} foram resetadas com sucesso!")
            print("Voce pode agora jogar novamente comecando do zero.")
        else:
            print(f"Aluno '{nome}' nao encontrado no banco de dados.")
    else:
        print("Nome invalido!")

# ===============================
# EXECUÇÃO PRINCIPAL DO JOGO
# ===============================

def main():
    """Função principal do programa"""
    db_manager = DatabaseManager()
    
    print("="*50)
    print("BEM-VINDO AO MINI-GAME EDUCATIVO COM ESTRELAS!")
    print("="*50)
    
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opcao (1-4): ").strip()
        
        if opcao == "1":
            # Jogar novo quiz
            nome = input("\nDigite seu nome: ").strip()
            if nome:
                aluno = Aluno(nome)
                jogar_quiz(aluno, db_manager)
            else:
                print("Nome invalido!")
        
        elif opcao == "2":
            # Continuar de onde parou
            nome = input("\nDigite seu nome para continuar: ").strip()
            if nome:
                aluno = db_manager.carregar_aluno(nome)
                if aluno:
                    print(f"Aluno encontrado! Nota atual: {aluno.nota}")
                    jogar_quiz(aluno, db_manager)
                else:
                    print(f"Aluno '{nome}' nao encontrado.")
                    criar_novo = input("Deseja criar um novo aluno? (s/n): ").lower()
                    if criar_novo == 's':
                        aluno = Aluno(nome)
                        jogar_quiz(aluno, db_manager)
            else:
                print("Nome invalido!")
        
        elif opcao == "3":
            # Resetar estrelas
            resetar_estrelas_menu(db_manager)
        
        elif opcao == "4":
            # Sair
            print("\nObrigado por jogar! Ate a proxima!")
            break
        
        else:
            print("Opcao invalida! Escolha uma opcao de 1 a 4.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()