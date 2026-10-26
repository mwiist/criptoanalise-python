def converter_binario(conteudo):
    caracteres = []

    for bloco in conteudo.split():
        numero = int(bloco, 2)
        caracteres.append(chr(numero))

    return "".join(caracteres)


def ler_binario(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return converter_binario(arquivo.read())
