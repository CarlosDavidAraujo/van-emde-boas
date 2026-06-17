import sys
import math

# Sentinelas internas que nao colidem com inteiros validos da entrada.
VEB_INFINITY = object()
VEB_NIL = object()
WORD_SIZE = 32

def calc_raiz(n):
    if n == 0:
        return 0
    return math.isqrt(n)

def high(x, U):
    if U == 2:
        return x >> 1
    return x // calc_raiz(U)

def low(x, U):
    if U == 2:
        return x & 1
    return x % calc_raiz(U)

def index(h, l, U):
    if U == 2:
        return (h << 1) | l
    return (h * calc_raiz(U)) + l

# Tabela Hash para armazenar os clusters ativos de forma dinâmica (Linear Space)
class TabelaHash:
    def __init__(self, cap=8):
        self.capacidade = cap
        self.tamanho = 0
        self.tabela = [[] for _ in range(self.capacidade)]

    def hash_func(self, chave):
        return chave % self.capacidade

    def inserir(self, chave, valor):
        # Table Doubling: se fator de carga >= 0.75, dobra o tamanho
        if self.tamanho / self.capacidade >= 0.75:
            self.redimensionar(self.capacidade * 2)

        idx = self.hash_func(chave)
        for i, (k, v) in enumerate(self.tabela[idx]):
            if k == chave:
                self.tabela[idx][i] = (chave, valor)
                return
        self.tabela[idx].append((chave, valor))
        self.tamanho += 1

    def buscar(self, chave):
        idx = self.hash_func(chave)
        for k, v in self.tabela[idx]:
            if k == chave:
                return v
        return None

    def remover(self, chave):
        idx = self.hash_func(chave)
        for i, (k, v) in enumerate(self.tabela[idx]):
            if k == chave:
                self.tabela[idx].pop(i)
                self.tamanho -= 1
                # Table Halving: se fator de carga <= 0.25, reduz pela metade (minimo cap=8)
                if self.capacidade > 8 and self.tamanho / self.capacidade <= 0.25:
                    self.redimensionar(self.capacidade // 2)
                return True
        return False

    def redimensionar(self, nova_cap):
        antiga_tabela = self.tabela
        self.capacidade = nova_cap
        self.tabela = [[] for _ in range(self.capacidade)]
        self.tamanho = 0
        for lista in antiga_tabela:
            for k, v in lista:
                self.inserir(k, v)

    def obter_chaves(self):
        chaves = []
        for lista in self.tabela:
            for k, v in lista:
                chaves.append(k)
        return chaves

# Árvore van Emde Boas com alocação preguiçosa de memória
class ArvoreVEB:
    def __init__(self, u):
        self.universe_size = u
        self.min_val = VEB_NIL
        self.max_val = VEB_NIL
        self.summary = None
        self.clusters = None

    def vazia(self):
        return self.min_val == VEB_NIL

    def contem(self, valor):
        if valor == self.min_val or valor == self.max_val:
            return True
        if self.universe_size <= 2:
            return False
        if self.clusters is None:
            return False
        h = high(valor, self.universe_size)
        l = low(valor, self.universe_size)
        sub_arvore = self.clusters.buscar(h)
        if sub_arvore is None:
            return False
        return sub_arvore.contem(l)

    def inserir(self, valor):
        if self.vazia():
            self.min_val = valor
            self.max_val = valor
            return

        if self.contem(valor):
            return

        if valor < self.min_val:
            valor, self.min_val = self.min_val, valor

        if self.universe_size > 2:
            # Inicialização lazy (só aloca se tiver > 1 elemento na estrutura)
            if self.clusters is None:
                l_raiz = calc_raiz(self.universe_size)
                u_raiz = ((self.universe_size - 1) // l_raiz + 1) if self.universe_size > 0 else 0
                self.summary = ArvoreVEB(u_raiz)
                self.clusters = TabelaHash()

            h = high(valor, self.universe_size)
            l = low(valor, self.universe_size)

            sub_arvore = self.clusters.buscar(h)
            if sub_arvore is None:
                l_raiz = calc_raiz(self.universe_size)
                sub_arvore = ArvoreVEB(l_raiz)
                self.clusters.inserir(h, sub_arvore)
                self.summary.inserir(h)

            sub_arvore.inserir(l)

        if valor > self.max_val:
            self.max_val = valor

    def remover(self, valor):
        if self.vazia() or valor < self.min_val or valor > self.max_val:
            return

        if self.min_val == self.max_val:
            self.min_val = VEB_NIL
            self.max_val = VEB_NIL
            self.summary = None
            self.clusters = None
            return

        if valor == self.min_val:
            if self.universe_size == 2:
                self.min_val = self.max_val
            else:
                primeiro_cluster = self.summary.min_val
                if primeiro_cluster == VEB_NIL:
                    return
                sub_arvore = self.clusters.buscar(primeiro_cluster)
                novo_min = index(primeiro_cluster, sub_arvore.min_val, self.universe_size)
                self.min_val = novo_min
                valor = self.min_val

        if self.universe_size > 2 and self.clusters is not None:
            h = high(valor, self.universe_size)
            l = low(valor, self.universe_size)

            sub_arvore = self.clusters.buscar(h)
            if sub_arvore is not None:
                sub_arvore.remover(l)
                if sub_arvore.vazia():
                    self.clusters.remover(h)
                    self.summary.remover(h)

        if valor == self.max_val:
            if self.vazia():
                self.max_val = VEB_NIL
                self.summary = None
                self.clusters = None
            elif self.universe_size == 2:
                self.max_val = self.min_val
            else:
                ultimo_cluster = self.summary.max_val
                if ultimo_cluster == VEB_NIL:
                    self.max_val = self.min_val
                else:
                    sub_arvore = self.clusters.buscar(ultimo_cluster)
                    novo_max = index(ultimo_cluster, sub_arvore.max_val, self.universe_size)
                    self.max_val = novo_max

        # Libera espaço se voltou a ter <= 1 elemento
        if self.min_val == self.max_val or self.vazia():
            self.summary = None
            self.clusters = None

    def sucessor(self, valor):
        if self.vazia():
            return VEB_INFINITY

        if valor < self.min_val:
            return self.min_val

        if valor >= self.max_val:
            return VEB_INFINITY

        if self.universe_size == 2:
            return 1 if (valor == 0 and self.max_val == 1) else VEB_INFINITY

        if self.clusters is None:
            return VEB_INFINITY

        h = high(valor, self.universe_size)
        l = low(valor, self.universe_size)

        sub_arvore = self.clusters.buscar(h)
        if sub_arvore is not None and l < sub_arvore.max_val:
            suc_low = sub_arvore.sucessor(l)
            return index(h, suc_low, self.universe_size)
        else:
            suc_cluster = self.summary.sucessor(h)
            if suc_cluster == VEB_INFINITY:
                return VEB_INFINITY
            sub_arvore = self.clusters.buscar(suc_cluster)
            return index(suc_cluster, sub_arvore.min_val, self.universe_size)

    def predecessor(self, valor):
        if self.vazia():
            return VEB_NIL

        if valor > self.max_val:
            return self.max_val

        if valor <= self.min_val:
            return VEB_NIL

        if self.universe_size == 2:
            return 0 if (valor == 1 and self.min_val == 0) else VEB_NIL

        if self.clusters is None:
            return self.min_val

        h = high(valor, self.universe_size)
        l = low(valor, self.universe_size)

        sub_arvore = self.clusters.buscar(h)
        if sub_arvore is not None and l > sub_arvore.min_val:
            pred_low = sub_arvore.predecessor(l)
            return index(h, pred_low, self.universe_size)
        else:
            pred_cluster = self.summary.predecessor(h)
            if pred_cluster == VEB_NIL:
                return self.min_val
            sub_arvore = self.clusters.buscar(pred_cluster)
            return index(pred_cluster, sub_arvore.max_val, self.universe_size)

    def imprimir_estrutura(self):
        if self.vazia():
            print("Min: NIL")
            return

        partes = [f"Min: {self.min_val}"]

        if self.universe_size > 2 and self.clusters is not None:
            c_conteudo = {}
            for ch in self.clusters.obter_chaves():
                sub_arvore = self.clusters.buscar(ch)
                if sub_arvore is not None:
                    elementos_sub = []
                    atual = sub_arvore.min_val
                    while atual != VEB_INFINITY and atual != VEB_NIL:
                        elementos_sub.append(atual)
                        atual = sub_arvore.sucessor(atual)

                    if elementos_sub:
                        valores_globais = []
                        for val in elementos_sub:
                            valores_globais.append(index(ch, val, self.universe_size))
                        valores_globais.sort()
                        c_conteudo[ch] = valores_globais

            for ch in sorted(c_conteudo.keys()):
                itens = [v for v in c_conteudo[ch] if v != self.min_val]
                if itens:
                    str_itens = ", ".join(map(str, itens))
                    partes.append(f"C[{ch}]: {str_itens}")

        print(", ".join(partes))

# Converte para int de 32 bits
def converter_int(texto):
    try:
        val = int(texto)
        if val > 2147483647:
            return 2147483647
        if val < -2147483648:
            return -2147483648
        return val
    except ValueError:
        return 0

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo_entrada>")
        sys.exit(1)

    caminho = sys.argv[1]
    tam_universo = 1 << WORD_SIZE
    arvore = ArvoreVEB(tam_universo)

    try:
        with open(caminho, 'r') as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split()
                if not partes:
                    continue
                cmd = partes[0]

                if cmd == "INC":
                    val = converter_int(partes[1])
                    arvore.inserir(val)
                elif cmd == "REM":
                    val = converter_int(partes[1])
                    arvore.remover(val)
                elif cmd == "SUC":
                    val = converter_int(partes[1])
                    print(f"SUC {val}")
                    res = arvore.sucessor(val)
                    if res == VEB_INFINITY:
                        print("+INF")
                    else:
                        print(res)
                elif cmd == "PRE":
                    val = converter_int(partes[1])
                    print(f"PRE {val}")
                    res = arvore.predecessor(val)
                    if res == VEB_NIL:
                        print("-INF")
                    else:
                        print(res)
                elif cmd == "IMP":
                    print("IMP")
                    arvore.imprimir_estrutura()
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
