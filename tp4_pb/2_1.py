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


def medir_tempo_insercao(trie, palavras):
    inicio = time.time()
    for palavra in palavras:
        trie.inserir(palavra)
    fim = time.time()
    return fim - inicio


def medir_tempo_busca(trie, palavras):
    inicio = time.time()
    for palavra in palavras:
        trie.buscar(palavra)
    fim = time.time()
    return fim - inicio


def comparar_desempenho_tamanho():
    tamanhos = [100, 1000, 5000, 10000, 50000]
    tempos_insercao = []
    tempos_busca = []

    for tamanho in tamanhos:
        palavras = gerar_lista_palavras(tamanho)

        trie = Trie()
        tempo_insercao = medir_tempo_insercao(trie, palavras)
        tempos_insercao.append(tempo_insercao)

        palavras_busca = random.sample(palavras, min(1000, len(palavras)))
        tempo_busca = medir_tempo_busca(trie, palavras_busca)
        tempos_busca.append(tempo_busca)

    plt.figure(figsize=(12, 6))
    plt.plot(tamanhos, tempos_insercao, 'o-', label='Tempo de Inserção')
    plt.plot(tamanhos, tempos_busca, 's-', label='Tempo de Busca (1000 palavras)')
    plt.xlabel('Número de Palavras')
    plt.ylabel('Tempo (segundos)')
    plt.title('Desempenho de Operações Trie por Tamanho da Lista')
    plt.legend()
    plt.grid(True)
    plt.savefig('trie_desempenho_tamanho.png', dpi=300)

    return tamanhos, tempos_insercao, tempos_busca


def comparar_desempenho_comprimento():
    comprimentos = [4, 8, 12, 16, 20]
    tempos_insercao = []
    tempos_busca = []

    quantidade = 10000

    for comprimento in comprimentos:
        palavras = gerar_lista_palavras(quantidade, tamanho_medio=comprimento, desvio_padrao=1)

        trie = Trie()
        tempo_insercao = medir_tempo_insercao(trie, palavras)
        tempos_insercao.append(tempo_insercao)

        palavras_busca = random.sample(palavras, 1000)
        tempo_busca = medir_tempo_busca(trie, palavras_busca)
        tempos_busca.append(tempo_busca)

    plt.figure(figsize=(12, 6))
    plt.plot(comprimentos, tempos_insercao, 'o-', label='Tempo de Inserção (10000 palavras)')
    plt.plot(comprimentos, tempos_busca, 's-', label='Tempo de Busca (1000 palavras)')
    plt.xlabel('Comprimento Médio das Palavras')
    plt.ylabel('Tempo (segundos)')
    plt.title('Desempenho de Operações Trie por Comprimento das Palavras')
    plt.legend()
    plt.grid(True)
    plt.savefig('trie_desempenho_comprimento.png', dpi=300)

    return comprimentos, tempos_insercao, tempos_busca


def inserir_manualmente():
    trie = Trie()
    print("Digite as palavras para inserir no Trie (digite 'sair' para finalizar):")

    while True:
        palavra = input("Palavra: ").strip().lower()
        if palavra == 'sair':
            break

        inicio = time.time()
        trie.inserir(palavra)
        fim = time.time()

        print(f"Palavra '{palavra}' inserida em {(fim - inicio) * 1000:.6f} ms")

    print(f"Total de {trie.contador_palavras} palavras inseridas.")
    return trie


def menu():
    print("=" * 50)
    print("IMPLEMENTAÇÃO DE TRIE")
    print("=" * 50)
    print("1. Inserir palavras manualmente")
    print("2. Executar teste automático e gerar gráficos")
    print("3. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        trie = inserir_manualmente()

        while True:
            print("\nOpções:")
            print("1. Buscar palavra")
            print("2. Imprimir todas as palavras")
            print("3. Voltar ao menu principal")

            sub_opcao = input("Escolha uma opção: ")

            if sub_opcao == '1':
                palavra = input("Digite a palavra para buscar: ").strip().lower()
                inicio = time.time()
                encontrada = trie.buscar(palavra)
                fim = time.time()

                if encontrada:
                    print(f"A palavra '{palavra}' foi encontrada na trie em {(fim - inicio) * 1000:.6f} ms")
                else:
                    print(f"A palavra '{palavra}' não foi encontrada na trie")

            elif sub_opcao == '2':
                inicio = time.time()
                palavras = trie.imprimir_palavras()
                fim = time.time()

                print(f"Palavras na trie ({len(palavras)}):")
                for palavra in palavras:
                    print(f"- {palavra}")
                print(f"Tempo para coletar: {(fim - inicio) * 1000:.6f} ms")

            elif sub_opcao == '3':
                break

    elif opcao == '2':
        print("Executando testes de desempenho...")

        print("Comparando desempenho por tamanho da lista...")
        tamanhos, tempos_insercao, tempos_busca = comparar_desempenho_tamanho()

        print("Resultados por tamanho:")
        for i, tamanho in enumerate(tamanhos):
            print(
                f"Tamanho: {tamanho}, Tempo de Inserção: {tempos_insercao[i]:.6f}s, Tempo de Busca: {tempos_busca[i]:.6f}s")

        print("\nComparando desempenho por comprimento das palavras...")
        comprimentos, tempos_insercao_comp, tempos_busca_comp = comparar_desempenho_comprimento()

        print("Resultados por comprimento:")
        for i, comprimento in enumerate(comprimentos):
            print(
                f"Comprimento: {comprimento}, Tempo de Inserção: {tempos_insercao_comp[i]:.6f}s, Tempo de Busca: {tempos_busca_comp[i]:.6f}s")

        print("\nGráficos salvos como 'trie_desempenho_tamanho.png' e 'trie_desempenho_comprimento.png'")

    elif opcao == '3':
        print("Saindo...")
        return False

    return True


def main():
    continuar = True
    while continuar:
        continuar = menu()


if __name__ == "__main__":
    main()
