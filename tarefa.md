# Trabalho Prático — Estrutura van Emde Boas com Espaço Linear

## Descrição Geral

O objetivo deste trabalho é implementar uma estrutura **van Emde Boas** com espaço linear no número de elementos, utilizando **tabela de dispersão (hash table) com table doubling/halving**.

A estrutura deve ser implementada considerando um **tamanho de palavra de 32 bits**.

O programa deve receber como entrada um arquivo de texto (`.txt`) passado como argumento na linha de comando. Esse arquivo conterá diversas operações sobre a estrutura de dados, uma por linha.

Os resultados das operações que geram saída devem ser impressos diretamente no terminal.

---

## Operações Suportadas

### Inclusão (`INC`)

Uma operação de inclusão é representada por uma linha contendo:

```text
INC <inteiro>
```

O valor informado deve ser inserido na estrutura de dados.

Nenhuma saída deve ser impressa.

#### Exemplo

Entrada:

```text
INC 13
```

---

### Remoção (`REM`)

Uma operação de remoção é representada por:

```text
REM <inteiro>
```

O valor informado deve ser removido da estrutura, caso exista.

Nenhuma saída deve ser impressa.

#### Exemplo

Entrada:

```text
REM 42
```

---

### Sucessor (`SUC`)

Uma operação de sucessor é representada por:

```text
SUC <inteiro>
```

O sucessor de um número `x` é o menor valor armazenado na estrutura que seja estritamente maior que `x`.

Se não existir tal valor, o resultado deve ser:

```text
+INF
```

#### Exemplo

Entrada:

```text
SUC 50
```

Saída:

```text
SUC 50
80
```

---

### Predecessor (`PRE`)

Uma operação de predecessor é representada por:

```text
PRE <inteiro>
```

O predecessor de um número `x` é o maior valor armazenado na estrutura que seja estritamente menor que `x`.

Se não existir tal valor, o resultado deve ser:

```text
-INF
```

#### Exemplo

Entrada:

```text
PRE 50
```

Saída:

```text
PRE 50
21
```

---

### Impressão (`IMP`)

Uma operação de impressão é representada por:

```text
IMP
```

A impressão deve mostrar uma visão do primeiro nível da estrutura van Emde Boas, incluindo:

- O valor mínimo da estrutura;
- Os clusters não vazios;
- Os elementos armazenados em cada cluster.

#### Exemplo

Entrada:

```text
IMP
```

Saída:

```text
IMP
Min: 102, C[0]: 268, 322, 14756, C[3]: 456, 728, 152, C[65535]: 0, 65535
```

---

# Grupos e Entrega

## Formação das Equipes

### Graduação

- Até **3 integrantes por equipe**.

### Pós-Graduação

- Trabalho **individual**.

---

## Arquivos Obrigatórios

O envio do trabalho deve conter:

### Código-fonte

Todo o código necessário para compilação e execução.

### Makefile

O arquivo `Makefile` deve possuir pelo menos as funcionalidades:

- `build`
- `run`

#### Requisitos

- O programa deve receber um arquivo `.txt` como entrada.
- O comando `run` deve permitir receber o caminho para esse arquivo como argumento.

### README.md

O arquivo `README.md` deve conter:

- Linguagem utilizada (incluindo versão);
- Instruções de compilação e execução;
- Descrição das funções utilizadas;
- Descrição das estruturas de dados utilizadas;
- Arquivos onde cada função e estrutura está implementada.

---

# Exemplo de Makefile

Considere que todos os arquivos estejam no mesmo diretório.

Neste exemplo existem dois comandos:

- `make build`
- `make run`

## Build

O comando:

```bash
make build
```

Compila o arquivo:

```text
main.cpp
```

e gera o executável:

```text
programa.exe
```

---

## Run

O comando:

```bash
make run
```

Executa:

```bash
./programa.exe entrada.txt
```

onde `entrada.txt` é o valor padrão definido na variável:

```makefile
INPUT = entrada.txt
```

---

## Utilizando outro arquivo de entrada

Para executar utilizando outro arquivo:

```bash
make run INPUT="entrada2.txt"
```

Neste caso, o programa será executado como:

```bash
./programa.exe entrada2.txt
```

---

# Testes

Uma estratégia recomendada é manter:

- Um arquivo de entrada;
- Um arquivo contendo a saída esperada.

Exemplo:

```text
entrada.txt
saida_esperada.txt
```

---

## Gerando a saída do programa

Após compilar:

```bash
./programa.exe entrada.txt > saida.txt
```

Esse comando salva toda a saída do programa no arquivo:

```text
saida.txt
```

---

## Comparando os resultados

### Linux/macOS

```bash
diff saida.txt saida_esperada.txt > diferencas.txt
```

### Windows (CMD)

```cmd
fc saida.txt saida_esperada.txt > diferencas.txt
```

O arquivo `diferencas.txt` conterá todas as divergências encontradas.

---

# Exemplo Completo

## Arquivo de Entrada

`entrada.txt`

```text
INC 655364
INC 65535
SUC 100000
IMP
```

---

## Saída Esperada

`saida_esperada.txt`

```text
SUC 100000
655364
IMP
Min: 65535, C[10]: 4
```

---

## Saída Obtida

`saida.txt`

```text
SUC 100000
655364
IMP
Min: 65535, C[20]: 4
```

---

## Resultado do diff

`diferencas.txt`

```text
4c4
< Min: 65535, C[20]: 4
---
> Min: 65535, C[10]: 4
```

> No Windows, utilizando `fc`, o formato da saída será diferente, mas a interpretação será equivalente.

Essas linhas indicam que existe uma diferença na linha 4 entre a saída obtida e a saída esperada.

Nesse exemplo, o erro provavelmente está relacionado:

- À segunda operação `INC`; ou
- À implementação da operação `IMP`.

Portanto, a análise do arquivo de diferenças auxilia na identificação de erros durante o desenvolvimento e testes do programa.
