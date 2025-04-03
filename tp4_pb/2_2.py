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
        self.contador_palavras = 0

    def inserir(self, palavra):
        no_atual = self.raiz

        for caractere in palavra:
            if caractere not in no_atual.filhos:
                no_atual.filhos[caractere] = NoTrie()
            no_atual = no_atual.filhos[caractere]

        if not no_atual.fim_palavra:
            no_atual.fim_palavra = True
            self.contador_palavras += 1

    def buscar(self, palavra):
        no_atual = self.raiz

        for caractere in palavra:
            if caractere not in no_atual.filhos:
                return False
            no_atual = no_atual.filhos[caractere]

        return no_atual.fim_palavra

    def imprimir_palavras(self):
        palavras = []
        self._coletar_palavras(self.raiz, "", palavras)
        return palavras

    def _coletar_palavras(self, no, prefixo, palavras):
        if no.fim_palavra:
            palavras.append(prefixo)

        for caractere, no_filho in no.filhos.items():
            self._coletar_palavras(no_filho, prefixo + caractere, palavras)


def gerar_palavra_aleatoria(tamanho=8):
    letras = string.ascii_lowercase
    return ''.join(random.choice(letras) for _ in range(tamanho))


def gerar_lista_palavras(quantidade, tamanho_medio=8, desvio_padrao=2):
    palavras = []
    for _ in range(quantidade):
        tamanho = max(1, int(np.random.normal(tamanho_medio, desvio_padrao)))
        palavras.append(gerar_palavra_aleatoria(tamanho))
    return palavras


def criar_trie_com_palavras(quantidade):
    trie = Trie()
    palavras = gerar_lista_palavras(quantidade)

    for palavra in palavras:
        trie.inserir(palavra)

    return trie, palavras


def medir_tempo_busca(trie, palavras, n_buscas=1000):
    palavras_para_buscar = []

    existentes = min(n_buscas // 2, len(palavras))
    nao_existentes = n_buscas - existentes

    palavras_existentes = random.sample(palavras, existentes)
    palavras_nao_existentes = [gerar_palavra_aleatoria() for _ in range(nao_existentes)]

    palavras_para_buscar = palavras_existentes + palavras_nao_existentes
    random.shuffle(palavras_para_buscar)

    inicio = time.time()
    resultados = [trie.buscar(palavra) for palavra in palavras_para_buscar]
    fim = time.time()

    return fim - inicio, sum(resultados), n_buscas - sum(resultados)


def comparar_tamanhos_trie():
    tamanhos = [100, 1000, 10000, 50000, 100000, 200000]
    tempos_busca = []
    acertos = []
    erros = []

    n_buscas = 1000

    for tamanho in tamanhos:
        print(f"Testando Trie com {tamanho} palavras...")
        trie, palavras = criar_trie_com_palavras(tamanho)
        tempo, acerto, erro = medir_tempo_busca(trie, palavras, n_buscas)

        tempos_busca.append(tempo)
        acertos.append(acerto)
        erros.append(erro)

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(tamanhos, tempos_busca, 'o-', linewidth=2)
    plt.xlabel('Tamanho da Trie (número de palavras)')
    plt.ylabel('Tempo de Busca (segundos)')
    plt.title(f'Tempo de Busca vs. Tamanho da Trie ({n_buscas} buscas)')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(tamanhos, [t / n_buscas * 1000 for t in tempos_busca], 'o-', linewidth=2)
    plt.xlabel('Tamanho da Trie (número de palavras)')
    plt.ylabel('Tempo Médio por Busca (ms)')
    plt.title('Tempo Médio por Busca vs. Tamanho da Trie')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('trie_busca_por_tamanho.png', dpi=300)

    return tamanhos, tempos_busca, acertos, erros


def comparar_com_lista():
    tamanhos = [100, 1000, 10000, 50000, 100000]
    tempos_trie = []
    tempos_lista = []
    n_buscas = 1000

    for tamanho in tamanhos:
        print(f"Comparando Trie vs Lista para {tamanho} palavras...")
        palavras = gerar_lista_palavras(tamanho)

        trie = Trie()
        for palavra in palavras:
            trie.inserir(palavra)

        palavras_busca = []
        existentes = min(n_buscas // 2, len(palavras))
        palavras_existentes = random.sample(palavras, existentes)
        palavras_nao_existentes = [gerar_palavra_aleatoria() for _ in range(n_buscas - existentes)]
        palavras_busca = palavras_existentes + palavras_nao_existentes
        random.shuffle(palavras_busca)

        inicio = time.time()
        for palavra in palavras_busca:
            trie.buscar(palavra)
        fim = time.time()
        tempos_trie.append(fim - inicio)

        inicio = time.time()
        for palavra in palavras_busca:
            palavra in palavras
        fim = time.time()
        tempos_lista.append(fim - inicio)

    plt.figure(figsize=(12, 6))
    plt.plot(tamanhos, tempos_trie, 'o-', label='Busca em Trie')
    plt.plot(tamanhos, tempos_lista, 's-', label='Busca em Lista')
    plt.xlabel('Número de Palavras')
    plt.ylabel('Tempo Total de Busca (segundos)')
    plt.title(f'Comparação: Trie vs. Lista ({n_buscas} buscas)')
    plt.legend()
    plt.grid(True)
    plt.savefig('trie_vs_lista.png', dpi=300)

    return tamanhos, tempos_trie, tempos_lista


def medir_busca_comprimento():
    comprimentos = [2, 4, 8, 12, 16, 20]
    tamanho_trie = 10000
    n_buscas = 1000
    tempos_busca = []

    for comprimento in comprimentos:
        print(f"Testando palavras com comprimento médio {comprimento}...")
        trie = Trie()
        palavras = gerar_lista_palavras(tamanho_trie, tamanho_medio=comprimento, desvio_padrao=1)

        for palavra in palavras:
            trie.inserir(palavra)

        palavras_busca = []
        existentes = min(n_buscas // 2, len(palavras))
        palavras_existentes = random.sample(palavras, existentes)
        palavras_nao_existentes = [gerar_palavra_aleatoria(comprimento) for _ in range(n_buscas - existentes)]
        palavras_busca = palavras_existentes + palavras_nao_existentes
        random.shuffle(palavras_busca)

        inicio = time.time()
        for palavra in palavras_busca:
            trie.buscar(palavra)
        fim = time.time()
        tempos_busca.append(fim - inicio)

    plt.figure(figsize=(12, 6))
    plt.plot(comprimentos, tempos_busca, 'o-', linewidth=2)
    plt.xlabel('Comprimento Médio das Palavras')
    plt.ylabel('Tempo de Busca (segundos)')
    plt.title(f'Tempo de Busca vs. Comprimento das Palavras (Trie com {tamanho_trie} palavras)')
    plt.grid(True)
    plt.savefig('trie_busca_por_comprimento.png', dpi=300)

    return comprimentos, tempos_busca


def main():
    print("Exercício 2.2 - Busca em Trie")
    print("=" * 50)

    print("\n1. Comparando tempos de busca para diferentes tamanhos de Trie...")
    tamanhos, tempos_busca, acertos, erros = comparar_tamanhos_trie()

    print("\nResultados por tamanho de Trie:")
    for i, tamanho in enumerate(tamanhos):
        print(f"Trie com {tamanho} palavras:")
        print(f"  - Tempo total de busca: {tempos_busca[i]:.6f} segundos")
        print(f"  - Tempo médio por busca: {tempos_busca[i] * 1000 / 1000:.6f} ms")
        print(f"  - Palavras encontradas: {acertos[i]}")
        print(f"  - Palavras não encontradas: {erros[i]}")

    print("\n2. Comparando busca em Trie vs. busca em Lista...")
    tamanhos, tempos_trie, tempos_lista = comparar_com_lista()

    print("\nResultados Trie vs. Lista:")
    for i, tamanho in enumerate(tamanhos):
        print(f"Tamanho {tamanho}:")
        print(f"  - Tempo de busca em Trie: {tempos_trie[i]:.6f} segundos")
        print(f"  - Tempo de busca em Lista: {tempos_lista[i]:.6f} segundos")
        print(f"  - Trie é {tempos_lista[i] / tempos_trie[i]:.2f}x mais rápido que Lista")

    print("\n3. Analisando impacto do comprimento das palavras...")
    comprimentos, tempos_busca_comp = medir_busca_comprimento()

    print("\nResultados por comprimento de palavra:")
    for i, comprimento in enumerate(comprimentos):
        print(f"Comprimento médio {comprimento}:")
        print(f"  - Tempo de busca: {tempos_busca_comp[i]:.6f} segundos")

    print("\nAnálise completa! Gráficos salvos como:")
    print("- trie_busca_por_tamanho.png")
    print("- trie_vs_lista.png")
    print("- trie_busca_por_comprimento.png")


if __name__ == "__main__":
    main()
