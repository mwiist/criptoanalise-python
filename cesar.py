def decifrar_cesar(texto, chave):
    resultado = []
    for caractere in texto:
        if "A" <= caractere <= "Z":
            numero = ord(caractere) - ord("A")
            letra = chr((numero - chave) % 26 + ord("A"))
            resultado.append(letra)
        else:
            resultado.append(caractere)
    return "".join(resultado)
