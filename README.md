# Representação numérica e criptoanálise em Python

Trabalho desenvolvido para a disciplina de Arquitetura de Computadores da Universidade Federal do ABC (UFABC).

O objetivo foi decifrar dois textos fornecidos em formato binário, investigando as transformações aplicadas e os padrões que poderiam ajudar a recuperar as mensagens.

## Como a solução funciona

Primeiro, os blocos de números binários são convertidos em caracteres ASCII. Essa conversão permite ler os textos cifrados, mas ainda não recupera as mensagens originais.

A partir disso, o programa realiza as seguintes etapas:

- Testa os deslocamentos da cifra de César.
- Conta a frequência das letras e mostra uma tentativa de substituição parcial.
- Busca uma chave de substituição, comparando a pontuação dos textos obtidos.
- Aplica a chave encontrada ao texto circular e testa uma segunda transformação, com deslocamentos que variam conforme a posição das letras.
- Confere se as transformações inversas recuperam os textos cifrados de entrada.

Para comparar as tentativas, usei uma tabela de frequências de sequências de quatro letras em inglês, chamadas de *quadgrams*. Ela ajuda a identificar combinações mais comuns no idioma e orientar a busca por uma chave.

## Organização dos arquivos

- `main.py`: reúne as etapas da investigação e mostra as prévias no terminal.
- `binario.py`: faz a conversão dos blocos binários em texto.
- `cesar.py`: aplica os deslocamentos da cifra de César.
- `substituicao.py`: conta letras, aplica chaves e realiza a busca por uma chave de substituição.
- `pontuacao.py`: lê a tabela de quadgrams e calcula a pontuação das tentativas.
- `circular.py`: testa os deslocamentos por posição e faz a transformação inversa.
- `dados/`: contém os textos de entrada e a tabela usada na pontuação.
- `resultados/`: recebe os arquivos gerados durante a execução.

## Como executar

É necessário ter o Python 3 instalado. O código usa apenas bibliotecas que já vêm com o Python.

Com o terminal aberto na pasta principal do projeto, execute:

```bash
python main.py
```

Mantenha os arquivos de entrada e a tabela de quadgrams nas pastas indicadas no código.

Durante a execução, o terminal mostra as etapas e algumas prévias. Os textos completos, as tentativas registradas e os resultados das verificações são salvos em `resultados/`.

## Resultados e limites

A solução recuperou as duas mensagens dos arquivos fornecidos. As verificações finais também confirmaram que é possível reconstruir os textos cifrados a partir das mensagens e das chaves encontradas.

Na análise inicial do `simple`, ao observar o texto e a contagem de letras, levantei a hipótese a sequência `VCO` representava a palavra `THE`, com as trocas `V → T`, `C → H` e `O → E`. Essa correspondência orientou as primeiras substituições. No `circular`, aplicar a mesma chave ainda não tornou o texto legível. Foi necessário desfazer também um deslocamento progressivo, com início em 12 e aumento de 1 por letra, sem contar espaços ou pontuação na posição.

## Referência dos dados

A tabela de quadgrams utilizada está disponível no repositório [simple-substitution-cipher, de Lucian Buzzo](https://github.com/LucianBuzzo/simple-substitution-cipher/blob/master/english_quadgrams.txt).

## Autoria

Melissa Nascimento Gonçalves  
Universidade Federal do ABC - UFABC
