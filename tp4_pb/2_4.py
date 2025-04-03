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

    def buscar(self, palavra):
        no_atual = self.raiz

        for caractere in palavra:
            if caractere not in no_atual.filhos:
                return False
            no_atual = no_atual.filhos[caractere]

        return no_atual.fim_palavra

    def remover(self, palavra):
        return self._remover_recursivamente(self.raiz, palavra, 0)

    def _remover_recursivamente(self, no, palavra, profundidade):
        if profundidade == len(palavra):
            if no.fim_palavra:
                no.fim_palavra = False
                return len(no.filhos) == 0
            return False

        caractere = palavra[profundidade]

        if caractere not in no.filhos:
            return False

        deve_remover_filho = self._remover_recursivamente(no.filhos[caractere], palavra, profundidade + 1)

        if deve_remover_filho:
            del no.filhos[caractere]
            return len(no.filhos) == 0 and not no.fim_palavra

        return False

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

    def contar_nos(self):
        return self._contar_nos_recursivamente(self.raiz)

    def _contar_nos_recursivamente(self, no):
        count = 1  # Contamos o nó atual
        for filho in no.filhos.values():
            count += self._contar_nos_recursivamente(filho)
        return count


def gerar_palavra_aleatoria(tamanho_min=3, tamanho_max=10):
    tamanho = random.randint(tamanho_min, tamanho_max)
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(tamanho))


def gerar_conjunto_palavras(quantidade):
    palavras = set()
    while len(palavras) < quantidade:
        palavras.add(gerar_palavra_aleatoria())
    return list(palavras)


def experimento_remocao_parcial():
    tamanhos_tries = [100, 500, 1000, 5000, 10000]
    proporcoes_remocao = [0.1, 0.25, 0.5, 0.75, 0.9]

    tempos_remocao = np.zeros((len(tamanhos_tries), len(proporcoes_remocao)))
    reducao_nos = np.zeros((len(tamanhos_tries), len(proporcoes_remocao)))

    for i, tamanho in enumerate(tamanhos_tries):
        print(f"\nExperimento com Trie de {tamanho} palavras:")

        trie = Trie()
        palavras = gerar_conjunto_palavras(tamanho)

        for palavra in palavras:
            trie.inserir(palavra)

        nos_inicial = trie.contar_nos()
        print(f"  - Número inicial de nós: {nos_inicial}")

        for j, proporcao in enumerate(proporcoes_remocao):
            quantidade_remover = int(tamanho * proporcao)
            palavras_remover = random.sample(palavras, quantidade_remover)

            inicio = time.time()
            for palavra in palavras_remover:
                trie.remover(palavra)
            fim = time.time()

            tempo_total = fim - inicio
            nos_final = trie.contar_nos()
            reducao = (nos_inicial - nos_final) / nos_inicial * 100

            tempos_remocao[i, j] = tempo_total
            reducao_nos[i, j] = reducao

            print(f"  - Removendo {quantidade_remover} palavras ({proporcao * 100:.1f}%):")
            print(f"    * Tempo total: {tempo_total:.6f} segundos")
            print(f"    * Tempo médio por palavra: {tempo_total / quantidade_remover:.6f} segundos")
            print(f"    * Redução de nós: {reducao:.2f}%")
            print(f"    * Nós finais: {nos_final}")

    return tamanhos_tries, proporcoes_remocao, tempos_remocao, reducao_nos


def experimento_remocao_palavras_especificas():
    tamanho_trie = 5000
    trie = Trie()
    palavras = gerar_conjunto_palavras(tamanho_trie)

    print(f"\nExperimento de remoção de palavras específicas em Trie de {tamanho_trie} palavras:")

    for palavra in palavras:
        trie.inserir(palavra)

    nos_inicial = trie.contar_nos()
    print(f"  - Número inicial de nós: {nos_inicial}")

    # Selecionando palavras de diferentes tamanhos para remoção
    palavras_por_tamanho = {}
    for palavra in palavras:
        tamanho = len(palavra)
        if tamanho not in palavras_por_tamanho:
            palavras_por_tamanho[tamanho] = []
        palavras_por_tamanho[tamanho].append(palavra)

    tamanhos = sorted(palavras_por_tamanho.keys())
    tempos_por_tamanho = []

    for tamanho in tamanhos:
        if len(palavras_por_tamanho[tamanho]) < 10:
            continue

        palavras_teste = random.sample(palavras_por_tamanho[tamanho], 10)
        tempos = []

        print(f"  - Removendo palavras de tamanho {tamanho}:")

        for palavra in palavras_teste:
            inicio = time.time()
            trie.remover(palavra)
            fim = time.time()

            tempo = fim - inicio
            tempos.append(tempo)

            print(f"    * Palavra '{palavra}': {tempo:.6f} segundos")

        tempo_medio = np.mean(tempos)
        tempos_por_tamanho.append((tamanho, tempo_medio))
        print(f"    * Tempo médio: {tempo_medio:.6f} segundos")

    return tamanhos, [t[1] for t in sorted(tempos_por_tamanho)]


def plotar_graficos_remocao_parcial(tamanhos, proporcoes, tempos, reducao_nos):
    plt.figure(figsize=(15, 10))

    # Gráfico 1: Tempo total de remoção por tamanho da Trie e proporção removida
    plt.subplot(2, 2, 1)
    for j, proporcao in enumerate(proporcoes):
        plt.plot(tamanhos, tempos[:, j], 'o-', label=f'{proporcao * 100:.0f}%')

    plt.title('Tempo Total de Remoção vs Tamanho da Trie')
    plt.xlabel('Número de Palavras na Trie')
    plt.ylabel('Tempo (segundos)')
    plt.legend(title='% Removida')
    plt.grid(True)

    # Gráfico 2: Tempo médio de remoção por palavra
    plt.subplot(2, 2, 2)
    for j, proporcao in enumerate(proporcoes):
        tempos_medios = tempos[:, j] / (np.array(tamanhos) * proporcao)
        plt.plot(tamanhos, tempos_medios, 'o-', label=f'{proporcao * 100:.0f}%')

    plt.title('Tempo Médio de Remoção por Palavra')
    plt.xlabel('Número de Palavras na Trie')
    plt.ylabel('Tempo por Palavra (segundos)')
    plt.legend(title='% Removida')
    plt.grid(True)

    # Gráfico 3: Redução percentual de nós
    plt.subplot(2, 2, 3)
    for j, proporcao in enumerate(proporcoes):
        plt.plot(tamanhos, reducao_nos[:, j], 'o-', label=f'{proporcao * 100:.0f}%')

    plt.title('Redução Percentual de Nós vs Tamanho da Trie')
    plt.xlabel('Número de Palavras na Trie')
    plt.ylabel('Redução de Nós (%)')
    plt.legend(title='% Removida')
    plt.grid(True)

    # Gráfico 4: Comparação com complexidade teórica
    plt.subplot(2, 2, 4)
    x = np.array(tamanhos)
    plt.plot(tamanhos, tempos[:, 2], 'bo-', label='Tempo Real (50%)')
    plt.plot(tamanhos, np.log(x) / 10000, 'g--', label='O(log n) - Referência')
    plt.plot(tamanhos, x / 100000, 'r--', label='O(n) - Referência')

    plt.title('Comparativo de Complexidade - Remoção')
    plt.xlabel('Número de Palavras na Trie')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('analise_remocao_trie.png')
    plt.show()


def plotar_grafico_tamanho_palavra(tamanhos, tempos):
    plt.figure(figsize=(10, 6))

    plt.plot(tamanhos, tempos, 'mo-')
    plt.title('Tempo de Remoção vs Tamanho da Palavra')
    plt.xlabel('Tamanho da Palavra')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('analise_remocao_por_tamanho.png')
    plt.show()


if __name__ == "__main__":
    print("Exercício 2.4 – Remoção de uma palavra do Trie")

    print("\nExperimento 1: Remoção parcial de palavras de Tries de diferentes tamanhos")
    tamanhos, proporcoes, tempos, reducao = experimento_remocao_parcial()
    plotar_graficos_remocao_parcial(tamanhos, proporcoes, tempos, reducao)

    print("\nExperimento 2: Tempo de remoção vs tamanho da palavra")
    tamanhos_palavras, tempos_por_tamanho = experimento_remocao_palavras_especificas()
    plotar_grafico_tamanho_palavra(tamanhos_palavras, tempos_por_tamanho)

    # Exemplo específico para ilustrar o funcionamento do método de remoção
    print("\nDemonstração do método de remoção:")
    trie_demo = Trie()
    palavras_demo = ["casa", "casamento", "casaco", "asa", "asado", "atlas", "atleta"]

    print("Inserindo palavras:", palavras_demo)
    for palavra in palavras_demo:
        trie_demo.inserir(palavra)

    print("Número de nós inicial:", trie_demo.contar_nos())

    prefixo = "cas"
    palavras_com_prefixo = trie_demo.buscar_palavras_com_prefixo(prefixo)
    print(f"Palavras com prefixo '{prefixo}':", palavras_com_prefixo)

    palavra_remover = "casa"
    print(f"Removendo palavra '{palavra_remover}'")
    trie_demo.remover(palavra_remover)

    print("A palavra ainda existe?", trie_demo.buscar(palavra_remover))
    print("Número de nós após remoção:", trie_demo.contar_nos())

    palavras_com_prefixo = trie_demo.buscar_palavras_com_prefixo(prefixo)
    print(f"Palavras com prefixo '{prefixo}' após remoção:", palavras_com_prefixo)
