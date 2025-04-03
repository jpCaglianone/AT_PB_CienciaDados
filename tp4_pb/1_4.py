import numpy as np
import matplotlib.pyplot as plt
import time
import heapq

def criar_min_heap(lista):
    if isinstance(lista, np.ndarray):
        lista = lista.tolist()  # Converte para lista Python se for um numpy.ndarray
    heapq.heapify(lista)
    return lista

def criar_max_heap(lista):
    if isinstance(lista, np.ndarray):
        lista = lista.tolist()  # Converte para lista Python se for um numpy.ndarray
    lista = [-x for x in lista]
    heapq.heapify(lista)
    return lista


def inserir_min_heap(heap, valor):
    heapq.heappush(heap, valor)
    return heap


def inserir_max_heap(heap, valor):
    heapq.heappush(heap, -valor)
    return heap


def remover_min_heap(heap):
    if not heap:
        return None, heap
    menor = heapq.heappop(heap)
    return menor, heap


def remover_max_heap(heap):
    if not heap:
        return None, heap
    maior = -heapq.heappop(heap)
    return maior, heap


def buscar_elemento_heap(heap, valor, eh_max_heap=False):
    if eh_max_heap:
        valor = -valor
    for elemento in heap:
        if elemento == valor:
            return True
    return False


def comparar_operacoes_heap():
    tamanhos = [100, 1000, 5000, 10000, 50000]
    tempos_min_insercao = []
    tempos_max_insercao = []
    tempos_min_remocao = []
    tempos_max_remocao = []

    for tamanho in tamanhos:
        lista = np.random.randint(1, tamanho * 10, tamanho)

        min_heap = criar_min_heap(lista)
        max_heap = criar_max_heap(lista)

        valor_inserir = np.random.randint(1, tamanho * 10)

        inicio = time.time()
        inserir_min_heap(min_heap, valor_inserir)
        fim = time.time()
        tempos_min_insercao.append(fim - inicio)

        inicio = time.time()
        inserir_max_heap(max_heap, valor_inserir)
        fim = time.time()
        tempos_max_insercao.append(fim - inicio)

        inicio = time.time()
        remover_min_heap(min_heap)
        fim = time.time()
        tempos_min_remocao.append(fim - inicio)

        inicio = time.time()
        remover_max_heap(max_heap)
        fim = time.time()
        tempos_max_remocao.append(fim - inicio)

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(tamanhos, tempos_min_insercao, 'o-', label='Inserção Min-Heap')
    plt.plot(tamanhos, tempos_max_insercao, 's-', label='Inserção Max-Heap')
    plt.xlabel('Tamanho da Heap')
    plt.ylabel('Tempo (segundos)')
    plt.title('Tempo de Inserção: Min-Heap vs Max-Heap')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(tamanhos, tempos_min_remocao, 'o-', label='Remoção Min-Heap')
    plt.plot(tamanhos, tempos_max_remocao, 's-', label='Remoção Max-Heap')
    plt.xlabel('Tamanho da Heap')
    plt.ylabel('Tempo (segundos)')
    plt.title('Tempo de Remoção: Min-Heap vs Max-Heap')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('comparacao_operacoes_heap.png')

    return {
        'tamanhos': tamanhos,
        'min_insercao': tempos_min_insercao,
        'max_insercao': tempos_max_insercao,
        'min_remocao': tempos_min_remocao,
        'max_remocao': tempos_max_remocao
    }


def demonstrar_operacoes():
    lista = [5, 2, 3, 7, 1]
    print("Lista original:", lista)

    min_heap = criar_min_heap(lista)
    print("Min-Heap criada:", min_heap)

    min_heap = inserir_min_heap(min_heap, 0)
    print("Min-Heap após inserção do valor 0:", min_heap)

    existe = buscar_elemento_heap(min_heap, 7)
    print("O elemento 7 existe na min-heap?", existe)

    menor, min_heap = remover_min_heap(min_heap)
    print("Elemento removido:", menor)
    print("Min-Heap após remoção:", min_heap)

    lista_original = [5, 2, 3, 7, 1]
    max_heap = criar_max_heap(lista_original)
    print("\nMax-Heap criada (valores internos negados):", max_heap)
    print("Max-Heap valores reais:", [-x for x in max_heap])

    max_heap = inserir_max_heap(max_heap, 8)
    print("Max-Heap após inserção do valor 8 (valores internos):", max_heap)
    print("Max-Heap após inserção (valores reais):", [-x for x in max_heap])

    maior, max_heap = remover_max_heap(max_heap)
    print("Elemento removido da max-heap:", maior)
    print("Max-Heap após remoção (valores reais):", [-x for x in max_heap])


def main():
    resultados = comparar_operacoes_heap()

    print("Análise de Desempenho de Min-Heap e Max-Heap")
    print("Tamanhos testados:", resultados['tamanhos'])
    print("Tempos médios de inserção em min-heap (s):", [round(t, 8) for t in resultados['min_insercao']])
    print("Tempos médios de inserção em max-heap (s):", [round(t, 8) for t in resultados['max_insercao']])
    print("Tempos médios de remoção em min-heap (s):", [round(t, 8) for t in resultados['min_remocao']])
    print("Tempos médios de remoção em max-heap (s):", [round(t, 8) for t in resultados['max_remocao']])

    print("\nDemonstração das operações de heap com exemplo específico:")
    demonstrar_operacoes()


if __name__ == "__main__":
    main()
