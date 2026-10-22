from pontuacao import pontuar


def desfazer_rotacao(texto, inicio, passo, contar_espacos):
    resultado = []
    posicao = 0

    for letra in texto:
        if "A" <= letra <= "Z":
            deslocamento = inicio + passo * posicao
            numero = ord(letra) - ord("A")
            original = chr((numero - deslocamento) % 26 + ord("A"))
            resultado.append(original)
            posicao += 1
        else:
            resultado.append(letra)
            if contar_espacos:
                posicao += 1

    return "".join(resultado)


def buscar_rotacao(texto, notas, piso):
    tentativas = []

    for contar_espacos in (False, True):
        for passo in range(26):
            for inicio in range(26):
                candidato = desfazer_rotacao(texto, inicio, passo, contar_espacos)
                letras = "".join(letra for letra in candidato if "A" <= letra <= "Z")
                nota = pontuar(letras, notas, piso)
                tentativas.append((nota, inicio, passo, contar_espacos, candidato))

    tentativas.sort(reverse=True)
    return tentativas


def recifrar_circular(texto, chave, inicio, passo, contar_espacos):
    inversa = {}

    for cifrada, original in chave.items():
        inversa[original] = cifrada


    resultado = []
    posicao = 0

    for letra in texto:
        if "A" <= letra <= "Z":
            numero = ord(letra) - ord("A")
            rotacionada = chr((numero + inicio + passo * posicao) % 26 + ord("A"))
            resultado.append(inversa[rotacionada])
            posicao += 1
        else:
            resultado.append(letra)
            if contar_espacos:
                posicao += 1

    return "".join(resultado)
