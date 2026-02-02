from datetime import datetime

PENALIDADE_POR_DICA = 5


def criar_historico(jogador, tema):
    return {
        "jogador": jogador,
        "tema": tema,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "perguntas": 0,
        "acertos": 0,
        "erros": 0,
        "puladas": 0,
        "pontos": 0,
        "dicas": 0,
        "penalidade": 0
    }


def responder(h, correta):
    h["perguntas"] += 1
    h["acertos"] += correta
    h["erros"] += not correta


def pontuar(h, pontos):
    h["pontos"] += pontos


def dica(h):
    h["dicas"] += 1


def aplicar_penalidade(h):
    excesso = max(0, h["dicas"] - 3)
    h["penalidade"] = excesso * PENALIDADE_POR_DICA
    h["pontos"] = max(0, h["pontos"] - h["penalidade"])


def mostrar(h):
    print(f"""
Jogador: {h['jogador']}
Tema: {h['tema']}
Data: {h['data']}
-------------------------
Perguntas: {h['perguntas']}
Acertos: {h['acertos']}
Erros: {h['erros']}
Puladas: {h['puladas']}
Dicas usadas: {h['dicas']}
Penalidade: {h['penalidade']}
Pontos finais: {h['pontos']}
""")