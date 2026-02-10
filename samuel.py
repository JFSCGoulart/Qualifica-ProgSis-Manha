import sqlite3
import datetime

class SistemaRanking:
    def __init__(self, db_nome="ranking.db"):
        self.db_nome = db_nome
        self.inicializar()
    
    def conectar(self):
        return sqlite3.connect(self.db_nome)
    
    def inicializar(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ranking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    pontuacao INTEGER DEFAULT 0,
                    nivel INTEGER DEFAULT 1,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def registrar_usuario(self, usuario):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT OR IGNORE INTO ranking (usuario) VALUES (?)', (usuario,))
                conn.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def apagar_pontuacao(self, usuario=None):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                
                if usuario:
                    cursor.execute('SELECT id FROM ranking WHERE usuario = ?', (usuario,))
                    if not cursor.fetchone():
                        return {'sucesso': False, 'mensagem': f'Usuário "{usuario}" não encontrado', 'afetados': 0}
                    
                    cursor.execute('UPDATE ranking SET pontuacao = 0, data_atualizacao = ? WHERE usuario = ?', 
                        (datetime.datetime.now(), usuario))
                    afetados = cursor.rowcount
                    msg = f'Pontuação de "{usuario}" zerada'
                else:
                    cursor.execute('UPDATE ranking SET pontuacao = 0, data_atualizacao = ?', 
                        (datetime.datetime.now(),))
                    cursor.execute('SELECT COUNT(*) FROM ranking')
                    afetados = cursor.fetchone()[0]
                    msg = f'Todas as pontuações ({afetados} usuários) zeradas'
                
                conn.commit()
                return {'sucesso': True, 'mensagem': msg, 'afetados': afetados}
        except Exception as e:
            return {'sucesso': False, 'mensagem': f'Erro: {e}', 'afetados': 0}
    
    def atualizar_pontuacao(self, usuario, pontos, operacao="+"):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                if operacao == "+":
                    cursor.execute('UPDATE ranking SET pontuacao = pontuacao + ?, data_atualizacao = ? WHERE usuario = ?',
                            (pontos, datetime.datetime.now(), usuario))
                elif operacao == "-":
                    cursor.execute('UPDATE ranking SET pontuacao = pontuacao - ?, data_atualizacao = ? WHERE usuario = ?',
                            (pontos, datetime.datetime.now(), usuario))
                else:
                    return False
                conn.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def definir_pontuacao(self, usuario, pontuacao):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE ranking SET pontuacao = ?, data_atualizacao = ? WHERE usuario = ?',
                        (pontuacao, datetime.datetime.now(), usuario))
                conn.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def atualizar_nivel(self, usuario, nivel):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE ranking SET nivel = ?, data_atualizacao = ? WHERE usuario = ?',
                    (nivel, datetime.datetime.now(), usuario))
                conn.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def get_ranking(self, limite=10, ordenar_por="pontuacao"):
        with self.conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            coluna = "pontuacao" if ordenar_por == "pontuacao" else "nivel"
            
            cursor.execute(f'''
                SELECT ROW_NUMBER() OVER (ORDER BY {coluna} DESC) as posicao,
                usuario, pontuacao, nivel, data_atualizacao
                FROM ranking
                ORDER BY {coluna} DESC
                LIMIT ?
            ''', (limite,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_posicao(self, usuario, ordenar_por="pontuacao"):
        with self.conectar() as conn:
            cursor = conn.cursor()
            coluna = "pontuacao" if ordenar_por == "pontuacao" else "nivel"
            
            cursor.execute(f'''
                SELECT posicao FROM (
                    SELECT usuario, ROW_NUMBER() OVER (ORDER BY {coluna} DESC) as posicao
                    FROM ranking
                ) WHERE usuario = ?
            ''', (usuario,))
            
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    
    def get_usuario(self, usuario):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT usuario, pontuacao, nivel, data_atualizacao FROM ranking WHERE usuario = ?', (usuario,))
            resultado = cursor.fetchone()
            if resultado:
                return {
                    'usuario': resultado[0], 
                    'pontuacao': resultado[1], 
                    'nivel': resultado[2], 
                    'data_atualizacao': resultado[3]
                }
            return None
    
    def remover_usuario(self, usuario):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM ranking WHERE usuario = ?', (usuario,))
                conn.commit()
                return cursor.rowcount > 0
        except:
            return False
    
    def resetar(self):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM ranking')
                conn.commit()
                return True
        except:
            return False
    
    def estatisticas(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            
            cursor.execute
            ('SELECT COUNT(*) FROM ranking')
            total = cursor.fetchone()[0]
            
            cursor.execute
            ('SELECT AVG(pontuacao) FROM ranking')
            media = round(cursor.fetchone()[0] or 0, 2)
            
            cursor.execute
            ('SELECT MAX(pontuacao) FROM ranking')
            maximo = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT usuario, pontuacao FROM ranking ORDER BY pontuacao DESC LIMIT 1')
            top = cursor.fetchone()
            
            return {
                'total_usuarios': total,
                'media_pontuacao': media,
                'maxima_pontuacao': maximo,
                'top_usuario': {'usuario': top[0], 'pontuacao': top[1]} if top else None
            }
    
    def menu_interativo(self):
        """Menu interativo para testar o sistema"""
        while True:
            print("\n" + "="*50)
            print("SISTEMA DE RANKING")
            print("="*50)
            print("1. Registrar usuário")
            print("2. Ver ranking")
            print("3. Apagar pontuação")
            print("4. Estatísticas")
            print("5. Sair")
            print("-"*50)
            
            opcao = input("Opção: ")
            
            if opcao == "1":
                usuario = input("Nome do usuário: ")
                if self.registrar_usuario(usuario):
                    print(f"✓ Usuário '{usuario}' registrado")
                else:
                    print("✗ Erro ao registrar")
            
            elif opcao == "2":
                ranking = self.get_ranking(10)
                print("\n--- TOP 10 ---")
                for jogador in ranking:
                    print(f"{jogador['posicao']}. {jogador['usuario']} - {jogador['pontuacao']} pts (Nível: {jogador['nivel']})")
            
            elif opcao == "3":
                print("\n1. Zerar usuário específico")
                print("2. Zerar todos")
                sub_op = input("Opção: ")
                
                if sub_op == "1":
                    usuario = input("Usuário: ")
                    resultado = self.apagar_pontuacao(usuario)
                    print(f"✓ {resultado['mensagem']}")
                elif sub_op == "2":
                    confirmar = input("Tem certeza? (s/n): ")
                    if confirmar.lower() == 's':
                        resultado = self.apagar_pontuacao()
                        print(f"✓ {resultado['mensagem']}")
                else:
                    print("Opção inválida")
            
            elif opcao == "4":
                stats = self.estatisticas()
                print("\n--- ESTATÍSTICAS ---")
                for chave, valor in stats.items():
                    if valor:
                        print(f"{chave.replace('_', ' ').title()}: {valor}")
            
            elif opcao == "5":
                print("Saindo...")
                break
            
            else:
                print("Opção inválida")
            
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    sistema = SistemaRanking()
    
    print("=== CONFIGURANDO DADOS DE TESTE ===")
    
    usuarios_teste = ["Alice", "Bob", "Carlos", "Diana", "Eduardo"]
    for usuario in usuarios_teste:
        sistema.registrar_usuario(usuario)
        print(f"Registrado: {usuario}")
    
    import random
    for usuario in usuarios_teste:
        pontos = random.randint(50, 200)
        sistema.definir_pontuacao(usuario, pontos)
        nivel = random.randint(1, 10)
        sistema.atualizar_nivel(usuario, nivel)
        print(f"{usuario}: {pontos} pontos, nível {nivel}")
    
    print("\n" + "="*50)
    print("DADOS DE TESTE PRONTOS!")
    print("="*50)
    
    sistema.menu_interativo()