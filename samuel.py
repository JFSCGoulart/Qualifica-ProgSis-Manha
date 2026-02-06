import sqlite3
import datetime

def sistema_ranking(db_nome="ranking.db"):
    """
    Sistema de ranking integrado com SQLite3
    Parâmetros:
    db_nome (str): Nome do arquivo do banco de dados
    Retorna:
    dict: Dicionário com todas as funções do sistema
    """
    
    def conectar():
        """Estabelece conexão com o banco de dados"""
        return sqlite3.connect(db_nome)
    
    def inicializar():
        """Cria as tabelas necessárias se não existirem"""
        with conectar() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ranking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL,
                    pontuacao INTEGER DEFAULT 0,
                    nivel INTEGER DEFAULT 1,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(usuario)
                )
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_pontuacao 
                ON ranking(pontuacao DESC)
            ''')
            
            conn.commit()
    
    def registrar_usuario(usuario):
        """
        Registra um novo usuário no sistema de ranking
        Parâmetros:
        usuario (str): Nome do usuário
        Retorna:
        bool: True se bem-sucedido, False caso contrário
        """
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT OR IGNORE INTO ranking (usuario) VALUES (?)',
                    (usuario,)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False
    
    def atualizar_pontuacao(usuario, pontos, operacao="+"):
        """
        Atualiza a pontuação de um usuário
        Parâmetros:
        usuario (str): Nome do usuário
        pontos (int): Pontos a adicionar/subtrair
        operacao (str): "+" para adicionar, "-" para subtrair
        Retorna:
        bool: True se bem-sucedido, False caso contrário
        """
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM ranking WHERE usuario = ?', (usuario,))
                if not cursor.fetchone():
                    return False
                
                if operacao == "+":
                    cursor.execute('''
                        UPDATE ranking 
                        SET pontuacao = pontuacao + ?,
                        data_atualizacao = ?
                        WHERE usuario = ?
                    ''', (pontos, datetime.datetime.now(), usuario))
                
                elif operacao == "-":
                    cursor.execute('''
                        UPDATE ranking 
                        SET pontuacao = pontuacao - ?,
                        data_atualizacao = ?
                        WHERE usuario = ?
                    ''', (pontos, datetime.datetime.now(), usuario))
                else:
                    return False
                
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False
    
    def definir_pontuacao(usuario, pontuacao):
        """
        Define uma pontuação específica para um usuário
        Parâmetros:
        usuario (str): Nome do usuário
        pontuacao (int): Nova pontuação
    
        Retorna:
        bool: True se bem-sucedido, False caso contrário
        """
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE ranking 
                    SET pontuacao = ?,
                    data_atualizacao = ?
                    WHERE usuario = ?
                ''', (pontuacao, datetime.datetime.now(), usuario))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False
    
    def atualizar_nivel(usuario, nivel):
        """
        Atualiza o nível de um usuário

        Parâmetros:
        usuario (str): Nome do usuário
        nivel (int): Novo nível
        Retorna:
            bool: True se bem-sucedido, False caso contrário
        """
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE ranking 
                    SET nivel = ?,
                    data_atualizacao = ?
                    WHERE usuario = ?
                ''', (nivel, datetime.datetime.now(), usuario))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False
    
    def obter_ranking_top_n(limite=10, ordenar_por="pontuacao"):
        """
        Obtém o top N do ranking

        Parâmetros:
        limite (int): Quantidade de posições a retornar
        ordenar_por (str): "pontuacao" ou "nivel"

        Retorna:
        list: Lista de dicionários com posição, usuário e pontuação
        """
        with conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            coluna = "pontuacao" if ordenar_por == "pontuacao" else "nivel"
            ordem = "DESC"
            
            cursor.execute(f'''
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY {coluna} {ordem}) as posicao,
                    usuario,
                    pontuacao,
                    nivel,
                    data_atualizacao
                FROM ranking
                ORDER BY {coluna} {ordem}
                LIMIT ?
            ''', (limite,))
            
            resultados = cursor.fetchall()
            
            ranking = []
            for row in resultados:
                ranking.append({
                    'posicao': row['posicao'],
                    'usuario': row['usuario'],
                    'pontuacao': row['pontuacao'],
                    'nivel': row['nivel'],
                    'data_atualizacao': row['data_atualizacao']
                })
            
            return ranking
    
    def obter_posicao_usuario(usuario, ordenar_por="pontuacao"):
        """
        Obtém a posição específica de um usuário no ranking

        Parâmetros:
        usuario (str): Nome do usuário
        ordenar_por (str): "pontuacao" ou "nivel"

        Retorna:
        int or None: Posição no ranking ou None se não encontrado
        """
        with conectar() as conn:
            cursor = conn.cursor()
            
            coluna = "pontuacao" if ordenar_por == "pontuacao" else "nivel"
            ordem = "DESC"
            
            cursor.execute(f'''
                SELECT posicao FROM (
                    SELECT 
                    usuario,
                    ROW_NUMBER() OVER (ORDER BY {coluna} {ordem}) as posicao
                    FROM ranking
                ) WHERE usuario = ?
            ''', (usuario,))
            
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    
    def obter_pontuacao_usuario(usuario):
        """
        Obtém a pontuação e nível de um usuário específico

        Parâmetros:
        usuario (str): Nome do usuário

        Retorna:
        dict or None: Dados do usuário ou None se não encontrado
        """
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT usuario, pontuacao, nivel, data_atualizacao
                FROM ranking
                WHERE usuario = ?
            ''', (usuario,))
            
            resultado = cursor.fetchone()
            if resultado:
                return {
                    'usuario': resultado[0],
                    'pontuacao': resultado[1],
                    'nivel': resultado[2],
                    'data_atualizacao': resultado[3]
                }
            return None
    
    def remover_usuario(usuario):
        """             
        Remove um usuário do ranking

        Parâmetros:
        usuario (str): Nome do usuário

        Retorna:
        bool: True se bem-sucedido, False caso contrário
        """
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM ranking WHERE usuario = ?', (usuario,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False
    
    def resetar_ranking():
        """
        Reseta todo o ranking (remove todos os registros)

        Retorna:
        bool: True se bem-sucedido, False caso contrário
        """
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM ranking')
                conn.commit()
                return True
        except sqlite3.Error:
            return False
    
    def obter_estatisticas():
        """
        Obtém estatísticas gerais do ranking
        
        Retorna:
        dict: Dicionário com estatísticas
        """
        with conectar() as conn:
            cursor = conn.cursor()
            
            estatisticas = {}
            
            # Total de usuários
            cursor.execute('SELECT COUNT(*) FROM ranking')
            estatisticas['total_usuarios'] = cursor.fetchone()[0]
            
            # Pontuação média
            cursor.execute('SELECT AVG(pontuacao) FROM ranking')
            estatisticas['pontuacao_media'] = round(cursor.fetchone()[0] or 0, 2)
            
            # Pontuação máxima
            cursor.execute('SELECT MAX(pontuacao) FROM ranking')
            estatisticas['pontuacao_maxima'] = cursor.fetchone()[0] or 0
            
            # Usuário com maior pontuação
            cursor.execute('''
                SELECT usuario, pontuacao 
                FROM ranking 
                ORDER BY pontuacao DESC 
                LIMIT 1
            ''')
            resultado = cursor.fetchone()
            if resultado:
                estatisticas['top_usuario'] = {
                    'usuario': resultado[0],
                    'pontuacao': resultado[1]
                }
            
            return estatisticas
    
    def exportar_ranking_csv(arquivo="ranking_exportado.csv"):
        """
        Exporta o ranking completo para um arquivo CSV

        Parâmetros:
        arquivo (str): Nome do arquivo de saída

        Retorna:
        bool: True se bem-sucedido, False caso contrário
        """
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT usuario, pontuacao, nivel, data_atualizacao
                    FROM ranking
                    ORDER BY pontuacao DESC
                ''')
                
                resultados = cursor.fetchall()
                
                with open(arquivo, 'w', encoding='utf-8') as f:
                    # Cabeçalho
                    f.write("Posição,Usuário,Pontuação,Nível,Data Atualização\n")
                    
                    # Dados
                    for i, (usuario, pontuacao, nivel, data) in enumerate(resultados, 1):
                        f.write(f'{i},{usuario},{pontuacao},{nivel},{data}\n')
                
                return True
        except Exception:
            return False
    
    # Inicializa o banco de dados
    inicializar()
    
    # Retorna um dicionário com todas as funções
    return {
        'registrar_usuario': registrar_usuario,
        'atualizar_pontuacao': atualizar_pontuacao,
        'definir_pontuacao': definir_pontuacao,
        'atualizar_nivel': atualizar_nivel,
        'obter_ranking_top_n': obter_ranking_top_n,
        'obter_posicao_usuario': obter_posicao_usuario,
        'obter_pontuacao_usuario': obter_pontuacao_usuario,
        'remover_usuario': remover_usuario,
        'resetar_ranking': resetar_ranking,
        'obter_estatisticas': obter_estatisticas,
        'exportar_ranking_csv': exportar_ranking_csv
    }



if __name__ == "__main__":
    
    ranking = sistema_ranking()
    ranking['registrar_usuario']("jogador1")
    ranking['registrar_usuario']("jogador2")
    ranking['registrar_usuario']("jogador3")
    
    
    ranking['atualizar_pontuacao']("jogador1", 130, "+")
    ranking['atualizar_pontuacao']("jogador2", 150, "+")
    ranking['atualizar_pontuacao']("jogador3", 75, "+")
    
     
    ranking['atualizar_nivel']("jogador1", 5)
    ranking['atualizar_nivel']("jogador2", 3)
    ranking['atualizar_nivel']("jogador3", 8)
    

    print("=== TOP 10 RANKING ===")
    top_10 = ranking['obter_ranking_top_n'](10)
    for jogador in top_10:
        print(f"{jogador['posicao']}. {jogador['usuario']} - {jogador['pontuacao']} pontos (Nível: {jogador['nivel']})")
    
    
    print("\n=== POSIÇÃO DO JOGADOR 1 ===")
    posicao = ranking['obter_posicao_usuario']("jogador1")
    print(f"Jogador1 está na posição: {posicao}")
    
    
    print("\n=== ESTATÍSTICAS ===")
    stats = ranking['obter_estatisticas']()
    for chave, valor in stats.items():
        print(f"{chave}: {valor}")