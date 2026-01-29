# Fazer atividades variadas:

#o Múltipla escolha
#o Verdadeiro ou Falso
#o Preencher lacunas
#o Ordenar etapas
#o Sequências lógicas
#o Correspondência (ligar colunas)
#o Classificação (separar categorias)
#o Escolha múltipla (várias corretas)
#o Palavra embaralhada
#o Mini-cenários com decisões

#• Pedir dica antes de responder
#• Ganhar 1 estrela por acerto (sem penalidade por erro)
import sqlite3

conexao=sqlite3.connect('sistema.db')
cursor=conexao.cursor()

def multipla_escolha():
    id_curso=int(input("Digite o identificador (ID) do curso: "))
    questão=input("Digite o enunciado da atividade: ")
    cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, ))
    conexao.commit()