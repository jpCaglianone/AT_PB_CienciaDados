
import numpy as np
import matplotlib.pyplot as plt
import time
import heapq
import random


def criar_heap(lista):
    heapq.heapify(lista)
    return lista


def criar_heap_manual(lista):
    n = len(lista)
    for i in range(n // 2 - 1, -1, -1):
        heapificar(lista, n, i)
    return lista


def heapificar(lista, n, i):
    maior = i
    esquerda = 2 * i + 1
    direita = 2 * i + 2

    if esquerda < n and lista[esquerda] > lista[maior]:
        maior = esquerda

    if direita < n and lista[direita] > lista[maior]:
        maior = direita

    if maior != i:
        lista[i], lista[maior] = lista[maior], lista[i]
        heapificar(lista, n, maior)


def exibir_heap(heap):
    return heap.copy()


def medir_tempo_criar_heap(tamanhos_listas):
    tempos_heapq = []
    tempos_manual = []

    for tamanho in tamanhos_listas:
        lista = [random.randint(1, 10000) for _ in range(tamanho)]

        inicio = time.time()
        criar_heap(lista.copy())
        fim = time.time()
        tempos_heapq.append(fim - inicio)

        inicio = time.time()
        criar_heap_manual(lista.copy())
        fim = time.time()
        tempos_manual.append(fim - inicio)

    return tempos_heapq, tempos_manual


def medir_tempo_exibir_heap(tamanhos_listas):
    tempos_exibir = []

    for tamanho in tamanhos_listas:
        lista = [random.randint(1, 10000) for _ in range(tamanho)]
        heap = criar_heap(lista)

        inicio = time.time()
        exibir_heap(heap)
        fim = time.time()
        tempos_exibir.append(fim - inicio)

    return tempos_exibir


def plotar_comparativo_tempo(tamanhos_listas, tempos_heapq, tempos_manual, tempos_exibir):
    plt.figure(figsize=(12, 10))

    plt.subplot(2, 1, 1)
    plt.plot(tamanhos_listas, tempos_heapq, 'b-o', label='HeapQ (Biblioteca)')
    plt.plot(tamanhos_listas, tempos_manual, 'r-o', label='Implementação Manual')
    plt.title('Comparativo de Tempo: Criação de Heap')
    plt.xlabel('Tamanho da Lista')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(tamanhos_listas, tempos_exibir, 'g-o', label='Exibição da Heap')
    plt.title('Tempo de Exibição da Heap')
    plt.xlabel('Tamanho da Lista')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('comparativo_heap.png')


def imprimir_heap_formatada(heap, tamanho=10):
    if not heap:
        print("Heap vazia")
        return

    if len(heap) > tamanho:
        print(f"Primeiros {tamanho} elementos da heap: {heap[:tamanho]}")
    else:
        print(f"Heap completa: {heap}")

    niveis = int(np.log2(len(heap))) + 1

    print("\nEstrutura da Heap:")
    for nivel in range(niveis):
        inicio = 2** nivel - 1
        fim = min(2 ** (nivel + 1) - 1, len(heap))
        print(f"Nível {nivel}: {heap[inicio:fim]}")


def principal():
    tamanhos_listas = [1000, 5000, 10000, 50000, 100000, 500000]

    tempos_heapq, tempos_manual = medir_tempo_criar_heap(tamanhos_listas)
    tempos_exibir = medir_tempo_exibir_heap(tamanhos_listas)

    plotar_comparativo_tempo(tamanhos_listas, tempos_heapq, tempos_manual, tempos_exibir)

    print("Comparação de tempo para criação e exibição de heap:")
    print("=" * 60)
    print(f"{'Tamanho':<12} {'HeapQ (s)':<12} {'Manual (s)':<12} {'Exibição (s)':<12}")
    print("-" * 60)

    for i, tamanho in enumerate(tamanhos_listas):
        print(f"{tamanho:<12} {tempos_heapq[i]:<12.6f} {tempos_manual[i]:<12.6f} {tempos_exibir[i]:<12.6f}")

    print("\nExemplo de uso das funções:")
    lista_exemplo = [4, 10, 3, 5, 1, 2]
    print(f"Lista original: {lista_exemplo}")

    heap_minima = criar_heap(lista_exemplo.copy())
    print(f"Heap mínima (biblioteca heapq): {exibir_heap(heap_minima)}")

    heap_maxima = criar_heap_manual([-x for x in lista_exemplo.copy()])
    heap_maxima = [-x for x in heap_maxima]
    print(f"Heap máxima (implementação manual): {heap_maxima}")

    print("\nExibição formatada da heap:")
    lista_grande = [random.randint(1, 100) for _ in range(15)]
    heap_grande = criar_heap(lista_grande)
    imprimir_heap_formatada(heap_grande)

    return {
        'tamanhos': tamanhos_listas,
        'tempos_heapq': tempos_heapq,
        'tempos_manual': tempos_manual,
        'tempos_exibir': tempos_exibir
    }


if __name__ == "__main__":
    resultados = principal()




