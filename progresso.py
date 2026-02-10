import sqlite3
from datetime import datetime

PENALIDADE_POR_DICA = 5
PONTOS_ACERTO = 10

# ===============================
# MODELOS
# ===============================

class Aluno:
    def __init__(self, nome):
        self.nome = nome
        self.nota = 0

    def acertou(self):
        self.nota += 1

    def errou(self):
        if self.nota > 0:
            self.nota -= 1

    def estrelas(self):
        if self.nota <= 2:
            return "*"
        elif self.nota <= 5:
            return "**"
        return "***"

    def desempenho(self):
        if self.nota >= 6:
            return "EXCELENTE"
        elif self.nota >= 3:
            return "BOM"
        return "EM DESENVOLVIMENTO"


class Pergunta:
    def __init__(self, texto, resposta):
        self.texto = texto
        self.resposta = resposta.lower()

    def fazer(self):
        return input(self.texto + " ").strip().lower() == self.resposta


class QuizHistorico:
    def __init__(self, aluno, tema):
        self.aluno = aluno.nome
        self.tema = tema
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.perguntas = 0
        self.acertos = 0
        self.erros = 0
        self.pontos = 0
        self.dicas = 0
        self.penalidade = 0

    def responder(self, correta):
        self.perguntas += 1
        if correta:
            self.acertos += 1
            self.pontos += PONTOS_ACERTO
        else:
            self.erros += 1

    def usar_dica(self):
        self.dicas += 1

    def aplicar_penalidade(self):
        excesso = max(0, self.dicas - 3)
        self.penalidade = excesso * PENALIDADE_POR_DICA
        self.pontos = max(0, self.pontos - self.penalidade)


# ===============================
# BANCO DE DADOS UNIFICADO
# ===============================

class Database:
    def __init__(self, arquivo="quiz.db"):
        self.arquivo = arquivo
        self._criar_tabelas()

    def conectar(self):
        return sqlite3.connect(self.arquivo)

    def _criar_tabelas(self):
        with self.conectar() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                nome TEXT PRIMARY KEY,
                nota INTEGER
            )
            """)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno TEXT,
                tema TEXT,
                data TEXT,
                perguntas INTEGER,
                acertos INTEGER,
                erros INTEGER,
                pontos INTEGER,
                dicas INTEGER,
                penalidade INTEGER
            )
            """)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS ranking (
                usuario TEXT PRIMARY KEY,
                pontuacao INTEGER DEFAULT 0,
                nivel INTEGER DEFAULT 1,
                data_atualizacao TEXT
            )
            """)

    # ---------- ALUNO ----------
    def salvar_aluno(self, aluno):
        with self.conectar() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO alunos VALUES (?, ?)",
                (aluno.nome, aluno.nota)
            )

    # ---------- HISTÓRICO ----------
    def salvar_historico(self, h):
        with self.conectar() as conn:
            conn.execute("""
            INSERT INTO historico (
                aluno, tema, data, perguntas, acertos, erros,
                pontos, dicas, penalidade
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                h.aluno, h.tema, h.data, h.perguntas,
                h.acertos, h.erros, h.pontos,
                h.dicas, h.penalidade
            ))

    # ---------- RANKING ----------
    def atualizar_ranking(self, usuario, pontos):
        with self.conectar() as conn:
            conn.execute("""
            INSERT INTO ranking (usuario, pontuacao, nivel, data_atualizacao)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(usuario) DO UPDATE SET
                pontuacao = pontuacao + excluded.pontuacao,
                nivel = (pontuacao / 100) + 1,
                data_atualizacao = excluded.data_atualizacao
            """, (usuario, pontos, datetime.now().isoformat()))

    def get_ranking(self, limite=10):
        with self.conectar() as conn:
            return conn.execute("""
            SELECT usuario, pontuacao, nivel
            FROM ranking
            ORDER BY pontuacao DESC
            LIMIT ?
            """, (limite,)).fetchall()


# ===============================
# JOGO
# ===============================

def jogar():
    db = Database()
    nome = input("Digite seu nome: ")
    aluno = Aluno(nome)


    historico = QuizHistorico(aluno, "Programação")

    for p in perguntas:
        if p.fazer():
            aluno.acertou()
            historico.responder(True)
        else:
            aluno.errou()
            historico.responder(False)

    historico.usar_dica()
    historico.usar_dica()
    historico.usar_dica()
    historico.usar_dica()

    historico.aplicar_penalidade()

    db.salvar_aluno(aluno)
    db.salvar_historico(historico)
    db.atualizar_ranking(nome, historico.pontos)

    print("\nRESULTADO FINAL")
    print(f"Aluno: {aluno.nome}")
    print(f"Nota: {aluno.nota}")
    print(f"Estrelas: {aluno.estrelas()}")
    print(f"Pontos: {historico.pontos}")
    print(f"Desempenho: {aluno.desempenho()}")

    print("\n🏆 RANKING TOP 5")
    for i, r in enumerate(db.get_ranking(5), 1):
        print(f"{i}. {r[0]} - {r[1]} pts (Nível {r[2]})")


if __name__ == "__main__":
    jogar()
