import json
from datetime import datetime
#sistema de ranking usando funçao def para classificar usuario,nome,xp,level
class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.xp = 0
        self.level = 1
        self.streak = 0
    
    def add_xp(self, xp):
        self.xp += xp
        # Atualizar level a cada 50 XP
        self.level = (self.xp // 50) + 1
#indentificando objeto  usuario
class Ranking:
    def __init__(self):
        self.users = {}
        self.next_id = 1
    # obtendo usuario pelo id   
    def get_user(self, user_id):
        return self.users.get(user_id)
    # adicionando usuario ao sistema
    def add_user(self, username):
        user = User(self.next_id, username)
        self.users[self.next_id] = user
        self.next_id += 1
        return user
        # adicionando atividade ao usuario
        
    def add_activity(self, user_id, activity_type="lições"):
        xp_values = {
            "lições": 10,
            "quiz": 15,
            "experiência": 8,
            "review": 12,
        }
# obtendo xp conforme atividade
        
        xp = xp_values.get(activity_type, 10)
        user = self.users.get(user_id)
# se usuario existir adiciona xp e streak
        if user:
            # Bônus de streak
            xp += user.streak
            user.streak += 1
            user.add_xp(xp)
            return {"xp": xp, "streak": user.streak}
        return None
# obtendo ranking dos usuarios
    def get_ranking(self, limit=10):
        """Retorna top usuário ordenados por XP"""
        sorted_users = sorted(self.users.values(),
                            key=lambda u: u.xp,
                            reverse=True)
# limitando ranking ao top 10        
        ranking = []
        for i, user in enumerate(sorted_users[:limit], 1):
            ranking.append({
                "pos": i,
                "user": user.username,
                "xp": user.xp,
                "level": user.level,
                "streak": user.streak
            })
        
        return ranking
# obtendo posiçao do usuario no ranking    
    def get_user_position(self, user_id):
        """Retornando a posicão do usuário no"""
        sorted_users = sorted(self.users.values(),
                            key=lambda u: u.xp,
                            reverse=True)
        
        for i, user in enumerate(sorted_users, 1):
            if user.user_id == user_id:
                return i
        return None

# Teste do sistema
if __name__ == "__main__":
    ranking = Ranking()
    
    users = ["Ana", "Carlos", "Beatriz"]
    for name in users:
        ranking.add_user(name)
    
    for i in range(3):
        ranking.add_activity(1, "lições")
        ranking.add_activity(2, "quiz")
        ranking.add_activity(3, "experiência")
    
    print("=== RANKING SIMPLES ===")
    for entry in ranking.get_ranking():
        print(f"{entry['pos']}. {entry['user']} - {entry['xp']} xp (level {entry['level']})")
    
    pos = ranking.get_user_position(1)
    print(f"\n está na posição: {pos}")