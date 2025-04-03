import numpy as np
import matplotlib.pyplot as plt
import time
import heapq


def criar_heap(lista):
    # Converter array NumPy para lista Python
    lista_python = lista.tolist()
    heapq.heapify(lista_python)
    return lista_python


def buscar_elemento_heap(heap, valor):
    for elemento in heap:
        if elemento == valor:
            return True
    return False


def comparar_tamanhos_heap():
    tamanhos = [100, 1000, 5000, 10000, 50000, 100000]
    tempos_busca = []

    for tamanho in tamanhos:
        lista = np.random.randint(1, tamanho * 10, tamanho)
        heap = criar_heap(lista)

        tempos_por_tamanho = []

        for _ in range(10):  # Executa 10 vezes para obter uma média
            valor_busca = np.random.randint(1, tamanho * 10)

            inicio = time.time()
            buscar_elemento_heap(heap, valor_busca)
            fim = time.time()

            tempos_por_tamanho.append(fim - inicio)

        tempos_busca.append(np.mean(tempos_por_tamanho))

    plt.figure(figsize=(12, 7))
    plt.plot(tamanhos, tempos_busca, 'o-', linewidth=2, markersize=8)
    plt.xlabel('Tamanho da Heap', fontsize=12)
    plt.ylabel('Tempo Médio de Busca (segundos)', fontsize=12)
    plt.title('Tempo de Execução da Busca por Tamanho da Heap', fontsize=14)
    plt.grid(True)
    plt.xscale('log')

    # Adicionando anotações com os valores
    for i, (tamanho, tempo) in enumerate(zip(tamanhos, tempos_busca)):
        plt.annotate(f'{tempo:.6f}s',
                     xy=(tamanho, tempo),
                     xytext=(5, 5),
                     textcoords='offset points')

    plt.savefig('tempo_busca_por_tamanho_heap.png', dpi=300, bbox_inches='tight')

    return tempos_busca, tamanhos


def calcular_complexidade(tamanhos, tempos):
    # Estimando a complexidade baseada na relação entre tamanho e tempo
    log_tamanhos = np.log(tamanhos)
    log_tempos = np.log(tempos)

    coef = np.polyfit(log_tamanhos, log_tempos, 1)
    return coef[0]  # O expoente da relação tempo = O(n^expoente)


def main():
    tempos_busca, tamanhos = comparar_tamanhos_heap()

    # Calculando a complexidade aproximada
    expoente = calcular_complexidade(tamanhos, tempos_busca)

    print("Análise de Busca em Heap para Diferentes Tamanhos:")
    print(f"Tamanhos testados: {tamanhos}")
    print(f"Tempos médios de busca (segundos): {[round(t, 6) for t in tempos_busca]}")
    print(f"Complexidade estimada: O(n^{expoente:.2f})")

    if 0.8 <= expoente <= 1.2:
        print("Os resultados confirmam que a busca em heap tem complexidade aproximadamente linear O(n).")
    elif expoente < 0.8:
        print(
            "Os resultados sugerem uma complexidade sublinear, possivelmente devido a otimizações do sistema ou casos de teste favoráveis.")
    else:
        print(
            "Os resultados sugerem uma complexidade superlinear, possivelmente devido a fatores externos como overhead de sistema.")

    print("\nConclusão:")
    print(
        "A busca em heap não oferece vantagem algoritmica em relação à busca linear, pois ambas precisam verificar cada elemento no pior caso.")
    print(
        "Para buscas eficientes, estruturas como dicionários (complexidade média O(1)) ou árvores de busca balanceadas (complexidade O(log n)) seriam mais adequadas.")


if __name__ == "__main__":
    main()
