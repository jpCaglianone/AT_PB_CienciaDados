import numpy as np
import matplotlib.pyplot as plt
import time
import string
import random


class NoTrie:
    def __init__(self):
        self.filhos = {}
        self.fim_palavra = False


class Trie:
    def __init__(self):
        self.raiz = NoTrie()

    def inserir(self, palavra):
        no_atual = self.raiz

        for caractere in palavra:
            if caractere not in no_atual.filhos:
                no_atual.filhos[caractere] = NoTrie()
            no_atual = no_atual.filhos[caractere]

        no_atual.fim_palavra = True

    def buscar_palavras_com_prefixo(self, prefixo):
        no_atual = self.raiz
        resultado = []

        for caractere in prefixo:
            if caractere not in no_atual.filhos:
                return []
            no_atual = no_atual.filhos[caractere]

        self._buscar_palavras_recursivamente(no_atual, prefixo, resultado)
        return resultado

    def _buscar_palavras_recursivamente(self, no, prefixo_atual, resultado):
        if no.fim_palavra:
            resultado.append(prefixo_atual)

        for caractere, filho in no.filhos.items():
            self._buscar_palavras_recursivamente(filho, prefixo_atual + caractere, resultado)


def gerar_palavra_aleatoria(tamanho_min=3, tamanho_max=10):
    tamanho = random.randint(tamanho_min, tamanho_max)
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(tamanho))


def gerar_conjunto_palavras(quantidade):
    palavras = set()
    while len(palavras) < quantidade:
        palavras.add(gerar_palavra_aleatoria())
    return list(palavras)


def medir_tempo_insercao(trie, palavras):
    inicio = time.time()
    for palavra in palavras:
        trie.inserir(palavra)
    fim = time.time()
    return fim - inicio


def medir_tempo_busca(trie, prefixos):
    tempos = []
    resultados = []

    for prefixo in prefixos:
        inicio = time.time()
        resultado = trie.buscar_palavras_com_prefixo(prefixo)
        fim = time.time()

        tempos.append(fim - inicio)
        resultados.append(len(resultado))

    return tempos, resultados


def executar_experimento():
    tamanhos_conjuntos = [100, 500, 1000, 5000, 10000]
    prefixos_teste = ['a', 'b', 'c', 'ab', 'ba', 'ca', 'abc']

    tempos_insercao = []
    tempos_busca_medio = []
    qtd_resultados_medio = []

    for tamanho in tamanhos_conjuntos:
        trie = Trie()
        palavras = gerar_conjunto_palavras(tamanho)

        tempo_insercao = medir_tempo_insercao(trie, palavras)
        tempos_insercao.append(tempo_insercao)

        tempos, resultados = medir_tempo_busca(trie, prefixos_teste)
        tempos_busca_medio.append(np.mean(tempos))
        qtd_resultados_medio.append(np.mean(resultados))

    plotar_graficos(tamanhos_conjuntos, tempos_insercao, tempos_busca_medio, qtd_resultados_medio)


def plotar_graficos(tamanhos, tempos_insercao, tempos_busca, qtd_resultados):
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 2, 1)
    plt.plot(tamanhos, tempos_insercao, 'bo-')
    plt.title('Tempo de Inserção vs Tamanho do Conjunto')
    plt.xlabel('Número de Palavras')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(tamanhos, tempos_busca, 'ro-')
    plt.title('Tempo Médio de Busca vs Tamanho do Conjunto')
    plt.xlabel('Número de Palavras')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.bar(range(len(tamanhos)), qtd_resultados, tick_label=[str(t) for t in tamanhos])
    plt.title('Média de Resultados por Prefixo vs Tamanho do Conjunto')
    plt.xlabel('Número de Palavras')
    plt.ylabel('Média de Resultados')

    plt.subplot(2, 2, 4)
    x = np.array(tamanhos)
    plt.plot(tamanhos, tempos_insercao, 'bo-', label='Tempo de Inserção')
    plt.plot(tamanhos, tempos_busca, 'ro-', label='Tempo de Busca')
    plt.plot(tamanhos, np.log(x) / 10000, 'g--', label='O(log n) - Referência')
    plt.plot(tamanhos, x / 100000, 'y--', label='O(n) - Referência')
    plt.title('Comparativo de Complexidade')
    plt.xlabel('Número de Palavras')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('analise_autocomplete_trie.png')
    plt.show()


def experimento_tempo_por_prefixo():
    tamanho_conjunto = 5000
    trie = Trie()
    palavras = gerar_conjunto_palavras(tamanho_conjunto)

    for palavra in palavras:
        trie.inserir(palavra)

    tamanhos_prefixo = range(1, 6)
    tempos_por_tamanho = []
    resultados_por_tamanho = []

    for tamanho in tamanhos_prefixo:
        prefixos_teste = [gerar_palavra_aleatoria(tamanho, tamanho) for _ in range(10)]
        tempos, resultados = medir_tempo_busca(trie, prefixos_teste)

        tempos_por_tamanho.append(np.mean(tempos))
        resultados_por_tamanho.append(np.mean(resultados))

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(tamanhos_prefixo, tempos_por_tamanho, 'go-')
    plt.title('Tempo Médio de Busca vs Tamanho do Prefixo')
    plt.xlabel('Tamanho do Prefixo')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(tamanhos_prefixo, resultados_por_tamanho, 'mo-')
    plt.title('Média de Resultados vs Tamanho do Prefixo')
    plt.xlabel('Tamanho do Prefixo')
    plt.ylabel('Média de Resultados')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('analise_tamanho_prefixo.png')
    plt.show()


if __name__ == "__main__":
    print("Experimento 1: Análise de desempenho por tamanho do conjunto de palavras")
    executar_experimento()

    print("\nExperimento 2: Análise de desempenho por tamanho do prefixo")
    experimento_tempo_por_prefixo()
