import numpy as np
import matplotlib.pyplot as plt
import time
import random
import heapq


def criar_heap(lista):
    lista_copia = lista.copy()
    heapq.heapify(lista_copia)
    return lista_copia


def inserir_elemento_heapq(heap, elemento):
    heap_copia = heap.copy()
    heapq.heappush(heap_copia, elemento)
    return heap_copia


def inserir_elemento_manual(heap, elemento):
    heap_copia = heap.copy()
    heap_copia.append(elemento)
    indice = len(heap_copia) - 1

    subir_elemento(heap_copia, indice)

    return heap_copia


def subir_elemento(heap, indice):
    pai = (indice - 1) // 2

    if indice > 0 and heap[pai] > heap[indice]:
        heap[indice], heap[pai] = heap[pai], heap[indice]
        subir_elemento(heap, pai)


def visualizar_heap(heap, titulo):
    G = criarGrafo(heap)
    pos = posicoes_nos(heap)

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue',
            font_size=12, arrows=False, font_weight='bold')

    plt.title(titulo)
    plt.axis('off')
    return plt.gcf()


def criarGrafo(heap):
    import networkx as nx
    G = nx.Graph()

    for i in range(len(heap)):
        G.add_node(i, label=str(heap[i]))

        pai = (i - 1) // 2
        if i > 0:
            G.add_edge(pai, i)

    return G


def posicoes_nos(heap):
    pos = {}
    niveis = int(np.log2(len(heap))) + 1

    for i in range(len(heap)):
        nivel = int(np.log2(i + 1))
        pos_nivel = i - (2 ** nivel - 1)
        total_nivel = min(2 ** nivel, len(heap) - (2 ** nivel - 1))

        x = pos_nivel - total_nivel / 2 + 0.5
        y = -nivel

        pos[i] = (x, y)

    return pos


def medir_tempo_insercao(tamanhos_heap, num_elementos, repeticoes=5):
    tempos_heapq = []
    tempos_manual = []

    for tamanho in tamanhos_heap:
        tempo_heapq_total = 0
        tempo_manual_total = 0

        for _ in range(repeticoes):
            lista_base = [random.randint(1, 1000) for _ in range(tamanho)]
            heap_base = criar_heap(lista_base)
            elementos = [random.randint(1, 1000) for _ in range(num_elementos)]

            # Medindo tempo para heapq
            inicio = time.time()
            heap_temp = heap_base.copy()
            for elem in elementos:
                heap_temp = inserir_elemento_heapq(heap_temp, elem)
            fim = time.time()
            tempo_heapq_total += (fim - inicio)

            # Medindo tempo para inserção manual
            inicio = time.time()
            heap_temp = heap_base.copy()
            for elem in elementos:
                heap_temp = inserir_elemento_manual(heap_temp, elem)
            fim = time.time()
            tempo_manual_total += (fim - inicio)

        tempos_heapq.append(tempo_heapq_total / repeticoes)
        tempos_manual.append(tempo_manual_total / repeticoes)

    return tempos_heapq, tempos_manual


def imprimir_heap_formatada(heap):
    if not heap:
        print("Heap vazia")
        return

    niveis = int(np.log2(len(heap))) + 1

    print("Estrutura da Heap:")
    for nivel in range(niveis):
        inicio = 2 ** nivel - 1
        fim = min(2 ** (nivel + 1) - 1, len(heap))
        espacos = " " * (2 ** (niveis - nivel - 1) - 1)
        elementos = espacos
        for j in range(inicio, fim):
            if j < len(heap):
                elementos += f"{heap[j]}{espacos * 2}"
        print(elementos)


def plotar_comparativo(tamanhos_heap, tempos_heapq, tempos_manual):
    plt.figure(figsize=(12, 10))

    plt.subplot(2, 1, 1)
    plt.plot(tamanhos_heap, tempos_heapq, 'b-o', label='HeapQ (Biblioteca)')
    plt.plot(tamanhos_heap, tempos_manual, 'r-o', label='Implementação Manual')
    plt.title('Comparativo de Tempo para Inserção de Elementos')
    plt.xlabel('Tamanho da Heap Inicial')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    razao = [t_manual / t_heapq if t_heapq > 0 else 0 for t_manual, t_heapq in zip(tempos_manual, tempos_heapq)]
    plt.plot(tamanhos_heap, razao, 'm-o')
    plt.title('Razão de Desempenho (Manual/HeapQ)')
    plt.xlabel('Tamanho da Heap Inicial')
    plt.ylabel('Razão de Tempo')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('comparativo_insercao_heap.png')

    # Gráfico adicional - tempo por elemento
    plt.figure(figsize=(10, 6))
    tempo_por_elemento_heapq = [t / 1000 for t in tempos_heapq]  # 1000 inserções
    tempo_por_elemento_manual = [t / 1000 for t in tempos_manual]  # 1000 inserções

    plt.plot(tamanhos_heap, tempo_por_elemento_heapq, 'b--o', label='HeapQ (por elemento)')
    plt.plot(tamanhos_heap, tempo_por_elemento_manual, 'r--o', label='Manual (por elemento)')
    plt.title('Tempo Médio por Inserção')
    plt.xlabel('Tamanho da Heap Inicial')
    plt.ylabel('Tempo por Elemento (ms)')
    plt.legend()
    plt.grid(True)
    plt.savefig('tempo_por_elemento.png')


def demostrar_insercao():
    import networkx as nx

    # Heap inicial
    heap_inicial = [2, 4, 8, 9, 7, 10, 14]
    heap_minima = criar_heap(heap_inicial.copy())

    elemento_novo = 3

    # Inserir o elemento
    heap_apos_insercao = inserir_elemento_heapq(heap_minima, elemento_novo)

    # Visualizar antes e depois
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    G1 = criarGrafo(heap_minima)
    pos1 = posicoes_nos(heap_minima)
    nx.draw(G1, pos1, with_labels=True, labels={i: str(heap_minima[i]) for i in range(len(heap_minima))},
            node_size=1800, node_color='lightblue', font_size=10, arrows=False, font_weight='bold')
    plt.title("Heap Antes da Inserção")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    G2 = criarGrafo(heap_apos_insercao)
    pos2 = posicoes_nos(heap_apos_insercao)
    nx.draw(G2, pos2, with_labels=True, labels={i: str(heap_apos_insercao[i]) for i in range(len(heap_apos_insercao))},
            node_size=1800, node_color='lightblue', font_size=10, arrows=False, font_weight='bold')
    plt.title(f"Heap Após Inserção do Elemento {elemento_novo}")
    plt.axis('off')

    plt.tight_layout()
    plt.savefig('demonstracao_insercao.png')

    return heap_minima, heap_apos_insercao, elemento_novo


def principal():
    # Demonstração visual de inserção
    heap_antes, heap_depois, elemento = demostrar_insercao()

    print(f"Heap antes da inserção: {heap_antes}")
    print(f"Elemento inserido: {elemento}")
    print(f"Heap após inserção: {heap_depois}")

    print("\nRepresentação da Heap antes da inserção:")
    imprimir_heap_formatada(heap_antes)

    print("\nRepresentação da Heap após inserção:")
    imprimir_heap_formatada(heap_depois)

    # Análise de desempenho
    tamanhos_heap = [1000, 5000, 10000, 50000, 100000, 200000]
    num_elementos_inserir = 1000  # Inserir 1000 elementos em cada teste

    print("\nMedindo tempo de inserção com diferentes tamanhos de heap...")
    tempos_heapq, tempos_manual = medir_tempo_insercao(tamanhos_heap, num_elementos_inserir)

    print("\nResultados da análise de tempo:")
    print("=" * 70)
    print(f"{'Tamanho Heap':<15} {'HeapQ (s)':<15} {'Manual (s)':<15} {'Razão M/H':<15}")
    print("-" * 70)

    for i, tamanho in enumerate(tamanhos_heap):
        razao = tempos_manual[i] / tempos_heapq[i] if tempos_heapq[i] > 0 else 0
        print(f"{tamanho:<15} {tempos_heapq[i]:<15.6f} {tempos_manual[i]:<15.6f} {razao:<15.2f}")

    plotar_comparativo(tamanhos_heap, tempos_heapq, tempos_manual)

    return {
        'heap_antes': heap_antes,
        'heap_depois': heap_depois,
        'elemento_inserido': elemento,
        'tamanhos_testados': tamanhos_heap,
        'tempos_heapq': tempos_heapq,
        'tempos_manual': tempos_manual
    }


if __name__ == "__main__":
    import networkx as nx

    resultados = principal()
