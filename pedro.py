#o Correspondência (ligar colunas) 
# def correspondecia (): 
    # id_curso=int(input("Digite o identificador (ID) do curso: "))
    # questão=input("Digite o enunciado da atividade: ")
    # pares = input("Digite os pares (ex: A-1; B-2; C-3)")
    # resposta_correta= pares
    # dica=input("Digite a dica: ")
    # pontuacao = 1 
    # cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, opcoes, resposta_correta, dica, pontuacao))
    # conexao.commit()



#o Classificação (separar categorias)
#  def classificacao (): 
    #  id_curso=int(input("Digite o identificador (ID) do curso: "))
    #  questão=input("Digite o enunciado da atividade: ")
    #  categorias = input("Digite categorias e itens (ex: Inteiro = 11 ,256 ; Racionais : 3.78 , 4/2 ;)")
    #  resposta_correta = categorias
    #  dica = input("Digite a dica: ")
    #  pontuacao= 1 
    #  cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, opcoes, resposta_correta, dica, pontuacao))
    #  conexao.commit()




#o Escolha múltipla (várias corretas)
#  def escolha_multipla():
    # id_curso=int(input("Digite o identificador (ID) do curso: "))
    #  questão=input("Digite o enunciado da atividade: ")
    #  opcao_a = input("Digite a "A" opção : ")
    #  opcao_b = input("Digite a "B" opção : ")
    #  opcao_c = input("Digite a "C" opção : ")
    #  opcao_d = input("Digite a "D" opção : ")
    #  opcao_e = input("Digite a "E" opção : ")
    #  resposta_correta=input("Digite as alternativas certas (ex: A,C) : ")
    #  dica=input("Digite a dica: ")
    #  pontuacao= 1 
    #  cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, opcoes, resposta_correta, dica, pontuacao))
    #  cursor.execute('''INSET INTO opcoes(acoes)) 
    # conexao.commit()




#o Palavra embaralhada
# def palavra_embralhada():
    # id_curso=int(input("Digite o identificador (ID) do curso: "))
    # palavra = input("Digite a palvara correrta : ")
    # embralhada = input("Digite a palavra embralhada : ")
    # pergunta = f"Desembralhe a palavra {embralhada}: "
    # dica=input("Digite a dica: ")
    # pontuacao = 1 
    # cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, opcoes, resposta_correta, dica, pontuacao))
    # conexao.commit()





#o Mini-cenários com decisões
# def mini_cenarios():
    #  id_curso=int(input("Digite o identificador (ID) do curso: "))
    #  cenario=input("Digite o cénario : ")
    #  decisoes = input("Digite as decisões que o aluno pode tomar : ")
    #  resposta_correta=input("Digite a decisão certa : ")
    #  dica=input("Digite a dica: ")
    #  pontuacao = 1
    #  cursor.execute('''INSET INTO atividades(cursor_id, perguntas, opcoes, resposta_correta, dica, pontuacoes) VALUES (?, ?, ?, ?, ?, ?)''', (id_curso, questão, opcoes, resposta_correta, dica, pontuacao))
    #  conexao.commit()