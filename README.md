# Estrutura van Emde Boas com Espaço Linear (Python)

Este projeto implementa uma árvore de **van Emde Boas (vEB)** com consumo de espaço linear, conforme os requisitos estabelecidos. A estrutura utiliza uma **tabela de dispersão (hash table)** própria com técnicas de **table doubling/halving** para armazenar os clusters ativos de forma dinâmica, reduzindo a complexidade de espaço de $O(U)$ para $O(n)$, onde $n$ é o número de elementos contidos na árvore.

---

## Detalhes do Ambiente

- **Linguagem:** Python 3.14+ (compatível com Python 3.8+)
- **Bibliotecas Standard Utilizadas:** `sys`, `math` (sem dependências externas)

---

## Arquivos do Projeto

- `main.py`: Contém a classe `TabelaHash`, a classe `ArvoreVEB` e a lógica principal de execução.
- `makefile`: Define os comandos para compilar/executar as operações.
- `test/`: Pasta contendo os arquivos de teste.
- `README.md`: Este arquivo com a documentação do projeto.

---

## Estruturas de Dados Utilizadas

### 1. `TabelaHash`
Implementação de uma tabela de dispersão utilizando tratamento de colisões por **encadeamento (chaining)** com listas encadeadas (representadas por listas nativas do Python).
- **Table Doubling:** Quando o fator de carga ($\alpha = \frac{\text{tamanho}}{\text{capacidade}}$) atinge ou ultrapassa $0.75$, a tabela dobra de tamanho.
- **Table Halving:** Quando o fator de carga cai para $0.25$ ou menos (e a capacidade é maior que a inicial de 8), a tabela reduz sua capacidade pela metade.
- **Complexidade de Espaço:** $O(k)$, onde $k$ é o número de chaves únicas inseridas.

### 2. `ArvoreVEB`
Implementação da árvore de van Emde Boas clássica modificada para obter espaço linear.
- Em vez de alocar um array estático de tamanho $\sqrt{U}$ para os clusters, utiliza-se a estrutura `TabelaHash` acima.
- **Alocação Preguiçosa (Lazy Allocation):** O `summary` e a `TabelaHash` de clusters só são instanciados quando a árvore contém mais de 1 elemento. Ao remover elementos e a árvore voltar a ter $\le 1$ elementos, essas estruturas auxiliares são liberadas (`None`), garantindo o consumo linear estrito de memória de $O(n)$.
- Evita inserção de elementos duplicados validando com o método `contem(x)`.

---

## Principais Funções e Métodos Implementados

### Funções Auxiliares:
- `calc_raiz(n)`: Retorna o piso da raiz quadrada de $n$ usando `math.isqrt`.
- `high(x, U)`: Retorna o índice do cluster ao qual $x$ pertence no universo de tamanho $U$.
- `low(x, U)`: Retorna o índice local de $x$ dentro de seu cluster no universo $U$.
- `index(h, l, U)`: Reconstrói o valor global a partir do cluster $h$ e índice local $l$ no universo $U$.
- `converter_int(texto)`: Emula a extração de inteiro de 32 bits com sinal de C++ (`std::istringstream`), saturando valores que excedem os limites (`2147483647` e `-2147483648`).

### Métodos de `ArvoreVEB`:
- `inserir(x)`: Insere o elemento $x$ na árvore.
- `remover(x)`: Remove o elemento $x$ da árvore.
- `sucessor(x)`: Retorna o sucessor estrito de $x$ na árvore, ou `VEB_INFINITY` se não houver.
- `predecessor(x)`: Retorna o predecessor estrito de $x$ na árvore, ou `VEB_NIL` se não houver.
- `imprimir_estrutura()`: Imprime a representação do primeiro nível da árvore (mínimo e clusters não vazios com seus respectivos elementos) no formato solicitado pela operação `IMP`.

---

## Instruções de Execução

O projeto inclui um `makefile` com suporte para execução rápida e dinâmica.

### 1. Compilação (Build)
Como Python é uma linguagem interpretada, esta etapa não gera binários, mas é mantida por conformidade de especificação:
```bash
make build
```

### 2. Execução
Para executar o programa com o arquivo padrão `entrada.txt`:
```bash
make run
```

Para rodar com um arquivo de testes arbitrário:
```bash
make run INPUT="test/1.txt"
```

### 3. Gerando arquivo de saída
Para salvar a saída gerada em um arquivo, use:
```bash
make output INPUT="test/1.txt" OUTPUT="saida.txt"
```

Para gerar as saídas dos sete arquivos de teste em `test/`, use:
```bash
make test-output
```

Esse comando cria:
- `test/1_saida.txt`
- `test/2_saida.txt`
- `test/3_saida.txt`
- `test/4_saida.txt`
- `test/5_saida.txt`
- `test/6_saida.txt`
- `test/7_saida.txt`

### 4. Comparando com a saida esperada
Os arquivos de saida esperada ficam em:
- `test/1_esperada.txt`
- `test/2_esperada.txt`
- `test/3_esperada.txt`
- `test/4_esperada.txt`
- `test/5_esperada.txt`
- `test/6_esperada.txt`
- `test/7_esperada.txt`

Para gerar novamente as saidas obtidas e comparar com as esperadas, use:
```bash
make test
```

Esse comando executa o programa para cada arquivo de entrada, atualiza os arquivos `*_saida.txt` e usa `fc` para comparar cada saida obtida com a respectiva saida esperada.
