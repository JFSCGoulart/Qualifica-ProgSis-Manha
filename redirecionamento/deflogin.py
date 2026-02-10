def fazer_login():
    print("\n" + "="*40)
    print("LOGIN")
    print("="*40)
    
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    
    cursor.execute('''
    SELECT id, nome, senha, tipo, email FROM usuarios 
    WHERE usuario = ?
    ''', (usuario,))
    
    resultado = cursor.fetchone()
    
    if resultado:
        usuario_id, nome, senha_hash, tipo, email = resultado
        
        if verificar_senha(senha, senha_hash):
            print(f"\nLogin bem-sucedido!")
            print(f"Bem-vindo(a), {nome}!")
            print(f"Tipo: {tipo}")
            
            info_usuario = {
                'id': usuario_id,
                'nome': nome,
                'usuario': usuario,
                'tipo': tipo,
                'email': email
            }
            
            return info_usuario
        else:
            print("Senha incorreta!")
    else:
        print("Usuário não encontrado!")
    
    return None

def alterar_senha(usuario_id):
    print("\n" + "="*40)
    print("ALTERAR SENHA")
    print("="*40)
    
    senha_atual = input("Senha atual: ")
    
    cursor.execute('SELECT senha FROM usuarios WHERE id = ?', (usuario_id,))
    resultado = cursor.fetchone()
    
    if resultado and verificar_senha(senha_atual, resultado[0]):
        nova_senha = input("Nova senha: ")
        confirmar_senha = input("Confirmar nova senha: ")
        
        if nova_senha == confirmar_senha:
            if len(nova_senha) >= 6:
                cursor.execute('UPDATE usuarios SET senha = ? WHERE id = ?', 
                (hash_senha(nova_senha), usuario_id))
                conn.commit()
                print("Senha alterada com sucesso!")
            else:
                print("A senha deve ter pelo menos 6 caracteres!")
        else:
            print("As senhas não coincidem!")
    else:
        print("Senha atual incorreta!")
        
def hash_senha(senha):
    """Criptografa a senha usando SHA-256"""
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha_digitada, senha_hash):
    """Verifica se a senha está correta"""
    return hash_senha(senha_digitada) == senha_hash

