import random
from pontuacao import pontuar


def buscar_chave(texto, notas, piso, reinicios=10, limite=2000):
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letras = "".join(letra for letra in texto if letra in alfabeto)
    random.seed(42)
    melhor_nota = float("-inf")
    melhor_chave = None
    historico = []
    avaliacoes = 0
    evolucao = []

    for reinicio in range(reinicios):
        chave = list(alfabeto)
        random.shuffle(chave)
        # Usando maketrans/translate para deixar o loop de busca mais rapido
        tabela = str.maketrans(alfabeto, "".join(chave))
        nota = pontuar(letras.translate(tabela), notas, piso)
        nota_inicial = nota
        avaliacoes += 1
        sem_melhora = 0
        evolucao.append((reinicio + 1, avaliacoes, nota, "".join(chave)))

        while sem_melhora < limite:
            a, b = random.sample(range(26), 2)
            chave[a], chave[b] = chave[b], chave[a]
            tabela = str.maketrans(alfabeto, "".join(chave))
            nova_nota = pontuar(letras.translate(tabela), notas, piso)
            avaliacoes += 1

            if nova_nota > nota:
                nota = nova_nota
                sem_melhora = 0
                evolucao.append((reinicio + 1, avaliacoes, nota, "".join(chave)))
            else:
                chave[a], chave[b] = chave[b], chave[a]
                sem_melhora += 1

        if nota > melhor_nota:
            melhor_nota = nota
            melhor_chave = dict(zip(alfabeto, chave))

        historico.append((reinicio + 1, nota_inicial, nota))
        print(f"Reinício {reinicio + 1}/{reinicios}: nota {nota:.2f}")

    return melhor_chave, melhor_nota, avaliacoes, historico, evolucao


def contar_letras(texto):
    frequencias = {}
    for letra in texto:
        if "A" <= letra <= "Z":
            frequencias[letra] = frequencias.get(letra, 0) + 1
    return frequencias


def aplicar_chave(texto, chave):
    resultado = []
    for letra in texto:
        if "A" <= letra <= "Z":
            resultado.append(chave.get(letra, "_"))
        else:
            resultado.append(letra)
    return "".join(resultado)
