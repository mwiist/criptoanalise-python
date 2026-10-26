import csv
from pathlib import Path
from time import perf_counter

from binario import ler_binario
from cesar import decifrar_cesar
from substituicao import contar_letras, aplicar_chave, buscar_chave
from pontuacao import carregar_quadgramas
from circular import desfazer_rotacao, buscar_rotacao, recifrar_circular


def salvar_csv(caminho, cabecalho, linhas):
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalho)
        escritor.writerows(linhas)


def main():
    pasta = Path(__file__).resolve().parent
    resultados = pasta / "resultados"
    resultados.mkdir(exist_ok=True)
    textos = {}

    print("\nConvertendo os arquivos binários...")

    for nome in ("simple", "circular"):
        texto = ler_binario(
            pasta / "dados" / "entrada" / f"encoded-{nome}.txt"
        )
        textos[nome] = texto

        saida = resultados / f"01_{nome}_ascii.txt"
        saida.write_text(texto, encoding="utf-8")

        print(f"\n{nome}: {len(texto)} caracteres")
        print(texto[:150])
        print(f"Texto convertido salvo em {saida.name}")

    print("\nTestando César com deslocamento fixo...")

    for nome in ("simple", "circular"):
        texto = textos[nome]
        tentativas = []

        print(f"\nTentativas para o {nome}:")

        for deslocamento in range(26):
            candidato = decifrar_cesar(texto, deslocamento)

            print(f"Deslocamento {deslocamento:2}: {candidato[:80]}")

            tentativas.append(f"Deslocamento {deslocamento}\n{candidato}\n\n")

        saida = resultados / f"02_{nome}_cesar.txt"
        saida.write_text("".join(tentativas), encoding="utf-8")
        print(f"Tentativas completas salvas em {saida.name}")

    print("\nAs possibilidades de César estão disponíveis para comparação.")
    print("A próxima etapa examina a substituição simples.")

    texto_simple = textos["simple"]

    print("\nContando as letras do simple...")

    frequencias = contar_letras(texto_simple)
    linhas = []

    for letra, quantidade in frequencias.items():
        print(f"{letra}: {quantidade}")
        linhas.append(f"{letra}: {quantidade}\n")

    saida = resultados / "03_simple_frequencias.txt"
    saida.write_text("".join(linhas), encoding="utf-8")
    print(f"Contagem salva em {saida.name}")

    # Essas trocas sao da analise inicial e nao da busca automatica
    hipotese = {
        "O": "E",
        "V": "T",
        "C": "H",
        "T": "A",
    }

    print("\nAplicando a hipótese parcial da análise inicial:")

    for cifrada, original in hipotese.items():
        print(f"{cifrada} -> {original}")

    parcial = aplicar_chave(texto_simple, hipotese)

    print("\nAntes:")
    print(texto_simple[:150])
    print("\nDepois:")
    print(parcial[:150])
    print("O sinal _ indica uma letra ainda sem correspondência.")

    saida = resultados / "04_simple_hipotese_parcial.txt"
    saida.write_text(parcial, encoding="utf-8")
    print(f"Texto parcial salvo em {saida.name}")

    print("\nCarregando a referência de grupos de quatro letras em inglês...")

    notas, piso = carregar_quadgramas(
        pasta / "dados" / "referencia" / "english_quadgrams.txt"
    )

    print(f"Referência carregada: {len(notas)} grupos.")
    print("Essa referência será usada para comparar as tentativas.")
    print("Quanto maior a nota, melhor o resultado segundo esse critério.")

    print("\nProcurando a chave completa do simple...")
    print("A busca começa com chaves embaralhadas.")
    print("As quatro trocas anteriores não são fornecidas à busca.")
    print("Serão feitas 10 tentativas, começando de chaves diferentes.")
    print("Cada tentativa termina após 2000 trocas consecutivas sem melhora.")

    inicio_busca = perf_counter()

    chave, nota_simple, avaliacoes, historico, evolucao = buscar_chave(
        texto_simple, notas, piso
    )

    tempo_simple = perf_counter() - inicio_busca
    simple_decifrado = aplicar_chave(texto_simple, chave)

    print("\nBusca do simple concluída.")
    print(f"Avaliações de chaves: {avaliacoes}")
    print(f"Melhor nota: {nota_simple:.4f}")
    print(f"Tempo: {tempo_simple:.3f} segundos")

    print("\nChave encontrada:")

    for cifrada, original in chave.items():
        print(f"{cifrada} -> {original}")

    print("\nPrévia do resultado:")
    print(simple_decifrado[:300])

    saida = resultados / "05_simple_decifrado.txt"
    saida.write_text(simple_decifrado, encoding="utf-8")

    salvar_csv(
        resultados / "05_simple_chave.csv",
        ["cifrada", "original"],
        chave.items(),
    )

    salvar_csv(
        resultados / "05_simple_reinicios.csv",
        ["reinicio", "nota_inicial", "nota_final"],
        historico,
    )

    salvar_csv(
        resultados / "05_simple_evolucao.csv",
        ["reinicio", "avaliacao", "nota", "chave_na_ordem_A_Z"],
        evolucao,
    )

    print("Texto, chave e evolução da busca salvos nos arquivos 05.")

    print("\nTestando a mesma tabela de substituição no circular...")
    print("Neste teste ainda não há rotação.")

    intermediario = aplicar_chave(textos["circular"], chave)

    print("\nAntes:")
    print(textos["circular"][:150])
    print("\nDepois de aplicar somente a tabela:")
    print(intermediario[:150])

    saida = resultados / "06_circular_so_substituicao.txt"
    saida.write_text(intermediario, encoding="utf-8")
    print(f"Texto intermediário salvo em {saida.name}")

    print("\nTestando se falta um deslocamento fixo após a substituição...")

    tentativas = []

    for inicio in range(26):
        candidato = desfazer_rotacao(intermediario, inicio, 0, False)

        print(f"Deslocamento {inicio:2}: {candidato[:80]}")

        tentativas.append(f"Deslocamento fixo {inicio}\n{candidato}\n\n")

    saida = resultados / "07_circular_rotacao_fixa.txt"
    saida.write_text("".join(tentativas), encoding="utf-8")
    print(f"Tentativas completas salvas em {saida.name}")

    print("\nTestando também uma rotação que varia com a posição.")
    print("Regra investigada: deslocamento = início + passo * posição")
    print("Início: de 0 a 25.")
    print("Passo: de 0 a 25.")
    print("Contagem: só letras ou todos os caracteres, incluindo espaços.")
    print("O passo zero inclui o deslocamento fixo.")
    print("Comparando as 1352 combinações pela pontuação de inglês...")

    inicio_busca = perf_counter()
    ranking = buscar_rotacao(intermediario, notas, piso)
    tempo_circular = perf_counter() - inicio_busca

    salvar_csv(
        resultados / "08_circular_ranking.csv",
        ["nota", "inicio", "passo", "contar_espacos", "texto"],
        ranking,
    )

    print(f"\nComparação concluída em {tempo_circular:.3f} segundos.")
    print("As cinco possibilidades com maior pontuação foram:")

    melhores = []
    colocacao = 1

    for nota, inicio, passo, contar_espacos, texto in ranking[:5]:
        if contar_espacos:
            contagem = "todos os caracteres"
        else:
            contagem = "somente letras"

        print(f"\n{colocacao}. Início {inicio}, passo {passo}, contando {contagem}")
        print(f"Nota: {nota:.4f}")
        print(texto[:200])

        melhores.append(
            f"Nota: {nota:.4f}; início: {inicio}; passo: {passo}; "
            f"contar espaços: {contar_espacos}\n{texto}\n\n"
        )

        colocacao += 1

    saida = resultados / "08_circular_melhores.txt"
    saida.write_text("".join(melhores), encoding="utf-8")
    print("\nRanking completo e cinco melhores textos salvos nos arquivos 08.")

    nota_circular, inicio, passo, contar_espacos, circular_decifrado = ranking[0]

    print("\nSelecionando a possibilidade com maior pontuação:")
    print(f"Início: {inicio}")
    print(f"Passo: {passo}")

    if contar_espacos:
        print("Os espaços avançam a contagem.")
    else:
        print("Os espaços não avançam a contagem.")

    print("\nPrévia do circular decifrado:")
    print(circular_decifrado[:300])

    saida = resultados / "09_circular_decifrado.txt"
    saida.write_text(circular_decifrado, encoding="utf-8")
    print(f"Texto completo salvo em {saida.name}")

    print("\nRecifrando os resultados para comparar com as entradas...")

    chave_inversa = {}

    for cifrada, original in chave.items():
        chave_inversa[original] = cifrada

    simple_reconstruido = aplicar_chave(
        simple_decifrado, chave_inversa
    )

    circular_reconstruido = recifrar_circular(
        circular_decifrado, chave, inicio, passo, contar_espacos
    )

    simple_confere = simple_reconstruido == texto_simple
    circular_confere = circular_reconstruido == textos["circular"]

    if simple_confere:
        print("Simple: a recifragem reproduziu exatamente a entrada.")
    else:
        print("Simple: a recifragem ficou diferente da entrada.")

    if circular_confere:
        print("Circular: a recifragem reproduziu exatamente a entrada.")
    else:
        print("Circular: a recifragem ficou diferente da entrada.")

    resumo = (
        "RESULTADO SIMPLE\n"
        "Busca: 10 reinicios, semente 42, limite de 2000 trocas sem melhora\n"
        f"Tamanho do texto: {len(texto_simple)} caracteres\n"
        f"Avaliacoes de chaves, incluindo repeticoes: {avaliacoes}\n"
        f"Melhor pontuacao: {nota_simple:.4f}\n"
        f"Tempo da busca: {tempo_simple:.3f} segundos\n"
        f"Recifragem igual a entrada: {simple_confere}\n\n"
        "RESULTADO CIRCULAR\n"
        f"Tamanho do texto: {len(textos['circular'])} caracteres\n"
        f"Combinacoes avaliadas: {len(ranking)}\n"
        f"Inicio encontrado: {inicio}\n"
        f"Passo encontrado: {passo}\n"
        f"Contou espacos e pontuacao na posicao: {contar_espacos}\n"
        f"Melhor pontuacao: {nota_circular:.4f}\n"
        f"Tempo da busca: {tempo_circular:.3f} segundos\n"
        f"Recifragem igual a entrada: {circular_confere}\n"
    )

    saida = resultados / "10_resumo.txt"
    saida.write_text(resumo, encoding="utf-8")

    print(f"\nMétricas e verificações salvas em {saida.name}")
    print(f"Resultados disponíveis em: {resultados}")


if __name__ == "__main__":
    main()
