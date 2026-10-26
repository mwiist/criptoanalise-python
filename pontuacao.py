from math import log10


def carregar_quadgramas(caminho):
    contagens = {}

    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:
            grupo, quantidade = linha.split()
            contagens[grupo] = int(quantidade)

    total = sum(contagens.values())
    notas = {}

    for grupo, quantidade in contagens.items():
        notas[grupo] = log10(quantidade / total)

    piso = log10(0.01 / total)
    return notas, piso


def pontuar(texto, notas, piso):
    pontuacao = 0

    for i in range(len(texto) - 3):
        grupo = texto[i:i + 4]
        pontuacao += notas.get(grupo, piso)

    return pontuacao
