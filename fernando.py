def situacao(estrelas):
    if estrelas >= 7:
        return "APROVADO"
    elif estrelas >= 5:
        return "RECUPERAÇÃO"
    else:
        return "REPROVADO"

def barra_progresso(atual, total):
    return "█" * atual + "░" * (total - atual)

# ===============================
# CONFIGURAÇÕES DO JOGO
# ===============================

VIDAS_MAX = 3
TOTAL_PERGUNTAS = 6

aluno = input("👤 Nome do aluno: ")

perguntas = [
    ("Quanto é 10 / 2?", ["5"]),
    ("Capital do Brasil?", ["brasilia", "brasília"]),
    ("Quanto é 7 + 3?", ["10"]),
    ("Quanto é 6 x 2?", ["12"]),
    ("Quanto é 9 - 4?", ["5"]),
    ("Quantos meses tem 1 ano?", ["12", "12 meses"]),
    ("quanto é 1 + 1?", ["2"]),
]

vidas = VIDAS_MAX
estrelas = 0
respondidas = 0

print("\n🎮 BEM-VINDO AO QUALIFICA GAME 🎮\n")

# ===============================
# LOOP DO JOGO
# ===============================

for pergunta, respostas in perguntas:

    if vidas == 0:
        print("💀 Game Over! Suas vidas acabaram.")
        break

    print(f"📘 Pergunta {respondidas + 1}/{TOTAL_PERGUNTAS}")
    print(pergunta)

    resp = input("👉 Resposta: ").strip().lower()

    if resp in respostas:
        estrelas += 1
        print("✅ Correto! +⭐")
    else:
        vidas -= 1
        print("❌ Errado! -❤️")

    respondidas += 1

    print(f"⭐ Estrelas: {estrelas}")
    print(f"❤️ Vidas: {vidas}/{VIDAS_MAX}")
    print(f"📊 Progresso: {barra_progresso(respondidas, TOTAL_PERGUNTAS)}\n")

# ===============================
# BOLETIM FINAL
# ===============================

print("\n🏁 FIM DO JOGO")
print("-" * 30)
print(f"Aluno: {aluno}")
print(f"Perguntas respondidas: {respondidas}")
print(f"Estrelas conquistadas: {estrelas}")
print(f"Situação final: {situacao(estrelas)}")
print("-" * 30)