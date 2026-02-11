from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import sqlite3
import os
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'sistema_educacional_secret_key_2024'

DB_NAME = "sistema_educacional.db"

# ==================== BANCO DE DADOS ====================

def conectar():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('aluno', 'professor', 'coordenador')),
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            descricao TEXT,
            professor_id INTEGER,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (professor_id) REFERENCES usuarios(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            curso_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            pergunta TEXT NOT NULL,
            opcoes TEXT,
            resposta_correta TEXT NOT NULL,
            dica TEXT,
            professor_id INTEGER,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (curso_id) REFERENCES cursos(id),
            FOREIGN KEY (professor_id) REFERENCES usuarios(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progresso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            atividade_id INTEGER NOT NULL,
            acertou BOOLEAN NOT NULL,
            estrelas_ganhas INTEGER DEFAULT 0,
            data_resposta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (aluno_id) REFERENCES usuarios(id),
            FOREIGN KEY (atividade_id) REFERENCES atividades(id),
            UNIQUE(aluno_id, atividade_id)
        )
    ''')
    
    conn.commit()
    conn.close()

# ==================== DECORADORES ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def aluno_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('tipo') != 'aluno':
            flash('Acesso restrito a alunos!', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def professor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('tipo') != 'professor':
            flash('Acesso restrito a professores!', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def coordenador_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('tipo') != 'coordenador':
            flash('Acesso restrito a coordenadores!', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ROTAS PRINCIPAIS ====================

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nome, tipo FROM usuarios WHERE nome = ? AND senha = ?",
            (nome, senha)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['nome'] = user['nome']
            session['tipo'] = user['tipo']
            flash(f'Bem-vindo, {user["nome"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nome ou senha incorretos!', 'danger')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        tipo = request.form['tipo']
        
        conn = conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, senha, tipo) VALUES (?, ?, ?)",
                (nome, senha, tipo)
            )
            conn.commit()
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Nome de usuário já existe!', 'danger')
        finally:
            conn.close()
    
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    tipo = session['tipo']
    if tipo == 'aluno':
        return redirect(url_for('aluno_dashboard'))
    elif tipo == 'professor':
        return redirect(url_for('professor_dashboard'))
    else:
        return redirect(url_for('coordenador_dashboard'))

# ==================== ROTAS DO ALUNO ====================

@app.route('/aluno')
@login_required
@aluno_required
def aluno_dashboard():
    conn = conectar()
    cursor = conn.cursor()
    
    # Estatísticas
    cursor.execute("""
        SELECT COALESCE(SUM(estrelas_ganhas), 0) as total 
        FROM progresso WHERE aluno_id = ?
    """, (session['user_id'],))
    estrelas = cursor.fetchone()['total']
    
    hoje = date.today().isoformat()
    cursor.execute("""
        SELECT COUNT(*) as quantidade 
        FROM progresso 
        WHERE aluno_id = ? AND date(data_resposta) = ?
    """, (session['user_id'], hoje))
    atividades_hoje = cursor.fetchone()['quantidade']
    
    # Cursos disponíveis
    cursor.execute("SELECT COUNT(*) as total FROM cursos")
    total_cursos = cursor.fetchone()['total']
    
    # Atividades pendentes
    cursor.execute("""
        SELECT COUNT(*) as total FROM atividades 
        WHERE id NOT IN (SELECT atividade_id FROM progresso WHERE aluno_id = ?)
    """, (session['user_id'],))
    pendentes = cursor.fetchone()['total']
    
    # Ranking
    cursor.execute("""
        SELECT u.nome, COALESCE(SUM(p.estrelas_ganhas), 0) as total_estrelas
        FROM usuarios u
        LEFT JOIN progresso p ON u.id = p.aluno_id
        WHERE u.tipo = 'aluno'
        GROUP BY u.id, u.nome
        ORDER BY total_estrelas DESC
        LIMIT 3
    """)
    ranking = cursor.fetchall()
    
    conn.close()
    
    return render_template('aluno/dashboard.html', 
                         estrelas=estrelas, 
                         atividades_hoje=atividades_hoje,
                         total_cursos=total_cursos,
                         pendentes=pendentes,
                         ranking=ranking)

@app.route('/aluno/cursos')
@login_required
@aluno_required
def aluno_cursos():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.*, u.nome as professor_nome,
               (SELECT COUNT(*) FROM atividades WHERE curso_id = c.id) as total_atividades,
               (SELECT COUNT(*) FROM progresso p 
                JOIN atividades a ON p.atividade_id = a.id 
                WHERE a.curso_id = c.id AND p.aluno_id = ?) as atividades_feitas
        FROM cursos c
        LEFT JOIN usuarios u ON c.professor_id = u.id
        ORDER BY c.nome
    """, (session['user_id'],))
    
    cursos = cursor.fetchall()
    conn.close()
    
    return render_template('aluno/cursos.html', cursos=cursos)

@app.route('/aluno/atividade', methods=['GET', 'POST'])
@login_required
@aluno_required
def aluno_atividade():
    conn = conectar()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        atividade_id = request.form['atividade_id']
        resposta = request.form['resposta'].lower().strip()
        usou_dica = request.form.get('usou_dica') == 'true'
        
        # Busca atividade
        cursor.execute("SELECT * FROM atividades WHERE id = ?", (atividade_id,))
        atividade = cursor.fetchone()
        
        # Verifica resposta
        resposta_correta = atividade['resposta_correta'].lower().strip()
        acertou = resposta == resposta_correta
        
        # Registra progresso
        try:
            cursor.execute("""
                INSERT INTO progresso (aluno_id, atividade_id, acertou, estrelas_ganhas)
                VALUES (?, ?, ?, ?)
            """, (session['user_id'], atividade_id, acertou, 1 if acertou else 0))
            conn.commit()
            
            resultado = {
                'acertou': acertou,
                'resposta_correta': atividade['resposta_correta'],
                'mensagem': 'Parabéns! +1 ⭐' if acertou else 'Que pena! Tente novamente.'
            }
            conn.close()
            return jsonify(resultado)
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'erro': 'Atividade já respondida!'})
    
    # GET - Buscar nova atividade
    curso_id = request.args.get('curso_id', type=int)
    
    if curso_id:
        cursor.execute("""
            SELECT a.*, c.nome as curso_nome 
            FROM atividades a
            JOIN cursos c ON a.curso_id = c.id
            WHERE a.curso_id = ? 
            AND a.id NOT IN (SELECT atividade_id FROM progresso WHERE aluno_id = ?)
            ORDER BY RANDOM()
            LIMIT 1
        """, (curso_id, session['user_id']))
    else:
        cursor.execute("""
            SELECT a.*, c.nome as curso_nome 
            FROM atividades a
            JOIN cursos c ON a.curso_id = c.id
            WHERE a.id NOT IN (SELECT atividade_id FROM progresso WHERE aluno_id = ?)
            ORDER BY RANDOM()
            LIMIT 1
        """, (session['user_id'],))
    
    atividade = cursor.fetchone()
    
    # Busca cursos para filtro
    cursor.execute("SELECT id, nome FROM cursos ORDER BY nome")
    cursos = cursor.fetchall()
    
    conn.close()
    
    return render_template('aluno/atividade.html', 
                         atividade=atividade, 
                         cursos=cursos,
                         curso_selecionado=curso_id)

@app.route('/aluno/progresso')
@login_required
@aluno_required
def aluno_progresso():
    conn = conectar()
    cursor = conn.cursor()
    
    # Estatísticas gerais
    cursor.execute("""
        SELECT COALESCE(SUM(estrelas_ganhas), 0) as total,
               COUNT(*) as total_atividades,
               SUM(CASE WHEN acertou = 1 THEN 1 ELSE 0 END) as acertos
        FROM progresso WHERE aluno_id = ?
    """, (session['user_id'],))
    stats = cursor.fetchone()
    
    # Histórico recente
    cursor.execute("""
        SELECT p.*, a.pergunta, c.nome as curso_nome
        FROM progresso p
        JOIN atividades a ON p.atividade_id = a.id
        JOIN cursos c ON a.curso_id = c.id
        WHERE p.aluno_id = ?
        ORDER BY p.data_resposta DESC
        LIMIT 10
    """, (session['user_id'],))
    historico = cursor.fetchall()
    
    # Desempenho por curso
    cursor.execute("""
        SELECT c.nome,
               COUNT(p.id) as total,
               SUM(CASE WHEN p.acertou = 1 THEN 1 ELSE 0 END) as acertos,
               ROUND(100.0 * SUM(CASE WHEN p.acertou = 1 THEN 1 ELSE 0 END) / COUNT(p.id), 1) as media
        FROM cursos c
        JOIN atividades a ON c.id = a.curso_id
        LEFT JOIN progresso p ON a.id = p.atividade_id AND p.aluno_id = ?
        GROUP BY c.id
        HAVING COUNT(p.id) > 0
    """, (session['user_id'],))
    por_curso = cursor.fetchall()
    
    conn.close()
    
    return render_template('aluno/progresso.html', 
                         stats=stats, 
                         historico=historico,
                         por_curso=por_curso)

@app.route('/aluno/ranking')
@login_required
@aluno_required
def aluno_ranking():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.nome,
               COALESCE(SUM(p.estrelas_ganhas), 0) as estrelas,
               COUNT(p.id) as atividades,
               SUM(CASE WHEN p.acertou = 1 THEN 1 ELSE 0 END) as acertos
        FROM usuarios u
        LEFT JOIN progresso p ON u.id = p.aluno_id
        WHERE u.tipo = 'aluno'
        GROUP BY u.id, u.nome
        ORDER BY estrelas DESC, acertos DESC
    """)
    
    ranking = cursor.fetchall()
    conn.close()
    
    return render_template('aluno/ranking.html', ranking=ranking)

@app.route('/aluno/resetar', methods=['POST'])
@login_required
@aluno_required
def resetar_progresso():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM progresso WHERE aluno_id = ?", (session['user_id'],))
    conn.commit()
    conn.close()
    flash('Progresso resetado com sucesso!', 'success')
    return redirect(url_for('aluno_progresso'))

# ==================== ROTAS DO PROFESSOR ====================

@app.route('/professor')
@login_required
@professor_required
def professor_dashboard():
    conn = conectar()
    cursor = conn.cursor()
    
    # Apenas cursos e atividades do professor logado
    cursor.execute("""
        SELECT COUNT(*) as total FROM cursos WHERE professor_id = ?
    """, (session['user_id'],))
    meus_cursos = cursor.fetchone()['total']
    
    cursor.execute("""
        SELECT COUNT(*) as total FROM atividades WHERE professor_id = ?
    """, (session['user_id'],))
    minhas_atividades = cursor.fetchone()['total']
    
    conn.close()
    
    return render_template('professor/dashboard.html',
                         meus_cursos=meus_cursos,
                         minhas_atividades=minhas_atividades)

@app.route('/professor/cursos', methods=['GET', 'POST'])
@login_required
@professor_required
def professor_cursos():
    conn = conectar()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        acao = request.form.get('acao')
        
        if acao == 'criar':
            nome = request.form['nome']
            descricao = request.form['descricao']
            
            try:
                cursor.execute("""
                    INSERT INTO cursos (nome, descricao, professor_id) VALUES (?, ?, ?)
                """, (nome, descricao, session['user_id']))
                conn.commit()
                flash('Curso adicionado com sucesso!', 'success')
            except sqlite3.IntegrityError:
                flash('Curso com este nome já existe!', 'danger')
        
        elif acao == 'editar':
            curso_id = request.form['curso_id']
            nome = request.form['nome']
            descricao = request.form['descricao']
            
            # Verifica se o curso pertence ao professor
            cursor.execute("SELECT professor_id FROM cursos WHERE id = ?", (curso_id,))
            curso = cursor.fetchone()
            
            if curso and curso['professor_id'] == session['user_id']:
                try:
                    cursor.execute("""
                        UPDATE cursos SET nome = ?, descricao = ? WHERE id = ?
                    """, (nome, descricao, curso_id))
                    conn.commit()
                    flash('Curso atualizado com sucesso!', 'success')
                except sqlite3.IntegrityError:
                    flash('Já existe um curso com este nome!', 'danger')
            else:
                flash('Você não tem permissão para editar este curso!', 'danger')
        
        elif acao == 'excluir':
            curso_id = request.form['curso_id']
            
            # Verifica se o curso pertence ao professor
            cursor.execute("SELECT professor_id FROM cursos WHERE id = ?", (curso_id,))
            curso = cursor.fetchone()
            
            if curso and curso['professor_id'] == session['user_id']:
                # Verifica se há atividades vinculadas
                cursor.execute("SELECT COUNT(*) as total FROM atividades WHERE curso_id = ?", (curso_id,))
                atividades = cursor.fetchone()['total']
                
                if atividades > 0:
                    flash('Não é possível excluir: curso possui atividades vinculadas!', 'danger')
                else:
                    cursor.execute("DELETE FROM cursos WHERE id = ?", (curso_id,))
                    conn.commit()
                    flash('Curso excluído com sucesso!', 'success')
            else:
                flash('Você não tem permissão para excluir este curso!', 'danger')
    
    # Lista apenas os cursos do professor logado
    cursor.execute("""
        SELECT c.*, 
               (SELECT COUNT(*) FROM atividades WHERE curso_id = c.id) as total_atividades
        FROM cursos c
        WHERE c.professor_id = ?
        ORDER BY c.nome
    """, (session['user_id'],))
    cursos = cursor.fetchall()
    conn.close()
    
    return render_template('professor/cursos.html', cursos=cursos)

@app.route('/professor/atividades', methods=['GET', 'POST'])
@login_required
@professor_required
def professor_atividades():
    conn = conectar()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        acao = request.form.get('acao')
        
        if acao == 'criar':
            curso_id = request.form['curso_id']
            
            # Verifica se o curso pertence ao professor
            cursor.execute("SELECT professor_id FROM cursos WHERE id = ?", (curso_id,))
            curso = cursor.fetchone()
            
            if curso and curso['professor_id'] == session['user_id']:
                tipo = request.form['tipo']
                pergunta = request.form['pergunta']
                opcoes = request.form.get('opcoes', '')
                resposta = request.form['resposta']
                dica = request.form.get('dica', 'Sem dica disponível')
                
                cursor.execute("""
                    INSERT INTO atividades 
                    (curso_id, tipo, pergunta, opcoes, resposta_correta, dica, professor_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (curso_id, tipo, pergunta, opcoes, resposta, dica, session['user_id']))
                conn.commit()
                flash('Atividade adicionada com sucesso!', 'success')
            else:
                flash('Você só pode adicionar atividades aos seus cursos!', 'danger')
        
        elif acao == 'editar':
            atividade_id = request.form['atividade_id']
            
            # Verifica se a atividade pertence ao professor
            cursor.execute("SELECT professor_id FROM atividades WHERE id = ?", (atividade_id,))
            atividade = cursor.fetchone()
            
            if atividade and atividade['professor_id'] == session['user_id']:
                curso_id = request.form['curso_id']
                
                # Verifica se o novo curso também pertence ao professor
                cursor.execute("SELECT professor_id FROM cursos WHERE id = ?", (curso_id,))
                curso = cursor.fetchone()
                
                if curso and curso['professor_id'] == session['user_id']:
                    tipo = request.form['tipo']
                    pergunta = request.form['pergunta']
                    opcoes = request.form.get('opcoes', '')
                    resposta = request.form['resposta']
                    dica = request.form.get('dica', 'Sem dica disponível')
                    
                    cursor.execute("""
                        UPDATE atividades 
                        SET curso_id = ?, tipo = ?, pergunta = ?, opcoes = ?, 
                            resposta_correta = ?, dica = ?
                        WHERE id = ?
                    """, (curso_id, tipo, pergunta, opcoes, resposta, dica, atividade_id))
                    conn.commit()
                    flash('Atividade atualizada com sucesso!', 'success')
                else:
                    flash('Você só pode mover atividades para seus próprios cursos!', 'danger')
            else:
                flash('Você não tem permissão para editar esta atividade!', 'danger')
        
        elif acao == 'excluir':
            atividade_id = request.form['atividade_id']
            
            # Verifica se a atividade pertence ao professor
            cursor.execute("SELECT professor_id FROM atividades WHERE id = ?", (atividade_id,))
            atividade = cursor.fetchone()
            
            if atividade and atividade['professor_id'] == session['user_id']:
                cursor.execute("DELETE FROM atividades WHERE id = ?", (atividade_id,))
                conn.commit()
                flash('Atividade excluída com sucesso!', 'success')
            else:
                flash('Você não tem permissão para excluir esta atividade!', 'danger')
    
    # Lista apenas os cursos do professor para o select
    cursor.execute("SELECT id, nome FROM cursos WHERE professor_id = ? ORDER BY nome", (session['user_id'],))
    cursos = cursor.fetchall()
    
    # Lista apenas as atividades do professor logado
    cursor.execute("""
        SELECT a.*, c.nome as curso_nome
        FROM atividades a
        JOIN cursos c ON a.curso_id = c.id
        WHERE a.professor_id = ?
        ORDER BY a.data_criacao DESC
    """, (session['user_id'],))
    atividades = cursor.fetchall()
    
    conn.close()
    
    tipos = [
        ('multipla_escolha', 'Múltipla Escolha'),
        ('verdadeiro_falso', 'Verdadeiro ou Falso'),
        ('preencher_lacunas', 'Preencher Lacunas'),
        ('ordenar', 'Ordenar Etapas'),
        ('sequencia_logica', 'Sequência Lógica'),
        ('correspondencia', 'Correspondência'),
        ('classificacao', 'Classificação'),
        ('escolha_multipla', 'Escolha Múltipla'),
        ('palavra_embaralhada', 'Palavra Embaralhada'),
        ('mini_cenario', 'Mini-Cenário')
    ]
    
    return render_template('professor/atividades.html', 
                         cursos=cursos, 
                         atividades=atividades,
                         tipos=tipos)

# ==================== ROTAS DO COORDENADOR ====================

@app.route('/coordenador')
@login_required
@coordenador_required
def coordenador_dashboard():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM usuarios WHERE tipo = 'aluno'")
    total_alunos = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM atividades")
    total_atividades = cursor.fetchone()['total']
    
    hoje = date.today().isoformat()
    cursor.execute("""
        SELECT COUNT(*) as total FROM progresso WHERE date(data_resposta) = ?
    """, (hoje,))
    atividades_hoje = cursor.fetchone()['total']
    
    cursor.execute("""
        SELECT COALESCE(SUM(estrelas_ganhas), 0) as total FROM progresso
    """)
    total_estrelas = cursor.fetchone()['total']
    
    conn.close()
    
    return render_template('coordenador/dashboard.html',
                         total_alunos=total_alunos,
                         total_atividades=total_atividades,
                         atividades_hoje=atividades_hoje,
                         total_estrelas=total_estrelas)

@app.route('/coordenador/ranking')
@login_required
@coordenador_required
def coordenador_ranking():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.nome,
               COALESCE(SUM(p.estrelas_ganhas), 0) as estrelas,
               COUNT(p.id) as atividades_feitas,
               SUM(CASE WHEN p.acertou = 1 THEN 1 ELSE 0 END) as acertos,
               ROUND(100.0 * SUM(CASE WHEN p.acertou = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(p.id), 0), 1) as percentual
        FROM usuarios u
        LEFT JOIN progresso p ON u.id = p.aluno_id
        WHERE u.tipo = 'aluno'
        GROUP BY u.id, u.nome
        ORDER BY estrelas DESC, acertos DESC
    """)
    
    ranking = cursor.fetchall()
    conn.close()
    
    return render_template('coordenador/ranking.html', ranking=ranking)

@app.route('/coordenador/relatorios')
@login_required
@coordenador_required
def coordenador_relatorios():
    conn = conectar()
    cursor = conn.cursor()
    
    # Desempenho por curso
    cursor.execute("""
        SELECT c.nome,
               COUNT(DISTINCT p.aluno_id) as alunos_participantes,
               COUNT(p.id) as total_tentativas,
               SUM(CASE WHEN p.acertou = 1 THEN 1 ELSE 0 END) as acertos,
               ROUND(100.0 * SUM(CASE WHEN p.acertou = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(p.id), 0), 1) as taxa_acerto
        FROM cursos c
        LEFT JOIN atividades a ON c.id = a.curso_id
        LEFT JOIN progresso p ON a.id = p.atividade_id
        GROUP BY c.id, c.nome
        ORDER BY c.nome
    """)
    por_curso = cursor.fetchall()
    
    # Atividades de hoje detalhadas
    hoje = date.today().isoformat()
    cursor.execute("""
        SELECT u.nome, COUNT(*) as quantidade
        FROM progresso p
        JOIN usuarios u ON p.aluno_id = u.id
        WHERE date(p.data_resposta) = ?
        GROUP BY u.id
        ORDER BY quantidade DESC
    """, (hoje,))
    atividades_hoje = cursor.fetchall()
    
    conn.close()
    
    return render_template('coordenador/relatorios.html', 
                         por_curso=por_curso,
                         atividades_hoje=atividades_hoje)

if __name__ == '__main__':
    criar_tabelas()
    app.run(host='0.0.0.0', port=5000, debug=True)