import sqlite3

# ===============================
# CONEXÃO COM O BANCO
# ===============================
conn = sqlite3.connect("qualifica.db")
cursor = conn.cursor()

# ===============================
# CRIAÇÃO DAS TABELAS
# ===============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS curso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS modulo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    curso_id INTEGER,
    FOREIGN KEY (curso_id) REFERENCES curso(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS atividade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    modulo_id INTEGER,
    FOREIGN KEY (modulo_id) REFERENCES modulo(id)
)
""")

conn.commit()

# ===============================
# FUNÇÕES DE MENU
# ===============================
def menu_principal():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Cursos")
        print("2 - Progresso (em breve)")
        print("3 - Ranking (em breve)")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            menu_cursos()
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

def menu_cursos():
    cursor.execute("SELECT id, nome FROM curso")
    cursos = cursor.fetchall()

    print("\n=== CURSOS DISPONÍVEIS ===")
    for c in cursos:
        print(f"{c[0]} - {c[1]}")

    curso_id = input("Selecione o curso (0 para voltar): ")

    if curso_id == "0":
        return
    else:
        menu_modulos(curso_id)

def menu_modulos(curso_id):
    cursor.execute(
        "SELECT id, nome FROM modulo WHERE curso_id = ?", (curso_id,)
    )
    modulos = cursor.fetchall()

    print("\n=== MÓDULOS ===")
    for m in modulos:
        print(f"{m[0]} - {m[1]}")

    modulo_id = input("Selecione o módulo (0 para voltar): ")

    if modulo_id == "0":
        return
    else:
        menu_atividades(modulo_id)

def menu_atividades(modulo_id):
    cursor.execute(
        "SELECT id, nome FROM atividade WHERE modulo_id = ?", (modulo_id,)
    )
    atividades = cursor.fetchall()

    print("\n=== ATIVIDADES ===")
    for a in atividades:
        print(f"{a[0]} - {a[1]}")

    input("Selecione uma atividade e pressione ENTER para concluir.")
    print("✅ Atividade concluída!\n")

# ===============================
# DADOS INICIAIS (SE VAZIO)
# ===============================
cursor.execute("SELECT COUNT(*) FROM curso")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO curso (nome) VALUES ('Lógica de Programação')")
    cursor.execute("INSERT INTO modulo (nome, curso_id) VALUES ('Variáveis', 1)")
    cursor.execute("INSERT INTO atividade (nome, modulo_id) VALUES ('Exercício 1', 1)")
    conn.commit()

# ===============================
# EXECUÇÃO
# ===============================
menu_principal()
conn.close()