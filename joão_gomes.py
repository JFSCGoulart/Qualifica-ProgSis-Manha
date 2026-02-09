import sqlite3
from datetime import datetime

PENALIDADE_POR_DICA = 5

class QuizHistorico:
    def __init__(self, player, tema):
        self.player = player
        self.tema = tema
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M") #data atual
        self.perguntas = 0
        self.acertos = 0
        self.erros = 0
        self.puladas = 0
        self.pontos = 0
        self.dicas = 0
        self.penalidade = 0

    def responder(self, correta: bool): #(pontuação)
        self.perguntas += 1
        if correta:
            self.acertos += 1
        else:
            self.erros += 1

    def pontuar(self, pontos: int):
        self.pontos += pontos

    def usar_dica(self):
        self.dicas += 1

    def aplicar_penalidade(self):
        excesso = max(0, self.dicas - 3)
        self.penalidade = excesso * PENALIDADE_POR_DICA
        self.pontos = max(0, self.pontos - self.penalidade)

    def exibir(self):
        print(f"""
player: {self.player}
Tema: {self.tema}
Data: {self.data}
-------------------------
Perguntas: {self.perguntas}
Acertos: {self.acertos}
Erros: {self.erros}
Puladas: {self.puladas}
Dicas usadas: {self.dicas}
Penalidade: {self.penalidade}
Total de pontos: {self.pontos}
""")

# parte do banco de dados abaixo
import sqlite3

class HistoricoDB:
    def __init__(self, arquivo="historico_quiz.db"):
        self.arquivo = arquivo
        self._criar_tabela()

    def _conectar(self):
        return sqlite3.connect(self.arquivo)

    def _criar_tabela(self):
        with self._conectar() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT,
                tema TEXT,
                data TEXT,
                perguntas INTEGER,
                acertos INTEGER,
                erros INTEGER,
                puladas INTEGER,
                pontos INTEGER,
                dicas INTEGER,
                penalidade INTEGER
            )
            """)

    def salvar(self, h: QuizHistorico):
        with self._conectar() as conn:
            conn.execute("""
            INSERT INTO historico (
                player, tema, data, perguntas, acertos, erros,
                puladas, pontos, dicas, penalidade
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                h.player,
                h.tema,
                h.data,
                h.perguntas,
                h.acertos,
                h.erros,
                h.puladas,
                h.pontos,
                h.dicas,
                h.penalidade
            ))

    def listar(self):
        with self._conectar() as conn:
            return conn.execute("SELECT * FROM historico").fetchall()
db = HistoricoDB()

jogo = QuizHistorico("João", "Python")

jogo.responder(True)
jogo.pontuar(10)

jogo.responder(False)

jogo.responder(True)
jogo.pontuar(10)

jogo.usar_dica()
jogo.usar_dica()
jogo.usar_dica()
jogo.usar_dica()

jogo.aplicar_penalidade()
jogo.exibir()

db.salvar(jogo)










# Feito por: João Gomes Peixoto