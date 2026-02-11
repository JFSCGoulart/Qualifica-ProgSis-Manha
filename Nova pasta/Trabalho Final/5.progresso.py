# Aluno

def ver_progresso_usuario(id_usuario):
    from datetime import date
    
    cursor.execute("""
        SELECT 
            curso.nome,
            COUNT(CASE WHEN progresso.acertou = 1 THEN 1 END) as estrelas,
            COUNT(progresso.id) as atividades_feitas,
            SUM(CASE WHEN progresso.data = ? THEN 1 ELSE 0 END) as atividades_hoje
        FROM usuario
        JOIN usuario_curso ON usuario.id = usuario_curso.id_usuario
        JOIN curso ON usuario_curso.id_curso = curso.id
        LEFT JOIN modulo ON curso.id = modulo.id_curso
        LEFT JOIN progresso ON usuario.id = progresso.id_usuario
        WHERE usuario.id = ?
        GROUP BY curso.id, curso.nome
    """, (str(date.today()), id_usuario))
    resultados = cursor.fetchall()
    
    if not resultados:
        print("Você ainda não está matriculado em nenhum curso.")
        return
    
    print("📊 SEU PROGRESSO:")
    for nome_curso, estrelas, atividades_feitas, atividades_hoje in resultados:
        print(f"\n🎓 Curso: {nome_curso}")
        print(f"   ⭐ Estrelas: {estrelas if estrelas else 0}")
        print(f"   📝 Atividades Feitas (Total): {atividades_feitas if atividades_feitas else 0}")
        print(f"   📅 Atividades Feitas (Hoje): {atividades_hoje if atividades_hoje else 0}")
        
def resetar_progresso(id_usuario):
    print("⚠️ Tem certeza que deseja resetar seu progresso?")
    print("1 - SIM")
    print("2 - NÃO")
    
    confirmacao = input("Escolha: ")
    
    if confirmacao == "1":
        cursor.execute("""
            DELETE FROM progresso
            WHERE id_usuario = ?
        """, (id_usuario,))
        
        cursor.execute("""
            UPDATE vidas_curso
            SET vidas_restantes = 3
            WHERE id_usuario = ?
        """, (id_usuario,))
        
        conexao.commit()
        print("✅ Seu progresso foi resetado com sucesso!")
    else:
        print("❌ Operação cancelada.")

def ver_ranking_top3():
    cursor.execute("""
        SELECT 
            usuario.nome_completo,
            COUNT(CASE WHEN progresso.acertou = 1 THEN 1 END) as total_estrelas,
            COUNT(progresso.id) as total_atividades
        FROM usuario
        JOIN progresso ON usuario.id = progresso.id_usuario
        WHERE usuario.tipo_usuario = 'ALUNO'
        GROUP BY usuario.id, usuario.nome_completo
        ORDER BY total_estrelas DESC
        LIMIT 3
    """)
    resultados = cursor.fetchall()
    print("🏆 TOP 3 MELHORES ALUNOS:")

    
    if not resultados:
        print("Nenhum aluno com progresso ainda.")
    else:
        for posicao, (nome, total_estrelas, total_atividades) in enumerate(resultados, 1):
            medalhas = ["🥇", "🥈", "🥉"]
            print(f"\n{medalhas[posicao-1]} {posicao}º - {nome}")
            print(f"   ⭐ Estrelas: {total_estrelas}")
            print(f"   📝 Atividades: {total_atividades}")
    
# Coordenador 

def ver_ranking_completo():
    cursor.execute("""
        SELECT 
            usuario.nome_completo,
            curso.nome,
            COUNT(CASE WHEN progresso.acertou = 1 THEN 1 END) as estrelas,
            COUNT(progresso.id) as atividades_feitas
        FROM usuario
        JOIN usuario_curso ON usuario.id = usuario_curso.id_usuario
        JOIN curso ON usuario_curso.id_curso = curso.id
        LEFT JOIN modulo ON curso.id = modulo.id_curso
        LEFT JOIN progresso ON usuario.id = progresso.id_usuario
        WHERE usuario.tipo_usuario = 'ALUNO'
        GROUP BY usuario.id, curso.id
        ORDER BY curso.nome, estrelas DESC
    """)
    resultados = cursor.fetchall()
    
    if not resultados:
        print("Nenhum aluno com progresso ainda.")
        return
    
    print("🏆 RANKING COMPLETO DA TURMA:")
    for nome, curso, estrelas, atividades in resultados:
        print(f"\nAluno: {nome} | Curso: {curso} | Estrelas: {estrelas} | Atividades Feitas: {atividades}")

def desempenho_por_curso():
    cursor.execute("""
        SELECT 
            curso.nome,
            COUNT(CASE WHEN progresso.acertou = 1 THEN 1 END) as acertos,
            COUNT(progresso.id) as total_atividades,
            ROUND((COUNT(CASE WHEN progresso.acertou = 1 THEN 1 END) * 100.0) / NULLIF(COUNT(progresso.id), 0), 2) as percentual_acerto
        FROM curso
        LEFT JOIN modulo ON curso.id = modulo.id_curso
        LEFT JOIN atividade ON modulo.id = atividade.id_modulo
        LEFT JOIN progresso ON atividade.id = progresso.id_atividade
        GROUP BY curso.id, curso.nome
    """)
    resultados = cursor.fetchall()
    
    print("\n📊 DESEMPENHO POR CURSO:")
    for nome_curso, acertos, total, percentual in resultados:
        print(f"\nCurso: {nome_curso} | Acertos: {acertos} | Total Atividades: {total} | Percentual de Acerto: {percentual}%")
